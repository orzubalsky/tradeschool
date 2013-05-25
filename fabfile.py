from fabric.api import env, task, sudo, prompt, cd, put, puts
from fabric.contrib.files import upload_template

env.hosts = [ '198.199.64.223', ]

#####
#
# tasks that will need to be done repeatedly.
#
#####

@task
def update_sourcecode():
    with cd('/opt/projects/ts/'):
        sudo('git pull',user='tradeschooler')

@task
def update_project_settings():
    filename = prompt( 'Enter name of local settings file:',
                       default='ts/settings/server.py' )
    destination = '/opt/projects/ts/settings/server.py'
    put(filename,destination,use_sudo=True)
    sudo('chown tradeschooler:webdev %s' % destination)

@task
def run_buildout():
    with cd('/opt/projects/ts/'):
        sudo('./bin/buildout -c server.cfg',user='tradeschooler')

@task
def update_db():
    with cd('/opt/projects/ts/'):
        sudo('./bin/django syncdb',user='tradeschooler')
        sudo('./bin/django migrate',user='tradeschooler')
    
@task
def update_static_files():
    # run the django command to update static files
    # then push them all to rackspace
    pass

@task
def restart_wsgi():
    with cd('/opt/projects/ts'):
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
    sudo('apt-get install git python-dev libjpeg62 libjpeg-dev libfreetype6 libfreetype6-dev zlib1g-dev ffmpeg')
    sudo('apt-get install postgresql-9.1 postgresql-server-dev-9.1')
    sudo('apt-get install binutils libproj-dev gdal-bin libgeoip1 python-gdal python-psycopg2')
    sudo('apt-get install postgresql-9.1-postgis')
    sudo('apt-get install apache2 libapache2-mod-wsgi')

@task
def init_tradeschooler_user():
    sudo('groupadd webdev')
    sudo('useradd -G postgres,webdev --create-home --shell /bin/bash tradeschooler')
    sudo('passwd tradeschooler')

    sudo('ssh-keygen -t rsa -C "tradeschooler@tradeschool.coop"',user='tradeschooler')
    puts('Created the following id_rsa.pub file for user tradeschooler:')
    sudo('cat /home/tradeschooler/.ssh/id_rsa.pub')
    prompt('Please upload this to github as a "deploy key" (https://github.com/orzubalsky/tradeschool/settings/keys).\n' \
               'When done, press enter to continue.')

@task
def init_project_sourcecode():
    sudo('mkdir --parents /opt/projects/ts')
    sudo('chown urtbot:webdev /opt/projects/ts')
    with cd('/opt/projects/ts'):
        sudo('git clone git@github.com:orzubalsky/tradeschool.git .',user='tradeschooler')

@task
def init_buildout():
    with cd('/opt/projects/ts'):
        sudo('python bootstrap.py -c server.cfg',user='tradeschooler')

@task
def init_postgres_db():
    sudo('chown postgres /opt/projects/urt/trunk/urt/etc/sh/*')
    sudo('chmod u+x /opt/projects/urt/trunk/urt/etc/sh/*')
    sudo('/opt/projects/ts/etc/sh/create_template_postgis-debian.sh',user='postgres')
    sudo('createuser tradeschooler',user='postgres')
    sudo('createdb --template=template_postgis --owner=tradeschooler tradeschool',user='postgres')

@task
def init_apache():
    filename = prompt( 'Enter name of local apache conf file:',
                       default='ts/etc/conf/apache.conf' )
    destination = '/etc/apache2/sites-available/tradeschool.coop'
    put(filename,destination,use_sudo=True)

    sudo('a2ensite tradeschool.coop')
    sudo('service apache2 reload') # do we need this line??

@task
def initialize_everything():
    init_os_package_setup()
    init_tradeschooler_user()
    init_project_sourcecode()
    update_project_settings()
    init_buildout()
    run_buildout()

    init_postgres_db()
    update_db()

    init_apache()

