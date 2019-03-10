# -*- coding: cp1252 -*-

def Paso_1(D,M,A):
	fecha = [int(str(D),16),int(str(M),16),int(str(A),16)]
	Pass = fecha[0]*fecha[1]*fecha[2];						#Equivalente en C
	#print("Contraseña generada para el dia ", D,"/",M,"/",A)
	return [Pass, fecha]

def Paso_2(Args,Dir):
	Pass, fecha = Args[0],Args[1]
	Pass = (Pass*Dir)+(fecha[(fecha[0]*Dir)%3]*fecha[(fecha[0]*Dir)%2]*fecha[(fecha[0]*Dir)%1]); #Equivalente en C con Dir = lado.Dir[Dir]
	return Pass,fecha,Dir

def Paso_3(Args):
	Pass, fecha, Dir = Args[0],Args[1],Args[2]
	Pass = Pass + fecha[0]*Dir;
	Pass = Pass*Dir;
	Pass = Pass*((Pass%Dir)+1);
	Pass = (Pass%1000000);
	if (Pass<1000):
		Pass = Pass*159357
	Pass = (Pass%1000000);
	return Pass

def Password_MFC(Dir=6,D=0,M=0,A=0):
	if(D == M == A == 0):
		#print("Datos por defecto")
		import datetime
		date = str(datetime.datetime.now())
		A = int(date.split(" ")[0].split("-")[0])-2000
		M = int(date.split(" ")[0].split("-")[1])
		D = int(date.split(" ")[0].split("-")[2])
	return "%06d" % Paso_3(Paso_2(Paso_1(D,M,A),Dir))

import datetime
import pandas as pd
'''
print("Construir password")
Struct_Pass = {'Mes': [0],'Dia': [0], 'Cara MFC': [0],'Password':['']}
df = pd.DataFrame(data=Struct_Pass)
fechas = []
for i in range(1,13):
	for j in range(32):
		try:
			aux = str(datetime.date(2019,i,j)).split('-')
			aux[0],aux[1],aux[2] = int(aux[0]),int(aux[1]),int(aux[2])
			fechas.append(aux)
		except Exception as e:
			pass
x = 0
for j in fechas:				
	for i in range(1,17):
		password = (Password_MFC(Dir=i,D=j[2],M=j[1],A=j[0]-2000))
		Row = [j[1],j[2],i,str(password)]
		df.loc[x] = Row
		x+=1
df.to_excel("info.xlsx")

Grupo = df.groupby("Mes")
for i, j in Grupo:
	writer = pd.ExcelWriter("Contra_Mes"+str(i)+".xlsx")
	Grupo2 = j.groupby("Dia")
	for m, n in Grupo2:
		n.Password = n.Password.apply('="{}"'.format)
		n.to_excel(writer,sheet_name  = "Dia "+str(m),index=False,encoding= "utf-8")
	writer.save()
'''
x = 0
j = [2096,1,1]
Struct_Pass = {'Mes': [0],'Dia': [0], 'Cara MFC': [0],'Password':['']}
df = pd.DataFrame(data=Struct_Pass)
for i in range(1,17):
	password = (Password_MFC(Dir=i,D=j[2],M=j[1],A=j[0]-2000))
	Row = [j[1],j[2],i,str(password)]
	df.loc[x] = Row
	x+=1
df.to_excel("info2096.xlsx")