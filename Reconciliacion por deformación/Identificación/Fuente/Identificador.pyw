import sys, re
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
import cv2

Aforo = pd.DataFrame()
Descarge = pd.DataFrame()
Ventas = pd.DataFrame()
VentasRef = pd.DataFrame()
Inventario = pd.DataFrame()
fileName = ""
Erno = False
Uso  = True

def MostrarRAM():
	pid = os.getpid()
	py = psutil.Process(pid)
	memoryUse = py.memory_info()[0]/2.**30  # memory use in GB...I think
	memoryUse = memoryUse*1000
	return(memoryUse)

def Cambiar_Estado():
	global Uso
	ti.sleep(1)
	Uso = not(Uso)
	return (Uso)

def ls(a):
	ruta = getcwd() + a
	return [arch.name for arch in scandir(ruta) if arch.is_file()]

def CargarArchivoPesado1():
	global Aforo
	global fileName
	try:
		Aforo = pd.read_excel(fileName,sheet_name='Aforo')
	except:
		1

def CargarArchivoPesado2():
	global Descarge
	global fileName
	try:
		Descarge = pd.read_excel(fileName,sheet_name='Descargue')
	except:
		1

def CargarArchivoPesado3():
	global Inventario
	global fileName
	try:
		Inventario = pd.read_excel(fileName,sheet_name='Inventario')
	except:
		1

def CargarArchivoPesado4():
	global Ventas
	global fileName
	try:
		Ventas = pd.read_excel(fileName,sheet_name='Ventas')
	except:
		1

def CargarArchivoPesado5():
	global VentasRef
	global fileName
	try:
		VentasRef = pd.read_excel(fileName,sheet_name='Surtidor')
	except:
		1

def RealizarProcesamiento():
	global Aforo
	global Descarge
	global Inventario
	global Ventas
	global VentasRef
	TanqueID = [0]*len(Ventas)
	for index, row in Ventas.iterrows():
		Aux = VentasRef.copy()
		Aux = Aux[Aux['Surtidor'] == row['SurtidorID']]
		Aux = Aux[Aux['Cara'] == row['Cara']]
		Aux = Aux[Aux['Manguera'] == row['Manguera']]
		tango = Aux.Tanque.tolist()[0]
		TanqueID[index] = tango
	STan = pd.Series(TanqueID)
	Ventas['TanqueID'] = STan
	if os.path.exists("D") == False:
		os.mkdir("D")
		path = "D"
		ctypes.windll.kernel32.SetFileAttributesW(path, 2)
	if os.path.exists("Datos") == False: 
		os.mkdir("Datos")
		path = "Datos"
		ctypes.windll.kernel32.SetFileAttributesW(path, 2)
	if os.path.exists("DefinitivoDiario") == False:
		os.mkdir("DefinitivoDiario")
		path = "DefinitivoDiario"
		ctypes.windll.kernel32.SetFileAttributesW(path, 2)
	if os.path.exists("Fechas") == False:
		os.mkdir("Fechas")
		path = "Fechas"
		ctypes.windll.kernel32.SetFileAttributesW(path, 2)
	if os.path.exists("Tanques") == False:
		os.mkdir("Tanques")
		path = "Tanques"
		ctypes.windll.kernel32.SetFileAttributesW(path, 2)	
	GrupoInventario = Inventario.groupby('TanqueID')
	for NombreTanque, Tanque in GrupoInventario:
		Tanque.to_excel('Tanques\\Inventario'+str(NombreTanque)+'.xlsx',index =False)
	GrupoAforo = Aforo.groupby('TanqueID')
	for NombreTanque, Tanque in GrupoAforo:
		Tanque.to_excel('Tanques\\Aforo'+str(NombreTanque)+'.xlsx',index =False)
	GrupoDescarge = Descarge.groupby('TanqueID')
	for NombreTanque, Tanque in GrupoDescarge:
		Tanque.to_excel('Tanques\\Descarge'+str(NombreTanque)+'.xlsx',index =False)
	GrupoVenta = Ventas.groupby('TanqueID')
	for NombreTanque, Tanque in GrupoVenta:
		Tanque.to_excel('Tanques\\Ventas'+str(NombreTanque)+'.xlsx',index =False)
	NumeroTanques = len(GrupoInventario)
	NombresTanques = [0]*NumeroTanques
	i = 0
	for NombreTanque, Tanque in GrupoInventario:
		NombresTanques[i] = NombreTanque
		i = i+1
	pd.DataFrame(NombresTanques).to_excel(str("refTanques.xlsx"))
	
