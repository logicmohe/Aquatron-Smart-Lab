#!/usr/bin/env python3

#    aquatron.py - Front end daemon for aquatron system based on Kivy
#
#    Copyright (C) 2020
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os
import sys
import random
import serial
from time import localtime, strftime,sleep
from datetime import datetime
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
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import BooleanProperty, ListProperty, StringProperty, ObjectProperty
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import FormatStrFormatter

from enum import Enum
import sqlite3

#Project Library: from aquatrond import 
import glob
'''
Initialization
'''
#initialize all the variables

_init=0.00
_init_min=0
_init_max=80

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

conn=sqlite3.connect('/run/aquatron/db.sqlite')
cur=conn.cursor()
#sensors, read in from GPIO
watertemp_sensor=waterlvl_sensor =waterleak_sensor   = \
    light_sensor=roomtemp_sensor=humidity_sensor=_init

#Setup: After reaching the limit, special event will be triggerred
watertemp_min=waterlvl_min=waterleak_min=light_min \
    =roomtemp_min=humidity_min=_init_min

watertemp_max=waterlvl_max=waterleak_max= \
    light_max=roomtemp_max=humidity_max=_init_max


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
        Clock.schedule_once(self.graph_generate)

    def graph_generate(self, dt): 
        try: #In case for initialization period, random data for first 24 hours
            global cur
            cur.execute('SELECT value FROM sensor_data WHERE name=? ORDER BY timestamp DESC LIMIT 144',('Water Tank 1 Temperature',))
            watertemp1=cur.fetchall()
            cur.execute('SELECT value FROM sensor_data WHERE name=? ORDER BY timestamp DESC LIMIT 144',('Water Tank 2 Temperature',))
            watertemp2=cur.fetchall()
            cur.execute('SELECT value FROM sensor_data WHERE name=? ORDER BY timestamp DESC LIMIT 144',('Water Level',))
            waterlvl=cur.fetchall()
            data1=[]
            for items in watertemp1:
                data1.append(float(items[0]))
            data2=[]
            for items in watertemp2:
                data2.append(float(items[0]))
            data3=[]
            for items in waterlvl:
                data3.append('ON' if int(items[0]) else 'OFF')
        except:
            data1 = data2 = data3 = [random.randrange(0,100) for i in range (144)]

        times = pd.date_range ('10-10-2020',periods=144, freq = '10MIN')

        self.graph_generate()
        figt=plt.figure(0)
        top=figt.add_subplot(111)
        plt.plot(times, data1, label="Upside")
        plt.plot(times, data2, label="Downside")
        plt.title('Water Temperature in 24 hours')
        plt.legend()
        xfmt=mdates.DateFormatter('%H:%M')
        top.xaxis.set_major_formatter(xfmt)
        self.ids.topline.add_widget(FigureCanvasKivyAgg(plt.gcf()))
        
        figb=plt.figure(1)
        bot=figb.add_subplot(111)
        plt.title('Water Level in 24 hours')
        plt.plot(times, data3)
        plt.legend()
        xfmt=mdates.DateFormatter('%H:%M')
        bot.xaxis.set_major_formatter(xfmt)
        self.ids.botline.add_widget(FigureCanvasKivyAgg(plt.gcf()))
        return


class RoomSensorScreen(Screen):
    data_items=ListProperty([])
    #build a simple graph

    def __init__(self, **kwargs):
        super(RoomSensorScreen, self).__init__(**kwargs)
        Clock.schedule_once(self.graph_generate)

    def graph_generate(self, dt): 
        try: #In case for initialization period, random data for first 24 hours
            global cur
            cur.execute('SELECT value FROM sensor_data WHERE name=? ORDER BY timestamp DESC LIMIT 144',('SI7021(temperature)',))
            roomtemp=cur.fetchall()
            cur.execute('SELECT value FROM sensor_data WHERE name=? ORDER BY timestamp DESC LIMIT 144',('SI7021(humidity)',))
            roomhumi=cur.fetchall()
            data1=[]
            for items in roomtemp:
                data1.append(float(items[0]))
            data2=[]
            for items in roomhumi:
                data2.append(float(items[0]))

        except:
            data1 = data2 = [random.randrange(0,100) for i in range (144)]

        times = pd.date_range ('10-10-2020',periods=144, freq = '10MIN')

        self.graph_generate()
        figt=plt.figure(0)
        top=figt.add_subplot(111)
        plt.title('Room Temperature in 24 hours')
        plt.plot(times, data1)
        plt.legend()
        xfmt=mdates.DateFormatter('%H:%M')
        top.xaxis.set_major_formatter(xfmt)
        self.ids.topline.add_widget(FigureCanvasKivyAgg(plt.gcf()))
        
        figb=plt.figure(1)
        bot=figb.add_subplot(111)
        plt.title('Room Humidity in 24 hours')
        plt.plot(times, data2)
        plt.legend()
        xfmt=mdates.DateFormatter('%H:%M')
        bot.xaxis.set_major_formatter(xfmt)
        self.ids.botline.add_widget(FigureCanvasKivyAgg(plt.gcf()))
        return

