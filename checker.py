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
import traceback

actuator_under_control = False

pifacedigitalio.init()

time.sleep(10)

piface_instance = piface.PiFace()

while True:
  logfile = open('/var/log/checker/checker.log' ,'a', 0)

  logfile.write("Checking if ecospec.py is running at " + str(datetime.datetime.today()) + "...\n")
  try:
    result = subprocess.check_output("ps -A | grep ecospec", shell=True)
  except subprocess.CalledProcessError:
    result = ""
  if not actuator_under_control:
    if (result + ' ') == ' ':
      logfile.write("No it's not, so let's start it!\n")
      try:
        result = subprocess.check_output("service ecospec start", shell=True)
      except subprocess.CalledProcessError as error:
        logfile.write("CalledProcessError({0}): {1}\n".format(error.errno, error.strerror))
        result = ""
      logfile.write(result + "\n")
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

  logfile.write("Checking if mover.py is running at " + str(datetime.datetime.today()) + "...\n")
  try:
    result = subprocess.check_output("ps -A | grep mover", shell=True)
  except subprocess.CalledProcessError:
    result = ""
  if not actuator_under_control:
    if (result + ' ') == ' ':
      logfile.write("No it's not, so let's start it!\n")
      try:
        result = subprocess.check_output("service mover start", shell=True)
      except subprocess.CalledProcessError as error:
        logfile.write("CalledProcessError({0}): {1}\n".format(error.errno, error.strerror))
        result = ""
      logfile.write(result + "\n")
    else:
      logfile.write("Yes it is.\n")
   
  logfile.close()
  logfile = open('/var/log/checker/checker.log' ,'a', 0)

  # Check the PiFace buttons for the next ten minutes
  logfile.write('Checking if a pushbutton is being pressed at ' + str(datetime.datetime.today()) + "...\n")
  for i in range(1, 120):
    if   pifacedigitalio.digital_read(0):
      logfile.write("PiFace pushbutton 1 pressed.  Shutting down.\n")
      result = ""
      try:
        shutdown = subprocess.check_output("shutdown -h now", shell=True)
      except subprocess.CalledProcessError as error:
        logfile.write("CalledProcessError({0}): {1}\n".format(error.errno, error.strerror))
        shutdown = ""
      logfile.write(shutdown + "\n")
    elif pifacedigitalio.digital_read(1):   
      logfile.write("PiFace pushbutton 2 pressed.  Rebooting.\n")
      result = ""
      try:
        result = subprocess.check_output("reboot", shell=True)
      except subprocess.CalledProcessError as error:
        logfile.write("CalledProcessError({0}): {1}\n".format(error.errno, error.strerror))
        result = ""
      logfile.write(result + "\n")
    elif pifacedigitalio.digital_read(2):
      logfile.write("PiFace pushbutton 3 pressed.  Extending actuator.\n")
      result = ""

      try:
        logfile.write("stopping service ecospec\n")
        result = subprocess.check_output("service ecospec stop", shell=True)
        actuator_under_control = True
      except subprocess.CalledProcessError as error:
        logfile.write("CalledProcessError({0}): {1}\n".format(error.errno, error.strerror))
        result = ""

      try:
        logfile.write("extending white reference arm\n")
        piface_instance.extend_white_reference_arm(ecospec.EcoSpec.ACTUATOR_RELAY)
      except:
        xtype, xvalue, xtb = sys.exc_info()
        logfile.write("{0}\n".format(xtype))
        logfile.write("{0}\n".format(xvalue))
        traceback.print_tb(xtb, None, logfile)

      logfile.write("{0}\n".format(str(result)))
    elif pifacedigitalio.digital_read(3):
      logfile.write("PiFace pushbutton 4 pressed.  Retracting actuator.\n")
      result = ""

      try:
        logfile.write("retracting white reference arm\n")
        piface_instance.retract_white_reference_arm(ecospec.EcoSpec.ACTUATOR_RELAY)
      except:
        xtype, xvalue, xtb = sys.exc_info()
        logfile.write("{0}\n".format(xtype))
        logfile.write("{0}\n".format(xvalue))
        traceback.print_tb(xtb, None, logfile)

      try:
        logfile.write("starting service ecospec\n")
        result = subprocess.check_output("service ecospec start", shell=True)
        actuator_under_control = False
      except subprocess.CalledProcessError as error:
        logfile.write("CalledProcessError({0}): {1}\n".format(error.errno, error.strerror))
        result = ""

      logfile.write("{0}\n".format(str(result)))
    else:
      pass
    time.sleep(5)

  logfile.close()
    
