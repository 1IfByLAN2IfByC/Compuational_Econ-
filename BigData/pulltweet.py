# script to pull twitter data 

from twython import Twython, TwythonStreamer
from numpy import *
import nltk 
import pprint 
import csv
import codecs 
from collections import defaultdict
from dateutil import parser

tokenizer = None 
tagger = None 

def normalize(s):
	if type(s) == unicode:
		return s.encode('utf8', 'ignore')
	else:
		return str(s)


# write to a csv for classification 
# ofile = open('/Users/Michael/git/CompEcon/BigData/corpus.csv', mode='w', encoding ='uft-8', errors='replace')

# writer = csv.writer(ofile)

# create twython creds
app_key = 'wZTYfz4PqHSVNgljYpcA'
app_key_secret = 'oleEwE1L4MaKGOTZPO1GhK0BmbW4Tg6ocYarNofDkw'
access_token = '265679542-Tfk6oCfq259Smu8PD557qkdIOgVJCSxugKMouDnj'
access_token_secret = 'W9lYBystbtl8ILhn85oZYH5wGnSq4q6ClTFP4nKrcWoNL'

twit = Twython(app_key, app_key_secret)

# pull all tweets with #google
search = twit.search(q = 'google', lang = 'en', since=2013-01-01, count=3000)
tweets = search['statuses']

store = defaultdict(list)


# with open('/Users/Michael/git/CompEcon/BigData/corpus.txt','w') as ofile:
# 	for tweet in tweets:
# 		dt = tweet['created_at']

# 		# parse all the timestamps
# 		dt = dt[4:19] + ' ' + dt[-4:]
# 		dt = parser.parse(dt)

# 		s = normalize(tweet['text'])
# 		print(s + '\n\n\n')
# 		store[dt] = s
# 		ofile.write(s + '\n')

class Streamer(TwythonStreamer):
	def on_success(self, data):
		if 'text' in data:
			print data['text'].encode('utf-8')

	def on_error(self, status_code, data):
		print(status_code)

stream = Streamer(app_key, app_key_secret, access_token, access_token_secret)

stream.statuses.filter( track= 'apple', language='en')




