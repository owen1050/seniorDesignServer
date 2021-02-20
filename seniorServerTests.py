import http.client

def req(conn, type, send):
	connection.request(type, send)
	response = connection.getresponse()
	print(str(type)+":"+send+":"+str(response.read().decode()))
	return response.read().decode()

connection = http.client.HTTPConnection('localhost:1234')
req(connection, 'POST', "/")
req(connection, 'GET', "/all")
req(connection, 'GET', "/device1")
req(connection, 'GET', "/!device2/device2")
req(connection, 'POST', "/bas")
req(connection, 'POST', "/new/newDev1")
req(connection, 'POST', "/set/newDev1/1")
