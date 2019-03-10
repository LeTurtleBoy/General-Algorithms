#estructuras.py

class Producto():
	"""docstring for producto"""
	def __init__(self):
		self.Nombre;

class Manguera():
	"""docstring for Manguera"""
	def __init__(self):
		self.Posicion
		self.NumManguera
		self.Producto = Producto()
		self.ppu = [0]*5
		self.totalesDV = [0]*24

class Posicion():
	def __init__(self):
		self.Posicion
		self.Cara
		self.NumeroComunicacion
		self.Mangueras = [Manguera()]*3
		self.estado

class Surtidor(): 
	def __init__(self):
		super(surtidor, self).__init__()
		self.PosImprimir.
		self.Posiciones = [Posicion()]*4
		self.Dir = [0]*4;
		self.Version = 0
		self.DecimalesDin = 0
		self.DecimalesVol = 0
		self.DecimalesPpu = 0
		self.okconfinicial = 0
		self.tiposurtidor = 0
		self.ppux10 = 0
		self.placa_obl = 0
		self.version_fuel= [0]*4
		self.preset_rapido = [0]*4

class Turno(): 
	"""
	docstring for turno
	"""
	def __init__(self):
		super(turno, self).__init__()
		self.estado = [0]*2
		self.tipo_id = [0]*2
		self.usuario = [""]*2 # maximo 20 bytes
		self.password = [""]*2 # maximo 11 bytes
		self.fecha = [[0]*6]*2
		self.fecha_anterior = [[0]*6]*2
		self.aceptado = [0]*2
		self.cedula = [[0]*10]*2 
		self.turno_acumulado_cargado = 0
		self.pidiendo_id_turno  = [0]*2
		self.peticion_cierre   = [0]*2
		self.programando_venta  = [0]*2 
		self.apertura_fuera_linea = 0
		self.mangueras = [[Manguera()]*3]*2
		#self.totales = [[0]*174]*2
		#self.totales_anteriores = [[0]*174]*2

class Pcol():  
	""" 
	docstring for pcol
	"""
	def __init__(self):
		super(pcol, self).__init__()
		self.habilitado = 0
		self.cedula = [[0]*10]*2
		self.contra = [[0]*10]*2
		self.valorv = [[0]*8]*2
		self.fechav = [[0]*6]*2
		self.tipo = [0]*2
		self.ok = [0]*2
		self.disponible = [[0]*10]*2
		self.redimible = [[0]*10]*2
		self.dinero = [[0]*10]*2
		self.totpar = [0]*2
		self.tipodoc = [0]*2

class Estacion():
	"""
	docstring for estación
	"""
	def __init__(self):
		super(estacion, self).__init__()
		self.nombre = 0
		self.nit = 0			
		self.telefono = 0
		self.direccion = 0
		self.lema1 = 0
		self.lema2 = 0

class recibo():
	"""
	docstring for recibo
	"""
	def __init__(self):
		super(recibo, self).__init__()
		self.autorizada = [0]*4
		self.posicion = [0]*4				 
		self.ppu = [[0]*6]*4
		self.dinero = [[0]*9]*4	
		self.volumen = [[0]*9]*4
		self.producto = [0]*4
		self.manguera = [0]*4
		self.preset = [[0]*8]*4			
		self.tipo_id = [0]*4
		self.id = [[0]*16]*4
		self.km = [[0]*11]*4
		self.placa = [[0]*6]*4
		self.tipo_venta = [[0]*6]*4
		self.totales_ini = [[0]*24]*4
		self.totales_fin = [[0]*24]*4
		self.fecha_ini = [[0]*6]*4
		self.fecha_fin = [[0]*6]*4
		self.cedula = [[0]*10]*4
		self.nit = [[0]*10]*4
		self.print = [0]*4
		self.placa_ok = [0]*4
		self.nit_ok = [0]*4
		self.cedula_ok = [0]*4
		self.escombustible = [0]*4
		self.ventas_acumuladas = [0]*4
		self.venta_acumulada_cargada = [0]*4
		self.trama_auto_cre = [[0]*260]*4
		self.volumen_redimido = [[0]*9]*4
		self.id_manguera = [0]*4
		self.fecha_consig = [[0]*6]*4
		self.consignacion = [0]*4
		self.valor_consig = [[0]*7]*4
		self.limite_consig = [0]*4
		self.forma_pago = [0]*4
		self.valor_forma_pago = [[0]*7]*4
		self.boucher_forma_pago = [[0]*16]*4
		self.tipo_vehiculo = [0]*4
		self.convenios = [0]*4

class clientefidelizado():
	"""
	docstring for clientefidelizado
	"""
	def __init__(self):
		super(clientefidelizado, self).__init__()
		self.cedula = [[0]*10]*2
		self.contrasenha = [[0]*4]*2					 

class canasta():
	"""
	docstring for canasta
	"""
	def __init__(self):
		super(canasta, self).__init__()
		self.id_cliente = [[0]*10]*4
		self.tipo_id_cliente = [0]*4
		self.id_producto = [[0]*13]*4
		self.n_producto = [[0]*20]*4;
		self.v_producto = [[0]*7]*4
		self.c_producto = [0]*4
		self.v_intproducto_total = [0]*4
		self.v_producto_total =  [[0]*7]*4
		self.producto_ok = [0]*4
		self.suma_total = [0]*4
		self.saldo_cliente = [0]*4

Can = canasta()
Fiel = clientefidelizado()
Recibo = recibo()
Estacion = estacion()
PCol = pcol()
Turno = turno()
Surtidor = surtidor()
infoS = infosurtidor()

