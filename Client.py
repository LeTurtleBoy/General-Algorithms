from Library import Base


class Son(Base):
	def __init__(self):
		print('Base has food', hasattr(Base, 'food'))
		print('Base has foo', hasattr(Base, 'foo'))

	def bar(self):				#if i dont implement bar class, i will have an error on the construct of this class
		return ("its ok Now")


a = Son()
print(a.foo())