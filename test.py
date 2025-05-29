import networkx as nx
import matplotlib.pyplot as plt
from pulp import LpProblem, LpMinimize, LpVariable, lpSum, LpBinary, PULP_CBC_CMD

def get_tr_broadcast_set(G, t, r):
    prob = LpProblem("TRBroadcastDomination", LpMinimize)
    x = {v: LpVariable(f"x_{v}", cat=LpBinary) for v in G.nodes()}

    # Objective: minimize number of towers
    prob += lpSum(x[v] for v in G.nodes())

    # Precompute shortest path lengths
    shortest_paths = dict(nx.all_pairs_shortest_path_length(G))

    # Constraints: each node must receive ≥ r signal
    for v in G.nodes():
        contributions = []
        for u in G.nodes():
            d = shortest_paths[u].get(v, float("inf"))
            strength = max(0, t - d)
            if strength > 0:
                contributions.append(strength * x[u])
        prob += lpSum(contributions) >= r

    prob.solve(PULP_CBC_CMD(msg=0))
    return {v for v in G.nodes() if x[v].varValue == 1}

def generate_grid_graph(rows, cols):
    G = nx.grid_2d_graph(rows, cols)
    mapping = {(r, c): r * cols + c + 1 for r in range(rows) for c in range(cols)}
    return nx.relabel_nodes(G, mapping), rows, cols

def generate_polygon_graph(sides):
    G = nx.cycle_graph(sides)
    mapping = {i: i + 1 for i in range(sides)}
    return nx.relabel_nodes(G, mapping), None, None

def visualize_graph(G, dom_set, title, rows=None, cols=None):
    if rows is not None and cols is not None:
        pos = {v: ((v - 1) % cols, -(v - 1) // cols) for v in G.nodes()}
    else:
        pos = nx.spring_layout(G, seed=42)

    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=500)
    nx.draw_networkx_nodes(G, pos, nodelist=dom_set, node_color='orange')
    plt.title(title)
    plt.show()

# === Main Menu ===
print("=== Graph (t, r)-Broadcast Domination Tool ===")
print("1. Grid Graph")
print("2. Polygon Graph")
choice = input("Enter your choice (1 or 2): ")

if choice == '1':
    rows = int(input("Enter number of rows: "))
    cols = int(input("Enter number of columns: "))
    G, grid_rows, grid_cols = generate_grid_graph(rows, cols)
    title = f"{rows}x{cols} Grid Graph"
elif choice == '2':
    sides = int(input("Enter number of sides (≥3): "))
    if sides < 3:
        print("A polygon must have at least 3 sides.")
        exit()
    G, grid_rows, grid_cols = generate_polygon_graph(sides)
    title = f"{sides}-gon Circular Graph"
else:
    print("Invalid choice.")
    exit()

# Get broadcast parameters
t = int(input("Enter broadcast tower strength (t): "))
r = int(input("Enter minimum required reception (r): "))

# Compute (t, r)-broadcast dominating set
dom_set = get_tr_broadcast_set(G, t, r)
dom_number = len(dom_set)

# Output
print("\nGraph nodes:", sorted(G.nodes()))
print("Graph edges:", sorted(G.edges()))
print("Broadcast Dominating Set:", sorted(dom_set))
print("Domination Number (t={}, r={}):".format(t, r), dom_number)

# Visualize
visualize_graph(G, dom_set, title + f"\n(t={t}, r={r}) Broadcast Domination", grid_rows, grid_cols)
