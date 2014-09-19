import socket
import struct

"""
	https://docs.python.org/2/library/socket.html
	https://docs.python.org/2/howto/sockets.html#socket-howto
	
"""	

connection = socket.socket()

host = "146.137.13.117"
port = 8080

connection.connect((host, port))

print connection.recv(1024)

connection.send("V")

response = connection.recv(1024)

fs4 = struct.unpack("!ii30sdi", response)

print fs4

connection.close()

