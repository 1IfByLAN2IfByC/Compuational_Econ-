from pandas.io.data import DataReader, DataFrame
from numpy import *
import datetime
import matplotlib.pylab as plt
import statsmodels.api as sm
from collections import defaultdict

# define method for pulling Adj Close from Yahoo! Finance
def Stock_Close(Ticker, YYYY, m, dd):
	start_date = datetime.datetime(YYYY, m, dd)
	pull = DataReader(Ticker, "yahoo", start = start_date) 
	close =  pull["Adj Close"]

	return close

# define method for pulling beta from Yahoo! Finance
def Stock_beta(Ticker, YYYY, m, dd):
	start_date = datetime.datetime(YYYY, m, dd)
	pull = DataReader(Ticker, "yahoo", start = start_date) 
	beta = pull["beta"]

	return beta 

# define method for pulling GDP from FRED
def Econ_env(YYYY, m, dd):	
	start_date = datetime.datetime(YYYY, m, dd)
	GDP = DataReader('GDP', "fred", start=start_date)
	sp500 = DataReader('^GSPC', "yahoo", start=start_date)

	Array = DataFrame({'S&P':sp500["Adj Close"]})

	return Array

def regression(DataFrame, assets, back, forward):
	window = defaultdict(list)
	regr = defaultdict(list)
	projection = {}
	profit = {}

	days = back*30 
	out = forward*30

	for ass in assets:
		for i in range(len(DataFrame.index) -1 , len(DataFrame.index) - days , -1):
			window[ass].append(DataFrame[ass][i])

		temp = sm.regression.linear_model.OLS(window[ass], range(0, 
		 len(window[ass])))

		reg = temp.fit()
		regr[ass] = (reg.params)

		projection[ass] = window[ass][1] + regr[ass]*30
		profit[ass] = projection[ass] - DataFrame[ass][len(DataFrame.index) - 1]



	return regr, window, projection, profit

def Stock_stats(dataFrame, weights, assets, lam):
	[m,n] = shape(dataFrame)
	std = dataFrame.std()
	corr = dataFrame.corr()
	STD = [] 
	buyin = []
	current = []
	ewma = {}
	EWMA = []

	# transform the dataFrame index to a series so regression will
	# work

	for ass in assets:
		temp= []
		j = 0
		
		for i  in range( (len(dataFrame.index)-1), 0, -1):
			temp.append(( pow((dataFrame[ass][i] - dataFrame[ass].mean()), 2)
			 * pow(lam, i)))
			j = j+1
		
		buyin.append(dataFrame[ass][0] * weights[ass] )
		STD.append([std[ass] * weights[ass]])
		current.append([dataFrame[ass][m-1] * weights[ass]])
		
		# sum the squared difference and compute EWMA over time for each asset
		ewma[ass] = sqrt((1-lam) * sum(temp))
		# take the weighted average of each asset, store in list and sum
		EWMA.append(ewma[ass] * weights[ass])

		
	# # calculate EWMA as described by Minkah
	# for ass in assets:
	# 	for i  in range( (len(dataFrame.index)-1), 0, -1):
	# 		temp.append((pow(dataFrame[ass][i] - dataFrame[ass].mean(), 2) * pow(lam, i)))
		
	# 	ewma[ass] = sqrt((1-lam) * sum(temp))
	# 	# take the weighted average of each asset, store in list and sum
	# 	EWMA.append(ewma[ass] * weights[ass])

	# calculate the line regression for the profit
	# parse and use only the past X months 

	# calculate the line of best fit for EWMA for each asset 

	# calculate the EU using the tail side risks and mean values and volility


	EWMA = sqrt(sum(EWMA))
	STD = sum(STD)
	
	return STD, EWMA

def DirichletDistro(num, sum):
	# creates a Dirchlet distribtion (D) with characteristics
	# sum(D) = sum and len(D) = 1 w/all numbers being 
	# pseudorandom

	D = random.dirichlet(ones(num), size=sum)
	return list(D.reshape(-1)) 		#convert to list

def utl(profit, EWMA, beta, delta, t): 
	return 1 - exp( - beta * (profit / EWMA) * pow(delta, t) )

def main():
	# define the desired portfolio characteristics
	std_max = 250		# maximum standard deviation 
	MAX_ITERS = 10 		# max number of iterations
	lam = .94  			# exponential decay number 
	exit_date = 12  	# when you sell stocks (in months)
	window_begin = 6    # how far back you want to window reg. (in months)

	assets = (['GOOGLE', 'APPLE', 'CAT', 'SPDR_GOLD', 'OIL',
	 'NATURAL_GAS', 'USD', 'GOLDMANSACHS', 'DOMINION'])

	print('Pulling data from Yahoo! Finance')
	# Pull data from Yahoo! Finance 
	GOOG= Stock_Close('GOOG', 2010, 1, 1)
	AAPL = Stock_Close('AAPL', 2010,1, 1)
	SP500 = Stock_Close('^GSPC', 2010, 1, 1)
	CAT = Stock_Close('CAT', 2010, 1, 1)
	GOLD = Stock_Close('GLD', 2010, 1, 1)
	GAS = Stock_Close('GAZ', 2010, 1, 1)
	OIL = Stock_Close('OIL', 2010, 1, 1)
	GS = Stock_Close('GS', 2010, 1, 1)
	DOM = Stock_Close('D', 2010, 1, 1)
	
	# FX currency
	USD = Stock_Close('UUP', 2010, 1, 1)

	# create a dataframe housing the above
	X = DataFrame({'GOOGLE':GOOG, 'APPLE':AAPL, 'CAT':CAT, 'SPDR_GOLD':GOLD,
	 'OIL':OIL, 'NATURAL_GAS':GAS, 'USD':USD, 'GOLDMANSACHS': GS, 'DOMINION':DOM})

	best = zeros(((3+len(assets)), MAX_ITERS))

	print('Running monte carlo simulation')
	for i in range(1, MAX_ITERS):
		print('Percent Done: \t' + str(float(i)/float(MAX_ITERS)*100)+' %')
		numWeight = DirichletDistro(len(assets),1)
		
		# check to make sure sum weights = 1
		if int(sum(numWeight)) < 1.01: # account for floating point err
			#create dictionary of weights for each of the assets
			weights = dict(zip(assets, numWeight))

			STD, EWMA = Stock_stats(X, weights, assets, lam)

			# calculate price at future period 
			regression, window, projection, profit = X, assets, window_begin, exit_date) 
			
			EU = utl(profit, )
			

			# check if the EWMA is above the specified limit
			if best[1, i] >std_max:
				best[:, i] = zeros(( (2+len(assets)) )) # drop the trial 
				# add more critera here...
			else:
				# store trial profit, EWMA, STD in column of best
				best[0:3, i] = [profit, EWMA, STD]
				best[3::, i] = numWeight

		else:
			print('Sum of weights does not equal 1')

	# # now that we have the monte carlo simulation setup, eliminate
	# # all trials that do not meet critera
	# for i in range(1, MAX_ITERS):
	# 	if best[1, i] >std_max:
	# 		best[:, i] = zeros(( (2+len(assets)) )) # drop the trial 
	# 		# add more critera here...
	# 	else:
	# 		pass


	maxP = max(best[0,:]) 
	print( "The maximum profit to be made is: %f") % maxP
	# find the column where the sum is equal to the max
	opt = where(best[0,:] == maxP)
	OptimalAllocation = dict(zip(assets, [float(xx) for xx in best[2:,opt]]))
	print('\n The optimal asset allocation in the portfolio is:')
	print(OptimalAllocation)
	return X, best, OptimalAllocation, assets


