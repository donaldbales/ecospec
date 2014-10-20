#!/usr/bin/python
# checker
# Make sure the critical EcoSpec components keep running
import datetime
import pifacedigitalio
import subprocess
import time

pifacedigitalio.init()

time.sleep(10)

while True:
  logfile = open('/var/log/checker.log' ,'a', 0)

  logfile.write("Checking if ecospec.py is running at " + str(datetime.datetime.today()) + "...\n")
  try:
    ecospec = subprocess.check_output("ps -A | grep ecospec", shell=True)
  except subprocess.CalledProcessError:
    ecospec = ""
  if (ecospec + ' ') == ' ':
    logfile.write("No it's not, so let's start it!\n")
    try:
      ecospec = subprocess.check_output("service ecospec start", shell=True)
    except subprocess.CalledProcessError as error:
      logfile.write("CalledProcessError({0}): {1}\n".format(error.errno, error.strerror))
      ecospec = ""
    logfile.write(ecospec + "\n")
  else:
    logfile.write("Yes it is.\n")
  logfile.write('Checking if wvdial is running at ' + str(datetime.datetime.today()) + "...\n")
  try:
    wvdial = subprocess.check_output("ps -A | grep wvdial", shell=True)
  except subprocess.CalledProcessError:
    wvdial = ""
  if (wvdial + ' ') == ' ':
    logfile.write("No it's not, so let's start it!\n")
    try:
      wvdial = subprocess.check_output("service wvdial start", shell=True)
    except subprocess.CalledProcessError as error:
      logfile.write("CalledProcessError({0}): {1}\n".format(error.errno, error.strerror))
      wvdial = ""
    logfile.write(wvdial + "\n")
  else:
    logfile.write("Yes it is.\n")

  logfile.close()
  logfile = open('/var/log/checker.log' ,'a', 0)

  # Check the PiFace buttons for the next ten minutes
  logfile.write('Checking if a pushbutton is being pressed at ' + str(datetime.datetime.today()) + "...\n")
  for i in range(1, (6 * 10)):
    if   pifacedigitalio.digital_read(0):
      logfile.write("PiFace pushbutton 1 pressed.  Shutting down.\n")
      try:
        shutdown = subprocess.check_output("shutdown -h now", shell=True)
      except subprocess.CalledProcessError as error:
        logfile.write("CalledProcessError({0}): {1}\n".format(error.errno, error.strerror))
        shutdown = ""
      logfile.write(shutdown + "\n")
    elif pifacedigitalio.digital_read(1):	
      logfile.write("PiFace pushbutton 2 pressed.  Rebooting.\n")
      try:
        reboot = subprocess.check_output("reboot", shell=True)
      except subprocess.CalledProcessError as error:
        logfile.write("CalledProcessError({0}): {1}\n".format(error.errno, error.strerror))
        reboot = ""
      logfile.write(reboot + "\n")
    elif pifacedigitalio.digital_read(2):
      pass
    elif pifacedigitalio.digital_read(3):
      pass
    else:
      pass
    time.sleep(10)	

  logfile.close()
    
