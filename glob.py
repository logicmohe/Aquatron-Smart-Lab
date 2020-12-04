#!/usr/bin/env python3

#    aquatrond - Backend daemon for aquatron system
#
#    Copyright (C) 2020 Josh Boudreau <josh.boudreau@dal.ca>
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

# TODO: Send data to ThingsBoard

SENSOR_CONFIG = '/etc/aquatron/sensors.conf'

import time
import configparser
import sys
import os
import json
from pathlib import Path
import RPi.GPIO as GPIO
import board
import busio
import adafruit_si7021
import Adafruit_ADS1x15
import adafruit_veml7700
import dataset
import signal
import paho.mqtt.client as mqtt

i2c = busio.I2C(board.SCL, board.SDA)
adc = Adafruit_ADS1x15.ADS1015()

DEFAULT_CONFIG_STR = (
'''# Global config
[Global]
# sensor polling period in seconds
Period = 10
ThingsBoard Host = 
ThingsBoard Access Token = 
# Write list of sensors here.
# Example:
# [Water Tank 1 Temperature]
# Bus = 1wire
# Address = 0x123
# Model = abc123
'''
)

########################################################################
# read_config
# receives: path to sensor config file as string
# does: creates path and file if either DNE, parses config
# returns: ConfigParser object filled with parsed info
########################################################################
def read_config(path_str):
	config_path = Path(path_str)
	# check if directory exists
	if not os.path.exists(config_path.parent):
		# create path
		try:
			os.mkdir(config_path.parent)
		except OSError as err:
			print("OS error: {0}".format(err))
			print("Are you root?")
			sys.exit(1)
	# check if file exists
	if not os.path.exists(config_path):
		# create path
		try:
			f = open(config_path, "w")
			f.write(DEFAULT_CONFIG_STR)
			f.close()
			print(f'Please populate {SENSOR_CONFIG}')
			sys.exit(0)
		except OSError as err:
			print("OS error: {0}".format(err))
			print("Are you root?")
			sys.exit(1)
	# file exists
	config = configparser.ConfigParser()
	try:
		config.read(config_path)
	except OSError as err:
		print("OS error: {0}".format(err))
		print("Are you root?")
		sys.exit(1)
	return config

########################################################################
# get_global_conf
# receives: ConfigParser object filled with parsed info
# does: grabs global section and deletes it from passed dictionary
# returns: ConfigParser object filled with only sensor info
########################################################################
def get_global_conf(config):
	glob = {}
	if "Global" in config:
		if "Period" in config["Global"]:
			try:
				glob["Period"] = float(config["Global"]["Period"])
			except ValueError as err:
				print("Invalid period in [Global]: {0}".format(err))
				print("Defaulting to Period = 10")
				glob["Period"] = 10.0
		else:
			# default to 10 second poll period
			print("Warning: no Period in [Global] in config. Default: 10")
			glob["Period"] = 10.0
		if "OWFS Mountpoint" in config["Global"]:
			glob["owfs"] = config["Global"]["OWFS Mountpoint"]
		else:
			glob["owfs"] = "/mnt/1wire" # default
		if "ThingsBoard Host" in config["Global"]:
			glob["tb_host"] = config["Global"]["ThingsBoard Host"]
			if "ThingsBoard Access Token" in config["Global"]:
				glob["use_tb"] = True
				glob["tb_token"] = config["Global"]["ThingsBoard Access Token"]
			else:
				print("Warning: No ThingsBoard Access Token set in config. Not using Thingsboard.");
				glob["use_tb"] = False
		else:
			print("Warning: No ThingsBoard Host set in config. Not using Thingsboard.");
			glob["use_tb"] = False
		del config["Global"]
	else:
		# default to 10 second poll period
		print("Warning: no [Global] section in config. Default period: 10")
		glob["Period"] = 10.0
		print("Warning: no OWFS Mountpoint set in config. Default: /mnt/owfs")
		glob["owfs"] = "/mnt/owfs"
	return glob

########################################################################
# build_sensor_lists
# receives: ConfigParser object obtained from read_config()
# does: sorts sensors from config into 1wire sensor list, i2c sensor
#       list, analog sensor lise, and digital IO sensor list,
#       verifying that needed fields are there
# returns: tuple of lists (oneWire, i2c, digitalIO, analog)
########################################################################
def build_sensor_lists(config):
	oneWire = []
	i2c = []
	digitalIO = []
	analog = []
	oneWireNames = ["1WIRE", "ONEWIRE"]
	i2cNames = ["2WIRE", "TWOWIRE", "TWI", "I2C"]
	digitalIONames = ["GPIO", "DIGITAL", "IO", "DIGITALIO", "BOOL", "BOOLEAN"]
	analogNames = ["ANALOG"]
	
	dontNeedAddress = ["SI7021", "VEML7700"]
	
	errors = False
	for friendly_name in config.sections():
		s = config[friendly_name]
		if "Bus" not in s:
			print(f'Bus type not specified for {friendly_name}.')
			errors = True
			continue
		
		sensor = {"value" : None}
		sensor["name"] = friendly_name
		
		if "Address" in s:
			sensor["addr"] = s["Address"]
		elif s["Model"].upper() not in dontNeedAddress:
			print(f'Address type not specified for {friendly_name}.')
			errors = True
		
		bus = s["Bus"].upper()
		
		if "Model" in s:
			sensor["model"] = s["Model"].upper()
		elif bus not in digitalIONames + analogNames:
			print(f'Model number not specified for {friendly_name}.')
			errors = True
		
		if bus in oneWireNames:
			oneWire.append(sensor.copy())
		elif bus in i2cNames:
			if sensor["model"] == "SI7021":
				sensor["type"] = "temperature"
				i2c.append(sensor.copy())
				i2c[-1]["name"] += "(temperature)"
				sensor["type"] = "humidity"
				i2c.append(sensor.copy())
				i2c[-1]["name"] += "(humidity)"
			else:
				i2c.append(sensor.copy())
		elif bus in digitalIONames:
			try:
				sensor["addr"] = int(sensor["addr"])
			except ValueError:
				print(f'{sensor["name"]} has invalid address')
				errors = True
			GPIO.setup(sensor["addr"], GPIO.IN)
			digitalIO.append(sensor.copy())
		elif bus in analogNames:
			try:
				sensor["addr"] = int(sensor["addr"])
			except ValueError:
				print(f'{sensor["name"]} has invalid address')
				errors = True
			analog.append(sensor.copy())
		else: # unknown bus type
			print(f'Unknown bus type for {friendly_name}: {s["Bus"]}')
			errors = True
	if errors:
		print(f'Please fix these errors in {SENSOR_CONFIG}')
		sys.exit(1)
	return oneWire, i2c, digitalIO, analog

def main():
	GPIO.setmode(GPIO.BCM)
	config = read_config(SENSOR_CONFIG)
	global_conf = get_global_conf(config)
	oneWire, i2c, digitalIO, analog = build_sensor_lists(config)

if __name__ == "__main__":
	main()
