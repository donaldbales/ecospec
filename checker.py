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

def log(message):
  logfile = open('/var/log/checker/checker.log' ,'a', 0)
  logfile.write(str(datetime.datetime.today()) + " checker: " + str(message) + "\n")
  logfile.close()

log("starting up")

actuator_under_control = False

pifacedigitalio.init()

time.sleep(10)

piface_instance = piface.PiFace()

while True:
  log("Checking if ecospec.py is running at " + str(datetime.datetime.today()))
  try:
    result = subprocess.check_output("ps -A | grep ecospec", shell=True)
  except subprocess.CalledProcessError:
    result = ""
  if not actuator_under_control:
    if (result + ' ') == ' ':
      log("No it's not, so let's start it!")
      try:
        result = subprocess.check_output("service ecospec start", shell=True)
      except subprocess.CalledProcessError as error:
        log("CalledProcessError({0}): {1}".format(error.errno, error.strerror))
        result = ""
      log(result + "")
    else:
      log("Yes it is.")
   
  log('Checking if wvdial is running at ' + str(datetime.datetime.today()))
  try:
    wvdial = subprocess.check_output("ps -A | grep wvdial", shell=True)
  except subprocess.CalledProcessError:
    wvdial = ""
  if (wvdial + ' ') == ' ':
    log("No it's not, so let's start it!")
    try:
      wvdial = subprocess.check_output("service wvdial start", shell=True)
    except subprocess.CalledProcessError as error:
      log("CalledProcessError({0}): {1}".format(error.errno, error.strerror))
      wvdial = ""
    log(wvdial + "")
  else:
    log("Yes it is.")

  log("Checking if mover.py is running at " + str(datetime.datetime.today()))
  try:
    result = subprocess.check_output("ps -A | grep mover", shell=True)
  except subprocess.CalledProcessError:
    result = ""
  if not actuator_under_control:
    if (result + ' ') == ' ':
      log("No it's not, so let's start it!")
      try:
        result = subprocess.check_output("service mover start", shell=True)
      except subprocess.CalledProcessError as error:
        log("CalledProcessError({0}): {1}".format(error.errno, error.strerror))
        result = ""
      log(result + "")
    else:
      log("Yes it is.")
   
  # Check the PiFace buttons for the next ten minutes
  log('Checking if a pushbutton is being pressed at ' + str(datetime.datetime.today()))
  for i in range(1, 60):
    if   pifacedigitalio.digital_read(0):
      log("PiFace pushbutton 1 pressed.  Shutting down.")
      result = ""
      try:
        shutdown = subprocess.check_output("shutdown -h now", shell=True)
      except subprocess.CalledProcessError as error:
        log("CalledProcessError({0}): {1}".format(error.errno, error.strerror))
        shutdown = ""
      log(shutdown + "")
    elif pifacedigitalio.digital_read(1):   
      log("PiFace pushbutton 2 pressed.  Rebooting.")
      result = ""
      try:
        result = subprocess.check_output("reboot", shell=True)
      except subprocess.CalledProcessError as error:
        log("CalledProcessError({0}): {1}".format(error.errno, error.strerror))
        result = ""
      log(result + "")
    elif pifacedigitalio.digital_read(2):
      log("PiFace pushbutton 3 pressed.  Extending actuator.")
      result = ""

      try:
        log("stopping service ecospec")
        result = subprocess.check_output("service ecospec stop", shell=True)
        actuator_under_control = True
      except subprocess.CalledProcessError as error:
        log("CalledProcessError({0}): {1}".format(error.errno, error.strerror))
        result = ""

      try:
        log("extending white reference arm")
        piface_instance.extend_white_reference_arm(ecospec.EcoSpec.ACTUATOR_RELAY)
      except:
        xtype, xvalue, xtb = sys.exc_info()
        log("{0}".format(xtype))
        log("{0}".format(xvalue))
        traceback.print_tb(xtb, None, logfile)

      log("{0}".format(str(result)))
    elif pifacedigitalio.digital_read(3):
      log("PiFace pushbutton 4 pressed.  Retracting actuator.")
      result = ""

      try:
        log("retracting white reference arm")
        piface_instance.retract_white_reference_arm(ecospec.EcoSpec.ACTUATOR_RELAY)
      except:
        xtype, xvalue, xtb = sys.exc_info()
        log("{0}".format(xtype))
        log("{0}".format(xvalue))
        traceback.print_tb(xtb, None, logfile)

      try:
        log("starting service ecospec")
        result = subprocess.check_output("service ecospec start", shell=True)
        actuator_under_control = False
      except subprocess.CalledProcessError as error:
        log("CalledProcessError({0}): {1}".format(error.errno, error.strerror))
        result = ""

      log("{0}".format(str(result)))
    else:
      pass
    time.sleep(5)

log("shuting down")
    