class Ventana(QMainWindow):
	def __init__(self):
		event = threading.Event()
		QMainWindow.__init__(self)
		uic.loadUi("identificacion.ui", self)
		self.setWindowTitle("SITACOM")
		QApplication.processEvents()
		resolucion = ctypes.windll.user32
		resolucion_ancho = resolucion.GetSystemMetrics(0)
		resolucion_alto = resolucion.GetSystemMetrics(1)
		left = (resolucion_ancho / 2) - (self.frameSize().width() / 2)
		top = (resolucion_alto / 2) - (self.frameSize().height() / 2)
		self.move(left, top)
		qfont = QFont("Arial", 10)
		self.setGeometry(left, top, 500, 250)
		self.Barra.setValue(0)
		self.Ram.display(0)
		self.Cargar.clicked.connect(self.CargarArchivo)
		self.Procesar.clicked.connect(self.ProcesarDatos)
		self.Ayuda.clicked.connect(self.MostrarAyuda)

	def MostrarAyuda(self):
		plt.figure(2)
		Img1 = cv2.imread("Ayuda\\P1A1.png")
		plt.axis("off")
		figManager = plt.get_current_fig_manager()
		figManager.window.showMaximized()
		plt.imshow(cv2.cvtColor(Img1, cv2.COLOR_BGR2RGB))
		plt.show()
		resultado = QMessageBox.question(self,"Menu de Ayuda.","El boton de cargar le permite ingresar al software el archivo base\n\nEs necesario que el documento cumpla con el formato estandar.\n ¿Desea ver cual es el formato?",QMessageBox.Yes|QMessageBox.No)
		if (resultado == QMessageBox.Yes):
					plt.figure(1)
					Img1 = cv2.imread("Ayuda\\P1A2.png")
					plt.axis("off")
					figManager = plt.get_current_fig_manager()
					figManager.window.showMaximized()
					plt.imshow(cv2.cvtColor(Img1, cv2.COLOR_BGR2RGB))
					plt.show()

	def closeEvent(self,event):
		resultado = QMessageBox.question(self,"Salir...","¿Seguro que quieres salir de la aplicación?",QMessageBox.Yes|QMessageBox.No)
		if (resultado == QMessageBox.Yes) & (threading.active_count() == 1):
			event.accept()
		else: 
			event.ignore()
	
	def run(self):
			A = MostrarRAM()
			ti.sleep(0.1)
			N = threading.active_count()
			self.Barra.setValue(20*(-(N-7)))
			self.Ram.display(float(A))
			if N > 2:
				self.run()
	def run2(self):
			
			N = threading.active_count()
			self.Barra.setValue(0)
			self.Cargar.setEnabled(False)
			self.Procesar.setEnabled(False)
			if N > 2:
				A = Cambiar_Estado()
				if A:
					self.Procesar.setStyleSheet("background-color: yellow")
				else:
					self.Procesar.setStyleSheet("background-color: orange")
				#self.Ram.display(MostrarRAM())
				self.run2()
			else:
				self.Procesar.setStyleSheet("background-color: green")
				self.Cargar.setEnabled(True)
				self.Procesar.setEnabled(True)
				self.Barra.setValue(100)

	def CargarArchivo(self):
			options = QFileDialog.Options()
			options |= QFileDialog.DontUseNativeDialog
			global fileName
			fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()","","Archivos de Excel (*.xls , *.xlsx)", options=options)
			if fileName == "":
				1
			else:
				subproceso1 = Thread(target=CargarArchivoPesado1, args=())
				subproceso2 = Thread(target=CargarArchivoPesado2, args=())
				subproceso3 = Thread(target=CargarArchivoPesado3, args=())
				subproceso4 = Thread(target=CargarArchivoPesado4, args=())
				subproceso5 = Thread(target=CargarArchivoPesado5, args=())
				subproceso1.start()
				subproceso2.start()
				subproceso3.start()
				subproceso4.start()
				subproceso5.start()
				t = Thread(target=self.run,daemon=True)
				t.start()
				self.Cargar.setEnabled(False)

	def ProcesarDatos(self):
		acum = 100-20*((VentasRef.empty + Ventas.empty) + (Descarge.empty + Inventario.empty)+Aforo.empty)
		self.Barra.setValue(acum)
		if (((VentasRef.empty | Ventas.empty) | (Descarge.empty | Inventario.empty))| Aforo.empty):
			self.Cargar.setStyleSheet("background-color: red")
			acum = 1
			if acum == 0:
				QMessageBox.question(self,"Error en carga de archivo","Primero debes cargar el archivo base",QMessageBox.Ok)
			else:
				if VentasRef.empty:
					QMessageBox.question(self,"Error en Referencias","No se encontrol el archivo de Referencia de los distribuidores para las ventas",QMessageBox.Ok)
				if Ventas.empty:
					QMessageBox.question(self,"Error en Ventas","No se encontrol el archivo de Ventas",QMessageBox.Ok)
				if Inventario.empty:
					QMessageBox.question(self,"Error en Inventario","No se encontrol el archivo de Inventarios",QMessageBox.Ok)
				if Aforo.empty:
					QMessageBox.question(self,"Error en Aforo","No se encontrol el archivo de Aforos",QMessageBox.Ok)
				if Descarge.empty:
					QMessageBox.question(self,"Error en Descarge","No se encontrol el archivo de Descargues",QMessageBox.Ok)
		else:
			self.Cargar.setStyleSheet("background-color: green")
			t = Thread(target=RealizarProcesamiento,daemon=True)
			QMessageBox.question(self,"Procesando","Cuando Los botones se activen el sistema ha terminado de procesar",QMessageBox.Ok)
			t.start()
			self.Procesar.setEnabled(False)
			t = Thread(target=self.run2,daemon=True)
			t.start()

app = QApplication(sys.argv)
app.setStyle('Fusion')
#palette = QtGui.QPalette()
'''palette.setColor(QtGui.QPalette.Window, QtGui.QColor(53,53,53))
palette.setColor(QtGui.QPalette.WindowText, QtCore.Qt.white)
palette.setColor(QtGui.QPalette.Base, QtGui.QColor(15,15,15))
palette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(53,53,53))
palette.setColor(QtGui.QPalette.ToolTipBase, QtCore.Qt.white)
palette.setColor(QtGui.QPalette.ToolTipText, QtCore.Qt.white)
palette.setColor(QtGui.QPalette.Text, QtCore.Qt.white)
palette.setColor(QtGui.QPalette.BrightText, QtCore.Qt.red)
palette.setColor(QtGui.QPalette.Highlight, QtGui.QColor(32, 155, 44).lighter())
palette.setColor(QtGui.QPalette.HighlightedText, QtCore.Qt.black)
app.setPalette(palette)'''
_ventana = Ventana()
_ventana.show()
app.exec_()
input()
