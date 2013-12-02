# script to find optimal portfolio of energy resources based on specified
# amount of CO2, MW, and cost. 

# cost/MW given from EIA.gov estimate 2013
# http://www.eia.gov/forecasts/aeo/electricity_generation.cfm

# CO2 per kWh for each source from EIA.gov (6-13-13)
# http://www.eia.gov/tools/faqs/faq.cfm?id=74&t=11

# coal is taken to be conventional coal, natural gas is taken to be 
# convetional combined cycle

from pandas import DataFrame
from numpy import *
from collections import defaultdict

# def portfolio(cost_max, CO2_max, per_dispatch, MW):

def DirichletDistro(num, sum):
	# creates a Dirchlet distribtion (D) with characteristics
	# sum(D) = sum and len(D) = 1 w/all numbers being 
	# pseudorandom

	D = random.dirichlet(ones(num), size=sum)
	return list(D.reshape(-1)) 		#convert to list

max_iter = 1000
types = ['gas', 'nuclear', 'coal', 'hydro', 'wind', 'solar', 'offshore_wind']

# create dict with the respective prices of each energy type
# levelized costs include the price of building and subsequent per MWh
costMW = {'coal': 123,
		  'gas': 67.1,
		  'nuclear': 108,
		  'hydro': 90,
		  'wind': 86,
		  'offshore_wind': 221,
		  'solar': 144}

# capacity factor repersents the amount percent of nominal capactiy 
# that can be made available at any given time (EIA)
cap_fact={'coal': .85 ,
		  'gas': .87,
		  'nuclear': .9,
		  'hydro': .52,
		  'wind': .34,
		  'offshore_wind': .37,
		  'solar': .25}

# energy load dictates that the variablitly of non-dispatchable resources
# be backed up by a certain capacity of "peaker" loads (usually gas or hydro)
# that can be turned on/off as demand fluctates 
peaker_cost = (costMW['gas'] + costMW['hydro']) / 2 
true_costMW = {}

for keys in costMW:
	true_costMW[keys] = costMW[keys] + ( (1-cap_fact[keys]) * peaker_cost)

# create dict with the CO2 emissions / MWh for each source
CO2_source = {'coal': 2130,
	   'gas': 1220,
	   'nuclear': 0,
	   'hydro': 0,  
	   'wind': 0,
	   'solar': 0,
	   'offshore_wind': 0}

# run Monte Carlo simulation to generate portfolios
i = 0
portfolio = zeros((max_iter, len(costMW)))
while (i<max_iter):
	portfolio_percent = DirichletDistro(len(costMW), 1)
	portfolio[i, :] = portfolio_percent
	i = i+1 

# transform into DataFrame and assign column names
portfolio = DataFrame(portfolio)
portfolio.columns = types

# find costs for each portfolio
costs = zeros((max_iter))
CO2 = zeros((max_iter))


for index, row in portfolio.iterrows():
	cost = []
	carbon = []
	for keys in true_costMW:
		cost.append(row[keys] * true_costMW[keys])
		carbon.append(row[keys] * CO2_source[keys])
	
	costs[index] = sum(cost)
	CO2[index] = sum(carbon)
		
# elimate portfolios who do not meet critera 


