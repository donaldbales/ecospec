# -*- coding: utf-8 -*-
#
# ptu_d300.py - Ecospec Pan-tilt Unit Program
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

import serial
import sys 

class PtuD300:
    """
        Pan-tilt command conventions:
        * may be in lower or upper case
        * a delimiter can be a space character or a carriage return character
        * successful command execution returns an asterisk followed by a carriage return: "*\r"
        * a failed command execution returns an exclamation mark followed by an error message, ending with a carriage return: "! <error message>\r"
        * successful query execution returns an asterisk followed by the query result ending with a carriage return: "* <query result>\r"
        * a pan axis limit error return an exclamation mark followed by P, ending with a carriage return: "!P\n"
        * a tilt axis limit error return an exclamation mark followed by T, ending with a carriage return: "!T\n"
    """
    CONFIGURE_COMMUNICATIONS   = "@"
    CONTROL_MODE_INDEPENDENT   = "CI"
    CONTROL_MODE_PURE_VELOCITY = "CV"
    CONTROL_MODE_QUERY         = "C"

    DEFAULTS_FACTORY           = "DF"
    DEFAULTS_RESTORE           = "DR"
    DEFAULTS_SAVE              = "DS"
    DELIMITER                  = " "

    ECHO_DISABLE               = "ED"
    ECHO_ENABLE                = "EE"
    ECHO_QUERY                 = "E"
    ERROR                      = "!"

    FEEDBACK_QUERY             = "F"
    FEEDBACK_TERSE             = "FT"
    FEEDBACK_VERBOSE           = "FV"

    HALT                       = "H"

    MONITORING                 = "M"
    MONITORING_DISABLE         = "MD"
    MONITORING_ENABLE          = "ME"
    MONITORING_QUERY           = "MQ"

    PAN_ACCELERATION           = "PA"
    PAN_AFTER_COMPLETION       = "S"
    PAN_AWAIT_COMPLETION       = "A"
    PAN_HALT                   = "HP"
    PAN_IMMEDIATELY            = "I"
    PAN_POSITION_ABSOLUTE      = "PP"
    PAN_POSITION_LIMIT_DISABLE = "LD"
    PAN_POSITION_LIMIT_ENABLE  = "LE"
    PAN_POSITION_LIMIT_QUERY   = "L"
    PAN_POSITION_MAXIMUM       = "PX"
    PAN_POSITION_MINIMUM       = "PN"
    PAN_POSITION_RELATIVE      = "PO"
    PAN_POWER_MODE_HOLD_LOW    = "PHL"
    PAN_POWER_MODE_HOLD_OFF    = "PHO"
    PAN_POWER_MODE_HOLD_QUERY  = "PH"
    PAN_POWER_MODE_HOLD_REG    = "PHR"
    PAN_POWER_MODE_MOVE_LOW    = "PML"
    PAN_POWER_MODE_MOVE_OFF    = "PMO"
    PAN_POWER_MODE_MOVE_QUERY  = "PM"
    PAN_POWER_MODE_MOVE_REG    = "PMR"
    PAN_RESOLUTION             = "PR"
    PAN_SPEED_ABSOLUTE         = "PS"
    PAN_SPEED_BASE             = "PB"
    PAN_SPEED_MAXIMUM          = "PU"
    PAN_SPEED_MINIMUM          = "PL"
    PAN_SPEED_RELATIVE         = "PD"
    PAN_STEP_MODE              = "WP"

    RESET_DISABLED_ON_POWER_UP = "RD"              
    RESET_ENABLED_ON_POWER_UP  = "RT"
    RESET_IMMEDIATELY          = "R"
    RESET_PAN_ONLY_ON_POWER_UP = "RP"
    RESET_PAN_TILT_ON_POWER_UP = "RE"

    STATUS_QUERY               = "O"
    SUCCESSFUL                 ="*"

    TILT_ACCELERATION          = "TA"
    TILT_HALT                  = "HT"
    TILT_POSITION_ABSOLUTE     = "TP"
    TILT_POSITION_MAXIMUM      = "TX"
    TILT_POSITION_MINIMUM      = "TN"
    TILT_POSITION_RELATIVE     = "TO"
    TILT_POWER_MODE_HOLD_LOW   = "THL"
    TILT_POWER_MODE_HOLD_OFF   = "THO"
    TILT_POWER_MODE_HOLD_QUERY = "TH"
    TILT_POWER_MODE_HOLD_REG   = "THR"
    TILT_POWER_MODE_MOVE_LOW   = "TML"
    TILT_POWER_MODE_MOVE_OFF   = "TMO"
    TILT_POWER_MODE_MOVE_QUERY = "TM"
    TILT_POWER_MODE_MOVE_REG   = "TMR"
    TILT_RESOLUTION            = "TR"
    TILT_SPEED_ABSOLUTE        = "TS"
    TILT_SPEED_BASE            = "TB"
    TILT_SPEED_MAXIMUM         = "TU"
    TILT_SPEED_MINIMUM         = "TL"
    TILT_SPEED_RELATIVE        = "TD"
    TILT_STEP_MODE             = "WT"

    VERSION_QUERY              = "V"

    def __init__(self, port, baud_rate):
        try:
            self.connection = serial.Serial(port, baud_rate, timeout=60.5)    
        except Exception, e:
	    print e
            raise Exception("Unable to open Serial port")
            exit

        self.connection.flushInput()
        self.connection.flushOutput()
	self.send(PtuD300.FEEDBACK_VERBOSE)
        self.send(PtuD300.VERSION_QUERY)
        self.send(PtuD300.RESET_PAN_ONLY_ON_POWER_UP)
        self.send(PtuD300.DEFAULTS_SAVE)
        self.send(PtuD300.RESET_IMMEDIATELY)
	self.send(PtuD300.PAN_AWAIT_COMPLETION)
	self.send(PtuD300.STATUS_QUERY)

	self.send(PtuD300.PAN_POSITION_LIMIT_DISABLE)

	result = str.split(self.send(PtuD300.PAN_SPEED_BASE))
	#print result
	self.pan_speed_base = int(result[6])
	print("self.pan_speed_base: " + str(self.pan_speed_base))

	result = str.split(self.send(PtuD300.PAN_SPEED_MAXIMUM))
	#print result
	self.pan_speed_maximum = int(result[6])
	print("self.pan_speed_maximum: " + str(self.pan_speed_maximum))

	result = str.split(self.send(PtuD300.PAN_ACCELERATION))
	#print result
	self.pan_acceleration = int(result[5])
	print("self.pan_acceleration: " + str(self.pan_acceleration))
	
	result = str.split(self.send(PtuD300.PAN_POSITION_MINIMUM))
	#print result
	self.pan_position_minimum = int(result[6])
	print("self.pan_position_minimum: " + str(self.pan_position_minimum))

	result = str.split(self.send(PtuD300.PAN_POSITION_MAXIMUM))
	#print result
	self.pan_position_maximum = int(result[6])
	print("self.pan_position_maximum: " + str(self.pan_position_maximum))

	result = str.split(self.send(PtuD300.PAN_RESOLUTION))
	#print result
        self.pan_resolution_in_seconds_per_arc = float(result[2])
        print("self.pan_resolution_in_seconds_per_arc: " + str(self.pan_resolution_in_seconds_per_arc))

	self.send(PtuD300.PAN_POSITION_MINIMUM + str(self.degrees_to_positions(-170)))
	self.send(PtuD300.PAN_POSITION_MAXIMUM + str(self.degrees_to_positions(170)))

    def send(self, command):    
        self.connection.flushInput()
        self.connection.flushOutput()
        self.connection.write(command + PtuD300.DELIMITER)
        result = self.connection.readline()
        print(command + ": " + result)
        return result
        
    # 92.5714 seconds arc per position
    # 1 second/arc = 1/(60 minutes/arc * 60 seconds/arc) = 0.0002778 degrees
    # 92.5714 seconds arc * 0.0002778 degrees = 0.025716 degrees
    def degrees_to_positions(self, degrees):
        result = int(degrees/(self.pan_resolution_in_seconds_per_arc * 0.0002778))
	#print(str(degrees) + " degrees equals " + str(result) + " positions.")
        return result

    
if __name__ == '__main__':
  
    exit()
    
