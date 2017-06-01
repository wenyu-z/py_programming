# -*- coding: utf-8 -*-
"""
Created on Thu Nov 17 14:34:25 2016

@author: WZhao10
"""

import datetime
import win32clipboard

win32clipboard.OpenClipboard()
data = win32clipboard.GetClipboardData()
win32clipboard.CloseClipboard()

utc = raw_input("\nUTC (default {0}): ".format(data))

if utc == '':
    utc = int(data)
else:
    utc = int(utc)
    
dt = datetime.datetime.fromtimestamp(utc)

print '\n'
print dt
