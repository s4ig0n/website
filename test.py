import networkx as nx
import numpy as np

def create_graph(vertices, edges):
    G = nx.Graph()
    G.add_nodes_from(vertices)
    G.add_edges_from(edges)
    return G

def get_dominating_set(G):
    # Approximate minimum dominating set using greedy algorithm
    dom_set = nx.algorithms.approximation.min_weighted_dominating_set(G)
    return dom_set

def main():
    # Example inputs
    vertices = [0, 1, 2, 3, 4, 5]
    edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (0, 5)]
    
    G = create_graph(vertices, edges)
    
    # Get dominating set and domination number
    dominating_set = get_dominating_set(G)
    domination_number = len(dominating_set)
    
    print("Graph vertices:", G.nodes())
    print("Graph edges:", G.edges())
    print("Dominating Set:", dominating_set)
    print("Domination Number:", domination_number)

    # Optional: visualize the graph
    try:
        import matplotlib.pyplot as plt
        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=500)
        nx.draw_networkx_nodes(G, pos, nodelist=dominating_set, node_color='orange')
        plt.title("Graph with Dominating Set Highlighted")
        plt.show()
        exit
    except ImportError:
        print("matplotlib not installed — skipping visualization.")

if __name__ == "__main__":
    main()
