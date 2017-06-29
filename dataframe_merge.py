# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 10:09:10 2015

@author: WZhao10
"""

import pandas as pd
import numpy as np

A = pd.DataFrame()
A['Building'] = ['150','150','110','110','555','150','555','110']
A['Data'] = np.random.normal(0,1,8)
print A

B = pd.DataFrame()
B['Building'] = ['150','555','110']
B['Center'] = ['HPS','HCS','HFE']
print B

C = pd.merge(A,B)
print C

D = pd.merge(B,A)
print D

#%%

A = pd.DataFrame()
A['Building'] = ['150','150','110','110','555','150','555','110']
A['Data'] = np.random.normal(0,1,8)
print A

B = pd.DataFrame()
B['Building'] = ['150','555','110','525']
B['Center'] = ['HPS','HCS','HFE','PPC']
print B

C = pd.merge(A,B)
print C

D = pd.merge(B,A)
print D


