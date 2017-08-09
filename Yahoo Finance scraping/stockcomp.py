# -*- coding: utf-8 -*-
"""
Created on Tue Oct 18 11:39:15 2016

@author: WZhao10
"""

import pandas as pd
import numpy as np
import os, datetime
from matplotlib import pyplot as plt

ticker1 = 'GRPOF'
ticker2 = 'TWMJF'

dirn = r'D:\Documents\SLB Personal\Benefits'
df1 = pd.read_csv(os.path.join(dirn, 'GRPOF.csv'))
df2 = pd.read_csv(os.path.join(dirn, 'TWMJF.csv'))

df1 = df1.apply(lambda x: pd.to_numeric(x, errors='ignore'))
df2 = df2.apply(lambda x: pd.to_numeric(x, errors='ignore'))

df1['DT'] = [datetime.datetime.strptime(string, '%Y-%m-%d') for string in df1.Date]
df2['DT'] = [datetime.datetime.strptime(string, '%Y-%m-%d') for string in df2.Date]

plt.figure()
plt.plot(df1.DT, df1['Adj Close'], 'r.:', label=ticker1)
#plt.plot(df2.DT, df2['Adj Close'], 'b.:', label=ticker2)
plt.ylabel('Adj Close')
plt.legend(loc='upper left')
plt.grid()


#%%

from yahoo_finance import Share

stock1 = Share('GRPOF')
stock2 = Share('TWMJF')

list1 = stock1.get_historical('2016-01-01', '2017-05-18')
list2 = stock2.get_historical('2016-01-01', '2017-05-18')



#%%

import urllib2, datetime
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

def urlgen(ticker, date1, date2):
    m1 = int(date1.split('-')[1])-1
    d1 = int(date1.split('-')[2])
    y1 = int(date1.split('-')[0])
    m2 = int(date2.split('-')[1])-1
    d2 = int(date2.split('-')[2])
    y2 = int(date2.split('-')[0])
    
    part1 = 'http://chart.finance.yahoo.com/table.csv?s='
    url0 = """%s%s&a=%d&b=%d&c=%d&d=%d&e=%d&f=%d&g=d&ignore=.csv"""
    
    params = (part1, ticker, m1, d1, y1, m2, d2, y2)
    url = url0 % params
    return url

def list2df(html):
    html = html.split('\n')
    data = np.array([k.split(',') for k in html[1:-1]])
    header = html[0].split(',')
    df = pd.DataFrame(data = data, columns = header)
    return df

ticker1 = 'GRPOF'
ticker2 = 'TWMJF'

ticker1 = 'BABA'
ticker2 = 'AMZN'

date1 = '2015-01-01'
date2 = '2017-02-14'

response1 = urllib2.urlopen(urlgen(ticker1, date1, date2))
html1 = response1.read()
df1 = list2df(html1); del html1

response2 = urllib2.urlopen(urlgen(ticker2, date1, date2))
html2 = response2.read()
df2 = list2df(html2); del html2

df1 = df1.apply(lambda x: pd.to_numeric(x, errors='ignore'))
df2 = df2.apply(lambda x: pd.to_numeric(x, errors='ignore'))

df1['DT'] = [datetime.datetime.strptime(string, '%Y-%m-%d') for string in df1.Date]
df2['DT'] = [datetime.datetime.strptime(string, '%Y-%m-%d') for string in df2.Date]

plt.figure()
#plt.plot(df1.DT, df1['Adj Close'], 'r.:', label=ticker1)
plt.plot(df2.DT, df2['Adj Close'], 'b.:', label=ticker2)
plt.ylabel('Adj Close')
plt.legend(loc='upper left')
plt.grid()

plt.figure()
plt.plot(df1.DT, df1['Adj Close'].values/df1['Adj Close'].loc[len(df1)-1], 'r.:', label=ticker1)
plt.plot(df2.DT, df2['Adj Close'].values/df2['Adj Close'].loc[len(df2)-1], 'b.:', label=ticker2)
plt.ylabel('return')
plt.legend(loc='upper left')
plt.grid()

#%%

from bs4 import BeautifulSoup
import urllib2
from re import sub
import pandas as pd

#all actions
url = 'http://www.marketwatch.com/investing/stock/hal/insideractions'
url_prefix = 'http://www.marketwatch.com'

page = urllib2.urlopen(url).read()
soup = BeautifulSoup(page, "lxml")

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


import urllib2, datetime
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

def urlgen(ticker, date1, date2):
    m1 = int(date1.split('-')[1])-1
    d1 = int(date1.split('-')[2])
    y1 = int(date1.split('-')[0])
    m2 = int(date2.split('-')[1])-1
    d2 = int(date2.split('-')[2])
    y2 = int(date2.split('-')[0])
    
    part1 = 'http://chart.finance.yahoo.com/table.csv?s='
    url0 = """%s%s&a=%d&b=%d&c=%d&d=%d&e=%d&f=%d&g=d&ignore=.csv"""
    
    params = (part1, ticker, m1, d1, y1, m2, d2, y2)
    url = url0 % params
    return url

def list2df(html):
    html = html.split('\n')
    data = np.array([k.split(',') for k in html[1:-1]])
    header = html[0].split(',')
    df = pd.DataFrame(data = data, columns = header)
    return df

ticker1 = 'RTM'
ticker2 = 'XLB'

date1 = '2008-01-01'
date2 = '2017-02-14'

response1 = urllib2.urlopen(urlgen(ticker1, date1, date2))
html1 = response1.read()
df1 = list2df(html1); del html1

response2 = urllib2.urlopen(urlgen(ticker2, date1, date2))
html2 = response2.read()
df2 = list2df(html2); del html2

df1 = df1.apply(lambda x: pd.to_numeric(x, errors='ignore'))
df2 = df2.apply(lambda x: pd.to_numeric(x, errors='ignore'))

df1['DT'] = [datetime.datetime.strptime(string, '%Y-%m-%d') for string in df1.Date]
df2['DT'] = [datetime.datetime.strptime(string, '%Y-%m-%d') for string in df2.Date]

df1 = df1.sort_values(by = 'DT', ascending = True).reset_index(drop = True)
df2 = df2.sort_values(by = 'DT', ascending = True).reset_index(drop = True)


df2['dayofyear'] = [k.dayofyear for k in df2['DT']]
df2['year'] = [k.year for k in df2['DT']]

df_year = list(df2.groupby(by='year'))
plt.figure()
for (k, df) in df_year:
    df['perc'] = df['Adj Close']/df['Adj Close'].values[0]
    plt.plot(df['dayofyear'], df['perc'], '.:', label = k)
    
plt.legend(loc = 'best')
plt.grid()



df1['dayofyear'] = [k.dayofyear for k in df1['DT']]
df1['year'] = [k.year for k in df1['DT']]

df_year = list(df1.groupby(by='year'))
plt.figure()
for (k, df) in df_year:
    df['perc'] = df['Adj Close']/df['Adj Close'].values[0]
    plt.plot(df['dayofyear'], df['perc'], '.:', label = k)
    
plt.legend(loc = 'best')
plt.grid()

#%%
