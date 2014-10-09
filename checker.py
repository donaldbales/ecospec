#!/usr/bin/python
# checker
# Make sure the critical EcoSpec components keep running
import subprocess
import datetime

while True:
  logfile = open('/var/log/checker.log' ,'a', 0)
  
  logfile.write("Checking that ecospec.py is running at " + str(datetime.datetime.today()) + "...\n")
  try:
    ecospec = check_output("ps -A | grep ecospec", shell=True)
  except CalledProcessError:
    ecospec = ''
  if (ecospec + ' ') == ' ':
    logfile.write("No it's not, so let's start it!\n")
    try:
      ecospec = check_output("service ecospec start", shell=True)
    except CalledProcessError as error:
      logfile.write("CalledProcessError({0}): {1}".format(error.errno, error.strerror)  
      ecospec = ''
    logfile.write(ecospec + "\n")
  else
    logfile.write("Yes it is.")
  fi
  
  logfile.write('Checking that wvdial is running at ' + str(datetime.datetime.today()) + "...\n")
  try:
    wvdial = check_output("ps -A | grep wvdial", shell=True)
  except CalledProcessError:
    wvdial = ''
  if (wvdial + ' ') == ' ':
    logfile.write("No it's not, so let's start it!\n")
    try:
      wvdial = check_output("service wvdial start", shell=True)
    except CalledProcessError as error:
      logfile.write("CalledProcessError({0}): {1}".format(error.errno, error.strerror)  
      wvdial = ''    
    logfile.write(wvdial + "\n")
  else
    logfile.write("Yes it is.")
  fi
  logfile.close()
