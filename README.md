## Trade School Everywhere ##


### Installation ###

Setup is done using buildout. 
There is a base configuration file base.cfg that is extended for installing on different environments:

1. development.cfg
2. testing.cfg
3. server.cfg

When installing locally, use development.cfg. Otherwise, fab is used to install the project remotely automatically.

To install locally:

    ./dev/setup_dev.sh


To run locally:

    ./bin/django runserver

To run tests:

    ./bin/django test tradeschool -v 2


To install remotely:

1. $ cp fab_config.py.sample fab_config.py
2. edit fab_config.py with testing and/or production domains
3. edit settings/testing.py and/or settings/server.py with database info and local paths
4. $ ./bin/fab <testing|production> initialize_everything
5. $ ./bin/fab <testing|production> deploy




