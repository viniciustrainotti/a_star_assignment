import math
from dists import dists

from modelo import *
from copy import deepcopy
from matplotlib import pyplot
from numpy import random

import sys

def str_to_Node(classname, Nodes):
    for node in Nodes:
        if node.cidade == classname:
            return node
    #return getattr(sys.modules[__name__], classname)

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

# goal sempre sera 'bucharest'
def a_star(start, goal='Bucharest'):
    """
    Retorna uma lista com o caminho de start até 
    goal segundo o algoritmo A*
    """
    Bucharest = Node("Bucharest")
    Vaslui = Node("Vaslui")
    Eforie = Node("Eforie")
    Oradea = Node("Oradea")
    Hirsova = Node("Hirsova")
    Zerind = Node("Zerind")
    Iasi = Node("Iasi")
    Giurgiu = Node("Giurgiu")
    Arad = Node("Arad")
    Urzineci = Node("Urzineci")
    Fagaras = Node("Fagaras")
    Sibiu = Node("Sibiu")
    Rimnicu_Vilcea = Node("Rimnicu_Vilcea")
    Craiova = Node("Craiova")
    Dobreta = Node("Dobreta")
    Mehadia = Node("Mehadia")
    Neamt = Node("Neamt")
    Lugoj = Node("Lugoj")
    Timisoara = Node("Timisoara")
    Pitesti = Node("Pitesti")

    Nodes = [Bucharest, Vaslui, Eforie, Pitesti, Lugoj, Oradea, Hirsova, Zerind, Iasi, Giurgiu, Arad, Urzineci, Fagaras, Sibiu, Rimnicu_Vilcea, Craiova, Dobreta, Mehadia, Neamt, Timisoara]

    #Cidades de partida e destino
    Node_Inicio = str_to_Node(start, Nodes)
    Node_Fim = str_to_Node(goal, Nodes)

    #Monta a heuristica de acordo com a cidade destino
    for node in Nodes:
        node.set_heuristica(node)
        print("{} - {}".format(node.cidade, node.get_heuristica()))

    #Inicializando vizinhos
    Arad.vizinhos = [Edge(Zerind, 75), Edge(Sibiu, 140), Edge(Timisoara, 118)]
    Zerind.vizinhos = [Edge(Oradea, 71), Edge(Arad, 75)]
    Oradea.vizinhos = [Edge(Zerind, 71), Edge(Sibiu, 151)]
    Sibiu.vizinhos = [Edge(Oradea, 151), Edge(Arad, 140), Edge(Fagaras, 99), Edge(Rimnicu_Vilcea, 80)]
    Fagaras.vizinhos = [Edge(Sibiu, 99), Edge(Bucharest, 211)]
    Rimnicu_Vilcea.vizinhos = [Edge(Sibiu, 80), Edge(Pitesti, 97), Edge(Craiova, 146)]
    Pitesti.vizinhos = [Edge(Rimnicu_Vilcea, 97), Edge(Bucharest, 101), Edge(Craiova, 138)]
    Timisoara.vizinhos = [Edge(Arad, 118), Edge(Lugoj, 111)]
    Lugoj.vizinhos = [Edge(Timisoara, 111), Edge(Mehadia, 70)]
    Mehadia.vizinhos = [Edge(Lugoj, 70), Edge(Dobreta, 75)]
    Dobreta.vizinhos = [Edge(Mehadia, 75), Edge(Craiova, 120)]
    Craiova.vizinhos = [Edge(Dobreta, 120), Edge(Rimnicu_Vilcea, 146), Edge(Pitesti, 138)]
    Bucharest.vizinhos = [Edge(Fagaras, 211), Edge(Pitesti, 101), Edge(Giurgiu, 90), Edge(Urzineci, 85)]
    Giurgiu.vizinhos = [Edge(Bucharest, 90)]
    Urzineci.vizinhos = [Edge(Bucharest, 85), Edge(Hirsova, 98), Edge(Vaslui, 142)]
    Hirsova.vizinhos = [Edge(Urzineci, 98), Edge(Eforie, 86)]
    Eforie.vizinhos = [Edge(Hirsova, 86)]
    Vaslui.vizinhos = [Edge(Urzineci, 142), Edge(Iasi, 92)]
    Iasi.vizinhos = [Edge(Vaslui, 92), Edge(Neamt, 87)]
    Neamt.vizinhos = [Edge(Iasi, 87)]

    #Calculando a rota
    Solucao = Rota(Node_Inicio, Node_Fim)

    return(f"Solução para {start} até {goal}")

if __name__ == "__main__":
    start = sys.argv[1]
    a_star(start=start)

# Example:
# $ python a_star.py Oradea