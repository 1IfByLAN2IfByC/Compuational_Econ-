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
import time 

# def portfolio(cost_max, CO2_max, per_dispatch, baseload, MW):
def DirichletDistro(num, sum):
	# creates a Dirchlet distribtion (D) with characteristics
	# sum(D) = sum and len(D) = 1 w/all numbers being 
	# pseudorandom

	D = random.dirichlet(ones(num), size=sum)
	return list(D.reshape(-1)) 		#convert to list

# define global constants 
max_iter = 20000
backup_rate = .7
export_location = 'ElectricData_p3.csv'
export_location_tax = 'ElectricData_tax_p3.csv'


types = ['gas', 'nuclear', 'coal', 'hydro', 'wind', 'solar', 'offshore_wind', 'peakers']

# capacity factor repersents the amount percent of nominal capactiy 
# that can be made available at any given time (EIA)
cap_fact={'coal': .85 ,
		  'gas': .87,
		  'nuclear': .9,
		  'hydro': .52,
		  'wind': .34,
		  'offshore_wind': .37,
		  'solar': .25,
		  'peakers':1}

# create dict with the CO2 emissions (lbs / MWh) for each source
CO2_source = {'coal': 2130.0,
	   'gas': 1220.0,
	   'nuclear': 0.0,
	   'hydro': 0.0,  
	   'wind': 0.0,
	   'solar': 0.0,
	   'offshore_wind': 0.0, 
	   'peakers': (.8*1220.0) + (.2*0) # account for the CO2 of 
	   # having backup peaker units assuming 80% of the power 
	   # comes from gas turbine and 20% hydro
}

# create dict with the respective prices of each energy type
# levelized costs include the price of building and subsequent per MWh

# energy load dictates that the variablitly of non-dispatchable resources
# be backed up by a certain capacity of "peaker" loads (usually gas or hydro)
# that can be turned on/off as demand fluctates 
costMW = {'coal': 123.0,
		  'gas': 67.1 * 1.5,
		  'nuclear': 108.0,
		  'hydro': 90.0,
		  'wind': 86.0,
		  'offshore_wind': 221.0,
		  'solar': 144.0,
		  'peakers': (.8*67.1) + (.2*90.0) # account for the cost of 
	   # having backup peaker units assuming 80% of the power 
	   # comes from gas turbine and 20% hydro
	   }



# run Monte Carlo simulation to generate portfolios
i = 0
portfolio = zeros((max_iter, len(costMW)))
t = time.time()
while (i<max_iter):
	portfolio_percent = zeros((len(costMW)))
	portfolio_percent[:-1] = DirichletDistro(len(costMW)-1, 1)
	portfolio[i, :] = portfolio_percent
	i = i+1 
print('Dirchlet Finished')
print('Elapsed time: ' + str(time.time() -t ))

# transform into DataFrame and assign column names
portfolio = DataFrame(portfolio)
portfolio.columns = types

# eliminate portfolios that do not meet base load criteria
# base load: nuclear + coal + gas
t = time.time()
for index, row in portfolio.iterrows():
	# assume that operators want a backup ratio for non-dispatchable
	portfolio['peakers'].ix[index] = backup_rate*(row['wind'] + row['offshore_wind']
	 + row['solar'])
	
	if row['nuclear'] + row['gas'] + row['coal'] < baseload:
		portfolio = portfolio.drop(index)
print('Culling Finished')
print('Elapsed time: ' + str(time.time() -t ))

# reset index after all the dropping
portfolio = portfolio.reset_index(drop=True)
portfolio_tax = portfolio


