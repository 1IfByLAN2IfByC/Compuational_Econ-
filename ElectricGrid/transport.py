# accounts for losses and returns a cost dataframe
from pandas import DataFrame
from pulp import *

def transport(distance, losses, global_losses, supply, demand, cities):
	# account for short range (residential) transport losses

cost = zeros((len(cities), len(cities) ))

# convert dict to dataframe because python
dist = DataFrame(dist)

for keys, values in losses.iteritems():
	print(dist[keys], losses[keys])
	dist[keys]= (1 + global_losses*dist[keys] + losses[keys])

		




 

	return supply
