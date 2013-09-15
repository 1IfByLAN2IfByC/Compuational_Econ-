from pulp import *

# create list of all supply nodes

Suppliers= ['Sea', 'SD']

# create a dict with the inventories of each warehouse
supply = {'Sea': 1000,
          'SD' : 4000}
          
Destinations = ['Chi', 'NY', 'Top']

demand = {'Chi': 500,
          'NY' : 1000,
          'Top': 200}
          
# create a cost matrix
costs = [ #Destinations
        #Chi    NY  Top
        [1, 5, 5],#Sea
        [1, 2, 3]#SD
        ]
     


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





