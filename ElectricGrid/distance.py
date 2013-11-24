# function finds gps distance based on the haversine formula:
import math 
def distance(lat1, lon1, lat2, lon2):
	r = 6371 # radius of earth in kilometers

	# convert to radians
	rad = lambda x: x * (3.14/180) 

	# haversine function
	a = (math.sin(rad( abs(lat1 - lat2)) / 2) * math.sin(rad(abs(lat1 - lat2)) / 2)
	 + math.sin(rad(lon1-lon2)/2) * math.sin(rad(abs(lon1-lon2)/2)) 
	 * math.cos(rad(lon1)) * math.cos(rad(lon2)))
	
	c = 2 * math.atan2(math.sqrt(abs(a)), math.sqrt(1-abs(a)))

	dist = r * c 

	return dist  
