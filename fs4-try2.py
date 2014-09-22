import fieldspec4

x = fieldspec4.FieldSpec4()

print x

x.open("146.137.13.117")

y = x.version()

print(y.header)
print(y.errbyte)
print(y.name)
print(y.value)
print(y.type)

x.close()
