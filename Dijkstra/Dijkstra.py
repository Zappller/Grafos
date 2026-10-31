import os, time, webbrowser
import osmnx as ox
import networkx as nx
import folium
import matplotlib.pyplot as plt

ox.settings.log_console = False
ox.settings.use_cache = True

casa = (-10.968831195960583, -37.0856515783314)   # A
ufs  = (-10.924758256888392, -37.10505198873507)   # B
centro = ((casa[0] + ufs[0]) / 2, (casa[1] + ufs[1]) / 2)

ARQUIVO = "aracaju.graphml"

# 1) Carrega do arquivo local ou baixa (com novas tentativas)
if os.path.exists(ARQUIVO):
    print("1/4 Carregando mapa salvo...")
    G = ox.load_graphml(ARQUIVO)
else:
    print("1/4 Baixando mapa...")
    G, espera = None, 10
    for tentativa in range(1, 6):
        try:
            print(f"  Tentativa {tentativa}/5")
            G = ox.graph_from_point(centro, dist=4500, network_type="drive")
            break
        except Exception as e:
            print(f"  Falhou ({type(e).__name__}). Aguardando {espera}s...")
            time.sleep(espera)
            espera *= 2
    if G is None:
        raise SystemExit("Servidor sobrecarregado. Tente de novo mais tarde.")
    ox.save_graphml(G, ARQUIVO)

# 2) Dijkstra
print("2/4 Calculando rota...")
origem  = ox.distance.nearest_nodes(G, X=casa[1], Y=casa[0])
destino = ox.distance.nearest_nodes(G, X=ufs[1],  Y=ufs[0])
rota   = nx.shortest_path(G, origem, destino, weight="length")
dist_m = nx.shortest_path_length(G, origem, destino, weight="length")
print(f"Distância: {dist_m/1000:.2f} km")

# 3) Mapa interativo
print("3/4 Gerando mapa interativo...")
coords = [(G.nodes[n]["y"], G.nodes[n]["x"]) for n in rota]
mapa = folium.Map(location=centro, zoom_start=13, tiles=None)
#API com imagem do mapa de Aracaju
folium.TileLayer(
     tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}",
    attr="Esri",           
    name="Esri",
).add_to(mapa)
folium.PolyLine(coords, color="red", weight=5).add_to(mapa)
folium.Marker(casa, tooltip="A - Casa", icon=folium.Icon(color="blue")).add_to(mapa)
folium.Marker(ufs,  tooltip="B - UFS",  icon=folium.Icon(color="green")).add_to(mapa)
mapa.fit_bounds(coords)
mapa.save("rota.html")
webbrowser.open("file://" + os.path.abspath("rota.html"))


# 4) Imagem
print("4/4 Gerando imagem...")
fig, ax = ox.plot_graph_route(G, rota, route_color="red", route_linewidth=4,
                              node_size=0, show=False, close=False)
ax.set_title(f"Casa → UFS ({dist_m/1000:.2f} km)")
plt.savefig("rota.png", dpi=200, bbox_inches="tight")
plt.show()
print("Pronto!")