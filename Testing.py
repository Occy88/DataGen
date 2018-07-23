import sys, configparser
import time
import os
import requests
import random

host = 'http://dice-zdac066:5000'


card={}
card['passenger']={'id':1}
card['balance']= random.randint(0,1000)
print(card)
req=requests.post(host+'/cards',json=card)
req=requests.get(host+'/cards/')
data=req.json()
for element in data:
    print(element)


