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
watertemp_min=_init
waterlvl_min=_init
liquid_min=_init
light_min=_init
airtemp_min=_init
humidity_min=_init

watertemp_max=_init
waterlvl_max=_init
liquid_max=_init
light_max=_init
airtemp_max=_init
humidity_max=_init

#Note for future : use for loop to check if any sensor value is 
#out of range, use correpsonding button to make it read
'''
OOP in case for future expandsion
WATERTEMP=0
WATERLVL=1
LIQUID=2
LIGHT=3
AIRTEMP=4
HUMIDITY=5
ListOfSensor=['watertemp','waterlvl','liquid','light','airtemp','humidity']
'''
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
    
    plt.ylabel('Statistic Graph in 24 hours')
    def __init__(self, **kwargs):
        super(StatisticScreen, self).__init__(**kwargs)
        #Considering whether we should just do it updating each 10 mins
        Clock.schedule_once(self.graph_test)
        #Clock.schedule_interval(self.graph_test,600) #proper callback time, for now is 0.1 s

    def graph_test(self, dt): 
        #Plot the graph using matplotlib
        self.graph_generate()
        plt.figure(0)
        plt.plot([1,23,2,4])
        plt.title('Temperature in 24 hours')
        self.ids.topline.add_widget(FigureCanvasKivyAgg(plt.gcf()))
        
        plt.figure(1)
        plt.plot([2,4,8, 16])
        plt.title('Humidity in 24 hours')
        self.ids.topline.add_widget(FigureCanvasKivyAgg(plt.gcf()))
        
        plt.figure(2)
        plt.plot([11,12,13,15])
        plt.title('Optic in 24 hours')
        self.ids.botline.add_widget(FigureCanvasKivyAgg(plt.gcf()))
        
        plt.figure(3)
        plt.plot([15,23,2,4])
        plt.title('Water Level in 24 hours')
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
        Clock.schedule_interval(self.get_data,10) #proper callback time, for now is 0.1 s
    def get_data(self,dt):
        global current_time
        current_time=strftime("%Y-%m-%d %H:%M:%S",localtime())
        self.ids.time_label.text=current_time
        self.alarm_check()
    def alarm_check(self):
        #if any sensor is beyond or below the threshold
        #Turn the button to be red and flashing
        #self.ids.alarm.background_color=(1,1,1,1)
        pass
    #def toggle_button(self):
    #design for the toggle button to contrl on and off
#testing plan:
#Whether I could use self.ids.ListOfSensors[Num] to identify the button




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