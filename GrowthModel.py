#! NAME: Growth Model 
# made for prof. kendricks computational economics class
# 
# Created by: Michael Lee
# 			  University of Texas at Austin

import numpy 
import scipy as sci 

class Growth:

# matrix defined as follows: 
#[ Consumption, C;
#  Production, P;
#  Capital, K;
#  Utility, U      ]

# with length equal to the defined number of time periods


	def __init__(self):
		# define static variables
		self.tau = 0.5	  # 
		self.beta = 0.98   # discount rate 	
		self.alpha = .33	  #
		self.theta = 0.3   # 
		self.target = 9.10
		self.N_periods = int(9)


	def capital(self, opt, i):
		opt[2, i] = opt[2, i-1] + self.theta * opt[2, i-1]^self.alpha - opt[0, i-1]

		return K 


	def production(self, opt, i):
		opt[1,i] = self.theta * opt[2, i]^self.alpha

		return P 


	def utility(self, opt):
		for i in range(0, self.N_periods):
			opt[3, i] = self.beta^i * (1/ (1-self.tau))*opt[0, i]^(1-self.tau)
		
		goal = sum(opt[3,:]) 
		
		return goal
		
	def utility_deriv(self, opt, sign=1.0):
		dUdC = zeros((1, self.N_periods))
		dUdt = zeros((1, self.N_periods))
		
		for i in range(0, self.N_periods):
			dUdC[0,i] = sign*( (1-self.tau) * self.beta^i * (1/(1-self.tau)) * opt[0, i]^
			(1-self.tau-1))
			
			dUdt[0, i] = sign*( i * self.beta^(i-1) * (1/(1-self.tau)) * opt[0,i]^(1-self.tau)) 

			deriv = vstack((dUdC, dUdt))
		
		return deriv 
		
	
	def main(self):
		opt = zeros((4, N_periods))
				
		# define initial conditions
		K[0,0] = 7.0
		
		# create a dictionary with the constraints 
		constraint = ({
		'type': 'ineq',
		'fun': lambda K: array(K) - self.target,
		'jac': lambda x: array([0.0, 1.0]) 
		})
		
		# maximize consumption subject to the condition 
		# K_f <= K_(f-1)
		
		result = minimize(self.utility, [0.0, 0.0], args=(-1.0,), jac=utility_deriv,
		constraints=constraint, method='SLSQP', options={'disp':True})
		
		
growth = Growth()
growth.main

