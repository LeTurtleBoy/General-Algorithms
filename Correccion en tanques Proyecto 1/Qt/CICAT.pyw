
import sys, re
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog
from PyQt5 import uic
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import numpy as np
import ctypes
import pandas as pd
import numpy as np
import os
import xlsxwriter as xlrw


Angulo = 0
Pos = True
#Clase heredada de QMainWindow (Constructor de ventanas)
class Ventana(QMainWindow):
 #Método constructor de la clase
	def __init__(self):
  #Iniciar el objeto QMainWindow
		QMainWindow.__init__(self)
		#Cargar la configuración del archivo .ui en el objeto
		uic.loadUi("MainWindow.ui", self)
		self.setWindowTitle("Software de correlación de volumenes para tanques inclinados")
		self.setMinimumSize(1336, 550)
		self.setMaximumSize(1336, 550)
		resolucion = ctypes.windll.user32
		resolucion_ancho = resolucion.GetSystemMetrics(0)
		resolucion_alto = resolucion.GetSystemMetrics(1)
		left = (resolucion_ancho / 2) - (self.frameSize().width() / 2)
		top = (resolucion_alto / 2) - (self.frameSize().height() / 2)
		self.move(left, top)
		qfont = QFont("Arial", 10)
		self.setFont(qfont)
		self.Ingresar.setStyleSheet("font-size: 14px")
		self.Angulo.clicked.connect(self.CalcularAngulo)
		self.Ingresar.clicked.connect(self.CalcularVolumen)
		self.Cargar.clicked.connect(self.CargarArchivo)
		self.Contacto.clicked.connect(self.Contactof)
		self.Recalcular.clicked.connect(self.CalcularTabla)
		self.Ayuda.clicked.connect(self.MensajeAyuda)
	
	def MensajeAyuda(self): 
		QMessageBox.question(self,"Ayuda","El software tiene condiciones necesarias para un correcto funcionamiento:\n1) El sensor principal debe ser ubicado en la parte más cercana posible al centro del tanque.\n2) El sensor secundario debe ser ubicado entre el sensor principal y el extremo del tanque más cercano a este.\n\nPara calcular la nueva tabla de aforo:\n1) Cargar la tabla de aforo actual del tanque a recalcular.\n2) Calcular el ángulo con las medidas obtenidas de los sensores y sus distancias. (No debe introducirse manualmente).\n3) Introducir las medidas entre el sensor principal y el centro del tanque\n4) Presionar \"Recalcular tabla de aforos\" (si ya existe, asegurarse que el archivo esté cerrado)\n\nNotas importantes: Con inclinaciones mayores a 4º, es de gran importancia ubicar el sensor principal a menos de 30 cms del centro, puesto que la tabla de aforos sufrirá cambios importantes.",QMessageBox.Ok)
############################################################################################################################################################################
	def Contactof(self): 
		QMessageBox.question(self,"Contacto","Diseñado por: Ing. Christian David Moreno Uribe\nContacto: Chris.mrn92@gmail.com\n App by: Leturtleboy",QMessageBox.Ok)
############################################################################################################################################################################
	def CargarArchivo(self):  
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()","","All Files (*);;Python Files (*.py)", options=options)
		if fileName:
			Tanque = CargarArchivos(fileName)
			X1 = Tanque[:][1]
			A = np.squeeze(np.asarray(X1))
			X2 = Tanque[:][0]
			B = np.squeeze(np.asarray(X2))
			A1=A[0:70]
			A2=A[:]
			A3=A[130:230]
			B1=B[0:70]
			B2=B[:]
			B3=B[130:230]
			coefs_0a50    =    np.polynomial.polynomial.polyfit(B1,A1,8)
			coefs_50a200  =    np.polynomial.polynomial.polyfit(B2,A2,8)
			coefs_200a230 =    np.polynomial.polynomial.polyfit(B3,A3,8)
			del X1,A,X2,B,A1,A2,A3,B1,B2,B3
			Mat = [coefs_0a50,coefs_50a200,coefs_200a230]
			guardarMatriz(Mat,"CoeficientesAforo.xlsx")
