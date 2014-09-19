# -*- coding: utf-8 -*-
#
# fieldspec4.py - Ecospec FieldSpec4 Program
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

import select
import socket
import struct
import time

#   ABORT RETURN VALUES
class FieldSpec4Abort:
	def __init__(self, response):
		fs4 = struct.unpack("!ii30sdi", response)
		self.header = fs4[0]
		self.errbyte = fs4[1]
		self.name = fs4[2]
		self.value = fs4[3]
		self.count = fs4[4]

#	ACQUIRE RETURN VALUES
class FieldSpec4VnirHeader:
	def __init__(self, response):
        #                     1234567890123456
		fs4 = struct.unpack("!iiiiiiiiiiiiiiii", response)
		self.it = fs4[0]
		self.scans = fs4[1]
		self.max_channel = fs4[2]
		self.min_channel = fs4[3]
		self.saturation = fs4[4]
		self.shutter = fs4[5]
		self.reserved0 = fs4[6]
		self.reserved1 = fs4[7]
		self.reserved2 = fs4[8]
		self.reserved3 = fs4[9]
		self.reserved4 = fs4[10]
		self.reserved5 = fs4[11]
		self.reserved6 = fs4[12]
		self.reserved7 = fs4[13]
		self.reserved8 = fs4[14]
		self.reserved9 = fs4[15]

class FieldSpec4SwirHeader:
	def __init__(self, response):
        #                     1234567890123456
		fs4 = struct.unpack("!iiiiiiiiiiiiiiii", response)
		self.tec_status = fs4[0]
		self.tec_current = fs4[1]
		self.max_channel = fs4[2]
		self.min_channel = fs4[3]
		self.saturation = fs4[4]
		self.a_scans = fs4[5]
		self.b_scans = fs4[6]
		self.dark_current = fs4[7]
		self.gain = fs4[8]
		self.offset = fs4[9]
		self.scansize1 = fs4[10]
		self.scansize2 = fs4[11]
		self.reserved0 = fs4[12]
		self.reserved1 = fs4[13]
		self.reserved2 = fs4[14]
		self.reserved3 = fs4[15]

class FieldSpec4SpectrumHeader:
	def __init__(self, response):
        #                     1234567890123456
		fs4 = struct.unpack("!iiiiiiiiiiiiiiii64s64s64s", response)
		self.header = fs4[0]
		self.errbyte = fs4[1]
		self.sample_count = fs4[2]
		self.trigger = fs4[3]
		self.voltage = fs4[4]
		self.current = fs4[5]
		self.temperature = fs4[6]
		self.motor_current = fs4[7]
		self.instrument_hours = fs4[8]
		self.instrument_minutes = fs4[9]
		self.instrument_type = fs4[10]
		self.ab = fs4[11]
		self.reserved0 = fs4[12]
		self.reserved1 = fs4[13]
		self.reserved2 = fs4[14]
		self.reserved3 = fs4[15]
		self.v_header = FieldSpec4VnirHeader(fs4[16])
		self.s1_header = FieldSpec4SwirHeader(fs4[17])
		self.s2_header = FieldSpec4SwirHeader(fs4[18])