for XX in range(20,150, 20):
	carbon_tax = double(XX)
	port_location = 'portfolio_' + str(XX) + '.csv'
	port_location_tax = 'portfolio_tax_' + str(XX) +'.csv'
	print(carbon_tax)

	carbon_cost = {}
	for keys, values in costMW.iteritems():
		carbon_cost[keys] = costMW[keys] + (carbon_tax * (CO2_source[keys]/2000.0))
		print(keys, costMW[keys], CO2_source[keys]/2000)
		
	## find costs for each portfolio
	costs = zeros((len(portfolio)))
	costs_wTax = zeros((len(portfolio)))
	CO2 = zeros((len(portfolio)))
	CO2_wTax = zeros((len(portfolio)))

	# calculate the cost and carbon output of each portfolio
	for index, row in portfolio.iterrows():
		cost = []
		carbon = []
		cost_wTax = []
		carbon_wTax = []	

		for keys in costMW:
			cost.append(row[keys] * costMW[keys])
			carbon.append(row[keys] * CO2_source[keys])

			cost_wTax.append(row[keys] * carbon_cost[keys])
			carbon_wTax.append(row[keys] * CO2_source[keys])

		costs[index] = sum(cost)
		CO2[index] = sum(carbon)
		costs_wTax[index] = sum(cost_wTax)
		CO2_wTax[index] = sum(carbon_wTax)

		# print((float(index)/float(len(portfolio.index))*100))
	# # eliminate portfolios who do not meet cost criteria 
	# delete_index = []
	# delete_index_tax = []
	# for i in range(0, len(portfolio)):
	# 	if costs[i] > cost_max:
	# 		delete_index.append(i)

	# for i in range(0, len(portfolio_tax)):
	# 	if costs_wTax[i] > cost_max:
	# 		delete_index_tax.append(i)


	# costs = delete(costs, delete_index) 	# trash the element from costs
	# portfolio = portfolio.drop(portfolio.index[delete_index])	# trash corresponding portfolio
	# CO2 = delete(CO2, delete_index) 	# trash the element from 		

	# costs_wTax = delete(costs_wTax, delete_index_tax) 	# trash the element from costs
	# portfolio_tax = portfolio_tax.drop(portfolio_tax.index[delete_index_tax])	# trash corresponding portfolio
	# CO2_wTax = delete(CO2_wTax, delete_index_tax) 	# trash the element from 	

	# # reset index after all the dropping
	# portfolio = portfolio.reset_index(drop=True)
	# portfolio_tax = portfolio_tax.reset_index(drop=True)


	# # eliminate portfolios that do notCO meet CO2 criteria
	# delete_index = [] 
	# delete_index_tax = []

	# for i in range(1, len(portfolio)):
	# 	if CO2[i] > CO2_max:
	# 		delete_index.append(i)

	# for i in range(1, len(portfolio_tax)):
	# 	if CO2_wTax[i] > CO2_max:
	# 		delete_index_tax.append(i)

	# costs = delete(costs, delete_index) 	# trash the element from costs
	# portfolio = portfolio.drop(portfolio.index[delete_index])	# trash corresponding portfolio
	# CO2 = delete(CO2, delete_index) 	# trash the element from CO2

	# costs_wTax = delete(costs_wTax, delete_index_tax) 	# trash the element from costs
	# portfolio_tax = portfolio_tax.drop(portfolio_tax.index[delete_index_tax])	# trash corresponding portfolio
	# CO2_wTax = delete(CO2_wTax, delete_index_tax) 	# trash the element from CO2

	# # reset index after all the dropping
	# portfolio = portfolio.reset_index(drop=True)
	# portfolio_tax = portfolio_tax.reset_index(drop=True)

	# normalize CO2 and cost by the specified maxes for plottitng
	export = zeros((len(CO2), 4))
	export[:,0] = CO2
	export[:,1] = costs 
	export[:,2] = CO2 / CO2_max
	export[:,3] = costs / cost_max

	export_tax = zeros((len(CO2_wTax), 4))
	export_tax[:,0] = CO2_wTax
	export_tax[:,1] = costs_wTax 
	export_tax[:,2] = CO2_wTax / CO2_max
	export_tax[:,3] = costs_wTax / cost_max

	# export normalized data to specified file location
	savetxt(export_location, export, delimiter=',')
	savetxt(export_location_tax, export_tax, delimiter=',')

	# find min and max
	minCO2 = where(CO2 == min(CO2))
	maxCO2 = where(CO2 == max(CO2))
	mincost = where(costs == min(costs))
	maxcost = where(costs == max(costs))

	minCO2_tax = where(CO2_wTax == min(CO2_wTax))
	maxCO2_tax = where(CO2_wTax == max(CO2_wTax))
	mincost_tax = where(costs_wTax == min(costs_wTax))
	maxcost_tax = where(costs_wTax == max(costs_wTax))

	# hackery to transform the above tuples to ints
	for i in minCO2:
		minCO2 = int(i)
	for i in maxCO2:
		maxCO2 = int(i)
	for i in mincost:
		mincost = int(i)
	for i in maxcost:
		maxcost = int(i)

	for i in minCO2_tax:
		minCO2_tax = int(i)
	for i in maxCO2_tax:
		maxCO2_tax = int(i)
	for i in mincost_tax:
		mincost_tax = int(i)
	for i in maxcost_tax:
		maxcost_tax = int(i)


	port = zeros((8,4))
	port_tax = zeros((8,4))
	port_cost = zeros((1,4))
	port_CO2 = zeros((1,4))
	port_cost_tax = zeros((1,4))
	port_CO2_tax = zeros((1,4))

	port[:,0] = portfolio[:].ix[minCO2]
	port[:,1] = portfolio[:].ix[maxCO2]
	port[:,2] = portfolio[:].ix[mincost]
	port[:,3] = portfolio[:].ix[maxcost]

	port_CO2[0,0] = CO2[minCO2]
	port_CO2[0,1] = CO2[maxCO2]
	port_CO2[0,2] = CO2[mincost]
	port_CO2[0,3] = CO2[maxcost]

	port_cost[0,0] = costs[minCO2]
	port_cost[0,1] = costs[maxCO2]
	port_cost[0,2] = costs[mincost]
	port_cost[0,3] = costs[maxcost]


	port_tax[:,0] = portfolio_tax[:].ix[minCO2_tax]
	port_tax[:,1] = portfolio_tax[:].ix[maxCO2_tax]
	port_tax[:,2] = portfolio_tax[:].ix[mincost_tax]
	port_tax[:,3] = portfolio_tax[:].ix[maxcost_tax]

	port_CO2_tax[0,0] = CO2_wTax[minCO2_tax]
	port_CO2_tax[0,1] = CO2_wTax[maxCO2_tax]
	port_CO2_tax[0,2] = CO2_wTax[mincost_tax]
	port_CO2_tax[0,3] = CO2_wTax[maxcost_tax]

	port_cost_tax[0,0] = costs_wTax[minCO2_tax]
	port_cost_tax[0,1] = costs_wTax[maxCO2_tax]
	port_cost_tax[0,2] = costs_wTax[mincost_tax]
	port_cost_tax[0,3] = costs_wTax[maxcost_tax]

	print('cost @ max CO2 without taxes: ' + str(costs[maxCO2]))
	print('cost @ max CO2 with taxes: ' + str(costs_wTax[maxCO2]))
	# print('@min cost, cost= ' + str(costs[where(costs == min(costs))]) + '\t CO2= ' + str(CO2[where(costs == min(costs))]))
	# print(where(costs == min(costs)))

	# print('@min CO2, cost= ' + str(costs[where(CO2 == min(CO2))])+'\t CO2= ' + str(CO2[where(CO2 == min(CO2))]))
	# print(where(CO2 == min(CO2)))

	# print('@max cost, cost= ' + str(costs[where(costs == max(costs))]) + '\t CO2= ' + str(CO2[where(costs == max(costs))]))
	# print(where(costs == max(costs)))

	# print('@max CO2, cost= ' + str(costs[where(CO2 == max(CO2))])+'\t CO2= ' + str(CO2[where(CO2 == max(CO2))]))
	# print(where(CO2 == max(CO2)))

	# export portfolios to csv
	savetxt(port_location, vstack((port, port_cost, port_CO2)), delimiter=',')
	savetxt(port_location_tax, vstack((port_tax, port_cost_tax, port_CO2_tax)), delimiter=',')



