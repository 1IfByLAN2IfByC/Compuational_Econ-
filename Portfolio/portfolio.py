from pandas.io.data import DataReader, DataFrame
from numpy import *
import datetime
import matplotlib.pylab as plt
from scipy import optimize

# define method for pulling financial data from yahoo!
def Stock_Close(Ticker, YYYY, m, dd):
	start_date = datetime.datetime(YYYY, m, dd)
	pull = DataReader(Ticker, "yahoo", start = start_date) 
	close =  pull["Adj Close"]

	return close

def Stock_beta(Ticker, YYYY, m dd):
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

def main():
	# define the desired portfolio characteristics
	std_max = 100	# maximum standard deviation 

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
	 'OIL':OIL, 'Natural Gas':GAS, 'Dollar Index':USD, 'GoldmanSachs': GS, 'Dominion': DOM})
	
	[m,n] = shape(X)

	# define weights of each assest held
	weights = {'GOOGLE':.2,
			    'APPLE':.1, 
			     'CAT':.1, 
		   'SPDR GOLD':.05,
	 	     	  'OIL':.1, 
	      'Natural Gas':.1, 
	     'Dollar Index':.05,
	     	 'Dominion':.1,
	     'GoldmanSachs':.2}
	
	# check to make sure sum weights = 1
	if int(sum(weights.values())) == 1:

		# run some statistics
		std = X.std()
		corr = X.corr()
		STD = [] 
		buyin = []
		current = []

		for keys in weights:
			buyin.append(X[keys][0])
			STD.append([std[keys] * weights[keys]])
			current.append([X[keys][m-1]])

		STD = sum(STD)
		profit = sum(current) - sum(buyin)

		print(corr)
		X.plot()
		plt.show()		
	else:
		print('Sum of weights does not equal 1')


	

	return X, weights, STD, corr, buyin, current

