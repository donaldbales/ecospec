#!/usr/bin/python
# checker
# Make sure the critical EcoSpec components keep running
import datetime
import ecospec
import pifacedigitalio
import piface
import subprocess
import sys
import time

actuator_under_control = False

pifacedigitalio.init()

time.sleep(10)

while True:
  logfile = open('/var/log/checker.log' ,'a', 0)

  logfile.write("Checking if ecospec.py is running at " + str(datetime.datetime.today()) + "...\n")
  try:
    ecospec = subprocess.check_output("ps -A | grep ecospec", shell=True)
  except subprocess.CalledProcessError:
    ecospec = ""
  if not actuator_under_control:
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
  for i in range(1, 120):
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
      logfile.write("PiFace pushbutton 3 pressed.  Extending actuator.\n")
      actuator = ""

      try:
        actuator = subprocess.check_output("service ecospec stop", shell=True)
        actuator_under_control = True
      except subprocess.CalledProcessError as error:
        logfile.write("CalledProcessError({0}): {1}\n".format(error.errno, error.strerror))
        actuator = ""

      try:
        x = piface.PiFace()        
        x.extend_white_reference_arm(ecospec.EcoSpec.ACTUATOR_RELAY)
      except:
        logfile.write("sys.exc_type: {0}\n".format(str(sys.exc_type)))
        logfile.write("sys.exc_value: {0}\n".format(str(sys.exc_value)))
        logfile.write("sys.exc_traceback: {0}\n".format(str(sys.exc_traceback)))
        logfile.write("sys.exc_info(): {0}\n".format(str(sys.exc_info())))

      logfile.write("{0}\n".format(str(actuator)))
    elif pifacedigitalio.digital_read(3):
      logfile.write("PiFace pushbutton 4 pressed.  Retracting actuator.\n")
      actuator = ""

      try:
        x = piface.PiFace()        
        x.retract_white_reference_arm(ecospec.EcoSpec.ACTUATOR_RELAY)
      except:
        logfile.write("sys.exc_type: {0}\n".format(str(sys.exc_type)))
        logfile.write("sys.exc_value: {0}\n".format(str(sys.exc_value)))
        logfile.write("sys.exc_traceback: {0}\n".format(str(sys.exc_traceback)))
        logfile.write("sys.exc_info(): {0}\n".format(str(sys.exc_info())))

      try:
        actuator = subprocess.check_output("service ecospec start", shell=True)
        actuator_under_control = False
      except subprocess.CalledProcessError as error:
        logfile.write("CalledProcessError({0}): {1}\n".format(error.errno, error.strerror))
        actuator = ""

      logfile.write("{0}\n".format(str(actuator)))
    else:
      pass
    time.sleep(5)

  logfile.close()
    
