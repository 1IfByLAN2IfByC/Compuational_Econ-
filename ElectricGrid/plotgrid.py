import networkx as nx
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap as Basemap
from collections import OrderedDict

def plotgrid(locations, cities, demand):
	print('plotgrid')
	cities = sorted(cities)

	m = Basemap(
			projection='merc',
	        llcrnrlon=-15,
	        llcrnrlat=30,
	        urcrnrlon=40,
	        urcrnrlat= 60,
	        lat_ts=0,
	        resolution='i',
	        suppress_ticks=True)

	pos = {}
	G=nx.Graph()
	edges = []

	for key in locations:
		for i in range(0,len(locations)):
			edges.append([key, cities[i]])

	for keys, values in locations.iteritems():
		pos[keys] = m(values[1],values[0])

	G.add_edges_from(edges)
	G.edges()

	nodesize_demand = []
	nodes = []
	# strip demand size 
	for keys, values in demand.iteritems():
		nodesize_demand.append(values)

	print('drawing map')
	pos = OrderedDict(sorted(pos.items(), key=lambda t: t[0]))
	
	nx.draw_networkx(G,pos,node_size= 200 ,node_color='blue')

	m.drawcountries()
	m.drawstates()
	m.bluemarble()
	plt.title('European Cities')
	plt.show()