class FieldSpec4Acquire:
	def __init__(self, response):
		format = "!256s"
		for i in range(1,2152):
			format += "f"
		fs4 = struct.unpack(format, response)
		self.spectrum_header = FieldSpec4SpectrumHeader(fs4[0])
		floats = []
		for i in range(1,2152):
			floats.append(fs4[i])
		self.spectrum_buffer = floats
	
	def to_tsv(self):
		delimiter = "\t"
		result = ""
		result += str(self.spectrum_header.header) + delimiter 
		result += str(self.spectrum_header.errbyte) + delimiter
		result += str(self.spectrum_header.sample_count) + delimiter
		result += str(self.spectrum_header.trigger) + delimiter
		result += str(self.spectrum_header.voltage) + delimiter
		result += str(self.spectrum_header.current) + delimiter
		result += str(self.spectrum_header.temperature) + delimiter
		result += str(self.spectrum_header.motor_current) + delimiter
		result += str(self.spectrum_header.instrument_hours) + delimiter
		result += str(self.spectrum_header.instrument_minutes) + delimiter
		result += str(self.spectrum_header.instrument_type) + delimiter
		result += str(self.spectrum_header.ab) + delimiter
		result += str(self.spectrum_header.reserved0) + delimiter
		result += str(self.spectrum_header.reserved1) + delimiter
		result += str(self.spectrum_header.reserved2) + delimiter
		result += str(self.spectrum_header.reserved3) + delimiter
		#result += str(self.spectrum_header.v_header = FieldSpec4VnirHeader(fs4[16])
		result += str(self.spectrum_header.v_header.it) + delimiter
		result += str(self.spectrum_header.v_header.scans) + delimiter
		result += str(self.spectrum_header.v_header.max_channel) + delimiter
		result += str(self.spectrum_header.v_header.min_channel) + delimiter
		result += str(self.spectrum_header.v_header.saturation) + delimiter
		result += str(self.spectrum_header.v_header.shutter) + delimiter
		result += str(self.spectrum_header.v_header.reserved0) + delimiter
		result += str(self.spectrum_header.v_header.reserved1) + delimiter
		result += str(self.spectrum_header.v_header.reserved2) + delimiter
		result += str(self.spectrum_header.v_header.reserved3) + delimiter
		result += str(self.spectrum_header.v_header.reserved4) + delimiter
		result += str(self.spectrum_header.v_header.reserved5) + delimiter
		result += str(self.spectrum_header.v_header.reserved6) + delimiter
		result += str(self.spectrum_header.v_header.reserved7) + delimiter
		result += str(self.spectrum_header.v_header.reserved8) + delimiter
		result += str(self.spectrum_header.v_header.reserved9) + delimiter
		#result += str(self.spectrum_header.s1_header = FieldSpec4SwirHeader(fs4[17])
		result += str(self.spectrum_header.s1_header.tec_status) + delimiter
		result += str(self.spectrum_header.s1_header.tec_current) + delimiter
		result += str(self.spectrum_header.s1_header.max_channel) + delimiter
		result += str(self.spectrum_header.s1_header.min_channel) + delimiter
		result += str(self.spectrum_header.s1_header.saturation) + delimiter
		result += str(self.spectrum_header.s1_header.a_scans) + delimiter
		result += str(self.spectrum_header.s1_header.b_scans) + delimiter
		result += str(self.spectrum_header.s1_header.dark_current) + delimiter
		result += str(self.spectrum_header.s1_header.gain) + delimiter
		result += str(self.spectrum_header.s1_header.offset) + delimiter
		result += str(self.spectrum_header.s1_header.scansize1) + delimiter
		result += str(self.spectrum_header.s1_header.scansize2) + delimiter
		result += str(self.spectrum_header.s1_header.reserved0) + delimiter
		result += str(self.spectrum_header.s1_header.reserved1) + delimiter
		result += str(self.spectrum_header.s1_header.reserved2) + delimiter
		result += str(self.spectrum_header.s1_header.reserved3) + delimiter
		#result += str(self.spectrum_header.s2_header = FieldSpec4VnirHeader(fs4[18])
		result += str(self.spectrum_header.s2_header.tec_status) + delimiter
		result += str(self.spectrum_header.s2_header.tec_current) + delimiter
		result += str(self.spectrum_header.s2_header.max_channel) + delimiter
		result += str(self.spectrum_header.s2_header.min_channel) + delimiter
		result += str(self.spectrum_header.s2_header.saturation) + delimiter
		result += str(self.spectrum_header.s2_header.a_scans) + delimiter
		result += str(self.spectrum_header.s2_header.b_scans) + delimiter
		result += str(self.spectrum_header.s2_header.dark_current) + delimiter
		result += str(self.spectrum_header.s2_header.gain) + delimiter
		result += str(self.spectrum_header.s2_header.offset) + delimiter
		result += str(self.spectrum_header.s2_header.scansize1) + delimiter
		result += str(self.spectrum_header.s2_header.scansize2) + delimiter
		result += str(self.spectrum_header.s2_header.reserved0) + delimiter
		result += str(self.spectrum_header.s2_header.reserved1) + delimiter
		result += str(self.spectrum_header.s2_header.reserved2) + delimiter
		result += str(self.spectrum_header.s2_header.reserved3) + delimiter
		for i in range(0, len(self.spectrum_buffer)):
			result += str(self.spectrum_buffer[i]) + delimiter
		return result