class OtherSensorScreen(Screen):
    data_items=ListProperty([])
    #build a simple graph

    def __init__(self, **kwargs):
        super(OtherSensorScreen, self).__init__(**kwargs)
        Clock.schedule_once(self.graph_generate)

    def graph_generate(self, dt): 
        try: #In case for initialization period, random data for first 24 hours
            global cur
            cur.execute('SELECT value FROM sensor_data WHERE name=? ORDER BY timestamp DESC LIMIT 144',('Ambient Light',))
            optic=cur.fetchall()
            cur.execute('SELECT value FROM sensor_data WHERE name=? ORDER BY timestamp DESC LIMIT 144',('Toggle Switch',))
            waterleak=cur.fetchall()
            data1=[]
            for items in optic:
                data1.append(float(items[0]))
            data2=[]
            for items in waterleak:
                data2.append('ON' if int(items[0]) else 'OFF')

        except:
            data1 = data2 = [random.randrange(0,100) for i in range (144)]

        times = pd.date_range ('10-10-2020',periods=144, freq = '10MIN')

        self.graph_generate()
        figt=plt.figure(0)
        top=figt.add_subplot(111)
        plt.plot(times, data1)
        plt.title('Ambient Light in 24 hours')
        plt.legend()
        xfmt=mdates.DateFormatter('%H:%M')
        top.xaxis.set_major_formatter(xfmt)
        self.ids.topline.add_widget(FigureCanvasKivyAgg(plt.gcf()))
        
        figb=plt.figure(1)
        bot=figb.add_subplot(111)
        plt.title('Water Leak in 24 hours')
        plt.plot(times, data2)
        plt.legend()
        xfmt=mdates.DateFormatter('%H:%M')
        bot.xaxis.set_major_formatter(xfmt)
        self.ids.botline.add_widget(FigureCanvasKivyAgg(plt.gcf()))
        return


#Kivy Setting Screen
class SettingScreen(Screen):
    #waiting for other items
    data_items=ListProperty([])
    def __init__(self, **kwargs):
        super(SettingScreen, self).__init__(**kwargs)
        Clock.schedule_interval(self.set_threshold,10)

    def set_threshold(self,dt):
        global SensorInfo
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
        return
    def setting_change(self, watertemp_min,watertemp_max, waterlvl_min, waterlvl_max,roomtemp_min, roomtemp_max, roomhumi_min, roomhumi_max, waterleak_min, waterleak_max, optic_min, optic_max):
        if watertemp_min <= watertemp_max and waterlvl_min <= waterlvl_max and roomtemp_min <= roomtemp_max and roomhumi_min <= roomhumi_max and waterleak_min <= waterleak_max and optic_min <= optic_max:
            ind = True
        else:
            ind = False
        popup=SettingPopup(self, ind)
        popup.open()
        if ind is True:
            global SensorInfo
            SensorInfo[SS.WATERTEMP.value][1]=watertemp_min
            SensorInfo[SS.WATERTEMP.value][2]=watertemp_max
            SensorInfo[SS.WATERLVL.value][1]=waterlvl_min
            SensorInfo[SS.WATERLVL.value][2]=waterlvl_max
            SensorInfo[SS.ROOMTEMP.value][1]=roomtemp_min
            SensorInfo[SS.ROOMTEMP.value][2]=roomtemp_max
            SensorInfo[SS.ROOMHUMI.value][1]=roomhumi_min
            SensorInfo[SS.ROOMHUMI.value][2]=roomhumi_max
            SensorInfo[SS.WATERLEAK.value][1]=waterleak_min
            SensorInfo[SS.WATERLEAK.value][2]=waterleak_max
            SensorInfo[SS.OPTIC.value][1]=optic_min
            SensorInfo[SS.OPTIC.value][2]=optic_max
            return
        else:
            return
#Popup
class SettingPopup(Popup):
    obj = ObjectProperty(None)

    def __init__(self, obj, ind):
        Popup.__init__(self)
        if ind is False:
            self.ids.popup.text="Error! Please try again"


