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
from kivy.uix.textinput import TextInput
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
import matplotlib.dates as mdates

'''
Initialization
'''
#initialize all the variables

_init=0.00
_init_min=0
_init_max=100

current_time='0000-00-00 00:00:00'      #initialize the time

#sensors, read in from GPIO
watertemp_sensor=waterlvl_sensor =liquid_sensor   = \
    light_sensor=airtemp_sensor=humidity_sensor=_init

#Setup: After reaching the limit, special event will be triggerred
watertemp_min=waterlvl_min=liquid_min=light_min \
    =airtemp_min=humidity_min=_init_min

watertemp_max=waterlvl_max=liquid_max= \
    light_max=airtemp_max=humidity_max=_init_max

#Note for future : use for loop to check if any sensor value is 
#out of range, use correpsonding button to make it read

# in case for future expandsion
# WATERTEMP=0
# WATERLVL=1
# LIQUID=2
# LIGHT=3
# AIRTEMP=4
# HUMIDITY=5
# ListOfSensor=['watertemp','waterlvl','liquid','light','airtemp','humidity']

'''
Data Processing
'''
#read in data and process in this section



'''
Kivy Interface
'''
#Kivy StatisticScreen for anylyzing the collected data in 24 hours
class WaterSensorScreen(Screen):
    data_items=ListProperty([])
    #build a simple graph
    
    plt.ylabel('Statistic Graph in 24 hours for water level and water temperature')
    def __init__(self, **kwargs):
        super(WaterSensorScreen, self).__init__(**kwargs)
        #Considering whether we should just do it updating each 10 mins
        Clock.schedule_once(self.graph_test)
        #Clock.schedule_interval(self.graph_test,600)

    def graph_test(self, dt): 
        #Plot the graph using matplotlib
        x = ['00:00','06:00','12:00','18:00']

        self.graph_generate()
        plt.figure(0)

        plt.plot(x,[17,19,23,20])
        plt.title('Average Water Temperature')
        self.ids.topline.add_widget(FigureCanvasKivyAgg(plt.gcf()))
        
        plt.figure(1)
        plt.plot(x,[18,19,22,20])
        plt.title('Upside Water Temperature')
        self.ids.topline.add_widget(FigureCanvasKivyAgg(plt.gcf()))

        plt.figure(2)
        plt.plot(x,[16,18,24,20])
        plt.title('Downside Water Temperature')
        self.ids.topline.add_widget(FigureCanvasKivyAgg(plt.gcf()))
        
        plt.figure(3)
        plt.plot(x,[11,11,13,11])
        plt.title('Average Water Level')
        self.ids.botline.add_widget(FigureCanvasKivyAgg(plt.gcf()))
        
        plt.figure(4)
        plt.plot(x,[11,12,13,11])
        plt.title('Leftside Water Level')
        self.ids.botline.add_widget(FigureCanvasKivyAgg(plt.gcf()
        ))

        plt.figure(5)
        plt.plot(x,[11,10,13,11])
        plt.title('Rightside Water Level')
        self.ids.botline.add_widget(FigureCanvasKivyAgg(plt.gcf()
        ))
        #return box
        #If this is keep refreshing, then use remove_widget(destination)
    def graph_generate(self):
        #overhere, read from postgreSQL data to generate Matplotlib graph
        pass

class OtherSensorScreen(Screen):
    data_items=ListProperty([])
    #build a simple graph
    

    plt.ylabel('Statistic Graph in 24 hours')
    def __init__(self, **kwargs):
        super(OtherSensorScreen, self).__init__(**kwargs)
        #Considering whether we should just do it updating each 10 mins
        Clock.schedule_once(self.graph_test)
        #Clock.schedule_interval(self.graph_test,600) #proper callback time, for now is 0.1 s

    def graph_test(self, dt): 
        #Plot the graph using matplotlib
        self.graph_generate()
        plt.figure(6)
        x = ['00:00','04:00','08:00','12:00','16:00','20:00',]
        plt.plot(x,[17,18,18,19,20,18])
        plt.title('Room Temperature in 24 hours')
        self.ids.topline.add_widget(FigureCanvasKivyAgg(plt.gcf()))
        
        plt.figure(7)
        plt.plot(x,[4,3,2,4,8, 16])
        plt.title('Room Humidity in 24 hours')
        self.ids.topline.add_widget(FigureCanvasKivyAgg(plt.gcf()))
        
        plt.figure(8)
        plt.plot(x,[0,0,11,12,13,15])
        plt.title('Optic in 24 hours')
        self.ids.botline.add_widget(FigureCanvasKivyAgg(plt.gcf()))
        
        plt.figure(9)
        plt.plot(x,[10,11,15,23,2,4])
        plt.title('Water Leak in 24 hours')
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
        Clock.schedule_interval(self.get_data,1)
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