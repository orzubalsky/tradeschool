#!/bin/bash
#
# Setup your build environment for the first time.
#
# Download dependencies, move dev config into place, create and load the
# database with some sample data.

set -e
set -x


python bootstrap.py -c development.cfg
./bin/buildout -c development.cfg
cp ts/settings/development.py.template ts/settings/development.py

secret_key=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 32 | head -n 1)
sed -i -e "s/SECRET_KEY = ''/SECRET_KEY = '$secret_key'/" ts/settings/development.py

./bin/django syncdb
./bin/django migrate
./bin/django loaddata email_initial_data.json \
        pages_initial_data.json \
        group_initial_data.json \
        language_initial_data.json \
        teacher-info.json

./bin/django loaddata sample_data.json

set +x
echo "

To run locally:
$ ./bin/django runserver

To run tests:
$ ./bin/django test tradeschool -v 2

"
