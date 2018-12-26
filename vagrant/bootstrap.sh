#!/usr/bin/env bash

# Script to bootstrap a Debian 9 virtual machine with:
# - the required Python version
# - any other other dependencies (MySQL, Django etc)



# Name of the python app and (optionally) corresponding systemd file. Use only letters/underscores.
APP_NAME=axe
SYSTEMD_UNIT=axe
PYTHON_VERSION=3.6.7


# Install utilities and (python) dependencies
lib_ssl_dev=libssl-dev
if [[ "$PYTHON_VERSION" =~ ^2.7 ]]; then
  if ! [[ "$PYTHON_VERSION" =~ ^2.7.13$ ]]; then
    lib_ssl_dev=libssl1.0-dev
  fi
fi
apt-get update
apt-get -y -qq install curl vim git wget net-tools mc sudo make build-essential ca-certificates \
    libsasl2-dev libldap2-dev $lib_ssl_dev zlib1g-dev libffi-dev libbz2-dev libreadline-dev libsqlite3-dev


# Install MySQL
debconf-set-selections <<< 'mysql-server mysql-server/root_password password axe123'
debconf-set-selections <<< 'mysql-server mysql-server/root_password_again password axe123'
apt-get update
apt-get install -y mysql-server
apt-get install -y mysql-client
apt-get install -y libmysqlclient-dev
apt-get install -y default-libmysqlclient-dev
apt-get install -y libmariadbclient-dev
apt-get install -y python3-dev
systemctl start mysql
systemctl enable mysql

ln -s /vagrant/ /home/vagrant/${APP_NAME}

# Install Python 3.6.7
wget https://www.python.org/ftp/python/3.6.7/Python-3.6.7.tgz
tar xvf Python-3.6.7.tgz
cd Python-3.6.7
./configure --enable-optimizations
make -j8
sudo make altinstall
python3.6

python3.6 -m venv /home/vagrant/${APP_NAME}_venv

source /home/vagrant/${APP_NAME}_venv/bin/activate
pip install -r /home/vagrant/${APP_NAME}/requirements.txt
#ln -s /home/vagrant/.pyenv/versions/${APP_NAME} /home/vagrant/${APP_NAME}_venv
chown vagrant:vagrant /home/vagrant/${APP_NAME}
chown vagrant:vagrant /home/vagrant/${APP_NAME}_venv

cd /home/vagrant/${APP_NAME}
mysql -u debian-sys-maint -paxe123 -e "source db.sql"