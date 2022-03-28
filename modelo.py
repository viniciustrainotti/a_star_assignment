class Node():
	#Classe que representa um nó (cidade)

	def __init__(self, nome_cidade, valor_heuristico):
		self.cidade = nome_cidade
		self.heuristica = valor_heuristico
		self.vizinhos = []

	def __init__(self, nome_cidade, coordenada):
		self.cidade = nome_cidade
		self.coordenada = coordenada
		self.heuristica = 0
		self.vizinhos = []

	def gera_heuristica(self, Node_alvo):
		self.heuristica = ((self.coordenada[0] - Node_alvo.coordenada[0])**2 + (self.coordenada[1] - Node_alvo.coordenada[1])**2)**0.5

	def get_heuristica(self):
		return self.heuristica

	def get_coordenada(self):
		return self.coordenada

	def __str__(self):
		return self.cidade

class Edge():
	#Classe que representa os Nós filhos (cidades vizinhas)

	def __init__(self, node_alvo, valor_custo):
		self.node = node_alvo
		self.distancia = valor_custo

	def custo(self):
		return self.distancia + self.node.heuristica

class Route():

	def __init__(self, Node_Inicial):
		self.distancias = 0
		#Nodes avaliados
		self.nodes = [Node_Inicial]
		#Nodes ainda não avaliados
		self.ramos = Node_Inicial.vizinhos

	def custo_ramos(self):
		custo_ramos = []
		for ramo in self.ramos:
			custo_ramos.append(self.distancias + ramo.custo())

		return custo_ramos

	def adiciona(self, Ramo):
		self.distancias += Ramo.distancia
		self.nodes.append(Ramo.node)
		self.ramos = Ramo.node.vizinhos

	def retira(self, Ramo):
		for ramo in self.ramos:
			if(ramo.node.cidade == Ramo.node.cidade):
				self.ramos.remove(ramo)

	def __str__(self):
		nodes = ""
		for node in self.nodes:
			nodes += " -> {}".format(node)
		return "{} - {}".format(nodes, self.distancias)
