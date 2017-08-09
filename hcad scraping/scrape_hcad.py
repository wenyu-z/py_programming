# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 09:14:38 2015

@author: WZhao10
"""

## http://docs.python-guide.org/en/latest/scenarios/scrape/#web-scraping

from lxml import html
import requests
from bs4 import BeautifulSoup
import urllib2
import pandas as pd
import re
import locale
from matplotlib import pyplot as plt
import numpy as np
import time
import math

#%%

columns = ['AccountNumber',
           'OwnerName',
           'Address',
           'Zip',
           'SqFt',
           'MarketValue',
           'AppraisedValue',
           'A2006',
           'A2007',
           'A2008',
           'A2009',
           'A2010',
           'A2011',
           'A2012',
           'A2013',
           'A2014',
           'A2015',
           'L2010',
           'I2010',
           'T2010',
           'L2011',
           'I2011',
           'T2011',
           'L2012',
           'I2012',
           'T2012',
           'L2013',
           'I2013',
           'T2013',
           'L2014',
           'I2014',
           'T2014',
           'L2015',
           'I2015',
           'T2015']

page = urllib2.urlopen("file:///D:/Documents/Python Scripts/view-source_www.hcad.org_records_selectrecord_2.asp.html").read()

history_prefix1 = 'http://www.hcad.org/records/HistoryValue.asp?currenttaxyear=2011&LastTaxYear=&acct='
history_prefix2 = 'http://www.hcad.org/records/HistoryValue.asp?currenttaxyear=2015&LastTaxYear=&acct='
        
det_prefix = ['http://www.hcad.org/records/recorddetails.asp?tab=&bld=1&card=1&taxyear=','&acct=']

soup = BeautifulSoup(page)

#%%

df = pd.DataFrame(columns=columns)

i = 0
trs = soup.find_all('tr')
for k in range(len(trs)):
    tr = trs[k]
    spans = tr.find_all('td')
    if spans[1].text.startswith(' <tr bgcolor="#ffffff"'):
        account_number = re.split('[<>]',trs[k+1].find_all('td')[1].text)[4]
        zip_code = re.split('[<>]',trs[k+4].find_all('td')[1].text)[2]
        if zip_code!='77008':
            continue
        
        print account_number
        
        history_page1 = urllib2.urlopen(history_prefix1+account_number)   
        history_soup1 = BeautifulSoup(history_page1)
        history_page2 = urllib2.urlopen(history_prefix2+account_number)    
        history_soup2 = BeautifulSoup(history_page2)
        
        history1 = history_soup1.find_all('th')
        history2 = history_soup2.find_all('th')
        
        det2015 = urllib2.urlopen('2015'.join(det_prefix)+account_number)
        det2015_soup = BeautifulSoup(det2015)
        valuations = det2015_soup.find_all('table')[23].find_all('td')
        Land2014 = int(valuations[9].text.replace(',',''))
        Impr2014 = int(valuations[15].text.replace(',',''))
        Tota2014 = int(valuations[21].text.replace(',',''))
        Land2015 = int(re.split('\r\n',valuations[12].text)[1].replace(',',''))
        Impr2015 = int(re.split('\r\n',valuations[18].text)[1].replace(',',''))
        Tota2015 = int(re.split('\r\n',valuations[24].text)[1].replace(',','')) 
        
        det2013 = urllib2.urlopen('2013'.join(det_prefix)+account_number)
        det2013_soup = BeautifulSoup(det2013)
        valuations = det2013_soup.find_all('table')[23].find_all('td')
        Land2012 = int(valuations[9].text.replace(',',''))
        Impr2012 = int(valuations[15].text.replace(',',''))
        Tota2012 = int(valuations[21].text.replace(',',''))
        Land2013 = int(re.split('\r\n',valuations[12].text)[1].replace(',',''))
        Impr2013 = int(re.split('\r\n',valuations[18].text)[1].replace(',',''))
        Tota2013 = int(re.split('\r\n',valuations[24].text)[1].replace(',','')) 
        
        det2011 = urllib2.urlopen('2011'.join(det_prefix)+account_number)
        det2011_soup = BeautifulSoup(det2011)
        valuations = det2011_soup.find_all('table')[23].find_all('td')
        Land2010 = int(valuations[9].text.replace(',',''))
        Impr2010 = int(valuations[15].text.replace(',',''))
        Tota2010 = int(valuations[21].text.replace(',',''))
        Land2011 = int(re.split('\r\n',valuations[12].text)[1].replace(',',''))
        Impr2011 = int(re.split('\r\n',valuations[18].text)[1].replace(',',''))
        Tota2011 = int(re.split('\r\n',valuations[24].text)[1].replace(',','')) 
        
        row = [re.split('[<>]',trs[k+1].find_all('td')[1].text)[4],
               re.split('[<>]',trs[k+2].find_all('td')[1].text)[2],
                re.split('[<>]',trs[k+3].find_all('td')[1].text)[2],
                re.split('[<>]',trs[k+4].find_all('td')[1].text)[2],
                int(re.split('[<>]',trs[k+5].find_all('td')[1].text)[2].replace(',','')),
                int(re.split('[<>]',trs[k+6].find_all('td')[1].text)[2][1:].replace(',','')),
                int(re.split('[<>]',trs[k+7].find_all('td')[1].text)[2][1:].replace(',','')),
                int(history1[4].text.replace(',','')),
                int(history1[3].text.replace(',','')),
                int(history1[2].text.replace(',','')),
                int(history1[1].text.replace(',','')),
                int(history1[0].text[1:].replace(',','')),
                int(history2[4].text.replace(',','')),
                int(history2[3].text.replace(',','')),
                int(history2[2].text.replace(',','')),
                int(history2[1].text.replace(',','')),
                int(history2[0].text[1:].replace(',','')),
                Land2010,
                Impr2010,
                Tota2010,
                Land2011,
                Impr2011,
                Tota2011,
                Land2012,
                Impr2012,
                Tota2012,
                Land2013,
                Impr2013,
                Tota2013,
                Land2014,
                Impr2014,
                Tota2014,
                Land2015,
                Impr2015,
                Tota2015,
                ]

        df.loc[i] = row
        i += 1
        
    else:
        pass

#%%

#plt.figure(1)
#df_th = df[df['Zip']=='77079']
#df_us = df[df['OwnerName']=='HOWARD RONALD M']
#
#for k in df_th.index:
#    plt.plot(np.arange(2006,2016,1), df_th.ix[k,7:]/float(df_th.ix[k,7])*100, 'b.-')
#
#plt.plot(np.arange(2006,2016,1), df_us.ix[df_us.index[0],7:]/float(df_us.ix[df_us.index[0],7])*100, 'r*-', linewidth=6)
#
#

#%%

df = pd.read_csv(r'D:\Documents\Python Scripts\13186TrailHollow.csv')

#%%

plt.figure(1)
for k in df.index:
    y = df.ix[k,['L2010','L2011','L2012','L2013','L2014','L2015']].values
    y = y/float(df.ix[k,['L2010']].values)*100
    x = range(2010,2016)
    plt.plot(x, y, 'b.-')

df_us = df[df['OwnerName']=='ZHAO WENYU']
xt = df_us.index[0]
y = df_us.ix[xt,['L2010','L2011','L2012','L2013','L2014','L2015']].values
y = y/float(df_us.ix[xt,['L2010']].values)*100
plt.plot(x, y, 'r*-', linewidth=6)

plt.xlabel('Year')
plt.ylabel('Land Value (%)')

#%%

plt.figure(2)
for k in df.index:
    y = df.ix[k,['I2010','I2011','I2012','I2013','I2014','I2015']].values
    y = y/float(df.ix[k,['I2010']].values)*100
    x = range(2010,2016)
    plt.plot(x, y, 'b.-')

df_us = df[df['OwnerName']=='ZHAO WENYU']
xt = df_us.index[0]
y = df_us.ix[xt,['I2010','I2011','I2012','I2013','I2014','I2015']].values
y = y/float(df_us.ix[xt,['I2010']].values)*100
plt.plot(x, y, 'r*-', linewidth=6)

plt.xlabel('Year')
plt.ylabel('Improvement (%)')

#%%

plt.figure(3)
for k in df.index:
    y = df.ix[k,['T2010','T2011','T2012','T2013','T2014','T2015']].values
    y = y/float(df.ix[k,['T2010']].values)*100
    x = range(2010,2016)
    plt.plot(x, y, 'b.-')
    
df_us = df[df['OwnerName']=='ZHAO WENYU']
xt = df_us.index[0]
y = df_us.ix[xt,['T2010','T2011','T2012','T2013','T2014','T2015']].values
y = y/float(df_us.ix[xt,['T2010']].values)*100
plt.plot(x, y, 'r*-', linewidth=6)

plt.xlabel('Year')
plt.ylabel('Total (%)')

