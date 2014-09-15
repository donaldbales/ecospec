# -*- coding: utf-8 -*-
#
# axis_q1604.py - Ecospec Axis Q1604 Program
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

class AxisQ1604:
	def __init__(self, data_set_id, host="146.137.13.119", port="80"):
		print ("AxisQ1604.__init__()...")
		self.data_set_id = data_set_id
		self.host        = host
		self.port        = port
		time_string      = "axis_q1604" #time.strftime("%Y%m%d%H%M%S")
		data_path        = ecospec.EcoSpec.DATA_PATH + self.data_set_id + "_" + time_string + ".jpg"
		log_path         = ecospec.EcoSpec.LOG_PATH  + self.data_set_id + "_" + time_string + ".jpg.log"
		subprocess.check_call("wget -b -d -nc -o " + log_path + " -O " + data_path -v + " http://" + self.host + ":" + self.port + "/axis-cgi/jpg/image.cgi")
		
		
		