############################################################################################################################################################################
	def CalcularTabla(self):
		Nombre = self.Nombre.text()
		if Nombre == "":
			Nombre = "TablaRecalculada.xlsx"
		else:
			Nombre = str(Nombre)+".xlsx"

		try:
			M1load= pd.read_excel(r"Coeficientes\\CoeficientesAforo.xlsx")
			M1 = M1load.as_matrix()
		except:
			self.Ok.setText("Por favor cargue archivo de aforos")
			return True
		try:
			if os.path.isfile("Coeficientes\\"+Nombre):
				os.remove("Coeficientes\\"+Nombre)
		except:
			self.Ok.setText("Por favor cierre el archivo de tablas")
			return True
    		
		WorkBook = xlrw.Workbook("Coeficientes\\"+Nombre)
		WorkSheet= WorkBook.add_worksheet()
		WorkSheet.write(0, 0, "Altura [cm]")
		WorkSheet.write(0, 1, "Volumen [Gal]")
		WorkSheet.write(0, 2, "Recuerde que algunos valores de volumen en lugares críticos seran incongruentes debido a la inclinación de los tanques")
		row=1
		col=0
		alpha = self.AnguloCalc.text()
		validar = re.match('^[0-9]+([.][0-9]+)?$', alpha, re.I)
		if alpha == "":
			flag = False
			alpha = 0
		elif not validar:
			flag = False
			alpha = 0
		else:
			alpha = float(alpha)
		Beta = self.DisCentro.text()
		validar = re.match('^[0-9]+([.][0-9]+)?$', Beta, re.I)
		if Beta == "":
			Beta = 0
		elif not validar:
			Beta = 0
		else:
			Beta = float(Beta)
		alpha = alpha*np.pi;
		Valor = Beta*np.sin(alpha/180)
		if self.VarGlobalPos.text() == "-":
			Valor = -Valor;
		else:
			Valor = Valor;
		del alpha
		for i in range(231):
			alpha = i + Valor;
			V = [0]*231
			if (alpha <= 0):	
				V[0] = 0;
			elif (alpha<50):
				V[i] = M1[0][8]*alpha**8 + M1[0][7]*alpha**7 + M1[0][6]*alpha**6 + M1[0][5]*alpha**5 + M1[0][4]*alpha**4 + M1[0][3]*alpha**3 + M1[0][2]*alpha**2 + M1[0][1]*alpha + M1[0][0]
			elif ((alpha >= 50)&(alpha < 180)):
				V[i]  = M1[1][8]*alpha**8 +M1[1][7]*alpha**7 + M1[1][6]*alpha**6 + M1[1][5]*alpha**5 + M1[1][4]*alpha**4 + M1[1][3]*alpha**3 + M1[1][2]*alpha**2 + M1[1][1]*alpha + M1[1][0]		
			elif (alpha >= 180):
				V[i]  = M1[2][8]*alpha**8 +M1[2][7]*alpha**7 + M1[2][6]*alpha**6 + M1[2][5]*alpha**5 + M1[2][4]*alpha**4 + M1[2][3]*alpha**3 + M1[2][2]*alpha**2 + M1[2][1]*alpha + M1[2][0]
			if(V[i]<0): V[i] = 0
			if(V[i]<V[i-1]): V[i] = 11970 #corregimos extremos de las aproximaciones
			WorkSheet.write_number(row, 0, i)
			WorkSheet.write_number(row, 1, V[i])
			row += 1
		WorkBook.close()
		self.Ok.setText("Tabla Recalculada")
		return True
############################################################################################################################################################################
	def openFileNamesDialog(self):    
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		files, _ = QFileDialog.getOpenFileNames(self,"QFileDialog.getOpenFileNames()", "","All Files (*);;Python Files (*.py)", options=options)
############################################################################################################################################################################
	def closeEvent(self,event):
		resultado = QMessageBox.question(self,"Salir...","¿Seguro que quieres salir de la aplicación?",QMessageBox.Yes|QMessageBox.No)
		if resultado == QMessageBox.Yes: event.accept()
		else: event.ignore()
############################################################################################################################################################################
	def CalcularAngulo(self):
		global Pos
		global Angulo
		flag = True
		#··············································································#
		Altura1 = self.Altura1.text()
		validar = re.match('^[0-9]+([.][0-9]+)?$', Altura1, re.I)
		if Altura1 == "":
			self.Altura1.setText('0')
			flag = False
			Altura1 = 0
		elif not validar:
			self.Altura1.setText('0')
			flag = False
			Altura1 = 0
		else:
			Altura1 = float(Altura1)
		#··············································································#
		Altura2 = self.Altura2.text()
		validar = re.match('^[0-9]+([.][0-9]+)?$', Altura2, re.I)
		if Altura1 == "":
			self.Altura2.setText('0')
			flag = False
			Altura2 = 0
		elif not validar:
			self.Altura2.setText('0')
			flag = False
			Altura2 = 0
		else:
			Altura2 = float(Altura2)
		#··············································································#
		DisSens = self.DisSens.text()
		validar = re.match('^[0-9]+([.][0-9]+)?$', DisSens, re.I)
		if Altura1 == "":
			self.DisSens.setText('0')
			flag = False
			DisSens = 0
		elif not validar:
			self.DisSens.setText('0')
			flag = False
			DisSens = 0
		else:
			DisSens = float(DisSens)
		#··············································································#
		if (Altura1 >= Altura2):
			Pos = "-"
		else:
			Pos = "+"
		#··············································································#
		a = max(Altura1,Altura2)-min(Altura1,Altura2)
		b = DisSens
		a2 = a*a
		b2 = b*b
		try:
			c = np.max(np.sqrt(a2+b2))
			alpha = np.arcsin(a/c)
			alpha = (alpha * 180 )/np.pi
			alpha = "%.5f" % alpha
			self.VarGlobalPos.setText(str(Pos))
			if (flag):
				Angulo = str(alpha) + "°"
				self.AnguloVis.setText(Angulo)
				self.AnguloCalc.setText(alpha)
			else:
				self.AnguloVis.setText("Por favor corrobore los datos introducidos.")
			return True
		except:
			self.AnguloVis.setText("Por favor corrobore los datos introducidos.")
		return True
