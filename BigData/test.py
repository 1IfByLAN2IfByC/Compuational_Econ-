from pattern.web import Twitter
from pattern.en import sentiment 

sent = []

t = Twitter()
i = None
cc = 0
for tweet in t.search('google', count=100, lang='en'):
	
	print(str(cc) + ':  '+ tweet.text+ '\n')
	sent.append([sentiment(tweet.text)])
	cc = cc + 1 




