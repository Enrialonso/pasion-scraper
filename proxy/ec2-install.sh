#!/bin/bash
sudo apt update -y
sudo apt install tinyproxy -y
echo "Allow 92.189.91.124" >> /etc/tinyproxy/tinyproxy.conf
sudo /etc/init.d/tinyproxy restart
