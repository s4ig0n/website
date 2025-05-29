import networkx as nx
import matplotlib.pyplot as plt
from pulp import LpProblem, LpMinimize, LpVariable, lpSum, LpBinary, PULP_CBC_CMD

def get_tr_broadcast_set(G, t, r):
    prob = LpProblem("TRBroadcastDomination", LpMinimize)
    x = {v: LpVariable(f"x_{v}", cat=LpBinary) for v in G.nodes()}
    shortest_paths = dict(nx.all_pairs_shortest_path_length(G))

    for v in G.nodes():
        prob += lpSum(max(0, t - shortest_paths[u].get(v, float("inf"))) * x[u] for u in G.nodes()) >= r

    prob += lpSum(x[v] for v in G.nodes())
    prob.solve(PULP_CBC_CMD(msg=0))
    return {v for v in G.nodes() if x[v].varValue == 1}

def get_standard_dominating_set(G):
    prob = LpProblem("StandardDomination", LpMinimize)
    x = {v: LpVariable(f"x_{v}", cat=LpBinary) for v in G.nodes()}
    for v in G.nodes():
        neighbors = list(G.neighbors(v)) + [v]
        prob += lpSum(x[u] for u in neighbors) >= 1
    prob += lpSum(x[v] for v in G.nodes())
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

def visualize_graph(G, dom_set=None, title="", cols=None):
    if cols:
        pos = {n: ((n - 1) % cols, -(n - 1) // cols) for n in G.nodes()}
    else:
        pos = nx.spring_layout(G, seed=42)

    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=500, edgecolors='black')
    if dom_set:
        nx.draw_networkx_nodes(G, pos, nodelist=dom_set, node_color='orange', node_size=500, edgecolors='black')

    plt.title(title)
    plt.axis("off")
    plt.show()

# === TOP LEVEL MENU ===
print("=== Graph Type ===")
print("1. (t, r)-Broadcast Dominating Set")
print("2. Standard Dominating Set")
graph_mode = input("Choose graph mode (1 or 2): ").strip()

if graph_mode not in {"1", "2"}:
    print("Invalid graph mode.")
    exit()

# === SHAPE MENU ===
print("\n=== Graph Shape ===")
print("a. Grid")
print("b. Polygon")
shape_choice = input("Choose shape (a or b): ").strip().lower()

if shape_choice == 'a':
    rows = int(input("Enter number of rows: "))
    cols = int(input("Enter number of columns: "))
    G = generate_grid_graph(rows, cols)
    title = f"{rows}x{cols} Grid"
elif shape_choice == 'b':
    sides = int(input("Enter number of polygon sides (≥3): "))
    if sides < 3:
        print("A polygon must have at least 3 sides.")
        exit()
    G = generate_polygon_graph(sides)
    cols = None
    title = f"{sides}-gon Polygon"
else:
    print("Invalid shape choice.")
    exit()

# === DOMINATION COMPUTATION ===
if graph_mode == "1":
    t = int(input("Enter tower strength (t): "))
    r = int(input("Enter required signal (r): "))
    dom_set = get_tr_broadcast_set(G, t, r)
    title += f"\n(t={t}, r={r}) Broadcast Domination"
else:
    dom_set = get_standard_dominating_set(G)
    title += "\nStandard Dominating Set"

print("\nDominating Set:", dom_set)
print("Domination Number:", len(dom_set))
visualize_graph(G, dom_set, title, cols if shape_choice == 'a' else None)
