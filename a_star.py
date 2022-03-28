import math
from dists import dists, straight_line_dists_from_bucharest

from modelo import *
from copy import deepcopy
from matplotlib import pyplot
from numpy import random

# goal sempre sera 'bucharest'
# def a_star(start, goal='Bucharest'):
#     """
#     Retorna uma lista com o caminho de start até 
#     goal segundo o algoritmo A*
#     """

#     print(f"distancia entre os vizinhos {dists}")
#     print(f"heuristica {straight_line_dists_from_bucharest}")

#     return(start, goal)

# print(f"{a_star(start='Lugoj')}")

def Cria_Mapa_Romenia():

	#Inicializando cidades
	#Os valores Heuristicos são dados de acordo com a distância em linha reta de Bucareste
	#Os nós recebem o nome da cidade e as coordenadas geográficas da cidade

	#https://ggbm.at/h7Vq2G4g
	Bucareste = Node("Bucareste", [0, 0])
	Vaslui = Node ("Vaslui", [255.3, 142])
	Eforie = Node("Eforie", [214.5, -58])
	Oradea = Node("Oradea", [-210, 293.5])
	Hirsova = Node("Hirsova", [180.7, 21.2])
	Zerind = Node("Zerind", [-281.2, 303.6])
	Iasi = Node("Iasi", [229, 230])
	Giurgiu = Node("Giurgiu", [-37, -82.1])
	Arad = Node("Arad", [-325, 242.5])
	Urzineci = Node("Urzineci", [82.6, 20])
	Fagaras = Node("Fagaras", [-132.7, 164])
	Sibiu = Node("Sibiu", [-230, 140.7])
	Rimnicu_Vilcea = Node("Rimnicu_Vilcea", [-182.7, 76.5])
	Craiova = Node("Craiova", [-180, -70])
	Drobreta = Node("Drobreta", [-300, -63])
	Mehadia = Node("Mehadia", [-292, 11.7])
	Neamt = Node("Neamt", [146.5, 258.2])
	Lugoj = Node("Lugoj", [-296, 81.6])
	Timisoara = Node("Timisoara", [-388.7, 142.8])
	Pitesti = Node("Pitesti", [-93.6, 37.9])


	#Cidades de partida e destino
	Node_Inicio = Lugoj
	Node_Fim = Bucareste

	Nodes = [Bucareste, Vaslui, Eforie, Pitesti, Lugoj, Oradea, Hirsova, Zerind, Iasi, Giurgiu, Arad, Urzineci, Fagaras, Sibiu, Rimnicu_Vilcea, Craiova, Drobreta, Mehadia, Neamt, Timisoara]

	#Monta a heuristica de acordo com a cidade destino
	for node in Nodes:
		node.gera_heuristica(Node_Fim)
		print("{} - {}".format(node.cidade, node.get_heuristica()))

	#Inicializando vizinhos
	Arad.vizinhos = [Edge(Zerind, 75), Edge(Sibiu, 140), Edge(Timisoara, 118)]
	Zerind.vizinhos = [Edge(Oradea, 71), Edge(Arad, 75)]
	Oradea.vizinhos = [Edge(Zerind, 71), Edge(Sibiu, 151)]
	Sibiu.vizinhos = [Edge(Oradea, 151), Edge(Arad, 140), Edge(Fagaras, 99), Edge(Rimnicu_Vilcea, 80)]
	Fagaras.vizinhos = [Edge(Sibiu, 99), Edge(Bucareste, 211)]
	Rimnicu_Vilcea.vizinhos = [Edge(Sibiu, 80), Edge(Pitesti, 97), Edge(Craiova, 146)]
	Pitesti.vizinhos = [Edge(Rimnicu_Vilcea, 97), Edge(Bucareste, 101), Edge(Craiova, 138)]
	Timisoara.vizinhos = [Edge(Arad, 118), Edge(Lugoj, 111)]
	Lugoj.vizinhos = [Edge(Timisoara, 111), Edge(Mehadia, 70)]
	Mehadia.vizinhos = [Edge(Lugoj, 70), Edge(Drobreta, 75)]
	Drobreta.vizinhos = [Edge(Mehadia, 75), Edge(Craiova, 120)]
	Craiova.vizinhos = [Edge(Drobreta, 120), Edge(Rimnicu_Vilcea, 146), Edge(Pitesti, 138)]
	Bucareste.vizinhos = [Edge(Fagaras, 211), Edge(Pitesti, 101), Edge(Giurgiu, 90), Edge(Urzineci, 85)]
	Giurgiu.vizinhos = [Edge(Bucareste, 90)]
	Urzineci.vizinhos = [Edge(Bucareste, 85), Edge(Hirsova, 98), Edge(Vaslui, 142)]
	Hirsova.vizinhos = [Edge(Urzineci, 98), Edge(Eforie, 86)]
	Eforie.vizinhos = [Edge(Hirsova, 86)]
	Vaslui.vizinhos = [Edge(Urzineci, 142), Edge(Iasi, 92)]
	Iasi.vizinhos = [Edge(Vaslui, 92), Edge(Neamt, 87)]
	Neamt.vizinhos = [Edge(Iasi, 87)]

	plot_cidades(Nodes)

	#Calculando a rota
	Solucao = Rota(Node_Inicio, Node_Fim)
	
	#Plota a melhor solução
	x = []
	y = []
	for node in Solucao:
		x.append(node.get_coordenada()[0])
		y.append(node.get_coordenada()[1])

	pyplot.plot(x, y, '-', color = 'red', lw=2)
	plot_cidades(Nodes)
	

