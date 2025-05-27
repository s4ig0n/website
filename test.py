import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

def generate_edges(rows, cols):
    edges = []
    for r in range(rows):
        for c in range(cols):
            node = r * cols + c + 1
            if c < cols - 1:
                edges.append((node, node + 1))
            if r < rows - 1:
                edges.append((node, node + cols))
    return edges

def create_graph(vertices, edges):
    G = nx.Graph()
    G.add_nodes_from(vertices)
    G.add_edges_from(edges)
    return G

def get_dominating_set(G):
    dom_set = nx.algorithms.approximation.min_weighted_dominating_set(G)
    return dom_set

# Input
rows = int(input("Enter number of rows: "))
cols = int(input("Enter number of columns: "))
verts = rows * cols
vertices = list(range(1, verts + 1))
edges = generate_edges(rows, cols)

# Graph setup
G = create_graph(vertices, edges)
dominating_set = get_dominating_set(G)
domination_number = len(dominating_set)

# Output
print("Graph vertices:", G.nodes())
print("Graph edges:", G.edges())
print("Dominating Set:", dominating_set)
print("Domination Number:", domination_number)

# Grid layout fix
pos = {node: ((node - 1) % cols, -((node - 1) // cols)) for node in G.nodes()}

# Draw
nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=600)
nx.draw_networkx_nodes(G, pos, nodelist=dominating_set, node_color='orange', edgecolors='black', node_size=600)
plt.title("Grid Graph with Dominating Set Highlighted")
plt.show()
