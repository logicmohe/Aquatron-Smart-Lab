import os
import sys
import random
import serial
#import board
#import busio
#import RPI.GPIO as GPIO
from time import localtime, strftime,sleep
import pandas as pd

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

from enum import Enum
'''
Initialization
'''
#initialize all the variables

_init=0.00
_init_min=0
_init_max=100

AlertEmail=["dalhousieaquatron@gmail.com","dalhousieaquatron@gmail.com","dalhousieaquatron@gmail.com"]

current_time='0000-00-00 00:00:00'      #initialize the time

class SS(Enum):
    WATERTEMP=0
    WATERLVL=1
    ROOMTEMP=2
    ROOMHUMI=3
    WATERLEAK=4
    OPTIC=5

SensorInfo={}
for i in range(6):
    SensorInfo[i]=[_init, _init_min, _init_max]

# #sensors, read in from GPIO
# watertemp_sensor=waterlvl_sensor =waterleak_sensor   = \
#     light_sensor=roomtemp_sensor=humidity_sensor=_init

# #Setup: After reaching the limit, special event will be triggerred
# watertemp_min=waterlvl_min=waterleak_min=light_min \
#     =roomtemp_min=humidity_min=_init_min

# watertemp_max=waterlvl_max=waterleak_max= \
#     light_max=roomtemp_max=humidity_max=_init_max

#Note for future : use for loop to check if any sensor value is 
#out of range, use correpsonding button to make it read

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

    def __init__(self, **kwargs):
        super(WaterSensorScreen, self).__init__(**kwargs)
        #Clock.schedule_once(self.graph_test)
        Clock.schedule_interval(self.graph_test,600)

    def graph_test(self, dt): 
        #Plot the graph using matplotlib
        data1 = [random.randrange(0,100) for i in range (144)]
        data2 = [random.randrange(0,50) for i in range (144)]
        data3 = [random.randrange(50,100) for i in range (144)]

        times = pd.date_range ('10-10-2020',periods=144, freq = '10MIN')

        self.graph_generate()
        figt=plt.figure(0)
        top=figt.add_subplot(111)
        plt.plot(times, data1, label="Upside")
        plt.plot(times, data2, label="Downside")
        plt.plot(times, data3, label="Average")
        plt.title('Water Temperature in 24 hours')
        plt.legend()
        plt.ylim(top=100);plt.ylim(bottom=0)
        xfmt=mdates.DateFormatter('%H:%M')
        top.xaxis.set_major_formatter(xfmt)
        self.ids.topline.add_widget(FigureCanvasKivyAgg(plt.gcf()))
        
        figb=plt.figure(1)
        bot=figb.add_subplot(111)
        plt.plot(times, data1, label="Leftside")
        plt.plot(times, data2, label="Rightside")
        plt.plot(times, data3, label="Average")
        plt.title('Water Level in 24 hours')
        plt.legend()
        plt.ylim(top=100);plt.ylim(bottom=0)
        xfmt=mdates.DateFormatter('%H:%M')
        bot.xaxis.set_major_formatter(xfmt)
        self.ids.botline.add_widget(FigureCanvasKivyAgg(plt.gcf()))

        #return box
        #If this is keep refreshing, then use remove_widget(destination)
    def graph_generate(self):
        #overhere, read from postgreSQL data to generate Matplotlib graph
        pass

class RoomSensorScreen(Screen):
    data_items=ListProperty([])
    #build a simple graph

    def __init__(self, **kwargs):
        super(RoomSensorScreen, self).__init__(**kwargs)
        #Clock.schedule_once(self.graph_test)
        Clock.schedule_interval(self.graph_test,600) #proper callback time, for now is 0.1 s

    def graph_test(self, dt): 
        #Plot the graph using matplotlib
        data1 = [random.randrange(0,100) for i in range (144)]

        times = pd.date_range ('10-10-2020',periods=144, freq = '10MIN')

        self.graph_generate()
        figt=plt.figure(2)
        top=figt.add_subplot(111)
        plt.plot(times, data1, label="Upside")
        plt.title('Room Temperature in 24 hours')
        plt.ylim(top=100);plt.ylim(bottom=0)
        xfmt=mdates.DateFormatter('%H:%M')
        top.xaxis.set_major_formatter(xfmt)
        self.ids.topline.add_widget(FigureCanvasKivyAgg(plt.gcf()))
        
        data2 = [random.randrange(0,100) for i in range (144)]
        figb=plt.figure(3)
        bot=figb.add_subplot(111)
        plt.plot(times, data2)
        plt.title('Room Humidity in 24 hours')
        plt.ylim(top=100);plt.ylim(bottom=0)
        xfmt=mdates.DateFormatter('%H:%M')
        bot.xaxis.set_major_formatter(xfmt)
        self.ids.botline.add_widget(FigureCanvasKivyAgg(plt.gcf()))
        #return box
        #If this is keep refreshing, then use remove_widget(destination)
    def graph_generate(self):
        #overhere, read from postgreSQL data to generate Matplotlib graph
        pass

