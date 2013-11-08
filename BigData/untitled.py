# script to pull twitter data 

from twython import Twython
from numpy import *

# create twython creds
app_key = wZTYfz4PqHSVNgljYpcA
app_key_secret = oleEwE1L4MaKGOTZPO1GhK0BmbW4Tg6ocYarNofDkw

twit = Twython(app_key, app_key_secret, oauth_version=2)

# pull all tweets with #unemploment 
unempl = twit.search(q = '#unemploment')

