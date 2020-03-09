'''
Project name: Aquatron Smart Lab
Version 1.2
--New Version Feature: Statistic Analyzer for 24 hours with 10 mins read in rate

Run file: python3 aquatron.py
Environment: Kivy, Python3, Rapsberry Pi 3

Description: This project is to build a sensor system for Aquatron Lab. Include the temperature sensor, humidity sensor light sensor, water detection on groud and water level sensor. This app is aiming to build a prototype that communicate will all the sensors in the lab and used a kivy based graphical user interface to show all the information from outside. The combination of warning light and email alerting system to form the alerting system.

Overview: Currently, we have six type of sensors, there will be two sensors of each type.


Setup: (Library Required)
sudo apt-get install python3, pip3
pip3 install kivy (Some configurations see online web)
garden install matplotlib
pip3 install matplotlib


Problems:
@Build connection to all sensors
    GPIO
    Bluetooth
@Kivy Interface
    Should we replace it with QT or TKinker

@Alarm system: Email

@In statistic screen, should we refresh the screen?

@Setting page: Use scroll to set the limit figure without keyboard, another option is virtual keyboard (Numberic)

@Updated on Feb 6th, still need to do:
--Try to build the basic frame
--Simple
--Need to add color change
--Add pics as background
--Frame different color block
--Change icon size

@Updated on March 5th
--Read in data from SQL post
--Test Plan

   -- Build postgreSQL on RPI
   https://www.postgresql.org/
   https://opensource.com/article/17/10/set-postgres-database-your-raspberry-pi

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
from kivy.uix.slider import Slider
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors import FocusBehavior
#from kivy.uix.recyclegridlayout import RecycleGridLayout
from kivy.uix.screenmanager import ScreenManager, Screen
#from kivy.uix.recycleview.layout import LayoutSelectionBehavior
#from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.properties import BooleanProperty, ListProperty, StringProperty, ObjectProperty

#update since version 1.2
#use matplotlib to plot the statistic graph
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import matplotlib.pyplot as plt

'''
Initialization
'''
#initialize all the variables

_init=0.0

current_time='0000-00-00 00:00:00'      #initialize the time

#sensors, read in from GPIO
watertemp_sensor=_init
waterlvl_sensor=_init
liquid_sensor=_init
light_sensor=_init
airtemp_sensor=_init
humidity_sensor=_init

#Setup: After reaching the limit, special event will be triggerred
watertemp_limit=_init
waterlvl_limit=_init
liquid_limit=_init
light_limit=_init
airtemp_limit=_init
humidity_limit=_init


'''
Data Processing
'''

#read in data and process in this section






'''
Kivy Interface
'''
#Kivy StatisticScreen for anylyzing the collected data in 24 hours
class StatisticScreen(Screen):
    data_items=ListProperty([])
    #build a simple graph
    plt.plot([1,23,2,4])
    plt.ylabel('Statistic Graph in 24 hours')
    def __init__(self, **kwargs):
        super(StatisticScreen, self).__init__(**kwargs)
        #Considering whether we should just do it updating each 10 mins
        Clock.schedule_once(self.graph_test)
        #Clock.schedule_interval(self.graph_test,600) #proper callback time, for now is 0.1 s

    def graph_test(self, dt):
        self.graph_generate()
        plt.ylabel('Temperature in 24 hours')
        self.ids.topline.add_widget(FigureCanvasKivyAgg(plt.gcf()))
        
        plt.ylabel('Humidity in 24 hours')
        self.ids.topline.add_widget(FigureCanvasKivyAgg(plt.gcf()))
        plt.plot([11,12,13,15])
        plt.ylabel('Optic in 24 hours')
        self.ids.botline.add_widget(FigureCanvasKivyAgg(plt.gcf()))
        plt.plot([15,23,2,4])
        plt.ylabel('Water Level in 24 hours')
        self.ids.botline.add_widget(FigureCanvasKivyAgg(plt.gcf()))
        #return box
        #If this is keep refreshing, then use remove_widget(destination)
    def graph_generate(self):
        #overhere, read from postgreSQL data to generate Matplotlib graph
        pass

#Kivy Setting Screen
class SettingScreen(Screen):
    #waiting for other items
    #could be wrong
    data_items=ListProperty([])
    pass



#Kivy Main Screen
class MainScreen(Screen):


    #waiting for other items
    data_items=ListProperty([])
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        Clock.schedule_interval(self.get_users,10) #proper callback time, for now is 0.1 s
    def get_users(self,dt):
        global current_time
        current_time=strftime("%Y-%m-%d %H:%M:%S",localtime())
        self.ids.time_label.text=current_time
    #def toggle_button(self):
    #design for the toggle button to contrl on and off





#AquaGUI screen manager
class ScreenManager(ScreenManager):
    pass

class AquaguiApp(App):
    title = "Aquatron Smart Lab"
    def build(self):
        return ScreenManager()



'''
Main Program
'''
if __name__=='__main__':
    #Build DWM connection
    #DWM=serial.Serial(port="/dev/ttyACM0",baudrate=115200,timeout=0.5) #The input port expire after  0.5 seconds
    AquaguiApp().run()