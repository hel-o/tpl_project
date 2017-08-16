# setup for Ubuntu:
sudo apt-get update
sudo apt-get upgrade

sudo apt-get install python3.6

# mariadb:
sudo apt-get install python3.6-dev
sudo apt-get install libmysqlclient-dev

# server tools
sudo apt-get install nginx
sudo apt-get install python-pip
sudo apt-get install git

# time zone America/Lima
sudo dpkg-reconfigure tzdata

# python tools:
sudo pip install virtualenvwrapper

source /usr/local/bin/virtualenvwrapper.sh
mkvirtualenv -p /usr/bin/python3.6 tpl_project
