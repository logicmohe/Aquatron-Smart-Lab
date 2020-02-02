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
import RPI.GPIO as GPIO
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