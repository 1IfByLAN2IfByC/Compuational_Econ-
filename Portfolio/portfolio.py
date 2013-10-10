from pandas.io.data import DataReader, DataFrame
from numpy import *
import datetime
import matplotlib.pylab as plt
import statsmodels.api as sm
# from scipy import optimize

# define method for pulling financial data from yahoo!
def Stock_Close(Ticker, YYYY, m, dd):
	start_date = datetime.datetime(YYYY, m, dd)
	pull = DataReader(Ticker, "yahoo", start = start_date) 
	close =  pull["Adj Close"]

	return close

def Stock_beta(Ticker, YYYY, m, dd):
	start_date = datetime.datetime(YYYY, m, dd)
	pull = DataReader(Ticker, "yahoo", start = start_date) 
	beta = pull["beta"]

	return beta 

# define a method for pulling data from FRED
def Econ_env(YYYY, m, dd):	
	start_date = datetime.datetime(YYYY, m, dd)
	GDP = DataReader('GDP', "fred", start=start_date)
	sp500 = DataReader('^GSPC', "yahoo", start=start_date)

	Array = DataFrame({'S&P':sp500["Adj Close"]})

	return Array

def Stock_stats(dataFrame, weights, assets, lam):
	[m,n] = shape(dataFrame)
	std = dataFrame.std()
	corr = dataFrame.corr()
	STD = [] 
	buyin = []
	current = []
	EWMA = {}

	# transform the dataFrame index to a series so regression will
	# work

	for ass in assets:
		buyin.append(dataFrame[ass][0] * weights[ass] )
		STD.append([std[ass] * weights[ass]])
		current.append([dataFrame[ass][m-1] * weights[ass]])

	STD = sum(STD)
	profit = sum(current) - sum(buyin)
	
	# calculate EWMA as described by Minkah
	for ass in assets:
		temp= []
		for i  in range( (len(dataFrame.index)-1), 0, -1):
			temp.append((pow(dataFrame[ass][i] - dataFrame[ass].mean(), 2) * pow(lam, i)))

		EWMA[ass] = sqrt((1-lam) * sum(temp))

		# sum the squared difference and compute EWMA for each asset
		# EWMA[j] = sqrt( (1-lam) * sum(ewma[ass].values()))


	return profit, STD, EWMA

def DirichletDistro(num, sum):
	# creates a Dirchlet distribtion (D) with characteristics
	# sum(D) = sum and len(D) = 1 w/all numbers being 
	# pseudorandom

	D = random.dirichlet(ones(num), size=sum)
	return list(D.reshape(-1)) 		#convert to list

def main():
	# define the desired portfolio characteristics
	std_max = 100	# maximum standard deviation 
	MAX_ITERS = 100 	# max number of iterations
	lam = .94  		# exponential decay number 

	assets = (['GOOGLE', 'APPLE', 'CAT', 'SPDR_GOLD', 'OIL',
	 'NATURAL_GAS', 'USD', 'GOLDMANSACHS', 'DOMINION'])

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

	# define weights of each asset held
	# weights = {'GOOGLE':.2,
	# 		    'APPLE':.1, 
	# 		     'CAT':.1, 
	# 	   'SPDR GOLD':.05,
	#  	     	  'OIL':.1, 
	#       'NATURAL GAS':.1, 
	#      		 'USD':.05,
	#      	 'DOMINION':.1,
	#      'GOLDMANSACHS':.2}

	best = zeros(((2+len(assets)), MAX_ITERS))

	for i in range(1, MAX_ITERS):
		# check to make sure sum weights = 1
		numWeight = DirichletDistro(len(assets),1)
		
		if int(sum(numWeight)) < 1.01:
			#create dictionary of weights for each of the assets
			weights = dict(zip(assets, numWeight))

			profit, STD, EWMA = Stock_stats(X, weights, assets, lam)

			# store trial profit, stdev in column of best
			best[0:2, i] = [ profit, STD]
			best[2::, i] = numWeight

		else:
			print('Sum of weights does not equal 1')

	# now that we have the monte carlo simulation setup, eliminate
	# all trials that do not meet critera
	for i in range(1, MAX_ITERS):
		if best[1, i] >std_max:
			best[:, i] = zeros(( (2+len(assets)), 1)) # drop the trial 
			# add more critera here...
		else:
			pass


	print( max(sum(best, 0)) ) 		# print the maximum portfolio
	return X, weights, STD, profit, numWeight, best, EWMA


