import numpy as numpy
from functools import reduce

def checksum(st):
    return reduce(lambda x,y:x+y, map(ord, st))

def RespAlarma(Tanque):
	if(Tanque == "00"):
		Tanque = "01"
	print("Alarma la respuesta se debe construir con el tanque:", Tanque)
	# tanque + fecha + tanque + producto
	R = Tanque+"1807061043"+Tanque+"1"+"0000"+"07"+"00100000"+"00100000"+"00100000"+"00100000"+"00100000"+"00100000"+"00100000"+"&&"
	R = R + str(checksum(R))
	print(R)
	return(R) 

RespAlarma("00")