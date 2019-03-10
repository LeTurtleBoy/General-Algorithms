import sys, re
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog
from PyQt5 import uic, QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import ctypes
import pandas as pd
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
from os import scandir, getcwd
import os as os
from threading import Thread
import threading
import psutil
import time as ti
import shutil
import cv2

Diagnosticando = 0
t = Thread()
Aforo = pd.DataFrame()
Descarge = pd.DataFrame()
Ventas = pd.DataFrame()
VentasRef = pd.DataFrame()
Inventario = pd.DataFrame()
fileName = ""
Factura = pd.DataFrame()
Imagenes = []
Ima = 0

Uso = True

def Cambiar_Estado():
	global Uso
	ti.sleep(0.5)
	Uso = not(Uso)
	return (Uso)

def DiagnoFuera(TankPri,TankSec):
	global Diagnosticando
	if os.path.exists("ImagenesCorr") == False:
		os.mkdir("ImagenesCorr")
		path = "ImagenesCorr"
		ctypes.windll.kernel32.SetFileAttributesW(path, 2)
	NombresTanques=[TankPri,TankSec]
	Elementos = ls("\\Fechas")
	Ntank = 1
	if TankSec != "":
		Ntank = 2
	Lista = [0]*Ntank
	for i in range(Ntank):
		Lista[i] = [Elementos for Elementos in Elementos if Elementos.endswith(str(NombresTanques[i])+'.xlsx')]
	for k in Lista:
		if len(k) == 3:
			Aforop = pd.read_excel("Tanques\\Aforo"+TankPri+".xlsx")
			Ventasp = pd.read_excel("Fechas\\"+k[2])
			Inventp = pd.read_excel("Fechas\\"+k[1])
			Descarp = pd.read_excel("Fechas\\"+k[0])
		if len(k) == 2:
			Aforos = pd.read_excel("Tanques\\Aforo"+TankSec+".xlsx")
			Invents = pd.read_excel("Fechas\\"+k[1])
			Descars = pd.read_excel("Fechas\\"+k[0])
	JJ = []
	for I,J in Descarp.groupby("DiaInicialDescarge"):
		J = J[["AlturaInicial","AlturaFinal","VolInicial","VolFinal","HoraFinalDescarge","DiaInicialDescarge","HoraInicialDescarge"]]
		JJ.append([J["DiaInicialDescarge"].tolist()[0],J["HoraFinalDescarge"].tolist()[0],J["VolFinal"].tolist()[0]-J["VolInicial"].tolist()[0]])

	A = pd.DataFrame(JJ)
	A.columns = ['DIA', 'HORA','Descarge']
	cols = ['DIA', 'HORA']
	A[cols] = A[cols].applymap(np.int64)
	Day2 = []
	Hour2 = []
	for i in A.DIA.tolist():
		Day2.append('%0.2d' % i)
	for i in A.HORA.tolist():
		Hour2.append('%0.2d' % i)
	indice = []
	for j in range(len(Day2)):
		indice.append(Day2[j]+Hour2[j])
	A.index = indice
	A.to_excel("DescargePrincipal"+".xlsx")
		
	if Ntank == 2:
		JJ = []
		for I,J in Descars.groupby("DiaInicialDescarge"):
			J = J[["AlturaInicial","AlturaFinal","VolInicial","VolFinal","HoraFinalDescarge","DiaInicialDescarge","HoraInicialDescarge"]]
			JJ.append([J["DiaInicialDescarge"].tolist()[0],J["HoraFinalDescarge"].tolist()[0],J["VolFinal"].tolist()[0]-J["VolInicial"].tolist()[0]])
		A = pd.DataFrame(JJ)

		A.columns = ['DIA', 'HORA','Descarge']
		cols = ['DIA', 'HORA']
		A[cols] = A[cols].applymap(np.int64)
		Day2 = []
		Hour2 = []
		for i in A.DIA.tolist():
			Day2.append('%0.2d' % i)

		for i in A.HORA.tolist():
			Hour2.append('%0.2d' % i)
		indice = []
		for j in range(len(Day2)):
			indice.append(Day2[j]+Hour2[j])
		A.index = indice
		A.to_excel("DescargeSecundario"+".xlsx")
	else:
		1
	GDia = Ventasp.groupby("DiaVenta")
	Diaux = []
	Horaux = []
	Ventaux = []
	Datos = [0]*len(GDia)
	i,j=[0,0]
	for Dia,Df in GDia:
		GHoras = Df.groupby("HoraVenta")
		j = 0
		for Hora, Df in GHoras:
			Diaux.append(Dia) 
			Horaux.append(Hora) 
			Ventaux.append(np.sum(Df["Volumen.1"].tolist()))
	Datos = [Diaux,Horaux,Ventaux]
	Datos = np.array(Datos).T.tolist()
	A = pd.DataFrame(Datos)
	A.columns = ['DIA', 'HORA','Venta']
	cols = ['DIA', 'HORA']
	A[cols] = A[cols].applymap(np.int64)

	Day2 = []
	for i in A.DIA.tolist():
		Day2.append('%0.2d' % i)
	Day = Day2


	Hour2 = []
	for i in A.HORA.tolist():
		Hour2.append('%0.2d' % i)

	indice = []
	for j in range(len(Day)):
		indice.append(Day2[j]+Hour2[j])
	A.index = indice



	GDia = Inventp.groupby("DiaInventario")
	Diaux = []
	Horaux = []
	Ventaux = []
	Ai = []
	Af = []
	Datos = [Dia]*len(GDia)
	i,j=[0,0]
	for Dia,Df in GDia:
		GHoras = Df.groupby("HoraInventario")
		j = 0
		for Hora, Df in GHoras:
			Diaux.append(Dia) 
			Horaux.append(Hora) 
			Ventaux.append((Df["Volumen"].tolist()[0]-Df["Volumen"].tolist()[len(Df["Volumen"].tolist())-1]))
			Ai.append((Df["Altura"].tolist()[0]))
			Af.append(Df["Altura"].tolist()[len(Df["Altura"].tolist())-1])
	Datos = [Diaux,Horaux,Ventaux,Ai,Af]
	Datos = np.array(Datos).T.tolist()
	B = pd.DataFrame(Datos)
	B.columns = ['DIA', 'HORA','Inventario','Altura I','Altura F']
	cols = ['DIA', 'HORA']
	B[cols] = B[cols].applymap(np.int64)
	Day2 = []
	for i in B.DIA.tolist():
		Day2.append('%0.2d' % i)
	Day = Day2


	Hour2 = []
	for i in B.HORA.tolist():
		Hour2.append('%0.2d' % i)

	indice = []
	for j in range(len(Day)):
		indice.append(Day2[j]+Hour2[j])
	B.index = indice
	result = pd.concat([A["Venta"],B], axis=1)
	result = result.fillna(0)
	result["Diferencia"] = np.array(result.Venta.tolist())-np.array(result.Inventario.tolist())
	result.to_excel("VentasInventarioPrincipal.xlsx")
	#NVENTARIO SECUNDARIO
	if Ntank == 2:
		GDia = Invents.groupby("DiaInventario")
		Diaux = []
		Horaux = []
		Ventaux = []
		Ai = []
		Af = []
		Datos = [Dia]*len(GDia)
		i,j=[0,0]
		for Dia,Df in GDia:
			GHoras = Df.groupby("HoraInventario")
			j = 0
			for Hora, Df in GHoras:
				Diaux.append(Dia) 
				Horaux.append(Hora) 
				Ventaux.append((Df["Volumen"].tolist()[0]-Df["Volumen"].tolist()[len(Df["Volumen"].tolist())-1]))
				Ai.append((Df["Altura"].tolist()[0]))
				Af.append(Df["Altura"].tolist()[len(Df["Altura"].tolist())-1])
		Datos = [Diaux,Horaux,Ventaux,Ai,Af]
		Datos = np.array(Datos).T.tolist()
		B = pd.DataFrame(Datos)
		B.columns = ['DIA', 'HORA','Inventario','Altura I','Altura F']
		cols = ['DIA', 'HORA']
		B[cols] = B[cols].applymap(np.int64)
		Day2 = []
		for i in B.DIA.tolist():
			Day2.append('%0.2d' % i)
		Day = Day2
		Hour2 = []
		for i in B.HORA.tolist():
			Hour2.append('%0.2d' % i)
		indice = []
		for j in range(len(Day)):
			indice.append(Day2[j]+Hour2[j])
		B.index = indice
		B.to_excel("InventarioSecundario.xlsx")
	#NVENTARIO SECUNDARIO
	if Ntank == 2:
		IS = pd.read_excel("InventarioSecundario.xlsx")
		DS = pd.read_excel("DescargeSecundario.xlsx")
		IVP = pd.read_excel("VentasInventarioPrincipal.xlsx")
		DP = pd.read_excel("DescargePrincipal.xlsx")
		result = pd.concat([IVP[["DIA","HORA","Venta","Inventario",'Altura I','Altura F']], IS["Inventario"],DP["Descarge"],DS["Descarge"]], axis=1)
		result = result.fillna(0)
		result.columns = ['Dia', 'Hora','Ventas prin','Inv prin','Altura I','Altura F','Inv sec','Desc prin','Desc sec']
		result["Balance"] = np.array(result["Ventas prin"].tolist()) - (np.array(result["Inv prin"].tolist())+np.array(result["Inv sec"].tolist())+np.array(result["Desc prin"].tolist())+np.array(result["Desc sec"].tolist()))
		result.to_excel("Balance.xlsx")
	else:
		IVP = pd.read_excel("VentasInventarioPrincipal.xlsx")
		DP = pd.read_excel("DescargePrincipal.xlsx")
		result = pd.concat([IVP[["DIA","HORA","Venta","Inventario",'Altura I','Altura F']], DP["Descarge"]], axis=1)
		result = result.fillna(0)
		result.columns = ['Dia', 'Hora','Ventas prin','Inv prin','Altura I','Altura F','Desc prin']
		result["Balance"] = np.array(result["Ventas prin"].tolist()) - (np.array(result["Inv prin"].tolist())+np.array(result["Desc prin"].tolist()))
		result.to_excel("Balance.xlsx")
	G1 = result.groupby("Dia")
	DataD = []
	DataV = []

	for i,j in G1:
		f, ax = plt.subplots(2)
		ax[0].set_title('Tanque principal dia: '+str(i))
		Dataux = j["Balance"].tolist()
		Dataux2 = i
		DataD.append(Dataux2)
		DataV.append(Dataux)
		ax[0].plot(j["Balance"],"X-")
		minx = np.min(j.index.tolist())
		maxx = np.max(j.index.tolist())
		miny = np.min(j["Balance"].tolist())+0.3*np.min(j["Balance"].tolist())
		maxy = np.max(j["Balance"].tolist())+0.3*np.max(j["Balance"].tolist())
		ax[0].set_xlabel('DIA HORA')
		ax[0].set_ylabel('Delta Balance [gal]')
		ax[0].axis([minx,maxx,miny,maxy])
		ax[1].annotate('Valor medio: '+str(np.mean(j["Balance"].tolist())),[0,0.8])
		ax[1].annotate('Varianza : '+str(np.std(j["Balance"].tolist())),[0,0.6])
		ax[1].annotate('Valor máximo: '+str(np.max(j["Balance"].tolist())),[0,0.4])
		ax[1].annotate('Valor mínimo: '+str(np.min(j["Balance"].tolist())),[0,0.2])
		ax[1].axis('off')
		plt.savefig('ImagenesCorr\\Tanque'+str(i)+'.tiff', format='tiff', dpi=600)
	Diagnosticando = 1

