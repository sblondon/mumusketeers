#! /bin/sh

sudo timeout 5 supervisorctl stop ywebstarter-uwsgi-integration
sudo supervisorctl start ywebstarter-uwsgi-integration

