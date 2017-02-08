#! /bin/sh

#sudo services apache2 reload
#sudo touch /opt/ywebstarter/production/scripts/production/run.py


sudo timeout 5 supervisorctl stop ywebstarter-uwsgi-production
sudo supervisorctl start ywebstarter-uwsgi-production