def ls(a):
	ruta = getcwd() + a
	return [arch.name for arch in scandir(ruta) if arch.is_file()]

def Analisis(Ubicacion,Tanque,Dia,Facturado):
	plt.close()
	try:
		dfD = pd.read_excel("Fechas\\FechasDescarge"+str(Tanque)+".xlsx")
		dfI = pd.read_excel("Fechas\\FechasInventario"+str(Tanque)+".xlsx")
		dfV = pd.read_excel("Fechas\\FechasVentas"+str(Tanque)+".xlsx")
		dfA = pd.read_excel("Tanques\\Aforo"+str(Tanque)+".xlsx")
	except:
		return 0
	G1 = dfD.groupby("DiaInicialDescarge")
	B = 0
	for i,j in G1:
		if B == 1:
			Final  = int(j["InicioFechaUniversal"].tolist()[0])-10
			break
		if str(i) == str(Dia):
			Inicio = int(j["FinalFechaUniversal"].tolist()[0])+10
			B = 1
	try:
		plt.close()
		plt.figure()
		dfI=dfI[(dfI['FechaUniversal'] >= (Inicio)) & (dfI['FechaUniversal'] <= (Final))]
		dfV=dfV[(dfV['FechaUniversal'] >= (Inicio)) & (dfV['FechaUniversal'] <= (Final))]
		Ventas = np.cumsum(np.array(dfV['Volumen.1'].tolist()))
		Delta = dfI['Volumen'].tolist()[len(dfI['Volumen'].tolist())-1]-dfI['Volumen'].tolist()[0]
		plt.plot(dfI["FechaUniversal"].tolist(),dfI['Volumen'].tolist(),'.')
		Ventas2 = np.array(Ventas)+np.min(np.array(dfI['Volumen'].tolist()))
		plt.plot(dfV["FechaUniversal"].tolist(),Ventas2,'.')
		plt.legend(('Inventario', 'Ventas'))
		plt.ylabel('Volumen [gal]')
		plt.xlabel('Identificador Temporal')
		plt.savefig(Ubicacion+'1'+'.tiff', format='tiff', dpi=600)
		plt.close()
		##################################################################################
		dfI.index = dfI["FechaUniversal"]
		plt.figure()
		dfI = dfI[["Volumen","Altura"]]
		dfV.index = dfV["FechaUniversal"]
		dfV = dfV[["Volumen.1"]]
		dfV = dfV.groupby(dfV.index).agg({'Volumen.1':sum})
		dfV = dfV[['Volumen.1']]
		dfI.drop_duplicates(inplace=True)
		result = dfI.join(dfV)
		result = result.fillna(0)
		Delta = Delta + np.sum(np.array(dfV["Volumen.1"].tolist())) #Este es el cambio de altura que debo modificar
		Alt_f = int(dfI["Altura"].tolist()[0]/10)
		Alt_i = int(dfI["Altura"].tolist()[len(dfI["Altura"].tolist())-1]/10)
		Aforo1 = dfA[(dfA['Medida'] <  Alt_i)]
		Aforo2 = dfA[(dfA['Medida'] >= Alt_i) & (dfA['Medida'] <= Alt_f)]
		Aforo3 = dfA[(dfA['Medida'] >  Alt_f)]
		Aforo1['Delta'] = np.zeros(len(Aforo1))
		x = len(Aforo2)
		Ind = Delta/x
		Data = np.linspace(1,x,x)
		Data = np.array(Data)*Ind
		Aforo2["Delta"]=Data
		x = len(Aforo3)
		Ind = Delta
		Data = np.ones(x)
		Data = np.array(Data)*Ind
		Aforo3["Delta"]=Data
		Aforo2.Galones = Aforo2['Galones'].add(Aforo2['Delta'])
		Aforo3.Galones = Aforo3['Galones'].add(Aforo3['Delta'])
		AforoCorregido= pd.concat([Aforo1,Aforo2,Aforo3])
		AforoCorregido['Galones Vieja'] = dfA['Galones']
		plt.plot(AforoCorregido['Medida'].tolist(),AforoCorregido['Galones'].tolist())
		plt.plot(dfA['Medida'].tolist(),dfA['Galones'].tolist())
		plt.legend(('Aforo Nuevo', 'Aforo Viejo'))
		AforoCorregido.to_excel(Ubicacion)
		plt.savefig(Ubicacion+'2'+'.tiff', format='tiff', dpi=600)
		##################################################################################
		return 1
	except:
		return 0



	#df[(df['column_name'] == some_value) & df['other_column'].isin(some_values)]

