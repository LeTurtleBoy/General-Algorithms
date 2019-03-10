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
Imagenes = []
Ima = 0
Uso = True

def DiagnoFuera():
			global Diagnosticando
			try:
				NombresTanques = pd.read_excel("refTanques.xlsx")[0].tolist()
				NumeroTanques = len(NombresTanques)
				if os.path.exists("DefinitivoDiario") == False:
					os.mkdir("DefinitivoDiario")
					path = "DefinitivoDiario"
					ctypes.windll.kernel32.SetFileAttributesW(path, 2)
				Lista = [0]*NumeroTanques
				Elementos = ls("\\Tanques")
				for i in range(NumeroTanques):
					Lista[i] = [Elementos for Elementos in Elementos if Elementos.endswith(str(NombresTanques[i])+'.xlsx')]
				Pendertuga = -1
				for file2 in Lista:
					Bandera2 = 0
					Pendertuga=Pendertuga+1
					for file in file2:
						if 'Descarge' in file:
							Bandera2 = Bandera2 +1
							Descarge = pd.read_excel('Tanques\\'+file)
							Descarge = Descarge[['FechaInicial','FechaFinal','AlturaInicial','AlturaFinal','VolInicial','VolFinal']]
							FechasDescargef = Descarge['FechaFinal']
							FSf	= [0]*(len(FechasDescargef))
							DiaSf = [0]*(len(FechasDescargef))
							HoraSf = [0]*(len(FechasDescargef))
							DSf  = [0]*(len(FechasDescargef))
							MSf  = [0]*(len(FechasDescargef))
							ASf  = [0]*(len(FechasDescargef))
							HSf  = [0]*(len(FechasDescargef))
							MiSf  = [0]*(len(FechasDescargef))
							SSf  = [0]*(len(FechasDescargef))
							FechasDescargei = Descarge['FechaInicial']
							FSi	= [0]*(len(FechasDescargei))
							DiaSi = [0]*(len(FechasDescargei))
							HoraSi = [0]*(len(FechasDescargei))
							DSi  = [0]*(len(FechasDescargei))
							MSi  = [0]*(len(FechasDescargei))
							ASi  = [0]*(len(FechasDescargei))
							HSi  = [0]*(len(FechasDescargei))
							MiSi  = [0]*(len(FechasDescargei))
							SSi  = [0]*(len(FechasDescargei))
							j = 0
							for koko in FechasDescargef:
								FSf[j] = koko.split(" ")
								DiaSf[j] = FSf[j][0].split("-")
								HoraSf[j]= FSf[j][1].replace(".",":")
								HoraSf[j]= HoraSf[j].split(":")
								DiaSf[j][0] = int(DiaSf[j][0])
								DiaSf[j][1] = int(DiaSf[j][1])
								DiaSf[j][2] = int(DiaSf[j][2])
								HoraSf[j][0] = int(HoraSf[j][0])
								HoraSf[j][1] = int(HoraSf[j][1])
								HoraSf[j][2] = int(HoraSf[j][2])
								DSf[j] = int(DiaSf[j][2])
								MSf[j] = int(DiaSf[j][1])
								ASf[j] = int(DiaSf[j][0])
								HSf[j] = int(HoraSf[j][0])
								MiSf[j] = int(HoraSf[j][1])
								SSf[j] = int(HoraSf[j][2])
								j = j+1
							j = 0
							for koko in FechasDescargei:
								FSi[j] = koko.split(" ")
								DiaSi[j] = FSi[j][0].split("-")
								HoraSi[j]= FSi[j][1].replace(".",":")
								HoraSi[j]= HoraSi[j].split(":")
								DiaSi[j][0] = int(DiaSi[j][0])
								DiaSi[j][1] = int(DiaSi[j][1])
								DiaSi[j][2] = int(DiaSi[j][2])
								HoraSi[j][0] = int(HoraSi[j][0])
								HoraSi[j][1] = int(HoraSi[j][1])
								HoraSi[j][2] = int(HoraSi[j][2])
								DSi[j] = int(DiaSi[j][2])
								MSi[j] = int(DiaSi[j][1])
								ASi[j] = int(DiaSi[j][0])
								HSi[j] = int(HoraSi[j][0])
								MiSi[j] = int(HoraSi[j][1])
								SSi[j] = int(HoraSi[j][2])
								j = j+1
							Descarge['DiaFinalDescarge'] = DSf
							Descarge['MesFinalDescarge'] = MSf
							Descarge['AnhoFinalDescarge'] = ASf
							Descarge['HoraFinalDescarge'] = HSf
							Descarge['MinFinalDescarge'] = MiSf
							Descarge['SegFinalDescarge'] = SSf
							Descarge['DiaInicialDescarge'] = DSi
							Descarge['MesInicialDescarge'] = MSi
							Descarge['AnhoInicialDescarge'] = ASi
							Descarge['HoraInicialDescarge'] = HSi
							Descarge['MinInicialDescarge'] = MiSi
							Descarge['SegInicialDescarge'] = SSi
							InicioDescargeFechaUniversal = np.array(MiSi)+60*np.array(HSi)+60*24*np.array(DSi)+31*24*60*np.array(MSi)
							FinalDescargeFechaUniversal  = np.array(MiSf)+60*np.array(HSf)+60*24*np.array(DSf)+31*24*60*np.array(MSf)
							Descarge['InicioFechaUniversal'] = InicioDescargeFechaUniversal
							Descarge['FinalFechaUniversal'] = FinalDescargeFechaUniversal
							Descarge.to_excel('Fechas\\Fechas'+file)
						if 'Inventario' in file:
							Bandera2 = Bandera2 +1
							Inventario = pd.read_excel('Tanques\\'+file)
							Inventario = Inventario[['Fecha','Altura','Volumen']]
							Fechasinventario =  Inventario['Fecha']
							FI	= [0]*(len(Fechasinventario))
							DiaI  = [0]*(len(Fechasinventario))
							HoraI = [0]*(len(Fechasinventario))
							DI  = [0]*(len(Fechasinventario))
							MI  = [0]*(len(Fechasinventario))
							AI  = [0]*(len(Fechasinventario))
							HI  = [0]*(len(Fechasinventario))
							MiI  = [0]*(len(Fechasinventario))
							SI  = [0]*(len(Fechasinventario))
							j = 0
							for koko in Fechasinventario:
								FI[j] = koko.split(" ")
								DiaI[j] = FI[j][0].split("-")
								HoraI[j]= FI[j][1].replace(".",":")
								HoraI[j]= HoraI[j].split(":")
								DiaI[j][0] = int(DiaI[j][0])
								DiaI[j][1] = int(DiaI[j][1])
								DiaI[j][2] = int(DiaI[j][2])
								HoraI[j][0] = int(HoraI[j][0])
								HoraI[j][1] = int(HoraI[j][1])
								HoraI[j][2] = int(HoraI[j][2])
								DI[j] = int(DiaI[j][2])
								MI[j] = int(DiaI[j][1])
								AI[j] = int(DiaI[j][0])
								HI[j] = int(HoraI[j][0])
								MiI[j] = int(HoraI[j][1])
								SI[j] = int(HoraI[j][2])
								j = j+1
							Inventario['DiaInventario'] = DI
							Inventario['MesInventario'] = MI
							Inventario['AnhoInventario'] = AI
							Inventario['HoraInventario'] = HI
							Inventario['MinInventario'] = MiI
							Inventario['SegInventario'] = SI
							FechaUniversal = np.array(MiI) + 60*np.array(HI)+60*24*np.array(DI)+31*24*60*np.array(MI)	
							Inventario['FechaUniversal'] = FechaUniversal
							Inventario.to_excel('Fechas\\Fechas'+file)
						if 'Aforo' in file:
							Bandera2 = Bandera2 +1
							Aforo = pd.read_excel('Tanques\\'+file)
							Aforo = Aforo[['Medida','Galones']]
						if 'Ventas' in file:
							Bandera2 = Bandera2 +1
							Ventas = pd.read_excel('Tanques\\'+file)
							Ventas = Ventas[['Fecha','Volumen.1']]
							FechasVenta =  Ventas['Fecha']
							FV	= [0]*(len(FechasVenta))
							DiaV  = [0]*(len(FechasVenta))
							HoraV = [0]*(len(FechasVenta))
							DV  = [0]*(len(FechasVenta))
							MV  = [0]*(len(FechasVenta))
							AV  = [0]*(len(FechasVenta))
							HV  = [0]*(len(FechasVenta))
							MiV  = [0]*(len(FechasVenta))
							SV  = [0]*(len(FechasVenta))
							j = 0
							for koko in FechasVenta:
								FV[j] = koko.split(" ")
								DiaV[j] = FV[j][0].split("-")
								HoraV[j]= FV[j][1].replace(".",":")
								HoraV[j]= HoraV[j].split(":")
								DiaV[j][0] = int(DiaV[j][0])
								DiaV[j][1] = int(DiaV[j][1])
								DiaV[j][2] = int(DiaV[j][2])
								HoraV[j][0] = int(HoraV[j][0])
								HoraV[j][1] = int(HoraV[j][1])
								HoraV[j][2] = int(HoraV[j][2])
								DV[j] = int(DiaV[j][2])
								MV[j] = int(DiaV[j][1])
								AV[j] = int(DiaV[j][0])
								HV[j] = int(HoraV[j][0])
								MiV[j] = int(HoraV[j][1])
								SV[j] = int(HoraV[j][2])
								j = j+1
							Ventas['DiaVenta'] = DV
							Ventas['MesVenta'] = MV
							Ventas['AnhoVenta'] = AV
							Ventas['HoraVenta'] = HV
							Ventas['MinVenta'] = MiV
							Ventas['SegVenta'] = SV
							FechaUniversal = np.array(MiV)+ 60*np.array(HV)+60*24*np.array(DV)+31*24*60*np.array(MV)
							Ventas['FechaUniversal'] = FechaUniversal
							Ventas.to_excel('Fechas\\Fechas'+file)
						meme = 0
						if (Bandera2 == 4):
							G1 = Ventas.groupby(['DiaVenta'])
							VolumenesVenta=[0]*len(G1)
							for Nombre, DfGrupo in G1:
								VolumenesVenta[meme] = [Nombre,np.sum(DfGrupo['Volumen.1'])]
								meme =  meme+1
							G2 = Inventario.groupby(['DiaInventario'])
							VolumenesInventario=[0]*len(G2)
							meme = 0
							for Nombre, DfGrupo in G2:
								Vol1 = DfGrupo['Volumen'].tolist()
								Vol2 = Vol1[0]
								Vol1 = Vol1[len(Vol1)-1]
								VolumenesInventario[meme] = [Nombre,Vol1-Vol2]
								meme = meme + 1
							G3 = Descarge.groupby(['DiaFinalDescarge'])
							VolumenesDescarge=[0]*len(G3)
							meme = 0
							for Nombre, DfGrupo in G3:
								if len(DfGrupo['VolInicial'].tolist()) > 1:
									Vi = np.sum(DfGrupo['VolInicial'].tolist())
									Vf = np.sum(DfGrupo['VolFinal'].tolist())
								else:
									Vi = DfGrupo['VolInicial'].tolist()[0]
									Vf = DfGrupo['VolFinal'].tolist()[0]
								VolumenesDescarge[meme] = [Nombre,Vf-Vi]
								meme = meme + 1
							pd.DataFrame(VolumenesDescarge).to_excel(str("DefinitivoDiario\\"+"Des"+str(NombresTanques[Pendertuga])+".xlsx"))
							pd.DataFrame(VolumenesInventario).to_excel(str("DefinitivoDiario\\"+"Inv"+str(NombresTanques[Pendertuga])+".xlsx"))
							pd.DataFrame(VolumenesVenta).to_excel(str("DefinitivoDiario\\"+"Ven"+str(NombresTanques[Pendertuga])+".xlsx"))
						if (Bandera2 == 3):
							G2 = Inventario.groupby(['DiaInventario'])
							VolumenesInventario=[0]*len(G2)
							meme = 0
							for Nombre, DfGrupo in G2:
								Vol1 = DfGrupo['Volumen'].tolist()
								Vol2 = Vol1[0]
								Vol1 = Vol1[len(Vol1)-1]
								VolumenesInventario[meme] = [Nombre,Vol1-Vol2]
								meme = meme + 1
							G3 = Descarge.groupby(['DiaFinalDescarge'])
							VolumenesDescarge=[0]*len(G3)
							meme = 0
							for Nombre, DfGrupo in G3:
								if len(DfGrupo['VolInicial'].tolist()) > 1:
									Vi = np.sum(DfGrupo['VolInicial'].tolist())
									Vf = np.sum(DfGrupo['VolFinal'].tolist())
								else:
									Vi = DfGrupo['VolInicial'].tolist()[0]
									Vf = DfGrupo['VolFinal'].tolist()[0]
								VolumenesDescarge[meme] = [Nombre,Vf-Vi]
								meme = meme + 1
							pd.DataFrame(VolumenesDescarge).to_excel(str("DefinitivoDiario\\"+"Des"+str(NombresTanques[Pendertuga])+".xlsx"))
							pd.DataFrame(VolumenesInventario).to_excel(str("DefinitivoDiario\\"+"Inv"+str(NombresTanques[Pendertuga])+".xlsx"))


				Tanques = pd.read_excel("refTanques.xlsx")
				Tanques = Tanques[0].tolist()
				Referencias = [0]*len(Tanques)
				Elementos = ls('\\DefinitivoDiario')
				if os.path.exists("Imagenes") == False:
					os.mkdir("Imagenes")
					path = "Imagenes"
					ctypes.windll.kernel32.SetFileAttributesW(path, 2)
				for i in range(len(Tanques)):
					Referencias[i] = [Elementos for Elementos in Elementos if Elementos.endswith(str(Tanques[i])+'.xlsx')]
					if (len(Referencias[i]) == 3):
						Des = pd.read_excel("DefinitivoDiario\\"+Referencias[i][0],)
						Inv = pd.read_excel("DefinitivoDiario\\"+Referencias[i][1])
						Ven = pd.read_excel("DefinitivoDiario\\"+Referencias[i][2])
						Des.rename(columns={0: 'DiaD',1: 'VolD'}, inplace=True)
						Des.index = Des.DiaD
						Inv.rename(columns={0: 'DiaI',1: 'VolI'}, inplace=True)
						Inv.index = Inv.DiaI
						Ven.rename(columns={0: 'DiaV',1: 'VolV'}, inplace=True)
						Ven.index = Ven.DiaV
						result = pd.concat([Ven, Inv,Des], axis=1)
						result = result.fillna(0)
						result = result[['VolV','VolI','VolD']]
						cuba = [0,0]
						Valores = [cuba]*len(result.index)
						V1 = [0]*len(result.index)
						V2 = [0]*len(result.index)
						Pa = -1
						resultDia = pd.DataFrame(np.array(result['VolI'].tolist())-np.array(result['VolD'].tolist())+np.array(result['VolV'].tolist()))
						resultDia["Index"] = result.index
						resultDia.to_excel("D\\DataC"+str(Tanques[i])+".xlsx")
						resultDia.index = result.index
						result.to_excel("D\\Data"+str(Tanques[i])+".xlsx")
					if (len(Referencias[i]) == 2):
						Des = pd.read_excel("DefinitivoDiario\\"+Referencias[i][0],)
						Inv = pd.read_excel("DefinitivoDiario\\"+Referencias[i][1])
						Des.rename(columns={0: 'DiaD',1: 'VolD'}, inplace=True)
						Des.index = Des.DiaD
						Inv.rename(columns={0: 'DiaI',1: 'VolI'}, inplace=True)
						Inv.index = Inv.DiaI
						result = pd.concat([Inv,Des], axis=1)
						result = result.fillna(0)
						result = result[['VolI','VolD']]
						cuba = [0,0]
						Valores = [cuba]*len(result.index)
						V1 = [0]*len(result.index)
						V2 = [0]*len(result.index)
						Pa = -1
						resultDia = pd.DataFrame(np.array(result['VolI'].tolist())-np.array(result['VolD'].tolist()))
						resultDia["Index"] = result.index
						resultDia.index = result.index
						resultDia.to_excel("D\\DataC"+str(Tanques[i])+".xlsx")
						result.to_excel("D\\Data"+str(Tanques[i])+".xlsx")
				Diagnosticando = 2
			except:
				return 0

