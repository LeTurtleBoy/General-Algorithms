import socket as Skt
import select
import threading
from queue import Queue
import time


#···············································································#
#Conección básica con una pagina a traves de un Socket

s = Skt.socket(Skt.AF_INET, Skt.SOCK_STREAM)
server = "127.0.0.1"
port = 10001
request = "GET / HTTP/1.1\nHost: "+ server +"\n\n"

s.connect((server,port))
s.send(request.encode())
s.settimeout(5.0)
Bandera = 0
Response = s.recv(1024)
while ((len(Response)>0) & (Bandera == 0)):
	print(Response)
	try:
		Response = s.recv(1024)
	except:
		Bandera = 1
		print("\n\n\nFinal de la Trama\n\n\n")

s.close()

#···············································································#
# Escaneo de puertos


s1 = Skt.socket(Skt.AF_INET, Skt.SOCK_STREAM)
s1.settimeout(5.0)
server = "http://127.0.0.1/"

def pscan(port):
	try:
		s1.connect((server))
		return True
	except:
		return False

for x in range(1,25500):
	if pscan(x):
		print("Port: ",x," is Open")
s1.close()
#···············································································#
# Escaneo de puertos

def portscan(port):
	s = Skt.socket(Skt.AF_INET, Skt.SOCK_STREAM)
	try:
		con = s.connect((target,port))
		with print_lock:
			print('Puerto ',port, ' esta Abierto')
			con.close
	except:
		print('Puerto ',port, ' no esta Abierto')
		pass

def Hilador():
	while True:
		worker = q.get()
		portscan(worker)
		q.task_done()


print_lock = threading.Lock()
target = 'http://pythonprogramming.net'
q = Queue()

for x in range(30):
	t = threading.Thread(target = Hilador)
	t.daemon = True
	t.start()

for worker in range(8060,8085):
	q.put(worker)

q.join()