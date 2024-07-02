# define necessary functions taken from ticket_to_ride.ipynb
import networkx as nx 
import numpy as np 
import json 
import os 
import random 
from time import time 
import matplotlib.pyplot as plt 
import matplotlib.image as mpimg 
from matplotlib.lines import Line2D
from networkx.utils import pairwise 
import sys
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.image import imread

# Define necessary game variables

# VERTICES are list of all cities
with open('data/cities.txt') as f:
    VERTICES = [i.rstrip() for i in f] # stripping "\n" from end of lines and seperating all lines
    
# EDGES are roads connecting 2 cities (City A,City B,Distance,Color)
with open('data/roads.txt') as f:
    next(f) # skipping header
    EDGES = [tuple(i.strip().split(',')) for i in f] # stripping "\n" and making other , seperated terms a tuple
    
# TICKETS are given by the game. The goal is to connect those 2 cities to earn points
# (City A,City B,Point)
with open('data/tickets.txt') as f:
    next(f) # skipping header
    TICKETS = [tuple(i.strip().split(',')) for i in f] # stripping "\n" and making other , seperated terms a tuple

# City_locations are dictionary of all cities as (cityname:[posx, posy])
with open('data/city_locations.json') as f:
    CITY_LOCATIONS = json.load(f)

# get specific weight of each edges used to calculate single road points
EDGES_DICT = {(city1,city2):int(weight) for city1,city2,weight,color in EDGES}
# adding weight conversion for edge points. (3 weight road is 4 point etc)
POINT_EDGE_DICT = {i:j for i,j in zip(range(1,7),[1,2,4,7,10,15])}

# Build bidirectional weighted graph from the VERTICES and EDGES
G = nx.MultiGraph()
G.add_nodes_from(VERTICES) #add vertices

for edge in EDGES:
    G.add_edge(edge[0], edge[1], weight = int(edge[2]), color = edge[3]) #add edges


'''
Note: Had "no attribute" problems for nx.steiner_tree() function. It is copied 
from the documentation, made some slight changes and removed unnecessary parts:
'''

def steiner_tree(G, terminal_nodes, weight="weight"):
    method = "mehlhorn"
    algo = _mehlhorn_steiner_tree

    edges = algo(G, terminal_nodes, weight)
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

# This function connects given vertices with minimum weighted edges
def connect_cities(list_cities):
    G2 =steiner_tree(G, list_cities) # find the shortest path connecting all cities in list_cities
    weight = int(G2.size(weight="weight")) # calculate it's weight
    
    return weight,G2

'''To calculate train cost and points of a collection of path, we can select some indexes
from 0 to 29 (len(TICKETS)=30). Then we're gonna calculate the weight, path and point.
(not including longest path point since it's single-player)'''
def calculate_point(indexes, tickets = TICKETS):
    city_list = [tickets[i][j] for i in indexes for j in range(2)] # add city1 and city2   
    weight, G2 = connect_cities(city_list)
    point_ticket = 0
    point_edge = 0
    for i in indexes:
        add = int(tickets[i][2]) # adding ticket points
        point_ticket += add

    for i,j in G2.edges():
        try: 
            edge_weight = EDGES_DICT[(i,j)]
        except KeyError:
            edge_weight = EDGES_DICT[(j,i)]
        finally:
            point_edge += POINT_EDGE_DICT[edge_weight]
            
    return (point_ticket, point_edge), weight, G2

def test_combinations(index_comb_lst, tickets = TICKETS): 
    max_point = 0
    best_weight = 0
    best_path_graph = []
    best_idx = []
    n = len(tickets)
    
    while True:
        (p1, p2), w, G2 = calculate_point(index_comb_lst, tickets)
        p = p1+p2
        if p > max_point and w<=45: # update the best path when max_point is exceeded
                max_point = p
                best_weight = w # it's actually just the weight that corresponds to p
                best_path_graph = G2
                best_idx = index_comb_lst.copy()
                
        if w <= 45:
            found_bool = False
            for i in range(1,len(index_comb_lst)+1):
                if index_comb_lst[-i] < n-i: # if the last term can increase by 1 without index error
                    max = index_comb_lst[-i] + 1 # max term that can be increased by 1
                    index_comb_lst.append(max)
                    index_comb_lst.sort()
                    found_bool = True # when bool is true, no need to remove a term
                    break  

        else: # change the last term. If max of the array can increase by 1, increase it. 
    #Otherwise increase the 2nd max, or 3rd etc.
            add_bool = False
            for i in range(1,len(index_comb_lst)+1):
                if index_comb_lst[-i] < n-i: # if the last term can increase by 1 without index error
                    index_comb_lst[-i] += 1
                    add_bool = True # when bool is true, no need to remove a term
                    break   
                
            if not add_bool: # return when no term can increase 
                return max_point, best_weight, best_path_graph, best_idx