class OtherSensorScreen(Screen):
    data_items=ListProperty([])
    #build a simple graph

    def __init__(self, **kwargs):
        super(OtherSensorScreen, self).__init__(**kwargs)
        #Clock.schedule_once(self.graph_test)
        Clock.schedule_interval(self.graph_test,600) #proper callback time, for now is 0.1 s

    def graph_test(self, dt): 
        #Plot the graph using matplotlib
        data1 = [random.randrange(0,100) for i in range (144)]

        times = pd.date_range ('10-10-2020',periods=144, freq = '10MIN')

        self.graph_generate()
        figt=plt.figure(4)
        top=figt.add_subplot(111)
        plt.plot(times, data1, label="Upside")
        plt.title('Water Leak in 24 hours')
        plt.ylim(top=100);plt.ylim(bottom=0)
        xfmt=mdates.DateFormatter('%H:%M')
        top.xaxis.set_major_formatter(xfmt)
        self.ids.topline.add_widget(FigureCanvasKivyAgg(plt.gcf()))
        
        data2 = [random.randrange(0,100) for i in range (144)]
        figb=plt.figure(5)
        bot=figb.add_subplot(111)
        plt.plot(times, data2)
        plt.title('Optic Level in 24 hours')
        plt.ylim(top=100);plt.ylim(bottom=0)
        xfmt=mdates.DateFormatter('%H:%M')
        bot.xaxis.set_major_formatter(xfmt)
        self.ids.botline.add_widget(FigureCanvasKivyAgg(plt.gcf()))
        #return box
        #If this is keep refreshing, then use remove_widget(destination)
    def graph_generate(self):
        #overhere, read from postgreSQL data to generate Matplotlib graph
        pass

#Kivy Setting Screen
class SettingScreen(Screen):
    #waiting for other items
    data_items=ListProperty([])
    def __init__(self, **kwargs):
        super(SettingScreen, self).__init__(**kwargs)
        set_threshold()

    def set_threshold(self):
        self.ids.watertemp_slider_min.value=SensorInfo[SS.WATERTEMP.value][1]
        self.ids.watertemp_slider_max.value=SensorInfo[SS.WATERTEMP.value][2]
        self.ids.waterlvl_slider_min.value=SensorInfo[SS.WATERLVL.value][1]
        self.ids.waterlvl_slider_max.value=SensorInfo[SS.WATERLVL.value][2]
        self.ids.roomtemp_slider_min.value=SensorInfo[SS.ROOMTEMP.value][1]
        self.ids.roomtemp_slider_max.value=SensorInfo[SS.ROOMTEMP.value][2]
        self.ids.roomhumi_slider_min.value=SensorInfo[SS.ROOMHUMI.value][1]
        self.ids.roomhumi_slider_max.value=SensorInfo[SS.ROOMHUMI.value][2]
        self.ids.waterleak_slider_min.value=SensorInfo[SS.WATERLEAK.value][1]
        self.ids.waterleak_slider_max.value=SensorInfo[SS.WATERLEAK.value][2]
        self.ids.optic_slider_min.value=SensorInfo[SS.OPTIC.value][1]
        self.ids.optic_slider_max.value=SensorInfo[SS.OPTIC.value][2]
    pass

#Kivy Setting Screen
class AlertingScreen(Screen):
    global AlertEmail
    #waiting for other items
    data_items=ListProperty([])
    def __init__(self, **kwargs):
        super(AlertingScreen, self).__init__(**kwargs)
        self.alert_email()

    def alert_email(self):
        self.ids.Email1.text=AlertEmail[0]
        self.ids.Email2.text=AlertEmail[1]
        self.ids.Email3.text=AlertEmail[2]

    def alert_change(self, email1, email2, email3):
        AlertEmail[0]=email1
        AlertEmail[1]=email2
        AlertEmail[2]=email3
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
        self.ids.roomtemp.background_color=(50,0,0,1)
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