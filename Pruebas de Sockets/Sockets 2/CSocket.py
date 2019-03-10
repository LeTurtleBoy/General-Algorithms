#Cliente Socket
import socket 

host = "localhost"
port = 9999

socket1=socket.socket()
socket1.connect((host,port))

try:
	while(True):
		cadena = input("Comando:")
		socket1.send(cadena.encode(encoding = 'utf-8', errors = 'strict').strip())
		try:
			CadenaRecServidor = socket1.recv(2).decode('utf-8')
			if CadenaRecServidor == "OK":
				CadenaRecServidor = socket1.recv(16).decode('utf-8')
			else:
				print(len(CadenaRecServidor))
			print("Servidor ",CadenaRecServidor)
		except:
			print("la respuesta del servidor me jodio")
			socket1.connect((host,port))
except Exception as exc:
	print("Error ",exc)

socket1.close()
