# function to store and house production function for each energy type
# cost/MW given from EIA.gov estimate 2013
# http://www.eia.gov/forecasts/aeo/electricity_generation.cfm

types = ['coal', 'gas', 'nuclear', 'hydro', 'wind', 
		 'offshore_wind', 'solar']

cities = ['london', 'paris', 'madrid', 'frankfurt', 'lisbon', 
		  'warsaw', 'milan', 'athens']


# levelized costs include the price of building and subsequent per MW
costMW = {'coal': 135,
		  'gas': 93,
		  'nuclear': 108,
		  'hydro': 90,
		  'wind': 86,
		  'offshore_wind': 221,
		  'solar': 144}

costCoal= {'paris': 136.1,
		   'london': 139.40,
		   'frankfurt': 152.6,
		   'milan': 143.68, # import cost 
		   'lisbon': 150.4,
		   'madrid': 128.55, # import cost
		   'warsaw': 79.20,
		   'athens': 136.00 } # no data!, use EU average 

