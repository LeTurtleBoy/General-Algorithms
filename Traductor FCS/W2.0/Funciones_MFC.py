# -*- coding: utf-8 -*-
import time

VersionMFC = "2.0"
VersionInt = "1.0.2.7"
Comandos_CDA = [0xC0,0xC1,0xC2,0xC3,0xC4,0xC5,0xC6,0xC7,0xCC,0xC8,0xC9,0xCA,0xCB,0xCD,0xCE,0xCF,0xD0,0xD2,0xD4,0xD5,0xD6,0xD7]

def Obtener_Password_Config(dir,D,M,A):
	fecha = [int(str(D),16),int(str(M),16),int(str(A),16)]
	Pass = fecha[0]*fecha[1]*fecha[2]
	print(Pass)
	Pass = Pass + fecha[dir%3]*fecha[dir%3]*fecha[dir%3]
	Pass = Pass + fecha[0]*dir
	Pass = Pass*dir
	Pass = Pass*((Pass%dir)+1)
	Pass = (Pass%1000000)
	print('Contraseña de acceso a la Configuración de la MFC: %06d' % Pass)

class Traductor():
	def __init__(self):
		print("Traductor de tramas entre la MFC versión {} y el integrador versión {} FCS".format(VersionMFC,VersionInt))
		self.log = ""
		self.comando = []

	def Comandos_int(self,argument):
		print("Comando: ", hex(argument))
		if argument == 0xC0:self.xconfiguraciones_iniciales(self) 	#Ok
		if argument == 0xC1:self.xpeticion_estado(self)				#Ok
		if argument == 0xC2:self.xconfigurar_productos(self) 		#Ok
		if argument == 0xC3:self.xcambiar_precios(self) 			#Ok
		if argument == 0xC4:self.xactualizar_hora(self) 			#Ok
		if argument == 0xC5:self.xreset(self)						#
		if argument == 0xC6:self.xreporte_venta(self)				# nope
		if argument == 0xC7:self.xpet_producto_canasta(self)		# nope
		if argument == 0xCC:self.ximprimir(self)					#
		if argument == 0xC8:self.xpautorizarventa(self)				#
		if argument == 0xC9:self.xautorizarventa(self)				#
		if argument == 0xCA:self.xdatosturno(self)					#
		if argument == 0xCB:self.xdatosproductocanasta(self)		#
		if argument == 0xCD:self.xventacanasta(self)				#
		if argument == 0xCE:self.xautorizaventacanasta(self)		#
		if argument == 0xCF:self.xconfirmacionturno(self)			#
		if argument == 0xD0:self.xpet_cerrar_turno(self)			#
		if argument == 0xD2:self.xconsignacion(self)				#
		if argument == 0xD4:self.xdatos_formapag(self)				#
		if argument == 0xD5:self.xnombre_productos(self)			#
		if argument == 0xD6:self.xobtener_informacion(self)			#
		if argument == 0xD7:self.xarqueo(self)						#
		return 0

	def h2s(self, arg): return "%0.2X" % arg

	def xcambiar_precios(self,arg):
		print("Cambio de Precios")
		ppu1= ""
		for i in self.comando[19:24]:
			ppu1+=(self.h2s(i)[1])
		print("Ppu1 : ",int(ppu1[::-1]))
		ppu2= ""
		for i in self.comando[24:29]:
			ppu2+=(self.h2s(i)[1])
		print("Ppu2 : ",int(ppu2[::-1]))
		ppu3= ""
		for i in self.comando[29:34]:
			ppu3+=(self.h2s(i)[1])
		print("Ppu3 : ",int(ppu3[::-1]))	

	def xpeticion_estado(self,*args): 
		print("Petición de estado a la dirección: {}".format(self.comando[17]))

	def xreporte_venta(self,*args): 
		print("Petición de reporte de venta a la dirección: {}".format(self.comando[17]))

	def xpet_producto_canasta(self,*args): 
		print("Petición de datos para producto canasta a la dirección: {}".format(self.comando[17]))

	def xconfigurar_productos(self,*args):
		print("Configurar producto")
		txt = ''
		for i in range(19,len(self.comando)-1):
			txt+=chr(self.comando[i])
		txt = txt.split(";")
		del txt[-1]
		print(txt)
		NombreProducto = ''.join(chr(x) for x in self.comando[92:122])
		print("Nombre Producto :", NombreProducto)

	def xconfiguraciones_iniciales(self,*args):
		print("Configuraciones Iniciales")
		print("Fecha :",self.h2s(self.comando[19]),"/",self.h2s(self.comando[20]),"/",self.h2s(self.comando[21]))
		print("Hora :",self.h2s(self.comando[22]),"/",self.h2s(self.comando[23]),"/",self.h2s(self.comando[24]))
		print("Número mangueras :",int(int(self.h2s(self.comando[25])[1])/2))
		print("Digitos :",int(self.h2s(self.comando[25])[1]))
		if(int(self.h2s(self.comando[27])[1])):
			ppu10="Si" 
		else: 
			ppu10="No"
		print("ppu x10 :",ppu10)
		if(int(self.h2s(self.comando[29])[1])):
			pOb="Si" 
		else: 
			pOb="No"
		print("Placa Obl :",pOb)
		print("Dec Dinero :",int(self.h2s(self.comando[30])[1]))
		print("Dec Volumen :",int(self.h2s(self.comando[31])[1]))
		print("Dec ppu :",int(self.h2s(self.comando[32])[1]))
		Nom = ''.join(chr(x) for x in self.comando[33:62])
		print("Nombre :", Nom)
		Dir = ''.join(chr(x) for x in self.comando[62:92])
		print("Dirección :", Dir)
		Lema1 = ''.join(chr(x) for x in self.comando[92:122])
		print("Municipio :", Lema1)
		Lema2 = ''.join(chr(x) for x in self.comando[122:152])
		print("Telefono :", Lema2)
		P1= ""
		P2= ""
		P3= ""
		Dir= ""
		for i in self.comando[152:159]:
			P1+=(self.h2s(i)[1])
		print("P1 : ",int(P1[::-1]))
		for i in self.comando[159:166]:
			P2+=(self.h2s(i)[1])
		print("P2 : ",int(P2[::-1]))
		for i in self.comando[166:174]:
			P3+=(self.h2s(i)[1])
		print("P3 : ",int(P3[::-1]))
		for i in self.comando[174:190]:
			Dir+=(self.h2s(i)[1])
		print("MFC Dir: ", Dir)

	def xdatosproductocanasta(self,*args):
		print("Datos Producto Canasta")
		Nombre = ''.join(chr(x) for x in self.comando[20:40])
		print("Nombre :", Nombre)
		Valor = ""
		for i in self.comando[40:47]:
			Valor+=(self.h2s(i)[1])
		print("Valor :",int(Valor[::-1]))

	def xactualizar_hora(self,*args):
		print("Actualizar hora")
		print("Fecha :",self.h2s(self.comando[19]),"/",self.h2s(self.comando[20]),"/",self.h2s(self.comando[21]))
		print("Hora :",self.h2s(self.comando[22]),"/",self.h2s(self.comando[23]),"/",self.h2s(self.comando[24]))
		
	def Cargar_Log(self, ruta):
		bandera = 0
		try:
			file = open(ruta,'r')
			try:
				self.log = file.read()
				file.close()
				bandera = 1
			except:
				print("Error de permisos")
				file.close()
		except:
			print("El archivo o la ruta no son correctos")

		self.Separar_Log(bandera)

	def Separar_Log(self, bandera):
		if(bandera):
			self.comando = self.log.split(" ")
			# try:
			aux = []
			for data in self.comando:
				aux2 = int(data,16)
				aux.append(aux2)

			self.comando = aux #[int(Data, 16) for Data in self.comando]
			self.Int2Hw()
			#except:
			#	print("El comando no puede comenzar con espacios  y debe tener solo caracteres hexadecimales")
		else:
			print("Log Vacío")

	def Int2Hw(self):
		Size = len(self.comando)
		if(self.Comandos_int(self.comando[18])==0): print("Errno")
	
T = Traductor()
T.Cargar_Log("Log.txt")
