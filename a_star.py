import math
from dists import dists, straight_line_dists_from_bucharest

#import dists

# goal sempre sera 'bucharest'
def a_star(start, goal='Bucharest'):
    """
    Retorna uma lista com o caminho de start até 
    goal segundo o algoritmo A*
    """

    print(f"distancia entre os vizinhos {dists}")
    print(f"heuristica {straight_line_dists_from_bucharest}")

    return(start, goal)

print(f"{a_star(start='Lugoj')}")