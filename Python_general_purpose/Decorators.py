#
import time

def timer(fun):
	def f(*args,**kwargs):
		b = time.time()
		Ret = fun(*args,**kwargs)
		a = time.time()
		print("Tiempo de ejecucucion: ",a-b)
		return Ret
	return f

@timer
def add(x,y=10):
	'''
	Vamo' a suma'
	'''
	time.sleep(1)
	return x+y
print(add(1,10))