#	CONTROL RETURN VALUES
class FieldSpec4Control:
	def __init__(self, response):
		fs4 = struct.unpack("!iiiii", response)
		self.header = fs4[0]   # header type used in TCP transfer
		self.errbyte = fs4[1]  # error code
		self.detector = fs4[2] # Detector number – 0 swir1, 1 swir2, 2 vnir
		self.cmd_type = fs4[3] # Command Type 0 IT, 1 Gain, 2 Offset, 3 Shutter, 4 Trigger
		self.value = fs4[4]    # Value issues 0 - 4096


#	INIT RETURN VALUES
class FieldSpec4Init:
	def __init__(self, response):
		fs4 = struct.unpack("!ii30sdi", response)
		self.header = fs4[0]   # header type used in TCP transfer.
		self.errbyte = fs4[1]  # error code
		self.name = fs4[2]     # 30 character name
		self.value = fs4[3]    # value
		self.count = fs4[4]    # number of entries used

#	OPTIMIZE RETURN VALUES
class FieldSpec4Optimize:
	def __init__(self, response):
		fs4 = struct.unpack("!iiiiiii", response)
		self.header = fs4[0]   # header type used in TCP transfer.
		self.errbyte = fs4[1]  # error code
		self.itime = fs4[2]    # optimized integration time
		self.gain1 = fs4[3]    # optimized gain for 2 SWIRs
		self.gain2 = fs4[4]    
		self.offset1 = fs4[5]  # optimized offset for 2 SWIRs
		self.offset2 = fs4[6]  

#	RESTORE RETURN VALUES
class FieldSpec4Restore:
	def __init__(self, response):
		fs4 = struct.unpack("!ii", response[0:8])
		self.header = fs4[0]   # header type used in TCP transfer.
		self.errbyte = fs4[1]  # error code
		if str(self.header) == "100":
			start = (len(response) - 1) - 8
			end = start + 8
			fs4 = struct.unpack("!ii", response[start:end])
			self.count = fs4[0]    # The number of used entries
			self.verify = fs4[1]   # the checksum
			name_value_pairs = response[8:start + 1]
			name_value_pairs_length = len(name_value_pairs)
			print "name_value_pairs_length: " + str(name_value_pairs_length)
			pairs = name_value_pairs_length / 38
			print "pairs: " + str(pairs) 
			format = "!"
			for i in range(0,200):
				format += "30s"
			print "length of names buffer: " + str(len(name_value_pairs[0:(30 * 200)]))
			fs4 = struct.unpack(format, name_value_pairs[0:(30 * 200)])
			names = []
			for i in range(0,200):
				names.append(fs4[i].rstrip("\x00"))
			self.names = names
			format = "!"
			for i in range(0,200):
				format += "d"
			print "length of values buffer: " + str(len(name_value_pairs[(30 * 200):((30 * 200) + (8 * 200))]))
			fs4 = struct.unpack(format, name_value_pairs[(30 * 200):((30 * 200) + (8 * 200))])
			values = []
			for i in range(0,200):
				values.append(fs4[i])
			self.values = values
		else:
			self.count = None    # The number of used entries
			self.verify = None   # the checksum
			names = []
			for i in range(0,199):
				names.append(None)
			self.names = names
			values = []
			for i in range(0,199):
				values.append(None)
			self.values = values


