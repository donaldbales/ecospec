import fieldspec4

"""
	Let's see if we can get some data back
"""

x = fieldspec4.FieldSpec4()

print x

x.open("146.137.13.115")

v = x.version()

print "version.name: " + v.name
print "version.value: " + str(v.value)
print "version.type: " + str(v.type)

r = x.restore("1")

if r.header != 100:
	r = x.restore("1")

print "header: " + str(r.header)
print "errbyte: " + str(r.errbyte)
for i in range(0, 200):
	if r.names[i]:
		print r.names[i] + ": " + str(r.values[i])
print "count: " + str(r.count)
print "verify: " + str(r.verify)

"""
a = x.abort()

print "abort.header: " + str(a.header)
print "abort.errbyte: " + str(a.errbyte)
print "abort.name: " + a.name
print "abort.value: " + str(a.value)
print "abort.count: " + str(a.count)

"""

o = x.optimize(fieldspec4.FieldSpec4.OPT_VNIR_SWIR1_SWIR2)

print "optimize header: " + str(o.header)
print "optimize errbyte: " + str(o.errbyte)
print "optimize itime: " + str(o.itime)
print "optimize gain1: " + str(o.gain1)
print "optimize gain2: " + str(o.gain2)
print "optimize offset1: " + str(o.offset1)
print "optimize offset2: " + str(o.offset2)

if o.header == 100:
	a = x.acquire(fieldspec4.FieldSpec4.ACQUIRE_SET_SAMPLE_COUNT, "10", "0")
	print "spectrum_header.header: " + str(a.spectrum_header.header)
	print "spectrum_header.errbyte: " + str(a.spectrum_header.errbyte)
	print "spectrum_header.sample_count: " + str(a.spectrum_header.sample_count)
	print "spectrum_header.trigger: " + str(a.spectrum_header.trigger)
	print "spectrum_header.voltage: " + str(a.spectrum_header.voltage)
	print "spectrum_buffer length: " + str(len(a.spectrum_buffer))
	spectrum_data = "spectrum_data: " + str(a.spectrum_buffer[0]) 
	for i in range(1, len(a.spectrum_buffer)):
		spectrum_data += ","
		spectrum_data += str(a.spectrum_buffer[i])
	#print spectrum_data
	print "tsv: " + a.to_tsv()


x.close()
