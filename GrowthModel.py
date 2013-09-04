#! NAME: Growth Model 
# made for prof. kendricks computational economics class
# 
# Created by: Michael Lee
# 			  University of Texas at Austin

import numpy 

class Growth:

	def __init__(self):
		# define static variables
		self.tau = 0.5	  # 
		self.beta = 0.98   # discount rate 	
		self.alpha = .33	  #
		self.theta = 0.3   # 
		self.target = 


	def capital(self, K, C, i):
		K[i] = K[i-1] + self.theta * K[i-1]^self.alpha - C[i-1]

		return K 


	def production(self, P, K, i):
		P[i] = self.theta * K[i]^self.alpha

		return P 


	def utility(self, U, C, i):
		U[i] = self.beta^i * (1/ (1-self.tau))*C[i]^(1-self.tau)