#	VERSION RETURN VALUES
class FieldSpec4Version:
	def __init__(self, response):
		fs4 = struct.unpack("!ii30sdi", response)
		self.header = fs4[0]   # header type used in TCP transfer.
		self.errbyte = fs4[1]  # error code
		self.name = fs4[2]     # 30 character Version and build
		self.value = fs4[3]    # Version number
		self.type = fs4[4]     # Type of instrument 1-Vnir, 4-Swir1, 5-Vnir/Swir1, 8-Siwr2, 9-Vnir/Swir2, 12-Swir1/Swir2, 13-Vnir/Swir1/Swir2


class FieldSpec4:
	# Collect interpolated data.
	COMMAND_ACQUIRE = "A"       
	# Aborts “C”, “A” and “OPT” commands
	COMMAND_ABORT   = "ABORT"   
	# Clears the contents of the flash.
	COMMAND_ERASE   = "ERASE"   
	# Instrument control command
	COMMAND_CONTROL = "IC"      
	# Get, add or change ini file settings in the flash.
	COMMAND_INIT    = "INIT"    
	# Optimize the instrument
	COMMAND_OPTIMIZE = "OPT"     
	# Get and return the contents of the flash.
	COMMAND_RESTORE = "RESTORE" 
	# Save ini file settings to the flash.
	COMMAND_SAVE    = "SAVE"    
	# Version of firmware
	COMMAND_VERSION = "V"       

	ACQUIRE_SET_SAMPLE_COUNT          = "1"
	ACQUIRE_SET_INTEGRATION_TIME      = "2"
	ACQUIRE_SET_GAIN_AND_OFFSET_SWIR1 = "3"
	ACQUIRE_SET_GAIN_AND_OFFSET_SWIR1 = "4"
	ACQUIRE_TOGGLE_THE_SHUTTER        = "5"
		
	CONTROL_SWIR1             = "0"
	CONTROL_SWIR2             = "1"
	CONTROL_VNIR              = "2"
	
	# Valid Values
	# 0 - 14
	CONTROL_INTEGRATION_TIME  = "0" 
	# 0 - 4096
	CONTROL_GAIN              = "1" 
	# 0 - 4096    
	CONTROL_OFFSET            = "2" 
	# 0 - 1
	CONTROL_SHUTTER           = "3" 
	CLOSE_SHUTTER             = "1"
	OPEN_SHUTTER              = "0"
	# 0
	CONTROL_TRIGGER           = "4" 

	INIT_GET_VALUE_FROM_FLASH = "0"	
	INIT_ADD_VALUE_TO_FLASH   = "1"
	INIT_SET_VALUE_IN_FLASH   = "2"

	OPT_VNIR                  = "1"
	OPT_SWIR1                 = "2"
	OPT_VNIR_AND_SWIR         = "3"
	OPT_SWIR2                 = "4"
	OPT_VNIR_AND_SWIR2        = "5"
	OPT_SWIR1_AND_SWIR2       = "6"
	OPT_VNIR_SWIR1_SWIR2      = "7"

	RESTORE_LOAD_ONLY                         = "0"
	RESTORE_LOAD_AND_BUILD_CALIBRATION_ARRAY  = "1"

	"""
	    Use struct to convert binary values to python values
	    https://docs.python.org/2/library/struct.html#format-characters
	    Example: struct.unpack("<L", "y\xcc\xa6\xbb")[0]

	    ERASE RETURN VAALUES

	    struct InitStruct
		{
		int Header; //header type used in TCP transfer.
		int errbyte; //error code
		char name [MAX_PARAMETERS][30]; //space for 200 entries with 30 character names
		double value [MAX_PARAMETERS]; //corresponding data values for the 200 entries
		int count; //The number of used entries
		int verify; //the checksum
		};

		
		SAVE RETURN VALUES

		struct InitStruct
		{
		int Header; //header type used in TCP transfer.
		int errbyte; //error code
		char name [MAX_PARAMETERS][30]; //space for 200 entries with 30 character names
		double value [MAX_PARAMETERS]; //corresponding data values for the 200 entries
		int count; //The number of used entries
		int verify; //the checksum
		};
		
	"""
	
	
	def __init__(self):
		print ("FieldSpec4.__init__()...")
		self.connection = None
		self.host = "146.137.13.117"
		self.port = 8080
	

	def abort(self):
		start_time = time.time()
		print ("FieldSpec4.abort()...")
		MESSAGE_LENGTH = 50
		self.connection.send(FieldSpec4.COMMAND_ABORT)
		chunks = []
		recvd = 0
		while recvd < MESSAGE_LENGTH:
			chunk = self.connection.recv(min(MESSAGE_LENGTH - recvd, 1024))
			if chunk == "":
				raise RuntimeError("socket connection broken")
			chunks.append(chunk)
			recvd = recvd + len(chunk)
			print "chunks: " + str(len(chunks))
		response = "".join(chunks)
		print ("FieldSpec4.reponse length: " + str(len(response)))
		result = FieldSpec4Abort(response)
		print result
		stop_time = time.time()
		print "abort(): " + str(stop_time - start_time) + " seconds."
		return result
	

	def acquire(self, param2, param3, param4=None):
		start_time = time.time()
		print ("FieldSpec4.acquire()...")
		# 256 bytes + (4 bytes * 2151) = 8860
		MESSAGE_LENGTH = 8860
		if param4:
			self.connection.send(FieldSpec4.COMMAND_ACQUIRE + "," + param2 + "," + param3 + "," + param4)
		elif param3:
			self.connection.send(FieldSpec4.COMMAND_ACQUIRE + "," + param2 + "," + param3)
		elif param2:
			self.connection.send(FieldSpec4.COMMAND_ACQUIRE + "," + param2)
		else:
			self.connection.send(FieldSpec4.COMMAND_ACQUIRE)
		chunks = []
		recvd = 0
		while recvd < MESSAGE_LENGTH:
			chunk = self.connection.recv(min(MESSAGE_LENGTH - recvd, 1024))
			if chunk == "":
				raise RuntimeError("socket connection broken")
			chunks.append(chunk)
			recvd = recvd + len(chunk)
			print "chunks: " + str(len(chunks))
		response = "".join(chunks)
		print ("FieldSpec4.reponse length: " + str(len(response)))
		result = FieldSpec4Acquire(response)
		print result
		stop_time = time.time()
		print "acquire(): " + str(stop_time - start_time) + " seconds."
		return result


	def close(self):
		print ("FieldSpec4.close()...")
		self.connection.close()
		return True


	def control(self, param2, param3, param4):
		start_time = time.time()
		print ("FieldSpec4.control()...")
		MESSAGE_LENGTH = 20
		self.connection.send(FieldSpec4.COMMAND_CONTROL + "," + param2 + "," + param3 + "," + param4)
		chunks = []
		recvd = 0
		while recvd < MESSAGE_LENGTH:
			chunk = self.connection.recv(min(MESSAGE_LENGTH - recvd, 1024))
			if chunk == "":
				raise RuntimeError("socket connection broken")
			chunks.append(chunk)
			recvd = recvd + len(chunk)
			print "chunks: " + str(len(chunks))
		response = "".join(chunks)
		print ("FieldSpec4.reponse length: " + str(len(response)))
		result = FieldSpec4Control(response)
		print result
		stop_time = time.time()
		print "control(): " + str(stop_time - start_time) + " seconds."
		return result


	def erase(self):
		start_time = time.time()
		print ("FieldSpec4.erase(): TODO")
		MESSAGE_LENGTH = 7616		
		stop_time = time.time()
		print "erase(): " + str(stop_time - start_time) + " seconds."
		

	def init(self, param2, param3, param4=None):
		start_time = time.time()
		print ("FieldSpec4.init()...")
		MESSAGE_LENGTH = 50
		if param4:
			self.connection.send(FieldSpec4.COMMAND_INIT + "," + str(param2) + "," + str(param3) + "," + str(param4))
		else:
			self.connection.send(FieldSpec4.COMMAND_INIT + "," + str(param2) + "," + str(param3))
		chunks = []
		recvd = 0
		while recvd < MESSAGE_LENGTH:
			chunk = self.connection.recv(min(MESSAGE_LENGTH - recvd, 1024))
			if chunk == "":
				raise RuntimeError("socket connection broken")
			chunks.append(chunk)
			recvd = recvd + len(chunk)
			print "chunks: " + str(len(chunks))
		response = "".join(chunks)
		print ("FieldSpec4.reponse length: " + str(len(response)))
		#print response
		result = FieldSpec4Init(response)
		print result
		stop_time = time.time()
		print "init(): " + str(stop_time - start_time) + " seconds."
		return result

		
	def more_to_read(self, connection):
		start_time = time.time()
		potential_readers = [connection]
		potential_writers = [connection]
		potential_errors  = [connection]
		ready_to_read, ready_to_write, in_error = select.select(potential_readers, potential_writers, potential_errors, 300)
		stop_time = time.time()
		print "more_to_read(): " + str(stop_time - start_time) + " seconds."
		if ready_to_read:
			return True
		else:
			return False


	def open(self, host_address=None):
		start_time = time.time()
		print ("FieldSpec4.open()...")
		if host_address:
			self.host = host_address
		self.connection = socket.socket()
		self.connection.settimeout(60)
		self.connection.connect((self.host, self.port))
		response = self.connection.recv(1024)
		print "response length: " + str(len(response))
		print response
		stop_time = time.time()
		print "open(): " + str(stop_time - start_time) + " seconds."
		return True


	def optimize(self, param2):
		start_time = time.time()
		print ("FieldSpec4.optimize()...")
		MESSAGE_LENGTH = 28
		self.connection.send(FieldSpec4.COMMAND_OPTIMIZE + "," + param2)
		chunks = []
		recvd = 0
		while recvd < MESSAGE_LENGTH:
			chunk = self.connection.recv(min(MESSAGE_LENGTH - recvd, 1024))
			if chunk == "":
				raise RuntimeError("socket connection broken")
			chunks.append(chunk)
			recvd = recvd + len(chunk)
			print "chunks: " + str(len(chunks))
		response = "".join(chunks)
		print ("FieldSpec4.reponse length: " + str(len(response)))
		result = FieldSpec4Optimize(response)
		print result
		stop_time = time.time()
		print "optimize(): " + str(stop_time - start_time) + " seconds."
		return result


	def restore(self, param2):
		start_time = time.time()
		print ("FieldSpec4.restore()...")		
		MESSAGE_LENGTH = 7616
		self.connection.send(FieldSpec4.COMMAND_RESTORE + "," + str(param2))
		chunks = []
		recvd = 0
		while recvd < MESSAGE_LENGTH:
			chunk = self.connection.recv(min(MESSAGE_LENGTH - recvd, 1024))
			if chunk == "":
				raise RuntimeError("socket connection broken")
			chunks.append(chunk)
			recvd = recvd + len(chunk)
			print "chunks: " + str(len(chunks))
		response = "".join(chunks)
		print ("FieldSpec4.response length: " + str(len(response)))
		#print response
		result = FieldSpec4Restore(response)
		print result
		stop_time = time.time()
		print "restore(): " + str(stop_time - start_time) + " seconds."
		return result


	def save(self):
		start_time = time.time()
		print ("FieldSpec4.save() TODO")
		MESSAGE_LENGTH = 7616		
		stop_time = time.time()
		print "save(): " + str(stop_time - start_time) + " seconds."
		

	def version(self):
		start_time = time.time()
		print ("FieldSpec4.version()...")
		MESSAGE_LENGTH = 50
		self.connection.send(FieldSpec4.COMMAND_VERSION)
		chunks = []
		recvd = 0
		while recvd < MESSAGE_LENGTH:
			chunk = self.connection.recv(min(MESSAGE_LENGTH - recvd, 1024))
			if chunk == "":
				raise RuntimeError("socket connection broken")
			chunks.append(chunk)
			recvd = recvd + len(chunk)
			print "chunks: " + str(len(chunks))

		response = "".join(chunks)
		#response = self.connection.recv(50)
		print ("FieldSpec4.reponse length: " + str(len(response)))
		result = FieldSpec4Version(response)
		print result
		stop_time = time.time()
		print "version(): " + str(stop_time - start_time) + " seconds."
		return result


