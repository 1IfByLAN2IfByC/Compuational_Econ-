from numpy import *
from collections import defaultdict, OrderedDict
from distance import distance
from plotgrid import plotgrid
from transport import transport

cities = ['london', 'paris', 'madrid', 'frankfurt', 'lisbon', 'warsaw', 'milan', 'athens']
line_losses = .03 

location = defaultdict(list)
population = defaultdict(list)

# city data

location = {'london': [51.5085, -.1257], 
		   'paris': [48.8534, 2.3488 ],
		   'frankfurt': [50.1166, 8.6833],
		   'madrid': [40.4165, -3.7025], 
		   'athens': [37.9794, 23.7168],
		   'milan': [45.4642, 9.189],
		   'lisbon':[38.7167, -9.1333],
		   'warsaw': [52.2298, 21.0117]}

population = {'london': 64.2,
			   'paris': 63.8,
			   'frankfurt': 80.64,
			   'madrid': 46.95,
			   'athens': 10.78,
			   'milan': 59.78,
			   'lisbon': 10.69,
			   'warsaw': 38.54}

growthRate = {'london': .73,
			   'paris': .49,
			   'frankfurt': .23,
			   'madrid': -.43,
			   'athens': -.13,
			   'milan': .35,
			   'lisbon': .19,
			   'warsaw': .08}

# demand in billion kilowatt-hours (IEA, 2009)
demand = { 'london': 325.81,
		   'paris': 451.37,
		   'frankfurt': 509.50,
		   'madrid': 256.59,
		   'athens': 58.71,
		   'milan': 296.31,
		   'lisbon': 47.81,
		   'warsaw': 127.23}

# supply in billion kilowatt-hours (IEA, 2009)
supply = { 'london': 349.67,
		   'paris': 510.23,
		   'frankfurt': 546.71,
		   'madrid': 274.69,
		   'athens': 57.57,
		   'milan': 272.21,
		   'lisbon': 46.83,
		   'warsaw': 141.96}

# transmission losses by percent (IEA, 2009)
# http://data.worldbank.org/indicator/EG.ELC.LOSS.ZS?order=wbapi_data_value_2011+wbapi_data_value+wbapi_data_value-last&sort=asc
losses = { 'london': .08,
		   'paris': .05,
		   'frankfurt': .04,
		   'madrid': .09,
		   'athens': .05,
		   'milan': .07,
		   'lisbon': .08,
		   'warsaw': .07}

# transform location unsorted dict to an ordered dict (needed for construcing...
# following distance dict)
location = OrderedDict(sorted(location.items(), key=lambda t: t[0]))
demand = OrderedDict(sorted(demand.items(), key=lambda t: t[0]))

# transform location to list (in alphabetical order)
location_tuple = []
for keys, values in location.iteritems():
	location_tuple.append(values)

# caluclate distance for each city to every other city
dist = defaultdict(list)
for keys, values in location.iteritems():
	for i in range(0,8):
		dist[keys].append(distance(values[0], values[1], location_tuple[i][0], location_tuple[i][1]))

plotgrid(location, cities, demand)



# supply = transport(dist, losses)







