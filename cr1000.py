# -*- coding: utf-8 -*-
#
# cr1000.py - Ecospec CR1000 Program
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

import ecospec
import subprocess

class CR1000:
	def __init__(self, data_set_id, current_pantilt_position_string, data_path, log_path, since_time, host="146.137.13.118", port="80"):
		print ("CR1000.__init__()...")
		self.data_set_id = data_set_id
		self.host        = host
		self.port        = port
#    self.tables      = ("_9_Sec", "_01_Min", "_30_Min", "_01_Day", "Status")
    self.tables      = ("_10_Sec", "_01_Min", "_30_Min", "_01_Day", "Status")
		for table in self.tables:
			time_string  = "cr1000" #time.strftime("%Y%m%d%H%M%S")
			data_file_path   = ecospec.EcoSpec.DATA_PATH + self.data_set_id + "-" + current_pantilt_position_string + "-" + time_string + "-" + table + ".csv"
			print("data_file_path: " + data_file_path)
			log_file_path    = ecospec.EcoSpec.LOG_PATH  + self.data_set_id + "-" + current_pantilt_position_string + "-" + time_string + "-" + table + ".log"
			print("log_file_path: " + log_file_path)
			wget_command     = "umask 000 && wget -b -d -nc -o " + log_file_path + " -O " + data_file_path + " -v 'http://" + self.host + ":" + self.port + "/?command=dataquery" + "&uri=" + table + "&format=toa5" + "&mode=since-time" + "&p1=" + since_time + "' && exit $?\n"
			print("wget_command: " + wget_command)
			subprocess.call(wget_command, shell=True)
			

