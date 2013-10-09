from pandas.io.data import DataReader, DataFrame
from numpy import *
import datetime
import matplotlib.pylab as plt
import statsmodels as sm
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

def Stock_stats(dataFrame, weights, assets):
	[m,n] = shape(dataFrame)
	std = dataFrame.std()
	corr = dataFrame.corr()
	STD = [] 
	buyin = []
	current = []
	OLS = []

	# transform the dataFrame index to a series so regression will
	# work
	ndx = dataFrame.reset_index()

	for keys in assets:
		buyin.append(dataFrame[keys][0])
		STD.append([std[keys] * weights[keys]])
		current.append([dataFrame[keys][m-1]])
		# OLS.append(sm.ols( dataFrame[keys], ndx))

	STD = sum(STD)
	profit = sum(current) - sum(buyin)

	return profit, STD, 

def DirichletDistro(num, sum):
	# creates a Dirchlet distribtion (D) with characteristics
	# sum(D) = sum and len(D) = 1 w/all numbers being 
	# pseudorandom

	return random.Dirchlet(np.ones(num), size=sum)

def main():
	# define the desired portfolio characteristics
	std_max = 100	# maximum standard deviation 
	MAX_ITERS = 100 	# max number of iterations

	assets = (['GOOGLE', 'APPLE', 'CAT', 'SPDR GOLD', 'OIL',
	 'NATURAL GAS', 'USD', 'GOLDMANSACHS', 'DOMINION'])

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
	X = DataFrame({'GOOGLE':GOOG, 'APPLE':AAPL, 'CAT':CAT, 'SPDR GOLD':GOLD,
	 'OIL':OIL, 'NATURAL GAS':GAS, 'USD':USD, 'GOLDMANSACHS': GS, 'DOMINION':DOM})

	# define weights of each assest held
	weights = {'GOOGLE':.2,
			    'APPLE':.1, 
			     'CAT':.1, 
		   'SPDR GOLD':.05,
	 	     	  'OIL':.1, 
	      'NATURAL GAS':.1, 
	     		 'USD':.05,
	     	 'DOMINION':.1,
	     'GOLDMANSACHS':.2}

	best = zeros((2, MAX_ITERS)))

	for i in range(1,MAX_ITERS):
		# check to make sure sum weights = 1
		if int(sum(weights.values())) == 1:
			numWeight = DirichletDistro(10,1)

			#create dictionary of weights for each of the assets
			weights = dict(zip(assets, numWeight))

			profit, STD = Stock_stats(X, weights, assets)

			# store trial profit, stdev in column of best
			best[:,i] = [ [profit], [STD] ]

		else:
			print('Sum of weights does not equal 1')

	# now that we have the monte carlo simulation setup, eliminate
	# all trials that do not meet critera
	for i in range(1, MAX_ITERS):
		if best[1, i] >std_max:
			best[:, i] = [] # drop the trial 
			# add more critera here...
		else:
			pass
	
	return X, weights, STD, profit, numWeight
