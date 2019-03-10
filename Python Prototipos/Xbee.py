import Constantes as cons
import Estructuras as struct
#Variables de trabajo modulo xbee

global Can
global Fiel
global Recibo
global Estacion
global PCol
global Turno
global Surtidor
global infoS

def XBee_GetRxBufferSize():
	#Tomar el Tamaño del Buffer del Xbee
	pass

def XBee_ClearRxBuffer():
	for i in range(len(XBee_Buffer)):
		XBee_Buffer[i]=0

def preprocesar():
	dir_a = XBee_rxBuffer[15] - lado.dir[0][0];
	respuesta[0]  = 0x7E;
	respuesta[3]  = 0x10;
	respuesta[4]  = 0x01;
	respuesta[5]  = XBee_rxBuffer[4];
	respuesta[6]  = XBee_rxBuffer[5];
	respuesta[7]  = XBee_rxBuffer[6];
	respuesta[8]  = XBee_rxBuffer[7];
	respuesta[9]  = XBee_rxBuffer[8];
	respuesta[10] = XBee_rxBuffer[9];
	respuesta[11] = XBee_rxBuffer[10];
	respuesta[12] = XBee_rxBuffer[11];
	respuesta[13] = 0xFF;
	respuesta[14] = 0xFE;
	respuesta[15] = 0x00;
	respuesta[16] = 0x00;	
	respuesta[17] = XBee_rxBuffer[15]

def call_xbee(cmd):
	preprocesar()
	#Continuar con la logica

def polling_xbee():
	struct.Estacion.nombre = "La Mojana"
	print(struct.Estacion.nombre)
	
	'''
	size1 = XBee_GetRxBufferSize()
	if(size1 >= 10):
		size2 = XBee_GetRxBufferSize()
		if(size2 == size1):
			if((XBee_Buffer[0] == 0x7E) & (XBee_Buffer[3] == 0x90)):
				cmd = XBee_Buffer[16]
				call_xbee(cmd)
				XBee_ClearRxBuffer()
			else:
				XBee_ClearRxBuffer()
				'''


