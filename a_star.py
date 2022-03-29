import math, sys
from copy import deepcopy
from dists import dists, straight_line_dists_from_bucharest

class Node():
    """Classe que representa um nó (cidade)"""
    def __init__(self, nome_cidade, valor_heuristico):
        self.cidade = nome_cidade
        self.heuristica = valor_heuristico
        self.vizinhos = []

    def __init__(self, nome_cidade):
        self.cidade = nome_cidade
        self.heuristica = 0
        self.vizinhos = []

    def set_heuristica(self, heuristica):
        self.heuristica = heuristica

    def get_heuristica(self):
        return self.heuristica

    def get_coordenada(self):
        return self.coordenada

    def __str__(self):
        return self.cidade

class Edge():
    """Classe que representa os Nós filhos (cidades vizinhas)"""
    def __init__(self, node_alvo, valor_custo):
        self.node = node_alvo
        self.distancia = valor_custo

    def custo(self):
        return self.distancia + self.node.heuristica

class Route():
    """Classe que representa as ações do algoritmo"""
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


def find_Node(classname, Nodes):
    return next((node for node in Nodes if node.cidade == classname), None)

# goal sempre sera 'Bucharest'
def a_star(start, goal='Bucharest'):
    """
    Retorna uma lista com o caminho de start até 
    goal segundo o algoritmo A*
    """
    Nodes = []
    # Iniciando os objectos Nodes com as cidades
    cities = list(straight_line_dists_from_bucharest.keys())
    for city in cities:
        Nodes.append(Node(city))

    # Setando para object Node as cidades de start e goal
    Node_Inicio = find_Node(start, Nodes)
    Node_Fim = find_Node(goal, Nodes)

    # Seta a heuristica de acordo com os valores de straight_line_dists_from_bucharest e
    # Inicializa vizinhos 
    for node in Nodes:
        node.set_heuristica(straight_line_dists_from_bucharest[node.cidade])
        # print("{} - {}".format(node.cidade, node.get_heuristica()))
        for neighboring_cities in dists[node.cidade]:
            node.vizinhos.append(Edge(find_Node(neighboring_cities[0], Nodes), neighboring_cities[1]))
            # print(f"{neighboring_cities} {neighboring_cities[0]} {neighboring_cities[1]} ")

    # Execução do algoritmo
    if(Node_Fim.cidade == Node_Inicio.cidade):
        return [Node_Inicio]

    Fila_De_Rotas = []

    rota = Route(Node_Inicio)
    Fila_De_Rotas.append(rota)

    while(True):
        melhores_ramos, index_melhores_ramos = [], []
        melhor_ramo, rota_com_melhor_ramo = None, None

        #Encontra o melhor ramo entre os ramos abertos
        for rota in Fila_De_Rotas:
            custo_ramos = rota.custo_ramos()
            melhores_ramos.append(min(custo_ramos))
            index_melhores_ramos.append(custo_ramos.index(min(custo_ramos)))

        indice_melhor_rota = melhores_ramos.index(min(melhores_ramos))
        # https://pt.stackoverflow.com/questions/247588/como-fazer-um-deep-copy-em-python
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
            print(f"=:: Execução Final: {rota_com_melhor_ramo}")
            break

    return rota_com_melhor_ramo.nodes

if __name__ == "__main__":
    start = sys.argv[1] if len(sys.argv) > 1 else 'Oradea'
    a_star(start=start)

# Examples input/output:
# $ python a_star.py 
# -> Oradea -> Sibiu -> Rimnicu_Vilcea -> Pitesti -> Bucharest - 429
#
# $ python a_star.py Oradea
# -> Oradea -> Sibiu -> Rimnicu_Vilcea -> Pitesti -> Bucharest - 429
#
# $ python a_star.py Arad
# -> Lugoj -> Mehadia -> Dobreta -> Craiova -> Pitesti -> Bucharest - 504
# 
# 
# Código baseado no fork
# https://github.com/viniciustrainotti/BuscaHeuristica
