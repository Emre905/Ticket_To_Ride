# define necessary functions taken from ticket_to_ride.ipynb
import networkx as nx 
import json 

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



'''To calculate train cost and points of a collection of path, we can select some indexes
from 0 to 29 (len(TICKETS)=30). Then we're gonna calculate the weight, path and point.'''

# calculate all points together
def calculate_point(routes, tickets):
    # Build bidirectional weighted graph from both players' taken VERTICES and EDGES
    G1 = nx.MultiGraph()  # get player1's graph
    G1.add_nodes_from(VERTICES)  # add vertices

    for (node1, node2), (weight, color) in routes.items():
        G1.add_edge(node1, node2, weight=int(weight), color=color)  # add edges

    point_ticket = 0
    for ticket in tickets:
        city1 = ticket[0]
        city2 = ticket[1]
        point = int(ticket[2])

        if nx.has_path(G1, city1, city2):
            point_ticket += point
        else:
            point_ticket -= point

    point_edge = 0
    for i, j in G1.edges():
        try:
            edge_weight = EDGES_DICT[(i, j)]
        except KeyError:
            edge_weight = EDGES_DICT[(j, i)]
        finally:
            point_edge += POINT_EDGE_DICT[edge_weight]

    longest_path_length, longest_path_edges = find_longest_path(G1)
                
    return point_ticket, point_edge, longest_path_length, longest_path_edges

# use DFS to get longest route
def find_longest_path(graph):
    longest_path_length = 0
    longest_path_edges = []

    for start_node in graph.nodes():
        stack = [(start_node, [], 0, set())]  # (current_node, current_path_edges, current_length, visited_edges)

        # perform DFS using a stack
        while stack:
            node, path_edges, length, visited_edges = stack.pop() # pop the last element from the stack

            # iterate over each neighbor of the current node
            for neighbor in graph.neighbors(node):
                # iterate over each edge between the current node and the neighbor
                for key, data in graph[node][neighbor].items():
                    edge = (node, neighbor, key)    # define the current edge and its reverse
                    reverse_edge = (neighbor, node, key)

                    #check if the edge and its reverse have not been visited
                    if edge not in visited_edges and reverse_edge not in visited_edges: 
                        new_length = length + data['weight'] # calculate the new length
                        new_path_edges = path_edges + [(node, neighbor, data['weight'])] # create a new path
                        new_visited_edges = visited_edges | {edge, reverse_edge} # get union of visited edges with new edge
                        stack.append((neighbor, new_path_edges, new_length, new_visited_edges)) # add visited edges

                        # update longest path if new length is bigger
                        if new_length > longest_path_length:
                            longest_path_length = new_length
                            longest_path_edges = new_path_edges

    return longest_path_length, longest_path_edges

# player_1_tickets = [('Duluth', 'El Paso', '10'), ('Seattle', 'New York', '22'), ('San Francisco', 'Atlanta', '17')]
# player_1_edges = {EDGES[i][:2]:EDGES[i][2:] for i in range(0,40,3)}
# calculate_point(player_1_edges, player_1_tickets)





