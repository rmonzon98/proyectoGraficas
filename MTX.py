"""
Clase para trabajar con matrices
"""
class MTX(object):
	
	"""
	constructor
	"""
	def __init__(self, data):
		self.data = data
		self.col = len(data[0])
		self.row = len(data)
		
	"""
	multiplicacion 
	"""
	def __mul__(self, MTX2):
		resultado = []
		for i in range(self.row):
			resultado.append([])
			for j in range(MTX2.col):
				resultado[-1].append(0)
		for i in range(self.row):
			for j in range(MTX2.col):
				for k in range(MTX2.row):
					resultado[i][j] += self.data[i][k] * MTX2.data[k][j]
		return MTX(resultado)
	
	"""
	get
	"""
	def getData(self):
		return self.data