#Kivy Setting Screen
class AlertingScreen(Screen):
    global AlertEmail
    #waiting for other items
    data_items=ListProperty([])
    def __init__(self, **kwargs):
        super(AlertingScreen, self).__init__(**kwargs)

    def alert_email(self):
        self.ids.Email1.text=AlertEmail[0]
        self.ids.Email2.text=AlertEmail[1]
        self.ids.Email3.text=AlertEmail[2]

    def alert_change(self, email1, email2, email3):
        AlertEmail[0]=email1
        AlertEmail[1]=email2
        AlertEmail[2]=email3
    

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
        #Get value from SQLite 3
        
        global cur
        cur.execute('SELECT value FROM sensor_data WHERE name=?  ORDER BY timestamp DESC LIMIT 1',('Water Tank 1 Temperature',))
        watertemp1=cur.fetchall()
        cur.execute('SELECT value FROM sensor_data WHERE name=?  ORDER BY timestamp DESC LIMIT 1',('Water Tank 2 Temperature',))
        watertemp2=cur.fetchall()
        self.ids.watertemp.text=str(round(float(watertemp1[0][0]),3))+" | "+str(round(float(watertemp2[0][0]),3))

        cur.execute('SELECT value FROM sensor_data WHERE name=?  ORDER BY timestamp DESC LIMIT 1',('Water Level',))
        waterlvl=cur.fetchall()
        self.ids.waterlvl.text=str(round(float(waterlvl[0][0]),3))

        cur.execute('SELECT value FROM sensor_data WHERE name=?  ORDER BY timestamp DESC LIMIT 1',('SI7021(temperature)',))
        roomtemp=cur.fetchall()
        self.ids.roomtemp.text=str(round(float(roomtemp[0][0]),3))

        cur.execute('SELECT value FROM sensor_data WHERE name=?  ORDER BY timestamp DESC LIMIT 1',('SI7021(humidity)',))
        roomhumi=cur.fetchall()
        self.ids.roomhumi.text=str(round(float(roomhumi[0][0]),3))

        cur.execute('SELECT value FROM sensor_data WHERE name=?  ORDER BY timestamp DESC LIMIT 1',('Toggle Switch',))
        waterleak=cur.fetchall()
        self.ids.waterleak.text=str(round(float(waterleak[0][0]),3))

        cur.execute('SELECT value FROM sensor_data WHERE name=?  ORDER BY timestamp DESC LIMIT 1',('Ambient Light',))
        optic=cur.fetchall()
        self.ids.optic.text=str(round(float(optic[0][0]),3))

        #Alarm check
        global SensorInfo
        if SensorInfo[SS.WATERTEMP.value][1] < float(watertemp1[0][0]) < SensorInfo[SS.WATERTEMP.value][2]:
            self.ids.watertemp.background_color=(1,1,1,1)
        else:
            self.ids.watertemp.background_color=(50,0,0,1)

        if SensorInfo[SS.WATERLVL.value][1] < float(waterlvl[0][0]) < SensorInfo[SS.WATERLVL.value][2]:
            self.ids.waterlvl.background_color=(1,1,1,1)
        else:
            self.ids.waterlvl.background_color=(50,0,0,1)

        if SensorInfo[SS.ROOMTEMP.value][1] < float(roomtemp[0][0]) < SensorInfo[SS.ROOMTEMP.value][2]:
            self.ids.roomtemp.background_color=(1,1,1,1)
        else:
            self.ids.roomtemp.background_color=(50,0,0,1)

        if SensorInfo[SS.ROOMHUMI.value][1] < float(roomhumi[0][0]) < SensorInfo[SS.ROOMHUMI.value][2]:
            self.ids.roomhumi.background_color=(1,1,1,1)
        else:
            self.ids.roomhumi.background_color=(50,0,0,1)

        if SensorInfo[SS.WATERLEAK.value][1] < float(waterleak[0][0]) < SensorInfo[SS.WATERLEAK.value][2]:
            self.ids.waterleak.background_color=(1,1,1,1)
        else:
            self.ids.waterleak.background_color=(50,0,0,1)

        if SensorInfo[SS.OPTIC.value][1] < float(optic[0][0]) < SensorInfo[SS.OPTIC.value][2]:
            self.ids.optic.background_color=(1,1,1,1)
        else:
            self.ids.optic.background_color=(50,0,0,1)

        return
    #def email_alert(self):
    #    yag=yagmail.SMTP('dalhousieaquatron@gmail.com','aquatron123')
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