def Rota(Node_Inicio, Node_Fim):

	if(Node_Fim.cidade == Node_Inicio.cidade):
		return [Node_Inicio]

	Fila_De_Rotas = []

	rota = Route(Node_Inicio)
	Fila_De_Rotas.append(rota)


	while(True):
		melhores_ramos = []
		melhor_ramo = None

		index_melhores_ramos = []
		rota_com_melhor_ramo = None
		
		#Encontra o melhor ramo entre os ramos abertos
		for rota in Fila_De_Rotas:
			custo_ramos = rota.custo_ramos()
			melhores_ramos.append(min(custo_ramos))
			index_melhores_ramos.append(custo_ramos.index(min(custo_ramos)))

		indice_melhor_rota = melhores_ramos.index(min(melhores_ramos))
		rota_com_melhor_ramo = deepcopy(Fila_De_Rotas[indice_melhor_rota])
		melhor_ramo = rota_com_melhor_ramo.ramos[index_melhores_ramos[indice_melhor_rota]]
	
		#Remove ramo da rota antiga
		rota = Fila_De_Rotas[indice_melhor_rota]
		rota.retira(melhor_ramo)
		
		rota_com_melhor_ramo.adiciona(melhor_ramo)
		Fila_De_Rotas.append(rota_com_melhor_ramo)

		#Adiciona uma nova rota ou remove uma rota que já acabou
		if(len(rota.ramos) == 0):
			Fila_De_Rotas.remove(rota)	

		#Condição de parada
		print(rota_com_melhor_ramo)
		if(melhor_ramo.node.cidade == Node_Fim.cidade):
			break;

	return rota_com_melhor_ramo.nodes
	
def plot_cidades(Nodes):

	coordenadas_x = []
	coordenadas_y = []
	for node in Nodes:
		coordenadas_x.append(node.get_coordenada()[0])
		coordenadas_y.append(node.get_coordenada()[1])

	colors = random.rand(len(coordenadas_x))

	x = [-210, -281.2, -325, -388.7, -296, -292, -300, -180, -182.7, -230, -210]
	y = [293.5, 303.6, 242.5, 142.8, 81.6, 11.7, -63, -70, 76.5, 140.7, 293.5]
	pyplot.plot(x, y, ':', color = 'black', lw=1)

	x = [-325, -230, -132.7, 0, -93.6, -182.7]
	y = [242.5, 140.7, 164, 0, 37.9, 76.5]
	pyplot.plot(x, y, ':', color = 'black', lw=1)

	x = [-180, -93.6]
	y = [-70, 37.9]
	pyplot.plot(x, y, ':', color = 'black', lw=1)

	x = [-37, 0, 82.6, 180.7, 214.5]
	y = [-82.1, 0, 20, 21.2, -58]
	pyplot.plot(x, y, ':', color = 'black', lw=1)

	x = [82.6, 255.3, 229, 146.5]
	y = [20, 142, 230, 258.2]
	pyplot.plot(x, y, ':', color = 'black', lw=1)

	pyplot.scatter(coordenadas_x, coordenadas_y, marker="o", c=colors, alpha=0.5)

	for node in Nodes:
		pyplot.annotate(node.cidade, xy = (node.get_coordenada()[0], node.get_coordenada()[1]))

	pyplot.show()




Cria_Mapa_Romenia()