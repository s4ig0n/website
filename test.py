import networkx as nx
import matplotlib.pyplot as plt
from pulp import LpProblem, LpVariable, LpMinimize, lpSum, LpBinary, PULP_CBC_CMD

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

def get_exact_dominating_set(G):
    prob = LpProblem("MinimumDominatingSet", LpMinimize)
    x = {v: LpVariable(f"x_{v}", cat=LpBinary) for v in G.nodes()}

    # Objective: Minimize number of nodes in dominating set
    prob += lpSum(x[v] for v in G.nodes())

    # Constraints: each node must be dominated by itself or a neighbor
    for v in G.nodes():
        prob += lpSum(x[u] for u in [v] + list(G.neighbors(v))) >= 1

    prob.solve(PULP_CBC_CMD(msg=0))

    # Return dominating set
    return {v for v in G.nodes() if x[v].varValue == 1}

# Input
rows = int(input("Enter number of rows: "))
cols = int(input("Enter number of columns: "))
verts = rows * cols
vertices = list(range(1, verts + 1))
edges = generate_edges(rows, cols)

# Graph setup
G = create_graph(vertices, edges)
dominating_set = get_exact_dominating_set(G)
domination_number = len(dominating_set)

# Output
print("Graph vertices:", list(G.nodes()))
print("Graph edges:", list(G.edges()))
print("Dominating Set:", dominating_set)
print("Domination Number:", domination_number)

# Layout
pos = {node: ((node - 1) % cols, -((node - 1) // cols)) for node in G.nodes()}

# Draw
nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=600)
nx.draw_networkx_nodes(G, pos, nodelist=dominating_set, node_color='orange', edgecolors='black', node_size=600)
plt.title("Grid Graph with Minimum Dominating Set")
plt.show()
