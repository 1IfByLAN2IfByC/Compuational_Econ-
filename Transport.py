from pulp import *
import numpy as np

def equilibrium(supply, demand, sellPrice, Lease):
    # create list of all supply nodes
  Suppliers = ['Sea', 'SD', 'Warehouse']
  
    # create a dict of all demand nodes      
  Destinations = ['Chi', 'NY', 'Top', 'Warehouse', 'Albuquerque', 'Boston']

  excess = sum(supply.values()) - sum(demand.values()) 
    #positve excess values = extra supply, negative = extra demand

  # create a dict with the inventories of each warehouse
  # supply_0 = {'Sea':     1200,
  #           'SD' :     600,
  #           'Warehouse': 0}

  # demand_0 = {'Chi':   325,
  #         'NY' :     300,
  #         'Top':     275,
  #         'Warehouse': 0}
  #  # create sell price array
  # sellPrice_0 = {'Chi': 10,
  #              'NY': 14,
  #              'Top': 6,
  #              'Warehouse': 0}   

  # add in excess to a warehouse
  if excess > 0:
    demand['Warehouse'] = excess
    print('Excess Supply... shipping to warehouse')

  elif excess < 0:
    supply['Warehouse'] = excess 
    print('Excess Demand... using warehouse inventories')

  else:
    print('Supply = Demand')


  ## create a distance array
  #dist = np.array( #Destinations
  #        # Chi    NY  Top  Warehouse
  #        [(1.7, 2.5, 1.8, 2.1),#Sea
  #         (1.8, 2.5, 1.4, 2.1),#SD
  #         ( .3,  .5,  .4, 0) #Warehouse
  #        ])

  ## create a time array 
  dist = np.array( #Destinations
          # Chi    NY  Top  warehouse   Alb.  Bos
          [(29, 41, 26, 10, 21, 44),#Sea
           (29, 40, 22, 10, 11, 44),#SD
           ( 6,  6,  6, 6,  6,  6) #Warehouse
          ])

  ##create a cost/mile array
  #costMile = np.array([ #Destinations
  #        #Chi  NY  Top  Warehouse
  #        (90,  90, 90,  90),#Sea
  #        (90,  90, 90,  90),#SD
  #        (90,  90, 90,  90) #Warehouse
  #        ])
  #        
  # assuming hourly wage is 22USD        
  costMile = np.array([ #Destinations
          #Chi  NY  Top  War Al  Bos
          (22,  22, 22,  22, 22, 22),#Sea
          (22,  22, 22,  22, 22, 22),#SD
          (22,  22, 22,  22, 22, 22) #Warehouse
          ])

  # specifiy how much each transport container can hold
  capacity = 100

  # create labor price dict. & caclulate total labor cost
  lab = {}
  laborPrice = {'Sea':  3,
                 'SD':  2,
          'Warehouse':  1}  
         
  for key, Value in supply.items():
    lab[key] = laborPrice[key] * Value
    
  # create revenue matrix
  rev = {}
  for key, Value in demand.items():
    rev[key] = Value * sellPrice[key]

  # create a cost matrix and convert to a list
  costs = (costMile * dist) / capacity
  costs = costs.tolist()

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

  for v in prob.variables():
    print(v.name, ' = ', v.varValue)
    
  # calculate profit 
  profit = sum(rev.values()) - sum(lab.values()) - value(prob.objective) - Lease

  print( 'total cost of transport = ', value(prob.objective))

  return profit

def main():

  #assume a MPC
  MPC = .5
  depreciation = .3
  Lease = 100

  # create a dict with the inventories of each warehouse
  supply_0 = {'Sea':     1200,
            'SD' :     800,
            'Warehouse': 0}

  demand_0 = {'Chi':   325,
          'NY' :     300,
          'Top':     275,
          'Warehouse': 0,
          'Albuquerque': 100,
          'Boston': 150}

    # create sell price array
  sellPrice_0 = {'Chi': 10,
               'NY': 14,
               'Top': 6,
               'Warehouse': ((10+14+6)/3)* depreciation,
               'Albuquerque': 8,
               'Boston': 13}


  prof = equilibrium(supply_0, demand_0, sellPrice_0, Lease)
  print('Profit is equal to: ' + str(prof))


