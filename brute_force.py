import networkx as nx 
from networkx.utils import pairwise 
import json 
from itertools import combinations 
from time import time 

# Let's call all libraries and define city and road variables

# VERTICES are list of all cities
with open('cities.txt') as f:
    VERTICES = [i.rstrip() for i in f] # stripping "\n" from end of lines and seperating all lines
    
# EDGES are roads connecting 2 cities (City A,City B,Distance,Color)
with open('roads.txt') as f:
    next(f) # skipping header
    EDGES = [tuple(i.strip().split(',')) for i in f] # stripping "\n" and making other , seperated terms a tuple
# get specific weight of each edges used to calculate single road points
EDGES_DICT = {(city1,city2):int(weight) for city1,city2,weight,color in EDGES}
# adding weight conversion for edge points. (3 weight road is 4 point etc)
POINT_EDGE_DICT = {i:j for i,j in zip(range(1,7),[1,2,4,7,10,15])}

# TICKETS are given by the game. The goal is to connect those 2 cities, 3rd input is the point you get from completing
# (City A,City B,Points)
with open('tickets.txt') as f:
    next(f) # skipping header
    TICKETS = [tuple(i.strip().split(',')) for i in f] # stripping "\n" and making other , seperated terms a tuple

# City_locations are dictionary of all cities as (cityname:[posx, posy])
with open('city_locations.json') as f:
    CITY_LOCATIONS = json.load(f)

# Build bidirectional weighted graph from the VERTICES and EDGES
G = nx.MultiGraph() # use networkx library Multigraph
G.add_nodes_from(VERTICES) #add vertices

for edge in EDGES:
    G.add_edge(edge[0], edge[1], 
    weight = int(edge[2]), colour = edge[3]) #add edges with weight and colour

# Steiner tree tries to find minimum sum of weights to connect given nods
''' Note: Finding optimal Steiner Tree is an NP problem,
the function nx.steiner_tree() just approximates    the best solution. 
Had "no attribute" problems for this function. It is copied from the documentation, 
made some slight changes and removed unnecessary functions:
'''

def steiner_tree(G, terminal_nodes, weight="weight"):
    method = "mehlhorn"  
    edges = _mehlhorn_steiner_tree(G, terminal_nodes, weight)

    # For multigraph we should add the minimal weight edge keys
    if G.is_multigraph():
        edges = (
            (u, v, min(G[u][v], key=lambda k: G[u][v][k][weight])) for u, v in edges
        )
    T = G.edge_subgraph(edges)
    return T

def _mehlhorn_steiner_tree(G, terminal_nodes, weight):
    paths = nx.multi_source_dijkstra_path(G, terminal_nodes)

    d_1 = {}
    s = {}
    for v in G.nodes():
        s[v] = paths[v][0]
        d_1[(v, s[v])] = len(paths[v]) - 1

    # G1-G4 names match those from the Mehlhorn 1988 paper.
    G_1_prime = nx.Graph()
    for u, v, data in G.edges(data=True):
        su, sv = s[u], s[v]
        weight_here = d_1[(u, su)] + data.get(weight, 1) + d_1[(v, sv)]
        if not G_1_prime.has_edge(su, sv):
            G_1_prime.add_edge(su, sv, weight=weight_here)
        else:
            new_weight = min(weight_here, G_1_prime[su][sv]["weight"])
            G_1_prime.add_edge(su, sv, weight=new_weight)

    G_2 = nx.minimum_spanning_edges(G_1_prime, data=True)

    G_3 = nx.Graph()
    for u, v, d in G_2:
        path = nx.shortest_path(G, u, v, weight)
        for n1, n2 in pairwise(path):
            G_3.add_edge(n1, n2)

    G_3_mst = list(nx.minimum_spanning_edges(G_3, data=False))
    if G.is_multigraph():
        G_3_mst = (
            (u, v, min(G[u][v], key=lambda k: G[u][v][k][weight])) for u, v in G_3_mst
        )
    G_4 = G.edge_subgraph(G_3_mst).copy()
    _remove_nonterminal_leaves(G_4, terminal_nodes)
    return G_4.edges()

def _remove_nonterminal_leaves(G, terminals):
    terminals_set = set(terminals)
    for n in list(G.nodes):
        if n not in terminals_set and G.degree(n) == 1:
            G.remove_node(n)

# for brute force testing all possible routes
def brute_force(n):
    max_score = 100
    for ticket_amount in range(n+4,n+5): # should be (n,n+6) or (n,n+7) for n = 12
        start = time()
        idx_list = combinations(range(30),ticket_amount)
        for idx in idx_list: # idx_list is a generator. need to iterate it for each term
            city_list = [TICKETS[i][j] for i in idx for j in range(2)] # add city1 and city2   
            G2 =steiner_tree(G, city_list) # find the shortest graph connecting all cities in city_list
            w = int(G2.size(weight="weight")) # calculate it's weight

            if w <= 45: # calculate point if weight <= 45
                point_ticket = 0
                point_edge = 0
                for i in idx:
                    add = int(TICKETS[i][2]) # adding ticket points
                    point_ticket += add
                
                for i,j in G2.edges(): # add edge(road) points
                    try: 
                        edge_weight = EDGES_DICT[(i,j)] # it may be reverse order
                    except KeyError:
                        edge_weight = EDGES_DICT[(j,i)]
                    finally:
                        point_edge += POINT_EDGE_DICT[edge_weight]

                if point_ticket + point_edge > max_score:
                    max_score = point_ticket + point_edge
                    weight = w
                    best_idx = list(idx)
        print(f'best {ticket_amount} ticket paths are achieved at {best_idx} giving {max_score} points with {weight} trains {time()-start:.2f} sec')
    return max_score, weight, best_idx
max_score, weight, best_idx = brute_force(2)
