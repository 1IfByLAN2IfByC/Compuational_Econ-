from numpy import *
from collections import defaultdict
from distance import distance

cities = ['london', 'paris', 'madrid', 'frankfurt', 'lisbon', 'warsaw', 'milan', 'athens']

location = defaultdict(list)
population = defaultdict(list)

location = {'london': [51.5085, -.1257], 
		   'paris': [48.8534, 2.3488 ],
		   'frankfurt': [50.1166, 8.6833],
		   'madrid': [40.4165, -3.7025], 
		   'athens': [37.9794, 23.7168],
		   'milan': [45.4642, 9.189],
		   'lisbon':[38.7167, -9.1333],
		   'warsaw': [52.2298, 21.0117]}

population = {'london': 9.576,
			   'paris': 10.896,
			   'frankfurt': 2.303,
			   'madrid': 6.097,
			   'athens': 3.510,
			   'milan': 5.248,
			   'lisbon': 2.697,
			   'warsaw': 1.715}

# transform location to tuple
location_tuple = []
for keys, values in location.iteritems():
	# london / paris/ madrid/ frankfurt/ lisbon/ warsaw/ milan/ athens
	location_tuple.append(values)

dist = defaultdict(list)
for keys, values in location.iteritems():
	for i in range(0,7):
		dist[keys].append(distance(values[0], values[1], location_tuple[i][0], location_tuple[i][1]))
