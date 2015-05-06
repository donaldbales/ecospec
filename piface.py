# -*- coding: utf-8 -*-
#
# piface.py - Ecospec Instrumenation PiFace module
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

try:
    import pifacedigitalio
except:
    print("Can't import pifacedigitalio.")

class PiFace:

    def __init__(self):
        print "Piface.__init__()..."
        try:
            self.piface = pifacedigitalio.PiFaceDigital()
        except:
            print("Can't access pifacedigitalio.")
            self.piface = None

    def extend_white_reference_arm(self, relay_no):
        print "PiFace.extend_white_reference_arm()..."
        if self.piface:
            self.piface.relays[relay_no].turn_on()
        return True


    def power_down(self, relay_no):
        print "PiFace.power_down()..."
        if self.piface:
            self.piface.relays[relay_no].turn_off()
        return True


    def power_up(self, relay_no):
        print "PiFace.power_up()..."
        if self.piface:
            self.piface.relays[relay_no].turn_on()
        return True


    def retract_white_reference_arm(self, relay_no):
        print "PiFace.retract_white_reference_arm()..."
        if self.piface:
            self.piface.relays[relay_no].turn_off()
        return True

    def is_raining(self, relay_no):
        print "PiFace.retract_white_reference_arm()..."
        if self.piface:
            return self.piface.digital_read(relay_no)
    
