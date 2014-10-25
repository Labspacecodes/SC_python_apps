#!usr/bin/python

import serial
import gspread
import time

auth_storage = ['','']
auth_details = open('auth_file')
count = 0
for line in auth_details:
	line = line.rstrip()
	auth_storage[count] = line
	count = count+1

user_name = auth_storage[0]
password = auth_storage[1]



values = []
port = serial.Serial('/dev/ttyACM0', 9600, timeout = 2)
count = 0

while count <= 6:
	analog_port = str(count)
	port.write(analog_port)
	print count
	data = port.readline()
	data = data.rstrip()
	print data
	values.insert(count,data)
	count = count + 1
	time.sleep(5)

row_value = 0
row_num_file = open('row_num')
for row_data in row_num_file:
	row_data = row_data.rstrip()
	row_value = row_data
row_num_file.close()

coloumns = ['a','b','c','d','e']
for letters in coloumns:
	cell = letters+str(row_value)
	google = gspread.Client(auth=(user_name, password))
	google.login()
	spreadsheet = google.open('update').sheet1
	spreadsheet.update_acell(cell,values[coloumns.index(letters)+1])

row_num_file = open('row_num','w')
row_value = int(row_value)
row_value = row_value + 1
row_value = str(row_value)
row_num_file.write(row_value)
row_num_file.close()
