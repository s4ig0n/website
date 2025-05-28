import networkx as nx
import matplotlib.pyplot as plt
from pulp import LpProblem, LpMinimize, LpVariable, lpSum, LpBinary, PULP_CBC_CMD

def get_exact_dominating_set(G):
    prob = LpProblem("MinimumDominatingSet", LpMinimize)
    x = {v: LpVariable(f"x_{v}", cat=LpBinary) for v in G.nodes()}
    
    prob += lpSum(x[v] for v in G.nodes())  # Objective

    for v in G.nodes():
        prob += lpSum(x[u] for u in [v] + list(G.neighbors(v))) >= 1

    prob.solve(PULP_CBC_CMD(msg=0))
    return {v for v in G.nodes() if x[v].varValue == 1}

def generate_grid_graph(rows, cols):
    G = nx.Graph()
    for r in range(rows):
        for c in range(cols):
            node = r * cols + c + 1
            G.add_node(node)

            if c < cols - 1:
                G.add_edge(node, node + 1)
            if r < rows - 1:
                G.add_edge(node, node + cols)
    return G

def generate_polygon_graph(sides):
    G = nx.cycle_graph(sides)
    mapping = {i: i + 1 for i in range(sides)}
    return nx.relabel_nodes(G, mapping)

def visualize_graph(G, dom_set, title):
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=500)
    nx.draw_networkx_nodes(G, pos, nodelist=dom_set, node_color='orange')
    plt.title(title)
    plt.show()

print("=== Graph Dominating Set Tool ===")
print("1. Grid Graph")
print("2. Polygon Graph")
choice = input("Enter your choice (1 or 2): ")

if choice == '1':
    rows = int(input("Enter number of rows: "))
    cols = int(input("Enter number of columns: "))
    G = generate_grid_graph(rows, cols)
    title = f"{rows}x{cols} Grid Graph"
elif choice == '2':
    sides = int(input("Enter number of sides (>=3): "))
    if sides < 3:
        print("A polygon must have at least 3 sides.")
        exit
    G = generate_polygon_graph(sides)
    title = f"{sides}-gon Circular Graph"
else:
    print("Invalid choice.")
    exit

dom_set = get_exact_dominating_set(G)
dom_number = len(dom_set)

print("\nGraph nodes:", list(G.nodes()))
print("Graph edges:", list(G.edges()))
print("Dominating Set:", dom_set)
print("Domination Number:", dom_number)

visualize_graph(G, dom_set, title)
