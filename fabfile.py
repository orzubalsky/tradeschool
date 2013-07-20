from fabric.api import env, task, sudo, prompt, cd, put, puts
from fabric.contrib.files import upload_template
from fab_config import Config

env.hosts            = Config.hosts
fab_username         = Config.fab_username
fab_password         = Config.fab_password
server_settings_file = Config.server_settings_file 
apache_conf_file     = Config.apache_conf_file

#####
#
# tasks that will need to be done repeatedly.
#
#####

@task
def update_sourcecode():
    with cd('/opt/projects/tse/'):
        sudo('git pull',user=fab_username)

@task
def update_project_settings():
    filename = prompt( 'Enter name of local settings file:',
                       default=server_settings_file )
    destination = '/opt/projects/tse/ts/settings/server.py'
    put(filename,destination,use_sudo=True)
    sudo('chown %s:webdev %s' % (fab_username, destination))

@task
def run_buildout():
    with cd('/opt/projects/tse/'):
        sudo('./bin/buildout -v -c server.cfg',user=fab_username)

@task
def update_db():
    with cd('/opt/projects/tse/'):
        sudo('./bin/django syncdb', user=fab_username)
        sudo('./bin/django migrate tradeschool', user=fab_username)
    
@task
def update_static_files():
    # run the django command to update static files
    with cd('/opt/projects/tse/'):
        sudo('./bin/django collectstatic', user=fab_username)    

@task 
def load_fixtures():
    # load fixtures
    with cd('/opt/projects/tse/'):
        sudo('./bin/django loaddata email_initial_data.json', user=fab_username)

@task
def restart_wsgi():
    with cd('/opt/projects/tse'):
        sudo('touch bin/django.wsgi')

@task
def deploy():
    update_sourcecode()

    update = prompt( 'Do you want to update the server settings file with a local file? (y/n)',
                     default='y', validate=r'^[yYnN]$' )
    if update.upper() == 'Y':
        update_project_settings()

    update = prompt( 'Do you want to re-run the buildout? (y/n)',
                     default='y', validate=r'^[yYnN]$' )
    if update.upper() == 'Y':
        run_buildout()

    update_db()
    update_static_files()
    restart_wsgi()


#####
#
# tasks that would need to be done once for a given server.
#
#####

@task
def init_os_package_setup():
    sudo('apt-get -y update')
    sudo('apt-get -y upgrade')
    sudo('apt-get install git python-dev')
    sudo('apt-get install mysql-server mysql-client libmysqlclient-dev')
    sudo('apt-get install apache2 libapache2-mod-wsgi')
    sudo('apt-get install gettext memcached')

@task
def init_fab_user():
    sudo('groupadd webdev')
    sudo('useradd -G mysql,webdev --create-home --shell /bin/bash %s' % fab_username)
    sudo('passwd %s' % fab_password)

    sudo('ssh-keygen -t rsa -C "fab@tradeschool.coop"',user=fab_username)
    puts('Created the following id_rsa.pub file for user %s:' % fab_username)
    sudo('cat /home/%s/.ssh/id_rsa.pub' % fab_username)
    prompt('Please upload this to github as a "deploy key" (https://github.com/orzubalsky/tradeschool/settings/keys).\n' \
               'When done, press enter to continue.')

@task
def init_project_sourcecode():
    sudo('mkdir --parents /opt/projects/tse')
    sudo('chown %s:webdev /opt/projects/tse' % fab_username)
    with cd('/opt/projects/tse'):
        sudo('git clone git@github.com:orzubalsky/tradeschool.git .',user=fab_username)

@task
def init_buildout():
    with cd('/opt/projects/tse'):
        sudo('python bootstrap.py -v 2.1.1 -c server.cfg',user=fab_username)

@task
def init_mysql_db():
    db_name = prompt( 'Enter name of database:',
                       default='tradeschool_test' )    
    #sudo('mysqladmin create %s -u root' % db_name, user=fab_username)
    
    db_user = prompt( 'Enter name of database user:',
                       default='tradeschooler' )
    db_password = prompt( 'Enter password:')
    
    sudo('mysql_install_db', user=fab_username)
    sudo('/usr/bin/mysql_secure_installation', user=fab_username)
        
    sudo('mysql -u root CREATE USER %s@localhost IDENTIFIED BY %s;' % (db_user, db_password))                      
    sudo('mysql -u root GRANT ALL PRIVILEGES ON %s.* TO %s@localhost;' % (db_name, db_user))

@task
def create_cache_folder():
    with cd('/opt/projects/tse'):
        sudo('mkdir tmp',user=fab_username)    


@task
def init_apache():
    filename = prompt( 'Enter name of local apache conf file:',
                       default=apache_conf_file )
    destination = '/etc/apache2/sites-available/tstest.net'
    put(filename,destination,use_sudo=True)

    sudo('a2ensite tstest.net')
    sudo('service apache2 reload') # do we need this line??

@task
def initialize_everything():
    init_os_package_setup()
    init_fab_user()
    init_project_sourcecode()
    update_project_settings()
    init_buildout()
    init_mysql_db()

    run_buildout()
    update_db()

    init_apache()