class Ventana(QMainWindow):	
	def __init__(self):
		event = threading.Event()
		QMainWindow.__init__(self)
		uic.loadUi("Correcion.ui", self)
		self.setWindowTitle("SIDICOM")
		QApplication.processEvents()
		resolucion = ctypes.windll.user32
		resolucion_ancho = resolucion.GetSystemMetrics(0)
		resolucion_alto = resolucion.GetSystemMetrics(1)
		left = (resolucion_ancho / 2) - (self.frameSize().width() / 2)
		top = (resolucion_alto / 2) - (self.frameSize().height() / 2)
		self.move(left, top)
		qfont = QFont("Arial", 10)
		self.setGeometry(left, top, 500, 250)
		self.Dependientes.setChecked(False)
		self.set_image("LOGO.jpg")
		self.Diagnostico.clicked.connect(self.Diagnosticar)
		self.Dependientes.clicked.connect(self.EnableBabe)
		self.Dep.setEnabled(False)
		self.Atras.clicked.connect(self.CambiarAt)
		self.Adelante.clicked.connect(self.CambiarAd)
		self.Atras.setEnabled(False)
		self.Adelante.setEnabled(False)
		self.Graficar.clicked.connect(self.Habilitar)
		self.IDes.clicked.connect(self.CargarDescargue)
		self.Ayuda.clicked.connect(self.MostrarAyuda)

	def MostrarAyuda(self):
		QMessageBox.question(self,"Menu de Ayuda.","ORDEN DE USO:\n 1. Especificar el tanque.\n 2. Indicar si hay dependencia y sobre que tanque.\n 3. Diagnosticar Especifico Diario \n 4. Graficar Diario",QMessageBox.Ok)
		QMessageBox.question(self,"Menu de Ayuda.","Para corregir el aforo del tanque debe cargarse el archivo de descargues de facturas.\nEste archivo debe contar con la estructura mostrada a continuación\nSe debe indicar sobre cual descargue se desea realizar la correción",QMessageBox.Ok)
		plt.figure(2,figsize=(250,250))
		Img1 = cv2.imread("Ayuda\\P3A1.png")
		plt.axis("off")
		figManager = plt.get_current_fig_manager()
		figManager.window.showMaximized()
		plt.imshow(cv2.cvtColor(Img1, cv2.COLOR_BGR2RGB))
		plt.show()
	def CargarDescargue(self):
		global Factura
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()","","Archivos de Excel (*.xls , *.xlsx)", options=options)
		if fileName == "":
			1
		else:
			Factura = pd.read_excel(fileName)
			G1 = Factura.groupby("TanqueID")
			for I,J in G1: 								############# Encuentro todos los tanques
				if (str(I)== str(self.Ind.toPlainText())):		# Pregunto si alguno de los tanques coincide con el que estoy analizando
					Band = 0
					for Dia in J["Dia"].tolist():
						if (str(Dia)==str(self.Desindi.toPlainText())): # Pregunto si en los dias de descargue existe alguno como la entrada
							Band =Band+1
					if Band == 0:
						QMessageBox.question(self,"Error en Dia","Error en el dia, los dias registrados con descargue son: "+str(J["Dia"].tolist()),QMessageBox.Ok)## Si no existe ninguno imprimo la lista de los dias que si estan.
					else:
						G2 = J.groupby("Dia") 								# Si el dia si existe, procedo a encontrar el Volumen descargado ese dia 
						for II,JJ in G2:
							if (str(II)== str(self.Desindi.toPlainText())):
								Facturado = JJ["Facturado"].tolist()[0] 		# Ac'a debo sumar todo lo descargado ese dia o especificar por horas que carajos hare
		if (Band != 0):
			VentasINventario = pd.read_excel("VentasInventarioPrincipal.xlsx")
			G1 = VentasINventario.groupby("DIA")							# Si el dia si existe, procedo a encontrar el Volumen descargado ese dia 
			for I,J in G1:
				if (str(I)== str(self.Desindi.toPlainText())):
					Reportado = np.sum(J["Diferencia"].tolist())
			Value = Facturado-Reportado
			QMessageBox.question(self,"Reporte","La diferencia entre lo reportado y lo facturado ese dia es de: "+str(Value),QMessageBox.Ok)
			if abs(Value) > 0:
				file = str(QFileDialog.getExistingDirectory(self, "Por favor seleccione la carpeta donde quiere guardar el nuevo aforo para el tanque"))
				file = file.replace("/", "\\") + "\\AforoNuevo"+str(self.Ind.toPlainText())+".xlsx"
				Bandera = Analisis(file,str(self.Ind.toPlainText()),str(self.Desindi.toPlainText()),Facturado)


	def set_image(self, filename):
		pixmap = QPixmap(filename)
		pic = self.Imagenes
		pic.setScaledContents(True)
		pic.setPixmap(pixmap)

	def Habilitar(self):
		global Diagnosticando
		if Diagnosticando != 0:
			self.Atras.setEnabled(True)
			self.Adelante.setEnabled(True)

	def closeEvent(self,event):
		resultado = QMessageBox.question(self,"Salir...","¿Seguro que quieres salir de la aplicación?",QMessageBox.Yes|QMessageBox.No)
		if (resultado == QMessageBox.Yes) & (threading.active_count() == 1):
			event.accept()
		else: 
			event.ignore()

	def EnableBabe(self):
		if self.Dependientes.isChecked():
			self.Dep.setEnabled(True)
		else:
			self.Dep.setEnabled(False)

	def Diagnosticar(self):
		self.Atras.setEnabled(False)
		self.Adelante.setEnabled(False)
		global Diagnosticando
		if Diagnosticando != 0:
			Diagnosticando = 0
			self.set_image("LOGO.jpg")

		if str(self.Ind.toPlainText()) == "":
			QMessageBox.question(self,"Error","Por favor ingrese el tanque a análizar",QMessageBox.Ok)
		else:
			if Diagnosticando == 0:
				try:
					if self.Dependientes.isChecked():
						t = Thread(target=DiagnoFuera,daemon=True,args=(str(self.Ind.toPlainText()),str(self.Dep.toPlainText())))
						t.start()
						Diagnosticando = 1
					else:
						t = Thread(target=DiagnoFuera,daemon=True,args=(str(self.Ind.toPlainText()),""))
						t.start()
						Diagnosticando = 1
				except :
					QMessageBox.question(self,"Error de Archivos","No se encontrol el archivo de Referencia de los tanques \nPor favor ejecute SITACOM",QMessageBox.Ok)
			if Diagnosticando == 1:
				self.set_image("Trabajando.jpg")

	def CambiarAd(self):
		Imagenes = ls("\\ImagenesCorr")
		global Ima
		Ima = Ima + 1
		if Ima == len(Imagenes):
			Ima = 0
		self.set_image("ImagenesCorr\\"+Imagenes[Ima])

	def CambiarAt(self):
		Imagenes = ls("\\ImagenesCorr")
		global Ima
		Ima = Ima - 1
		if Ima < 0:
			Ima = len(Imagenes)-1
		self.set_image("ImagenesCorr\\"+Imagenes[Ima])

