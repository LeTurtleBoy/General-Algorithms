import sys
import socketserver as SocketServer
import subprocess
import serial
from functools import reduce

Alarma = "i101"
Inventario = "i201"
Descargues = "i202"
CorteTurno = "i20M"

UltimoCliente = ''

def checksum(st):
    return reduce(lambda x,y:x+y, map(ord, st))

def RespAlarma(Tanque):
	print("Alarma la respuesta se debe construir con el tanque:", Tanque)
	return "Test"
	

def RespInven(Tanque):
	if(Tanque == "00"):
		Tanque = "01"
	print("Inventario la respuesta se debe construir con el tanque:", Tanque)
	R = Tanque+"1807061043"+Tanque+"1"+"0000"+"07"+"00100000"+"00100000"+"00100000"+"00100000"+"00100000"+"00100000"+"00100000"+"&&"
	R = R + str(checksum(R))
	print(R)
	return(R)

def RespDesc(Tanque):
	print("Descargue la respuesta se debe construir con el tanque:", Tanque)
	return "Test"

def RespCorte(Tanque):
	print("Corte la respuesta se debe construir con el tanque:", Tanque)
	return "Test"





def f(x):
    return {
        Alarma: 1,
        Inventario: 2,
        Descargues: 3,
        CorteTurno: 4
    }.get(x, 0)

B = 0
class SingleTCPHandler(SocketServer.BaseRequestHandler):

	def handle(self):
		global UltimoCliente
		try:
			self.longitud =self.request.recv(5).decode('ascii')
			if self.longitud[4] == 'M':
				self.longitud = self.longitud + self.request.recv(26).decode('ascii')
			else:
				self.longitud = self.longitud + self.request.recv(2).decode('ascii')
			UltimoCliente = self.client_address[0]
			print("Cliente Actual: ", UltimoCliente)
			pregunta = f(self.longitud[1:5])
			if (len(self.longitud)== 7):
				Tanque = self.longitud[5:7]
				if (pregunta == 1):
					Res = RespAlarma(Tanque)
				if (pregunta == 2):
					Res = RespInven(Tanque)
					self.request.send((self.longitud[0:5]+Res+self.longitud[len(self.longitud)-1]).encode())
				if (pregunta == 3):
					Res = RespDesc(Tanque)
			else:
				if(pregunta == 4):
					Res = RespCorte(Tanque)
			print(Res)

		except Exception as exc:
			print("Error ", exc)

class SimpleServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):

	timeout = 20
	daemon_threads = True
	allow_reuse_address = True
	B = 0
	def __init__(self, server_address, RequestHandlerClass):
		SocketServer.TCPServer.__init__(self, server_address, RequestHandlerClass)
	
	def handle_timeout(self):
		print("TimeOut")
	

def running(Host,Port):
	server = SimpleServer((Host,Port), SingleTCPHandler)
	try: 
		server.handle_request()
	except KeyboardInterrupt:
	  sys.exit(0)

print("Inicio de programa...")
while True:
	try:
		running('192.168.10.110',10001)
	except Exception as Exc:
		proc = subprocess.Popen("netstat -ano|findstr 9999", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.PIPE)
		stdout, stderr = proc.communicate()
		respuesta=stdout.decode('ascii').split(" ")
		respuesta[len(respuesta)-1] = respuesta[len(respuesta)-1].split("\r")[0]
		R = []
		for i in respuesta:
			if i != "":
				R.append(i)
		#if R:
		print(R)
		proceso = R[len(R)-1]
		#tskill Proceso
		Trama = "taskkill.exe /f /pid "+ proceso
		proc = subprocess.Popen(Trama, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.PIPE)
		stdout, stderr = proc.communicate()
		print(stdout.decode('ascii'))