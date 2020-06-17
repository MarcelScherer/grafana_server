#!/bin/bash

echo "install influxdb:"
sudo apt-get install apt-transport-https
curl -sL https://repos.influxdata.com/influxdb.key | sudo apt-key add -
echo "deb https://repos.influxdata.com/debian stretch stable" | sudo tee /etc/apt/sources.list.d/influxdb.list
sudo apt update
sudo apt install influxdb
sudo cp influxdb.conf /etc/influxdb/influxdb.conf
sudo systemctl enable influxdb
sudo systemctl start influxdb 

echo "install grafana:"
wget https://s3-us-west-2.amazonaws.com/grafana-releases/release/grafana_5.2.2_armhf.deb 
sudo dpkg -i grafana_5.2.2_armhf.deb 
sudo systemctl enable grafana-server 
sudo systemctl start grafana-server
sudo rm grafana_5.2.2_armhf.deb 

echo "update python3:"
sudo pip3 install influxdb
