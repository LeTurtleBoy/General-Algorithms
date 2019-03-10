from sqlite3 import connect
from time import sleep

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
def conect():
	with connect('test.db') as conn:
		cur = conn.cursor()
		cur.execute('create table points(x int,y int)')
		cur.execute('insert into points (x,y) values (0,0)')
		cur.execute('insert into points (x,y) values (0,1)')
		cur.execute('insert into points (x,y) values (1,0)')
		cur.execute('insert into points (x,y) values (1,1)')
		for row in cur.execute('select x,y from points'):
			print(row)
		for row in cur.execute('select sum(x+y) from points'):
			print(row)
		#cur.commit()
		sleep(10)
		cur.execute('drop table points')

conect()