## Trade School Everywhere ##


### Installation ###

Setup is done using buildout. 
There is a base configuration file base.cfg that is extended for installing on different environments:

1. development.cfg
2. testing.cfg
3. server.cfg

When installing locally, use development.cfg. Otherwise, fab is used to install the project remotely automatically.

To install locally:

1. $ python bootstrap.py -c development.cfg
2. $ ./bin/buildout -c development.cfg
3. edit settings/development.py with database info and local paths
4. $ ./bin/django syncdb
5. $ ./bin/django migrate
6. $ ./bin/django loaddata email_initial_data.json pages_initial_data.json group_initial_data.json language_initial_data.json teacher-info.json
7. (optional) ./bin/django loaddata sample_data.json

To run locally:
$ ./bin/django runserver

To test:
$ ./bin/django test tradeschool -v 2


To install remotely:

1. $ cp fab_config.py.sample fab_config.py
2. edit fab_config.py with testing and/or production domains
3. edit settings/testing.py and/or settings/server.py with database info and local paths
4. $ ./bin/fab <testing|production> initialize_everything
5. $ ./bin/fab <testing|production> deploy




