# Introduction
Project name: Aquatron Smart Lab  
Version 1.3 updated on Dec 4th, 2020

Description: This project is to build a sensor system for Dalhousie Aquatron Lab. In total 6 types of sensors and two of each type. Include the temperature sensor, humidity sensor light sensor, water detection on groud and water level sensor. This app is aiming to build a prototype that communicate will all the sensors in the lab and used a kivy based graphical user interface to show all the information from outside. The combination of warning light and email alerting system to form the alerting system.

# Installation
Setup: (Library: Kivy, python3, Matplotlib)
sudo apt-get install python3, pip3
sudo apt install libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev \
   pkg-config libgl1-mesa-dev libgles2-mesa-dev \
   python-setuptools libgstreamer1.0-dev git-core \
   gstreamer1.0-plugins-{bad,base,good,ugly} \
   gstreamer1.0-{omx,alsa} python-dev libmtdev-dev \
   xclip xsel libjpeg-dev
pip3 install kivy
garden install matplotlib
pip3 install matplotlib
sudo apt install postgresql libpq-dev postgresql-client postgresql-client-common -y
sudo pip3 install psycopg2
sudo apt-get install python3-pandas
pip3 install yagmail
sudo apt install matchbox-keyboard
