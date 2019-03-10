import socket as socket
import sys as sys

host = '' 			#
port = 5555 		# el Objetivo

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
	s.bind((host, port))
except socket.error as e:
	print(str(e))

s.listen(5) #Maximo 5 conecciones antes de morir

conn, addr = s.accept()

print('Conectado a: '+addr[0]+':'+str(addr[1]))