#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# ecospec.py - Ecospec Instrumenation Package Main Program
# Copyright (C) 2014  Donald J. Bales, Argonne National Laboratory
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

try:
	import pifacedigitalio
except:
	print("Can't import pifacedigitalio.")

import axis_q1604
import cr1000
import datetime
import ephem
import fieldspec4
import os
import ptu_d300
import sys
import time

class EcoSpec:
	DATA_PATH         = "/home/ecospec/data/"
	LOG_PATH          = "/home/ecospec/log/"
	AXIS_Q1604_HOST   = "146.137.13.119"
	CR1000_HOST       = "146.137.13.118"
	FIELDSPEC4_HOST   = "146.137.13.117"
	PAN_TILE_DELAY    = 10
	PAN_TILT_HOST     = "/dev/ttyUSB0"
	POWER_RELAY       = 0
	ACTUATOR_RELAY    = 1
	ACTUATOR_DELAY    = 3
	ONE_MINUTE        = 60
	THIRTY_MINUTES    = 30 * 60

	def __init__(self):
		print "Ecospec.__init__()..."
		if not os.path.exists(EcoSpec.DATA_PATH):
			os.makedirs(EcoSpec.DATA_PATH)
		if not os.path.exists(EcoSpec.LOG_PATH):
			os.makedirs(EcoSpec.LOG_PATH)
		#self.camera_thread_status     = False
		#self.datalogger_thread_status = False
		self.data_set_time            = None
		self.data_set_id              = None
		self.since_time               = None
		self.sunrise                  = None
		self.sunset                   = None
		self.dark_current_results     = []
		self.white_reference_results  = []
		self.subject_matter_results   = []
		self.pantilt                  = None
		self.pantilt_position         = -1
		self.pantilt_positions        = [-170, -139, -108, -77, -46, -15, 15, 46, 77, 108, 139, 170]
		try:
			self.piface = pifacedigitalio.PiFaceDigital()
		except:
			print("Can't access pifacedigitalio.")
			self.piface               = None
		self.spectrometer             = None
		

	def main(self):
		print "EcoSpec.main()..."
		self.sunrise_time = self.calculate_sunrise()
		self.since_time   = time.strftime("%Y-%m-%dT05:00:00.00")
		self.sunset_time  = self.calculate_sunset()

		# Wait until 25 minutes before sunrise, then turn on the 
		# rest of the equipment, in order to warm up the spectrometer
		while time.time() < self.sunrise_time - EcoSpec.THIRTY_MINUTES:
			time.sleep(EcoSpec.ONE_MINUTE)
		
		self.power_up()

		# Wait until sunrise, then start collecting data
		while time.time() < self.sunrise_time:
			time.sleep(EcoSpec.ONE_MINUTE)

		count = 0
		# Collect data until sunset
		while time.time() < self.sunset_time:
			self.activate_pantilt()
			try:
				self.activate_spectrometer()
			except:
				# Darn if that spectrometer's TCP/IP interface doesn't respond sometimes!
				# If that happens, power it off and on, the try again.
				self.power_down()
				self.power_up()
				time.sleep(3)
				self.activate_spectrometer()
			
			#if count > 99:
			#	break
			count += 1
		
		self.power_down()

		exit(0)


	def get_next_position(self, current_position):
		if current_position < 11:
			next_position = current_position + 1
		else:
			next_position = 0

		return next_position


	def current_pantilt_position_string(self):
		return '{:+04d}'.format(self.pantilt_positions[self.pantilt_position])


	def activate_pantilt(self):
		# A serial communications device
		print "EcoSpec.activate_pantilt()..."

		if not self.pantilt:
			self.pantilt = ptu_d300.PtuD300('/dev/ttyUSB0', 38400)

		self.pantilt_position = self.get_next_position(self.pantilt_position)

		if self.pantilt_position == 0:
			self.pantilt.send(ptu_d300.PtuD300.STATUS_QUERY)
			#self.pantilt.send(ptu_d300.PtuD300.PAN_SPEED_ABSOLUTE + str(self.pantilt.pan_speed_maximum))
			self.pantilt.send(ptu_d300.PtuD300.PAN_SPEED_ABSOLUTE + str(1000))
		else:
			self.pantilt.send(ptu_d300.PtuD300.PAN_SPEED_ABSOLUTE + str(1000))

		self.pantilt.send(ptu_d300.PtuD300.PAN_IMMEDIATELY)

		self.pantilt.send(ptu_d300.PtuD300.PAN_POSITION_ABSOLUTE + str(self.pantilt.degrees_to_positions(self.pantilt_positions[self.pantilt_position])))

		result = self.pantilt.send(ptu_d300.PtuD300.PAN_AWAIT_COMPLETION)

		# Add a manual delay while the pan-tilt makes the long journey around
		if self.pantilt_position == 0:
			time.sleep(EcoSpec.PAN_TILT_DELAY)

		#print("result: '" + result +"'")
		#print(result[2:4])
		#if result[2:4] == "!P":
		if "!P" in result:
			print("trying again...")
			self.pantilt.send(ptu_d300.PtuD300.PAN_POSITION_ABSOLUTE)
			self.pantilt.send(ptu_d300.PtuD300.PAN_POSITION_ABSOLUTE + str(self.pantilt.degrees_to_positions(self.pantilt_positions[self.pantilt_position])))
			self.pantilt.send(ptu_d300.PtuD300.PAN_AWAIT_COMPLETION)

		return True


	def activate_spectrometer(self):
		# TCP/IP communications device
		print "EcoSpec.activate_spectrometer()..."

		self.white_reference_results = []
		self.dark_current_results    = []
		self.subject_matter_results  = []
		try:
			if not self.spectrometer:
				self.spectrometer = fieldspec4.FieldSpec4()

				print self.spectrometer

				self.spectrometer.open(EcoSpec.FIELDSPEC4_HOST)

				version = self.spectrometer.version()

				print "version.name: " + version.name
				print "version.value: " + str(version.value)
				print "version.type: " + str(version.type)

				restore = self.spectrometer.restore("1")
				print "restore.header: " + str(restore.header)

				if restore.header != 100:
					print "Trying restore again..."
					restore = self.spectrometer.restore("1")
					print "restore.header: " + str(restore.header)

				"""
					print "restore.header: " + str(restore.header)
					print "restore.errbyte: " + str(restore.errbyte)
					for i in range(0, 200):
						if restore.names[i]:
							print restore.names[i] + ": " + str(restore.values[i])
					print "restore.count: " + str(restore.count)
					print "restore.verify: " + str(restore.verify)
				"""
			else:
				self.spectrometer.open(EcoSpec.FIELDSPEC4_HOST)


			"""
			a = self.spectrometer.abort()

			print "abort.header: " + str(a.header)
			print "abort.errbyte: " + str(a.errbyte)
			print "abort.name: " + a.name
			print "abort.value: " + str(a.value)
			print "abort.count: " + str(a.count)
			"""

			self.extend_white_reference_arm()

			time.sleep(EcoSpec.ACTUATOR_DELAY)

			# Optimize the spectrometer with the white reference in field of view
			
			print "Optimize..."
			optimize = self.spectrometer.optimize(fieldspec4.FieldSpec4.OPT_VNIR_SWIR1_SWIR2)
			print "optimize.header: " + str(optimize.header)

			"""
			print "optimize.header: " + str(optimize.header)
			print "optimize.errbyte: " + str(optimize.errbyte)
			print "optimize.itime: " + str(optimize.itime)
			print "optimize.gain1: " + str(optimize.gain1)
			print "optimize.gain2: " + str(optimize.gain2)
			print "optimize.offset1: " + str(optimize.offset1)
			print "optimize.offset2: " + str(optimize.offset2)
			"""

			# Open the shutter and collect 10 white reference readings
			acquire = None
			if optimize.header == 100:
				print "Acquire White Reference Readings..."
				acquire_white_reference_readings = self.spectrometer.acquire(fieldspec4.FieldSpec4.ACQUIRE_SET_SAMPLE_COUNT, "10", "0")
				print "acquire_white_reference_readings.spectrum_header.header: " + str(acquire_white_reference_readings.spectrum_header.header)
				self.white_reference_results.append(acquire_white_reference_readings)
				"""
				print "acquire_white_reference_readings.spectrum_header.header: " + str(acquire_white_reference_readings.spectrum_header.header)
				print "acquire_white_reference_readings.spectrum_header.errbyte: " + str(acquire_white_reference_readings.spectrum_header.errbyte)
				print "acquire_white_reference_readings.spectrum_header.sample_count: " + str(acquire_white_reference_readings.spectrum_header.sample_count)
				print "acquire_white_reference_readings.spectrum_header.trigger: " + str(acquire_white_reference_readings.spectrum_header.trigger)
				print "acquire_white_reference_readings.spectrum_header.voltage: " + str(acquire_white_reference_readings.spectrum_header.voltage)
				print "acquire_white_reference_readings.spectrum_buffer length: " + str(len(acquire_white_reference_readings.spectrum_buffer))
				spectrum_data = "spectrum_data: " + str(acquire_white_reference_readings.spectrum_buffer[0]) 
				for i in range(1, len(acquire_white_reference_readings.spectrum_buffer)):
					spectrum_data += ","
					spectrum_data += str(acquire_white_reference_readings.spectrum_buffer[i])
				print spectrum_data
				"""				

			# Close the shutter and collect 25 dark current readings 
			# TODO get time for ensuring restraction
			self.retract_white_reference_arm()
			self.retract_white_reference_start_time = time.time()

			control = None
			if optimize.header                                         == 100 and \
			   acquire_white_reference_readings.spectrum_header.header == 100:
			   	print "Close the shutter..."
				control = self.spectrometer.control(fieldspec4.FieldSpec4.CONTROL_VNIR, fieldspec4.FieldSpec4.CONTROL_SHUTTER, fieldspec4.FieldSpec4.CLOSE_SHUTTER)
				print "control.header: " + str(control.header)
				if control.header == 100:
					print "Acquire Dark Current Readings..."
					acquire_dark_current_readings = self.spectrometer.acquire(fieldspec4.FieldSpec4.ACQUIRE_SET_SAMPLE_COUNT, "25", "0")
					print "acquire_dark_current_readings.spectrum_header.header: " + str(acquire_dark_current_readings.spectrum_header.header)
					self.dark_current_results.append(acquire_dark_current_readings)
					"""
					print "acquire_dark_current_readings.spectrum_header.header: " + str(acquire_dark_current_readings.spectrum_header.header)
					print "acquire_dark_current_readings.spectrum_header.errbyte: " + str(acquire_dark_current_readings.spectrum_header.errbyte)
					print "acquire_dark_current_readings.spectrum_header.sample_count: " + str(acquire_dark_current_readings.spectrum_header.sample_count)
					print "acquire_dark_current_readings.spectrum_header.trigger: " + str(acquire_dark_current_readings.spectrum_header.trigger)
					print "acquire_dark_current_readings.spectrum_header.voltage: " + str(acquire_dark_current_readings.spectrum_header.voltage)
					print "acquire_dark_current_readings.spectrum_buffer length: " + str(len(acquire_dark_current_readings.spectrum_buffer))
					spectrum_data = "spectrum_data: " + str(acquire_dark_current_readings.spectrum_buffer[0]) 
					for i in range(1, len(acquire_dark_current_readings.spectrum_buffer)):
						spectrum_data += ","
						spectrum_data += str(acquire_dark_current_readings.spectrum_buffer[i])
					print spectrum_data
					"""
			   	print "Open the shutter..."
				control = self.spectrometer.control(fieldspec4.FieldSpec4.CONTROL_VNIR, fieldspec4.FieldSpec4.CONTROL_SHUTTER, fieldspec4.FieldSpec4.OPEN_SHUTTER)
				print "control.header: " + str(control.header)

			#Verify retraction
			self.retract_white_reference_stop_time = time.time()
			self.acquire_dark_reading_elapsed_time = self.retract_white_reference_stop_time - self.retract_white_reference_start_time
			if self.acquire_dark_reading_elapsed_time < EcoSpec.ACTUATOR_DELAY:
				time.sleep(EcoSpec.ACTUATOR_DELAY - self.acquire_dark_reading_elapsed_time)

			self.data_set_time = time.time()
			print(self.data_set_time)
			self.data_set_id   = time.strftime("%Y%m%d%H%M%S", time.localtime(self.data_set_time))
			self.activate_camera()

			# Open the shutter and collect 10 subject matter readings

			if optimize.header                                         == 100 and \
			   acquire_white_reference_readings.spectrum_header.header == 100 and \
			   acquire_dark_current_readings.spectrum_header.header    == 100 and \
			   control.header                                          == 100:
				print "Acquire Subject Matter Readings 15x..."
				for j in range(0, 14):
					acquire_subject_matter_readings = self.spectrometer.acquire(fieldspec4.FieldSpec4.ACQUIRE_SET_SAMPLE_COUNT, "10", "0")
					print "acquire_subject_matter_readings.spectrum_header.header: " + str(acquire_subject_matter_readings.spectrum_header.header)
					self.subject_matter_results.append(acquire_subject_matter_readings)
					"""
					print "acquire_subject_matter_readings.spectrum_header.header: " + str(acquire_subject_matter_readings.spectrum_header.header)
					print "acquire_subject_matter_readings.spectrum_header.errbyte: " + str(acquire_subject_matter_readings.spectrum_header.errbyte)
					print "acquire_subject_matter_readings.spectrum_header.sample_count: " + str(acquire_subject_matter_readings.spectrum_header.sample_count)
					print "acquire_subject_matter_readings.spectrum_header.trigger: " + str(acquire_subject_matter_readings.spectrum_header.trigger)
					print "acquire_subject_matter_readings.spectrum_header.voltage: " + str(acquire_subject_matter_readings.spectrum_header.voltage)
					print "acquire_subject_matter_readings.spectrum_buffer length: " + str(len(acquire_subject_matter_readings.spectrum_buffer))
					spectrum_data = "spectrum_data: " + str(acquire_subject_matter_readings.spectrum_buffer[0]) 
					for i in range(1, len(acquire_subject_matter_readings.spectrum_buffer)):
						spectrum_data += ","
						spectrum_data += str(acquire_subject_matter_readings.spectrum_buffer[i])
					print spectrum_data
					"""

			self.activate_datalogger()
			self.since_time = time.strftime("%Y-%m-%dT%H:%M:%S.00", time.localtime(self.data_set_time))
			self.save_spectrometer_readings()
			self.spectrometer.close()

			# Wait for the camera and data logger to finish up
