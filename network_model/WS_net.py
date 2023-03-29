import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import ndlib.models.epidemics as ep
import ndlib.models.ModelConfig as mc
from bokeh.io import output_notebook, show
from ndlib.viz.bokeh.DiffusionTrend import DiffusionTrend

G = nx.watts_strogatz_graph(1000,8,1)
nx.draw(G)
plt.show()

print(nx.info(G))
print(nx.average_shortest_path_length(G))
print(nx.average_clustering(G))