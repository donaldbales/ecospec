#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# mover.py - Ecospec Pan-tilt Unit Program
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

from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
import urllib2

import os
import time
import uuid
import settings

def get_guid():
  ten = settings.TEN
  #ten = "1_>C/_9j`'"
  six = time.strftime("%Y %y %m %d %H %M").split()
  six[0] = six[0][0:2]
  sixteen = [ten[0:2]]
  for i in range(0, 6):
    #print x[i + 1:i + 2]
    sixteen.append(chr(int(six[i]) + 32))
    sixteen.append(ten[i + 2:i + 3])
  sixteen.append(ten[9:10])
  #print "type(sixteen)=" + str(type(sixteen)) + ", ''.join(sixteen)=" + ''.join(sixteen)
  guid = uuid.uuid5(uuid.NAMESPACE_URL, ''.join(sixteen))
  #print guid
  return guid

# wait for a network connection
time.sleep(60)

# Register the streaming http handlers with urllib2
register_openers()

data_path = '/home/ecospec/data'

while True:
  all_files = os.listdir(data_path)
  all_files.sort
  files = []
  type(files)
  for file in all_files:
    if file[-4:] == '.csv' or file[-4:] == '.jpg':
      files.append(file)
  
  for file in files:
    #print file + "\n"
    get_guid()
    # Start the multipart/form-data encoding of the file "DSC0001.jpg"
    # "image1" is the name of the parameter, which is normally set
    # via the "name" parameter of the HTML <input> tag.
  
    # headers contains the necessary Content-Type and Content-Length
    # datagen is a generator object that yields the encoded parameters
    filename = data_path + "/" + file
    print "\ntransferring " + filename + "..."
    datagen, headers = multipart_encode({"commit": "Upload", "guid": get_guid(), "content": open(filename, "rb")})
    # Create the Request object
    request = urllib2.Request("http://146.137.248.12/ecospec/uploads", datagen, headers)
    try:
      urllib2.urlopen(request).read()
      transferedname = filename + ".transfered_" + time.strftime("%Y%m%d%H%M")
      #print "renaming " + filename + " to " + transferedname
      os.rename(filename, transferedname)
    except Exception as error:
      print("Can't transfer the file.")
      print str(error)
  
  time.sleep(300)	
