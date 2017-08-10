# -*- coding: utf-8 -*-
"""
Created on Fri Oct 21 19:26:31 2016

@author: Wenyu
"""

from bs4 import BeautifulSoup
import urllib2
from re import sub
import pandas as pd

#all actions
url = 'http://www.marketwatch.com/investing/stock/mcd/insideractions'
url_prefix = 'http://www.marketwatch.com'

page = urllib2.urlopen(url).read()
soup = BeautifulSoup(page)

table = soup.find_all('table', 'actions')[0]

tds = table.find_all('td', 'date')
dates = [k.text for k in tds]

tds = table.find_all('td', 'name')
names = [k.text.split('\n')[1].rstrip() for k in tds]
indiv_url = [url_prefix+k.find_all('a')[0].attrs['href'] if len(k.find_all('a'))>0 else None for k in tds]
positions = [k.text.split('\n')[2] for k in tds]

tds = table.find_all('td', 'shares')
shares = [int(sub(r'[^\d.]', '', k.text)) for k in tds]

spans = table.find_all('span', 'transactionArea')
transPosNeg = [k.find_all('span', 'transPosNeg')[0].attrs['class'][1] for k in spans]
transPosNeg = ['Purchase' if k=='pos' else 'Sale' for k in transPosNeg]
transactionDesc = [k.find_all('span', 'transactionDesc')[0].text for k in spans]

tds = table.find_all('td', 'value')
value = [int(sub(r'[^\d.]', '', k.text)) for k in tds]

data = [('Date', dates),
        ('Name', names),
        ('Position', positions),
        ('Indiv_url', indiv_url),
        ('Shares', shares),
        ('TransType', transPosNeg),
        ('TransDesc', transactionDesc),
        ('Value', value)]

df = pd.DataFrame.from_items(data)

# print name and url
print df.dropna(subset = ['Indiv_url'], how='any').groupby(['Name'])['Position'].unique()

#select a name
namenow = raw_input('select a name: ')
urlnow = df[df['Name'] == namenow]['Indiv_url'].values[0]

#individual actions
page = urllib2.urlopen(urlnow).read()
soup = BeautifulSoup(page, "lxml")
table = soup.find_all('table', 'actions individual')[0]

tds = table.find_all('td', 'date')
dates = [k.text for k in tds]

tds = table.find_all('td', 'shares')
shares = [int(sub(r'[^\d.]', '', k.text)) for k in tds]

spans = table.find_all('span', 'transactionArea')
transPosNeg = [k.find_all('span', 'transPosNeg')[0].attrs['class'][1] for k in spans]
transPosNeg = ['Purchase' if k=='pos' else 'Sale' for k in transPosNeg]
transactionDesc = [k.find_all('span', 'transactionDesc')[0].text for k in spans]

tds = table.find_all('td', 'value')
value = [int(sub(r'[^\d.]', '', k.text)) for k in tds]

data = [('Date', dates),
        ('Shares', shares),
        ('TransType', transPosNeg),
        ('TransDesc', transactionDesc),
        ('Value', value)]

df_ind = pd.DataFrame.from_items(data)


#%%





