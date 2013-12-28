import os
from fabric.operations import local as lrun
from fabric.operations import run
from fabric.context_managers import settings
from fabric.api import env, task, sudo, prompt, cd, put, puts
from fab_config import Config

apache_conf_file = Config.apache_conf_file


#####
#
# setup environment
#
#####
@task
def local():
    env.run = lrun
    env.hosts = ['localhost']
    env.project_dir = Config.local_project_dir
    env.username = Config.local_username
    env.password = Config.local_password
    env.buildout_config_file = 'development.cfg'
    env.setting_file = Config.local_settings_file
    env.setting_file_path = os.path.join(
        Config.local_project_dir,
        Config.local_settings_file
    )


@task
def testing():
    env.run = run
    env.hosts = [Config.testing_domain]
    env.project_dir = Config.test_project_dir
    env.username = Config.testing_username
    env.password = Config.testing_password
    env.buildout_config_file = 'server.cfg'
    env.setting_file = Config.testing_settings_file
    env.setting_file_path = os.path.join(
        Config.testing_project_dir,
        Config.testing_settings_file
    )


@task
def prod():
    env.run = run
    env.hosts = [Config.production_domain]
    env.project_dir = Config.production_project_dir
    env.username = Config.production_username
    env.password = Config.production_password
    env.buildout_config_file = 'server.cfg'
    env.setting_file = Config.production_settings_file
    env.setting_file_path = os.path.join(
        Config.production_project_dir,
        Config.production_settings_file
    )


#####
#
# setup local machine
#
#####
@task
def setup_local():
    # clone repository

    # run buildout

    # copy development.py settings file

    # enter db settings

    # sync database

    # migrate database

    # load data fixtures

    # load sample data

    pass


@task
def create_ftp_user(username=None, password=None):
    if username is not None and password is not None:

        user_dir = "/home/%s/public_html" % username

        with settings(warn_only=True):
            # create system user
            sudo("useradd -p `mkpasswd -H md5 %s` %s" % (password, username))

            # create user ftp dir
            sudo("mkdir -p %s" % user_dir)

        # set owneership
        sudo("chown root:root /home/%s" % username)
        sudo("chown -R %s:root %s" % (username, user_dir))

        # set permissions
        sudo("chmod -R 0777 %s" % user_dir)

        # mount the branch html dir
        sudo("mount --bind /opt/projects/tse/ts/apps/branches/%s %s" %(username, user_dir))

        add_line = "/opt/projects/tse/ts/apps/branches/%s %s none bind 0" % (username, user_dir)
        sudo("echo %s >> /etc/fstab" % add_line)

        # restart vsftp daemon
        sudo("service vsftpd restart")


#####
#
# tasks that will need to be done repeatedly.
#
#####
@task
def update_sourcecode():
    with cd(env.project_dir):
        sudo('git pull', user=env.username)


@task
def update_project_settings():
    filename = prompt(
        'Enter name of local settings file:',
        default=env.setting_file
    )
    destination = env.setting_file_path
    put(filename, destination, use_sudo=True)
    sudo('chown %s:webdev %s' % (env.username, destination))


@task
def run_buildout():
    with cd(env.project_dir):
        sudo(
            './bin/buildout -v -c %s' % env.buildout_config_file,
            user=env.username
        )


@task
def update_db():
    with cd(env.project_dir):
        sudo('./bin/django syncdb --verbosity 2', user=env.username)
        sudo('./bin/django migrate', user=env.username)


@task
def update_static_files():
    # run the django command to update static files
    with cd(env.project_dir):
        sudo('./bin/django collectstatic', user=env.username)


@task
def load_fixtures():
    # load fixtures
    with cd(env.project_dir):
        sudo('./bin/django loaddata email_initial_data.json pages_initial_data.json teacher-info.json', user=env.username)


@task
def restart_memcached():
    with cd('/etc/init.d/memcached'):
        sudo('restart')


