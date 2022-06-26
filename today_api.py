from urllib import request,parse
import json
from pprint import pprint
import datetime
import re

today=datetime.datetime.today()
print(today)
day_url='%s月%s日'%(today.month,today.day)
print(day_url)

# https://www.autumn-color.com/archives/24

base_url='https://ja.wikipedia.org/w/api.php?format=json&action=query&prop=revisions&rvprop=content&exintro&explaintext&redirects=1&titles='