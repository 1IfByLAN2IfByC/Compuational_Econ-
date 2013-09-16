from pulp import *
import numpy as np

# create list of all supply nodes

Suppliers= ['Sea', 'SD']

# create a dict with the inventories of each warehouse
supply = {'Sea': 350,
          'SD' : 600}
          
Destinations = ['Chi', 'NY', 'Top']

demand = {'Chi': 325,
          'NY' : 300,
          'Top': 275}
          
# create a distance array
dist = np.array( #Destinations
        #Chi    NY  Top
        [(1.7, 2.5, 1.8),#Sea
        (1.8, 2.5, 1.4)#SD
        ])

#create a cost/mile array
costMile = np.array([ #Destinations
        #Chi    NY  Top
        (90, 90, 90),#Sea
        (90, 90, 90)#SD
        ])

# create a cost matrix and convert to a list
costs = costMile * dist
costs.tolist()

costs = makeDict([Suppliers, Destinations], costs, 0)
# setup the cost minimization problem
prob = LpProblem('Canning Distribution Problem', LpMinimize)

# create a list of all possible routes
routes = [(S,D) for S in Suppliers for D in Destinations]

# create a dictionary to contain all referenced variables
route_var = LpVariable.dicts("Route", (Suppliers, Destinations), 0, None, LpInteger)

# add the objective function to the problem
prob += lpSum([route_var[S][D]*costs[S][D] for (S,D) in routes])

# constraints functions
for S in Suppliers:
	prob += lpSum([route_var[S][D] for D in Destinations]) <= supply[S]
"sum_of_products_out_of_suppliers_%s" %S
for D in Destinations:
	prob += lpSum([route_var[S][D] for S in Suppliers]) >= demand[D]
"sum_of_products_into_destinations_%s" %D

prob.writeLP('Transport_problem.lp')
prob.solve()

print( "status:", LpStatus[prob.status])
print( 'total cost of transport = ', value(prob.objective))





