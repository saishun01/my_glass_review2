import matplotlib.pyplot as plt
import networkx as nx

#G = nx.DiGraph()
#nx.add_path(G, [3, 5, 4, 1, 0, 2, 7, 8, 9, 6])
#nx.add_path(G, [3, 0, 6, 4, 2, 7, 1, 9, 8, 5])

population = 10
rearange_edges = 4
network = nx.barabasi_albert_graph(population, rearange_edges)

#nx.draw_networkx(G)
nx.draw_networkx(network)
plt.show()