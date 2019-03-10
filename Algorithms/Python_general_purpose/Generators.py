#generators 
from time import sleep
#top level syntax or function -> underscore method

def add(x,y):
	return x+y

class adder:
	def __init__(self):
		self.z = 0

	def __call__(self,x,y):
		self.z +=1
		return x+y+self.z

def compute():
	rv = []
	for i in range(10):
		sleep(0.5)
		rv.append(i)
	return rv



class compute2():
	'''
	def __call__(self):
		rv = []
		for i in range(10):
			sleep(0.5)
			rv.append(i)
		return rv
	'''
	def __iter__(self):
		self.last = 0
		return self

	def __next__(self):
		rv = self.last
		self.last += 1

		if self.last > 10:
			raise StopIteration()
		sleep(.5) #Proceso
		return rv


def computegen():
	for i in range(10):
		sleep(0.5)
		yield i

for val in computegen():
	print(val)



#Los generadores estan pensados para subrutinas que se corren una vez y sale para pintura
def first():
	print(1)
def second():
	print(2)
def last():
	print('n')

class Api:
	def run_this_first(self):
		first()
	def run_this_second(self):
		second()
	def run_this_last(self):
		last()