@task
def restart_wsgi():
    with cd(env.project_dir):
        sudo('touch bin/django.wsgi')


@task
def restart():
    #restart_memcached()
    restart_wsgi()

    sudo('/etc/init.d/apache2 restart')


@task
def test():
    with cd(env.project_dir):
        sudo('./bin/django test tradeschool -v 3', user=env.username)


@task
def load_data():
    filename = prompt(
        'Enter name of sql file:',
        default='data.sql'
    )
    #sudo('mkdir /opt/projects/tse/sql',user=env.username)

    destination = '%s/sql/data.sql' % env.project_dir

    db_name = prompt(
        'Enter name of database:',
        default='tradeschool_test'
    )

    put(filename, destination, use_sudo=True)

    with cd('%s/sql' % env.project_dir):
        sudo('mysql -u root %s < data.sql' % (db_name), user=env.username)


@task
def update_and_test():
    update_sourcecode()

    restart()

    #test()


@task
def deploy():
    update_sourcecode()

    update = prompt(
        'Do you want to update the server settings file with a local file? (y/n)',
        default='y',
        validate=r'^[yYnN]$'
    )
    if update.upper() == 'Y':
        update_project_settings()

    update = prompt(
        'Do you want to re-run the buildout? (y/n)',
        default='y',
        validate=r'^[yYnN]$'
    )
    if update.upper() == 'Y':
        run_buildout()

    update_db()
    load_fixtures()
    update_static_files()
    restart()
    test()


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
    #sudo('groupadd webdev')
    sudo('useradd -G mysql,webdev --create-home --shell /bin/bash %s' % env.username)
    sudo('passwd %s' % env.username)

    sudo('ssh-keygen -t rsa -C "fab@tradeschool.coop"', user=env.username)
    puts('Created the following id_rsa.pub file for user %s:' % env.username)
    sudo('cat /home/%s/.ssh/id_rsa.pub' % env.username)
    prompt(
        'Please upload this to github as a "deploy key"'
        '(https://github.com/orzubalsky/tradeschool/settings/keys).\n'
        'When done, press enter to continue.'
    )


@task
def init_project_sourcecode():
    sudo('mkdir --parents %s' % env.project_dir)
    sudo('chown %s:webdev %s' % (env.username, env.project_dir))
    with cd(env.project_dir):
        sudo('git clone git@github.com:orzubalsky/tradeschool.git .', user=env.username)


@task
def init_buildout():
    with cd(env.project_dir):
        sudo(
            'python bootstrap.py -c %s' % env.buildout_config_file,
            user=env.username
        )


@task
def init_mysql_db():
    db_name = prompt(
        'Enter name of database:',
        default='tradeschool_test'
    )
    #sudo('mysqladmin create %s -u root' % db_name, user=env.username)

    db_user = prompt(
        'Enter name of database user:',
        default='tradeschooler'
    )
    db_password = prompt('Enter password:')

    sudo('mysql_install_db', user=env.username)
    sudo('/usr/bin/mysql_secure_installation', user=env.username)

    sudo('mysql -u root -p CREATE DATABASE %s;' % db_name)
    sudo("mysql -u root -p CREATE USER '%s'@'localhost' IDENTIFIED BY '%s';" % (db_user, db_password))
    sudo("mysql -u root -p GRANT ALL PRIVILEGES ON %s.* TO '%s'@'localhost';" % (db_name, db_user))
    sudo("mysql -u root -p FLUSH PRIVILEGES;")


@task
def create_cache_folder():
    with cd(env.project_dir):
        sudo('mkdir tmp', user=env.username)


@task
def init_apache():
    filename = prompt(
        'Enter name of local apache conf file:',
        default=apache_conf_file
    )
    destination = '/etc/apache2/sites-available/%s' % env.hosts[0]
    put(filename, destination, use_sudo=True)

    sudo('a2ensite %s' % env.hosts[0])

    sudo('a2dissite default')

    sudo('service apache2 reload')  # do we need this line??


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
