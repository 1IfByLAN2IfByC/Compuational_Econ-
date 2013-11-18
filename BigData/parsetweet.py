import re 
from collections import defaultdict
location = '/users/michael/dropbox/corpus.txt'

f = open(location, 'r')

timetweeted = defaultdict(list)

def findword(string):
    return re.compile(r'\b({0})\b'.format(string), flags=re.IGNORECASE).search

artists = ['television', 'thee oh sees', 'little boots', 'rjd2', 'tontons', \
'mac demarco', 'the walkmen', 'pelican', 'judge', 'chromatics', 'tycho', 'bleached', \
'geographer', 'cloud nothings', 'cro-mags', 'true widow', 'deltron 3030', 'the julie ruin', 'xxyyxx']

for lines in f:
	numtimes = 0
	for bands in artists:
		if bands in lines:
			timetweeted[bands].append(bands)
			print(lines)
		else:
			pass

# count number of mentions
for bands in artists:
	timetweeted[bands] = len(timetweeted[bands])



