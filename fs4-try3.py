import fieldspec4

"""
	Let's see if we can get the initialization values from flash
"""

x = fieldspec4.FieldSpec4()

print x

x.open("146.137.13.115")

y = x.version()

print "version.name: " + y.name
print "version.value: " + str(y.value)
print "version.type: " + str(y.type)

y = x.restore("0")

if y.header != 100:
	y = x.restore("0")

print "header: " + str(y.header)
print "errbyte: " + str(y.errbyte)
for i in range(0, 200):
	if y.names[i]:
		print y.names[i] + ": " + str(y.values[i])
print "count: " + str(y.count)
print "verify: " + str(y.verify)

y = x.init(fieldspec4.FieldSpec4.INIT_GET_VALUE_FROM_FLASH, "Version")

print "version: " + str(y.value)

x.close()
