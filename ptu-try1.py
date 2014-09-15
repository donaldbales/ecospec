#!/usr/bin/env python

import ptu_d300
import time

positions = [-170, -139, -108, -77, -46, -15, 15, 46, 77, 108, 139, 170]

def get_next_position(current_position):
	if current_position < 11:
		next_position = current_position + 1
	else:
		next_position = 0

	return next_position


ptu = ptu_d300.PtuD300('/dev/ttyUSB0', 38400)

count            = 0
current_position = -1

while count < 18:
	current_position = get_next_position(current_position)

	if current_position == 0:
		ptu.send(ptu_d300.PtuD300.STATUS_QUERY)
		ptu.send(ptu_d300.PtuD300.PAN_SPEED_ABSOLUTE + str(ptu.pan_speed_maximum))
	else:
		ptu.send(ptu_d300.PtuD300.PAN_SPEED_ABSOLUTE + str(1000))

	ptu.send(ptu_d300.PtuD300.PAN_IMMEDIATELY)

	ptu.send(ptu_d300.PtuD300.PAN_POSITION_ABSOLUTE + str(ptu.degrees_to_positions(positions[current_position])))

	result = ptu.send(ptu_d300.PtuD300.PAN_AWAIT_COMPLETION)
	#print("result: '" + result +"'")
	#print(result[2:4])
	#if result[2:4] == "!P":
	if "!P" in result:
		print("trying again...")
		ptu.send(ptu_d300.PtuD300.PAN_POSITION_ABSOLUTE)
		ptu.send(ptu_d300.PtuD300.PAN_POSITION_ABSOLUTE + str(ptu.degrees_to_positions(positions[current_position])))
		ptu.send(ptu_d300.PtuD300.PAN_AWAIT_COMPLETION)
	
	count = 1
	time.sleep(9)

print("fininshed!")

Linux/Unix
syntax
arp
-s
<IP
address>
<serial
number>
temp
ping
-l
408
<IP
address>
Linux/Unix
example
arp
-s
192.168.0.125
00:40:8c:18:10:00
temp
ping
-l
408
192.168.0.125


