import networkx as nx
import matplotlib.pyplot as plt

def create_graph():
    G = nx.Graph()
    G.add_nodes_from([1, 2, 3]) #São os vértices
    G.add_edges_from([(1, 2), (1, 3)])  #São as arestas
    return G

def draw_graph(G, caminho = None):
    plt.figure("Árvore Binária") #Edita o título da janela
    pos = {
        1: (0, 1),    # raiz, em cima
        2: (-1, 0),   # filho esquerdo (Lembre de Árvore Binária em ED)
        3: (1, 0),    # filho direito
    }
    nx.draw(G, pos, with_labels=True, node_color='lightblue',
            edge_color='gray', node_size=2000, font_size=16) #Edita o design do grafo
   

    if caminho:
        arestas_caminho = list(zip(caminho, caminho[1:]))
        nx.draw_networkx_nodes(G, pos, nodelist=caminho,
                               node_color='salmon', node_size=2000)
        nx.draw_networkx_edges(G, pos, edgelist=arestas_caminho,
                               edge_color='red', width=4)
        nx.draw_networkx_labels(G, pos, font_size=16)

    plt.show()

G = create_graph()
caminho = (G, 2, 3)   # de uma extremidade a outra
print("Caminho:", caminho)       # [2, 1, 3]
draw_graph(G, caminho)