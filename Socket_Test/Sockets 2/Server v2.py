import sys
import socketserver as SocketServer
import subprocess
import serial

class SingleTCPHandler(SocketServer.BaseRequestHandler):
	def handle(self):
		#Aqui se maneja la comunicación del servidor
		try:
			self.ACK=self.request.recv(2).decode('ascii')
			if (self.ACK == "OK"):
				self.longitud=self.request.recv(3).decode('ascii')
				self.longitud = int(self.longitud);
				print("Trama de tamaño: ",self.longitud)
				try:
					print("Ok1")
					self.Trama=self.request.recv(self.longitud).decode('utf-8')
					self.comandos = self.cadena.split(',')

					#De Aquí en adelante configuro todos los comandos
				except:
					print("La trama llego incompleta")
					self.request.send("NO".encode(encoding = 'utf-8', errors = 'strict'))



			else:
				print("Not Ok")
		except Exception as exc:
			print("Error ", exc)

class SimpleServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
	timeout = 30
	daemon_threads = True
	allow_reuse_address = True

	def __init__(self, server_address, RequestHandlerClass):
		SocketServer.TCPServer.__init__(self, server_address, RequestHandlerClass)

	def handle_timeout(self):
		print('Timeout!')

def running(Host,Port):
	server = SimpleServer((Host,Port), SingleTCPHandler)
	try: 
		server.handle_request()

	except KeyboardInterrupt:
	  sys.exit(0)

print("Inicio de programa...")
while True:
	try:
		running('',9999)
	except Exception as Exc:
		proc = subprocess.Popen("netstat -ano|findstr 9999", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.PIPE)
		stdout, stderr = proc.communicate()
		respuesta=stdout.decode('ascii').split(" ")
		respuesta[len(respuesta)-1] = respuesta[len(respuesta)-1].split("\r")[0]
		R = []
		for i in respuesta:
			if i != "":
				R.append(i)
		proceso = R[len(R)-1]
		#tskill Proceso
		Trama = "taskkill.exe /f /pid "+ proceso
		proc = subprocess.Popen(Trama, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.PIPE)
		stdout, stderr = proc.communicate()
		print(stdout.decode('ascii'))