#··-··-··-··-··-··-··-··-··-··-··-··-··-··-··-··-··-··-··-··-··-··-··-··-··-··-··#
app = QApplication(sys.argv)
app.setStyle('Fusion')
'''app.setStyle('Fusion')
palette = QtGui.QPalette()
palette.setColor(QtGui.QPalette.Window, QtGui.QColor(53,53,53))
palette.setColor(QtGui.QPalette.WindowText, QtCore.Qt.white)
palette.setColor(QtGui.QPalette.Base, QtGui.QColor(15,15,15))
palette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(53,53,53))
palette.setColor(QtGui.QPalette.ToolTipBase, QtCore.Qt.white)
palette.setColor(QtGui.QPalette.ToolTipText, QtCore.Qt.white)
palette.setColor(QtGui.QPalette.Text, QtCore.Qt.white)
palette.setColor(QtGui.QPalette.Button, QtGui.QColor(53,53,53))
palette.setColor(QtGui.QPalette.ButtonText, QtCore.Qt.white)
palette.setColor(QtGui.QPalette.BrightText, QtCore.Qt.red)
palette.setColor(QtGui.QPalette.Highlight, QtGui.QColor(142,45,197).lighter())
palette.setColor(QtGui.QPalette.HighlightedText, QtCore.Qt.black)
app.setPalette(palette)'''
_ventana = Ventana()
_ventana.show()
app.exec_()
input()