import networkx as nx
import matplotlib.pyplot as plt

def create_graph():
    G = nx.Graph()
    G.add_nodes_from([1, 2, 3]) #São os vértices
    G.add_edges_from([(1, 2), (1, 3)])  #São as arestas
    return G

def draw_graph(G):
    plt.figure("Árvore Binária") #Edita o título da janela
    pos = {
        1: (0, 1),    # raiz, em cima
        2: (-1, 0),   # filho esquerdo (Lembre de Árvore Binária em ED)
        3: (1, 0),    # filho direito
    }
    nx.draw(G, pos, with_labels=True, node_color='lightblue',
            edge_color='gray', node_size=2000, font_size=16) #Edita o design do grafo
    plt.show()

G = create_graph()
draw_graph(G)