#			while self.camera_thread_status     < 1 and \
#			      self.datalogger_thread_status < 1:
#			    time.sleep(1)
		except:
			print "EcoSpec.activate_spectrometer(): ERROR:"
			print "sys.exc_type: " 
			print  sys.exc_type
			print "sys.exc_value: "
			print  sys.exc_value
			print "sys.exc_traceback: "
			print  sys.exc_traceback
			print "sys.exc_info(): " 
			print  sys.exc_info()
			if not self.spectrometer:
				self.spectrometer.close()
			raise


		return True


	def activate_camera(self):
		# TCP/IP communications device
		print "EcoSpec.activate_camera()..."

		camera = axis_q1604.AxisQ1604(self.data_set_id, self.current_pantilt_position_string(), EcoSpec.DATA_PATH, EcoSpec.LOG_PATH, EcoSpec.AXIS_Q1604_HOST)

		return True


	def activate_datalogger(self):
		# A serial communications device
		print "EcoSpec.activate_datalogger()..."

		data_logger = cr1000.CR1000(self.data_set_id, self.current_pantilt_position_string(), EcoSpec.DATA_PATH, EcoSpec.LOG_PATH, self.since_time, EcoSpec.CR1000_HOST)

		return True


	def calculate_sunrise(self):
		print "EcoSpec.calculate_sunrise()..."

		today_datetime = datetime.datetime.today()
		today_string   = today_datetime.strftime("%Y%m%d")
		#print 'today_datetime: ' + str(type(today_datetime))
		#print 'today_datetime: ' + str(today_datetime)
		#print 'today_string:   ' + today_string

		#Make an observer
		observer      = ephem.Observer()

		#PyEphem takes and returns only UTC times. 15:00 is noon in observerericton
		#observer_datetime = datetime.datetime(2014,10,7,0,0,0)
		#observer_datetime = datetime.datetime(2014,10,8,5,0,0)
		observer_datetime = datetime.datetime.utcnow()
		observer.date = observer_datetime
		#print 'observer.date:  ' + str(type(observer.date))
		#print 'observer.date:  ' + str(observer.date)

		#Location of Batvia, IL
		#41.848889, -88.308333
		#Location of Fermilab in Batavia, IL
		#41.850617, -88.263688
		observer.lon  = str(-88.263688) #Note that lon should be in string format
		observer.lat  = str(41.850617)      #Note that lat should be in string format

		#Elevation of Batavia, IL (666 ft) in metres
		observer.elev = 203

		#To get U.S. Naval Astronomical Almanac values, use these settings
		observer.pressure= 0
		observer.horizon = '-0:34'

		# Get the sunset time so we can compare it against the current time
		sunset_datetime  = ephem.localtime(observer.next_setting(ephem.Sun())) #Sunset
		sunset_string    = sunset_datetime.strftime("%Y%m%d")
		if sunset_string != today_string:
			sunset_datetime  = ephem.localtime(observer.previous_setting(ephem.Sun())) #Sunset

		#print 'if ' + str(sunset_datetime) + ' < ' + str(ephem.localtime(observer.date)) + ":"
		# If the sun has already set, get the next day's settings
		if ephem.localtime(observer.date) > sunset_datetime:
			today_datetime    = today_datetime + datetime.timedelta(days=1)
			today_string      = today_datetime.strftime("%Y%m%d")
			observer_datetime = observer_datetime + datetime.timedelta(days=1)
			observer.date     = observer_datetime

		sunrise_datetime = ephem.localtime(observer.next_rising(ephem.Sun())) #Sunrise
		sunrise_string   = sunrise_datetime.strftime("%Y%m%d")
		if sunrise_string != today_string:
			sunrise_datetime = ephem.localtime(observer.previous_rising(ephem.Sun())) #Sunrise

		sunset_datetime  = ephem.localtime(observer.next_setting(ephem.Sun())) #Sunset
		sunset_string    = sunset_datetime.strftime("%Y%m%d")
		if sunset_string != today_string:
			sunset_datetime  = ephem.localtime(observer.previous_setting(ephem.Sun())) #Sunset

		#print 'sunrise: ' + str(type(sunrise_datetime))
		#print 'sunset: ' + str(type(sunset_datetime))
		#print "sunrise: " + str(sunrise_datetime)
		#print "sunset:  " + str(sunset_datetime)		

		print sunrise_datetime.strftime('%Y-%m-%dT%H:%M:%S')
		return time.mktime(time.strptime(sunrise_datetime.strftime('%Y-%m-%dT%H:%M:%S'), '%Y-%m-%dT%H:%M:%S'))


	def calculate_sunset(self):
		today_datetime = datetime.datetime.today()
		today_string   = today_datetime.strftime("%Y%m%d")
		#print 'today_datetime: ' + str(type(today_datetime))
		#print 'today_datetime: ' + str(today_datetime)
		#print 'today_string:   ' + today_string

		#Make an observer
		observer      = ephem.Observer()

		#PyEphem takes and returns only UTC times. 15:00 is noon in observerericton
		#observer_datetime = datetime.datetime(2014,10,7,0,0,0)
		#observer_datetime = datetime.datetime(2014,10,8,5,0,0)
		observer_datetime = datetime.datetime.utcnow()
		observer.date = observer_datetime
		#print 'observer.date:  ' + str(type(observer.date))
		#print 'observer.date:  ' + str(observer.date)

		#Location of Batvia, IL
		#41.848889, -88.308333
		#Location of Fermilab in Batavia, IL
		#41.850617, -88.263688
		observer.lon  = str(-88.263688) #Note that lon should be in string format
		observer.lat  = str(41.850617)      #Note that lat should be in string format

		#Elevation of Batavia, IL (666 ft) in metres
		observer.elev = 203

		#To get U.S. Naval Astronomical Almanac values, use these settings
		observer.pressure= 0
		observer.horizon = '-0:34'

		# Get the sunset time so we can compare it against the current time
		sunset_datetime  = ephem.localtime(observer.next_setting(ephem.Sun())) #Sunset
		sunset_string    = sunset_datetime.strftime("%Y%m%d")
		if sunset_string != today_string:
			sunset_datetime  = ephem.localtime(observer.previous_setting(ephem.Sun())) #Sunset

		#print 'if ' + str(sunset_datetime) + ' < ' + str(ephem.localtime(observer.date)) + ":"
		# If the sun has already set, get the next day's settings
		if ephem.localtime(observer.date) > sunset_datetime:
			today_datetime    = today_datetime + datetime.timedelta(days=1)
			today_string      = today_datetime.strftime("%Y%m%d")
			observer_datetime = observer_datetime + datetime.timedelta(days=1)
			observer.date     = observer_datetime

		sunrise_datetime = ephem.localtime(observer.next_rising(ephem.Sun())) #Sunrise
		sunrise_string   = sunrise_datetime.strftime("%Y%m%d")
		if sunrise_string != today_string:
			sunrise_datetime = ephem.localtime(observer.previous_rising(ephem.Sun())) #Sunrise

		sunset_datetime  = ephem.localtime(observer.next_setting(ephem.Sun())) #Sunset
		sunset_string    = sunset_datetime.strftime("%Y%m%d")
		if sunset_string != today_string:
			sunset_datetime  = ephem.localtime(observer.previous_setting(ephem.Sun())) #Sunset

		#print 'sunrise: ' + str(type(sunrise_datetime))
		#print 'sunset: ' + str(type(sunset_datetime))
		#print "sunrise: " + str(sunrise_datetime)
		#print "sunset:  " + str(sunset_datetime)		

		print sunset_datetime.strftime('%Y-%m-%dT%H:%M:%S')
		return time.mktime(time.strptime(sunset_datetime.strftime('%Y-%m-%dT%H:%M:%S'), '%Y-%m-%dT%H:%M:%S'))


	def extend_white_reference_arm(self):
		print "EcoSpec.extend_white_reference_arm()..."
		if self.piface:
			self.piface.relays[EcoSpec.ACTUATOR_RELAY].turn_on()
		return True


	def power_down(self):
		print "EcoSpec.power_down()..."
		if self.piface:
			self.piface.relays[EcoSpec.POWER_RELAY].turn_off()
		return True


	def power_up(self):
		print "EcoSpec.power_up()..."
		if self.piface:
			self.piface.relays[EcoSpec.POWER_RELAY].turn_on()
		return True


	def retract_white_reference_arm(self):
		print "EcoSpec.retract_white_reference_arm()..."
		if self.piface:
			self.piface.relays[EcoSpec.ACTUATOR_RELAY].turn_off()
		return True


	def save_spectrometer_readings(self):
		print "EcoSpec.save_spectrometer_readings()..."
		delimiter = ","
		data_set_timestamp_string = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.data_set_time))
		file_name = EcoSpec.DATA_PATH + self.data_set_id + "-" + self.current_pantilt_position_string() + "-fieldspec4" + "-white_reference.csv"
		file_handle = open(file_name, "w")
		for i in range(0, len(self.white_reference_results)):
			if i == 0:
				file_handle.write("data_set_time"           + delimiter + "pantilt_position"                     + delimiter + self.white_reference_results[i].to_csv_heading() + "\n")
				file_handle.write(data_set_timestamp_string + delimiter + self.current_pantilt_position_string() + delimiter + self.white_reference_results[i].to_csv()         + "\n")
			else:
				file_handle.write(data_set_timestamp_string + delimiter + self.current_pantilt_position_string() + delimiter + self.white_reference_results[i].to_csv() + "\n")
		file_handle.close()

		file_name = EcoSpec.DATA_PATH + self.data_set_id + "-" + self.current_pantilt_position_string() + "-fieldspec4" + "-dark_current.csv"
		file_handle = open(file_name, "w")
		for i in range(0, len(self.dark_current_results)):
			if i == 0:
				file_handle.write("data_set_time"           + delimiter + "pantilt_position"                     + delimiter + self.dark_current_results[i].to_csv_heading() + "\n")
				file_handle.write(data_set_timestamp_string + delimiter + self.current_pantilt_position_string() + delimiter + self.dark_current_results[i].to_csv()         + "\n")
			else:
				file_handle.write(data_set_timestamp_string + delimiter + self.current_pantilt_position_string() + delimiter + self.dark_current_results[i].to_csv() + "\n")
		file_handle.close()

		file_name = EcoSpec.DATA_PATH + self.data_set_id + "-" + self.current_pantilt_position_string() + "-fieldspec4" + "-subject_matter.csv"
		file_handle = open(file_name, "w")
		for i in range(0, len(self.subject_matter_results)):
			if i == 0:
				file_handle.write("data_set_time"           + delimiter + "pantilt_position"                     + delimiter + self.subject_matter_results[i].to_csv_heading() + "\n")
				file_handle.write(data_set_timestamp_string + delimiter + self.current_pantilt_position_string() + delimiter + self.subject_matter_results[i].to_csv()         + "\n")
			else:
				file_handle.write(data_set_timestamp_string + delimiter + self.current_pantilt_position_string() + delimiter + self.subject_matter_results[i].to_csv() + "\n")
		file_handle.close()
		return True


if __name__ == '__main__':
	program = EcoSpec()
	program.main()
