class Poly:
	def __init__(self, *coeffs):
		self.coeffs = coeffs

	def __len__(self):
		return len(self.coeffs)-1

	def __add__(self, other):
		if(len(self)==(len(other))):
			return Poly(*(x+y for x,y in zip(self.coeffs, other.coeffs)))
		else:
			pass

	def __repr__(self):
		return '\nClase: Poly\nCoeficientes {}\n'.format(self.coeffs)



P = Poly(1,2,3,4,5)
P2= Poly(4,3,2,1,0)

print(P+P2)