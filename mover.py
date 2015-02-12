
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
import urllib2

import os
import time
import uuid

def get_guid():
  x = 'eeBoPu8h'
  six = time.strftime("%C %y %m %d %H %M").split()
  sixteen = [x[0:1]]
  for i in range(0, 6):
    #print x[i + 1:i + 2]
    sixteen.append(chr(int(six[i]) + 32))
    sixteen.append(x[i + 1:i + 2])
  sixteen.append(x[7:8])
  #print sixteen
  guid = uuid.uuid5(uuid.NAMESPACE_URL, str(sixteen))
  print guid
  return guid

# Register the streaming http handlers with urllib2
register_openers()


all_files = os.listdir('/home/ecospec/data')
all_files.sort
files = []
type(files)
for file in all_files:
  if file[-4:] == '.csv' or file[-4:] == '.jpg':
    files.append(file)

for file in files:
#  print file + "\n"
  # Start the multipart/form-data encoding of the file "DSC0001.jpg"
  # "image1" is the name of the parameter, which is normally set
  # via the "name" parameter of the HTML <input> tag.

  # headers contains the necessary Content-Type and Content-Length
  # datagen is a generator object that yields the encoded parameters
  filename = "/home/ecospec/data/" + file
  # ADD OTHER PARAMETERS LIKE GUID HERE
  datagen, headers = multipart_encode({"content": open(filename, "rb")})
  # Create the Request object
  request = urllib2.Request("http://146.137.248.12/ecospec/uploads", datagen, headers)
  print urllib2.urlopen(request).read()
  # ADD MOVE HERE








get_guid()
 