############################################################################################################################################################################
	def CalcularVolumen(self):
		#··············································································#
		alpha = self.AnguloCalc.text()
		validar = re.match('^[0-9]+([.][0-9]+)?$', alpha, re.I)
		if alpha == "":
			flag = False
			alpha = 0
		elif not validar:
			flag = False
			alpha = 0
		else:
			alpha = float(alpha)
		#··············································································#
		Beta = self.DisCentro.text()
		validar = re.match('^[0-9]+([.][0-9]+)?$', Beta, re.I)
		if Beta == "":
			Beta = 0
		elif not validar:
			Beta = 0
		else:
			Beta = float(Beta)
		#··············································································#
		alpha = alpha*np.pi;
		Valor = (Beta*np.sin(alpha/180))
		if self.VarGlobalPos.text() == "-":
			Valor = -Valor;
		else:
			Valor = Valor;
		#··············································································#
		Altura1 = self.Altura1.text()
		validar = re.match('^[0-9]+([.][0-9]+)?$', Altura1, re.I)
		if Altura1 == "":
			self.Altura1.setText('0')
			flag = False
			Altura1 = 0
		elif not validar:
			self.Altura1.setText('0')
			flag = False
			Altura1 = 0
		else:
			Altura1 = float(Altura1)
			
		alpha = Altura1 + Valor;
		M1load= pd.read_excel(r"Coeficientes\\CoeficientesAforo.xlsx")
		M1 = M1load.as_matrix()
		if (alpha == 0):
			Volumen =  "0 Galones"
			self.VolVis.setText(Volumen)
			return True		
		if (alpha >= 230):
			alpha = 230
		if (alpha<50):
			V = M1[0][8]*alpha**8 + M1[0][7]*alpha**7 + M1[0][6]*alpha**6 + M1[0][5]*alpha**5 + M1[0][4]*alpha**4 + M1[0][3]*alpha**3 + M1[0][2]*alpha**2 + M1[0][1]*alpha + M1[0][0]
		if ((alpha >= 50)&(alpha < 180)):
			V = M1[1][8]*alpha**8 +M1[1][7]*alpha**7 + M1[1][6]*alpha**6 + M1[1][5]*alpha**5 + M1[1][4]*alpha**4 + M1[1][3]*alpha**3 + M1[1][2]*alpha**2 + M1[1][1]*alpha + M1[1][0]		
		if (alpha >= 180):
			V = M1[2][8]*alpha**8 +M1[2][7]*alpha**7 + M1[2][6]*alpha**6 + M1[2][5]*alpha**5 + M1[2][4]*alpha**4 + M1[2][3]*alpha**3 + M1[2][2]*alpha**2 + M1[2][1]*alpha + M1[2][0]
		Volumen = str(V) + " Galones"
		self.VolVis.setText(Volumen)
		return True
#Instancia para iniciar una aplicación
############################################################################################################################################################################
def CargarArchivos(Archivo):
        M1load= pd.read_excel(Archivo, sheetname=0)
        M1 = M1load.as_matrix()
        return M1.transpose()
############################################################################################################################################################################
def guardarMatriz(data,Nombre):
    if os.path.isfile("Coeficientes\\"+Nombre):
        os.remove("Coeficientes\\"+Nombre)
    WorkBook = xlrw.Workbook("Coeficientes\\"+Nombre)
    WorkSheet= WorkBook.add_worksheet()
    row=1
    col=0
    Relleno = "Coef"
    for x in data:
        for y in x:
            WorkSheet.write(0, col, Relleno+str(col))
            WorkSheet.write_number(row, col, y)
            col+=1
        row += 1
        col = 0
    WorkBook.close()
############################################################################################################################################################################



app = QApplication(sys.argv)
_ventana = Ventana()
_ventana.show()
app.exec_()
#input()


#PyInstaller -w -F --distpath="." Mainwindow.pyw

