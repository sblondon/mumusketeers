#! /bin/sh

#sudo services apache2 reload
#sudo touch /opt/ywebstarter/recette/scripts/recette/run.py


/opt/ywebstarter/recette/runtests 2>&1

sudo timeout 5 supervisorctl stop ywebstarter-uwsgi-recette
sudo supervisorctl start ywebstarter-uwsgi-recette

