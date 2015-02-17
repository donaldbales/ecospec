
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
import urllib2

import os
import time
import uuid

def get_guid():
  ten = "1_>C/_9j`'"
  six = time.strftime("%Y %y %m %d %H %M").split()
  six[0] = six[0][0:2]
  sixteen = [ten[0:2]]
  for i in range(0, 6):
    #print x[i + 1:i + 2]
    sixteen.append(chr(int(six[i]) + 32))
    sixteen.append(ten[i + 2:i + 3])
  sixteen.append(ten[9:10])
  print "type(sixteen)=" + str(type(sixteen)) + ", ''.join(sixteen)=" + ''.join(sixteen)
  guid = uuid.uuid5(uuid.NAMESPACE_URL, ''.join(sixteen))
  print guid
  return guid

# Register the streaming http handlers with urllib2
register_openers()

#data_path = '/home/ecospec/data'
data_path = '.'
all_files = os.listdir(data_path)
all_files.sort
files = []
type(files)
for file in all_files:
  if file[-4:] == '.csv' or file[-4:] == '.jpg':
    files.append(file)

for file in files:
  print file + "\n"
  get_guid()
  # Start the multipart/form-data encoding of the file "DSC0001.jpg"
  # "image1" is the name of the parameter, which is normally set
  # via the "name" parameter of the HTML <input> tag.

  # headers contains the necessary Content-Type and Content-Length
  # datagen is a generator object that yields the encoded parameters
  filename = data_path + "/" + file
  print filename + "\n"
  datagen, headers = multipart_encode({"commit": "Upload", "guid": get_guid(), "content": open(filename, "rb")})
  # Create the Request object
  request = urllib2.Request("http://146.137.248.12/ecospec/uploads", datagen, headers)
  try:
    print urllib2.urlopen(request).read()
    # ADD MOVE HERE
    transferedname = filename + ".transfered_" + time.strftime("%Y%m%d%H%M")
    print "rename " + filename + " to " + transferedfile
    os.rename(filename, transferedname)
  except:
    print("Can't transfer the file.")
