'''
Project name: Aquatron Smart Lab
Python file: python3 aquatron.py

Description: This project is to build a sensor system for Aquatron Lab. Include the temperature sensor, humanity sensor, light sensor, water
detection on groud and water level sensor. This app is aiming to build a prototype that communicate will all the sensors in the lab and used
a kivy based graphical user interface to show all the information from outside. The combination of warning light and email alerting system 
to form the alerting system.

Problems:
@Build connection to all sensors
    GPIO
    Bluetooth
@Kivy Interface

@Alarm system: Email



'''
import os
import sys
import serial
#import board
#import busio
#import RPI.GPIO as GPIO
from time import localtime, strftime,sleep

from kivy.app import App
from kivy.clock import Clock
from kivy.graphics import Color
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recyclegridlayout import RecycleGridLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.properties import BooleanProperty, ListProperty, StringProperty, ObjectProperty

'''
Initialization
'''
#initialize all the variables

_init=0.0

#sensors, read in from GPIO
watertemp_sensor=_init
waterlvl_sensor=_init
liquid_sensor=_init
light_sensor=init
airtemp_sensor=_init
humanity_sensor=_init

#Setup: After reaching the limit, special event will be triggerred
watertemp_limit=_init
waterlvl_limit=_init
liquid_limit=_init
light_limit=init
airtemp_limit=_init
humanity_limit=_init


'''
Data Processing
'''

#read in data and process in this section






'''
Kivy Interface
'''
#Kivy Setting Screen
class SettingScreen(Screen):
    #waiting for other items
    pass



#Kivy Main Screen
class MainScreen(Screen):
    #waiting for other items
    pass





#AquaGUI screen manager
class ScreenManager(ScreenManager):
    pass

class AquaguiApp(App):
    title = "Aquatron Smart Lab"
    def build(self):
        return ScreenManager



'''
Main Program
'''
if __name__=='__main__':
    #Build DWM connection
    #DWM=serial.Serial(port="/dev/ttyACM0",baudrate=115200,timeout=0.5) #The input port expire after  0.5 seconds
    AquaguiApp().run()