def ls(a):
	ruta = getcwd() + a
	return [arch.name for arch in scandir(ruta) if arch.is_file()]

def Cambiar_Estado():
	global Uso
	ti.sleep(0.5)
	Uso = not(Uso)
	return (Uso)

class Ventana(QMainWindow):	
	def __init__(self):
		event = threading.Event()
		QMainWindow.__init__(self)
		uic.loadUi("Diagnostico.ui", self)
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
		self.set_image("LOGO.jpg")
		self.Diagnistico.clicked.connect(self.Diagnosticar)
		self.Graficar.clicked.connect(self.GraficarTanques)
		self.Dependientes.setChecked(False)
		self.Dependientes.clicked.connect(self.EnableBabe)
		self.Ind.setEnabled(False)
		self.Dep.setEnabled(False)
		self.Atras.setEnabled(False)
		self.Adelante.setEnabled(False)
		self.Atras.clicked.connect(self.CambiarAt)
		self.Adelante.clicked.connect(self.CambiarAd)
		self.Errores.clicked.connect(self.Deteccion)
		self.Ayuda.clicked.connect(self.MostrarAyuda)
		self.Graficar.setEnabled(False)

	def MostrarAyuda(self):
		QMessageBox.question(self,"Menu de Ayuda.","ORDEN DE USO:\n 1. Indicar si hay dependencia y especificar los tanques.\n 2. Diagnosticar  \n 3. Graficar \n 4. Detectar Errores",QMessageBox.Ok)
		plt.figure(2)
		Img1 = cv2.imread("Ayuda\\P2A1.png")
		plt.axis("off")
		figManager = plt.get_current_fig_manager()
		figManager.window.showMaximized()
		plt.imshow(cv2.cvtColor(Img1, cv2.COLOR_BGR2RGB))
		plt.show()
		resultado = QMessageBox.question(self,"Menu de Ayuda.","Indicaciones especiales:\n - Cuando un par de tanques son dependientes, el independiente\nes el tanque desde el cual se hacen las ventas.\n - Los nombres de los tanques deben ser las referencias a el TanqueID\n",QMessageBox.Ok)

	def EnableBabe(self):
		if self.Dependientes.isChecked():
			self.Ind.setEnabled(True)
			self.Dep.setEnabled(True)
		else:
			self.Ind.setEnabled(False)
			self.Dep.setEnabled(False)

	def set_image(self, filename):
		pixmap = QPixmap(filename)
		pic = self.Imagenes
		pic.setScaledContents(True)
		pic.setPixmap(pixmap)

	def closeEvent(self,event):
		resultado = QMessageBox.question(self,"Salir...","¿Seguro que quieres salir de la aplicación?",QMessageBox.Yes|QMessageBox.No)
		if (resultado == QMessageBox.Yes) & (threading.active_count() == 1):
			event.accept()
		else: 
			event.ignore()

	def Esperar(self):
		global Diagnosticando
		ti.sleep(1)
		A = Cambiar_Estado()
		if A:
			self.Diagnistico.setStyleSheet("background-color: yellow")
		else:
			self.Diagnistico.setStyleSheet("background-color: orange")
		if Diagnosticando == 2:
			self.Diagnosticar()
			self.Diagnistico.setStyleSheet("background-color: green")
		else:
			self.Esperar()

	def Diagnosticar(self):
		global Diagnosticando
		try:
			NombresTanques = pd.read_excel("refTanques.xlsx")[0].tolist()
			if Diagnosticando == 0:
				try:
					t = Thread(target=DiagnoFuera,daemon=True)
					t.start()
					Diagnosticando = 1
				except error:
					1
					QMessageBox.question(self,"Error de Archivos","No se encontrol el archivo de Referencia de los tanques \nPor favor ejecute SITACOM",QMessageBox.Ok)
			if Diagnosticando == 1:
				self.set_image("Trabajando.jpg")
				t = Thread(target=self.Esperar,daemon=True)
				t.start()
			if Diagnosticando == 2:
				self.set_image("LOGO.jpg")
				self.Graficar.setEnabled(True)
		except:
			QMessageBox.question(self,"Error de Archivos","No se encontrol el archivo de Referencia de los tanques \nPor favor ejecute SITACOM",QMessageBox.Ok)

	def GraficarTanques(self):
		self.set_image("LOGO.jpg")
		self.Atras.setEnabled(False)
		self.Adelante.setEnabled(False)
		try:
			shutil.rmtree('Imagenes')
			shutil.rmtree('Final')
		except:
			1
		if os.path.exists("Imagenes") == False: 
			os.mkdir("Imagenes")
			path = "Imagenes"
			ctypes.windll.kernel32.SetFileAttributesW(path, 2)
		if os.path.exists("Final") == False: 
			os.mkdir("Final")
			path = "Final"
			ctypes.windll.kernel32.SetFileAttributesW(path, 2)

		NombresTanques = pd.read_excel("refTanques.xlsx")[0].tolist()
		NumeroTanques = len(NombresTanques)
		Lista = [0]*NumeroTanques
		Elementos = ls("\\D")
		for i in range(NumeroTanques):
			Lista[i] = [Elementos for Elementos in Elementos if Elementos.endswith("C"+str(NombresTanques[i])+'.xlsx')]
		if self.Dependientes.isChecked():
			Dep = []
			Ind = []
			BandGraf = 0
			for i in range(NumeroTanques):
				Normal = 0
				if (str(NombresTanques[i]) == str(self.Dep.toPlainText())):
					Dep = pd.read_excel("D\\"+Lista[i][0])
					Dep = Dep[0].tolist()
				else:
					if (str(NombresTanques[i]) == str(self.Ind.toPlainText())):
						Ind = pd.read_excel("D\\"+Lista[i][0])
						xi = Ind["Index"].tolist()
						Ind = Ind[0].tolist()
					else:
						Normal = pd.read_excel("D\\"+Lista[i][0])
						x = Normal["Index"].tolist()
						Normal = Normal[0].tolist()
						Normal = list(Normal)
						x = list(x)
						del Normal[0],x[0]
						plt.ylabel("Galones \"Extra\" ")
						plt.xlabel("Dia")
						plt.xticks(x)
						plt.rc('axes', axisbelow=True)
						plt.grid(alpha = 0.5)
						plt.title("Tanque " + str(NombresTanques[i]))
						plt.bar(x,Normal)
						if os.path.exists("Imagenes") == False: 
							os.mkdir("Imagenes")
							path = "Imagenes"
							ctypes.windll.kernel32.SetFileAttributesW(path, 2)
						plt.savefig('Imagenes\\Tanque'+str(NombresTanques[i])+'.tiff', format='tiff', dpi=600)
						plt.figure()
						Df = pd.DataFrame(Normal)
						Df.index = x
						Df.to_excel("Final\\"+Lista[i][0])
				if (((Dep != []) & (Ind != [])) & (BandGraf == 0)):
					BandGraf = 1
					plt.ylabel("Galones \"Extra\" ")
					plt.xlabel("Dia")
					plt.rc('axes', axisbelow=True)
					plt.grid(alpha = 0.5)
					plt.title(str(self.Ind.toPlainText()) +"_Dependiente_de"+ str(self.Dep.toPlainText()))
					X1 = np.array(Ind)
					X2 = np.array(Dep)
					X3 = X1+X2
					X3 = list(X3)
					xi = list(xi)
					del X3[0],xi[0]
					plt.bar(xi,X3)
					plt.xticks(xi)
					Df = pd.DataFrame(X3)
					Df.index = xi
					if os.path.exists("Imagenes") == False: 
						os.mkdir("Imagenes")
						path = "Imagenes"
						ctypes.windll.kernel32.SetFileAttributesW(path, 2)
					plt.savefig('Imagenes\\Tanques'+str(self.Ind.toPlainText()) +"_Dependiente_de"+ str(self.Dep.toPlainText())+'.tiff', format='tiff', dpi=600)
					plt.figure()
					Df.to_excel("Final\\"+str(self.Ind.toPlainText()) +"_Dependiente_de_"+ str(self.Dep.toPlainText())+'.xlsx')

		else:
			for i in range(NumeroTanques):
				Normal = pd.read_excel("D\\"+Lista[i][0])
				x = Normal["Index"].tolist()
				x = list(x)
				Normal = Normal[0].tolist()
				del Normal[0],x[0]
				plt.ylabel("Galones \"Extra\" ")
				plt.xlabel("Dia")
				plt.xticks(x)
				Df = pd.DataFrame(Normal)
				Df.index = x
				Df.to_excel("Final\\"+Lista[i][0])
				plt.rc('axes', axisbelow=True)
				plt.grid(alpha = 0.5)
				plt.title("Tanque " + str(NombresTanques[i]))
				plt.bar(x,Normal)
				if os.path.exists("Imagenes") == False: 
						os.mkdir("Imagenes")
						path = "Imagenes"
						ctypes.windll.kernel32.SetFileAttributesW(path, 2)
				plt.savefig('Imagenes\\Tanque'+str(NombresTanques[i])+'.tiff', format='tiff', dpi=600)
				plt.figure()
		self.Atras.setEnabled(True)
		self.Adelante.setEnabled(True)
		global Imagenes
		global ima
		Ima = 0
		Imagenes = ls("\\Imagenes")

	def CambiarAd(self):
		Imagenes = ls("\\Imagenes")
		global Ima
		Ima = Ima + 1
		if Ima == len(Imagenes):
			Ima = 0
		self.set_image("Imagenes\\"+Imagenes[Ima])

	def CambiarAt(self):
		Imagenes = ls("\\Imagenes")
		global Ima
		Ima = Ima - 1
		if Ima < 0:
			Ima = len(Imagenes)-1
		self.set_image("Imagenes\\"+Imagenes[Ima])

	def Deteccion(self):
		try:
			Datos = ls("\\Final")
			Elementos = [0]*len(Datos)
			for i in range(len(Datos)):
				kha = pd.read_excel("Final\\"+Datos[i])
				kha = np.abs(np.array(kha[0].tolist()))
				Elementos[i] = np.mean(kha)
			i = -1
			for E in Elementos:
				i = i +1
				E = int(E)
				if E > 80:
					resultado = QMessageBox.question(self,"Error En Tanque","Tenemos un error en el tanque "+str(Datos[i]),QMessageBox.Ok)

		except:
			resultado = QMessageBox.question(self,"Error En Software","Tenemos un error detectando los tanques",QMessageBox.Ok)

app = QApplication(sys.argv)
app.setStyle('Fusion')
'''
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

