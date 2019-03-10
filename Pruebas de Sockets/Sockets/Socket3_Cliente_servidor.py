import socket as socket
import sys as sys
import select
import threading
from queue import Queue
import time
from _thread import *

MSGLEN = 37
MSGLEN2 = 2048
class MySocket:

	def __init__(self, sock=None):
		if sock is None:
			self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		else:
			self.sock = sock
		self.sock.settimeout(1)

	def connect(self, host, port):
		self.sock.connect((host, port))

	def mysend(self, msg):
		totalsent = 0
		while totalsent < MSGLEN:
			sent = self.sock.send(msg[totalsent:])
			print(sent)
			if sent == 0:
				raise RuntimeError("socket connection broken")
			totalsent = totalsent + sent

	def myreceive(self):
		chunks = []
		bytes_recd = 0
		chunk = [0]
		while len(chunk) > 0:
			try:
				chunk = self.sock.recv(2048)
				if chunk == b'':
					raise RuntimeError("socket connection broken")
				chunks.append(chunk)
				bytes_recd = bytes_recd + len(chunk)
			except:
				print("Tiempo de espera agotado")
				break
		return b''.join(chunks)
	def close(self):
		self.sock.close()

s = MySocket()
s.connect('www.google.com',80)
request = "GET / HTTP/1.1\nHost: www.google.com\n\n"
s.mysend(request.encode())
Datos = s.myreceive()
print(Datos)
s.close()


















































'''
host = '' 			#
port = 1234		# el Objetivo

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
	s.bind((host, port))
except socket.error as e:
	print(str(e))

s.listen(5)
print("esperando Coneccion")
def threaded_client(conn):
	conn.send(str.encode('Welcome, Type your info\n'))
	while True:
		try:
			data = conn.recv(2048)
			reply = 'Server output: \n'+data.decode('utf-8')
		except:
			conn.close()
			break
		if not data:
			break
		conn.sendall(str.encode(reply))
	conn.close()

while True:
	conn, addr = s.accept()
	conn.settimeout(5.0)
	print('connected to: '+addr[0]+':'+str(addr[1]))
	start_new_thread(threaded_client,(conn,))

	'''