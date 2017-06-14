# -*- coding: utf-8 -*-
"""
Created on Wed Jun 14 17:18:19 2017

@author: WZhao10
"""


measurements = [
                {'Sex': 'Male', 'Nationality':'Indonesia', 'Wears Glasses':False, 'Age': 32},
                {'Sex': 'Male', 'Nationality':'China', 'Wears Glasses':True, 'Age': 31},
                {'Sex': 'Female', 'Nationality':'US', 'Wears Glasses':True, 'Age': 32},
                {'Sex': 'Female', 'Nationality':'Unknown', 'Wears Glasses':True, 'Age': 34},
                ]

from sklearn.feature_extraction import DictVectorizer
vec = DictVectorizer()
data = vec.fit_transform(measurements).toarray()
vec.get_feature_names()


#%%
import pandas as pd

df = pd.DataFrame({'Sex': ['Male', 'Male', 'Female', 'Female'],
                   'Nationality': ['Indonesia', 'China', 'US', 'Unkown'],
                    'Wears Glasses': [False, True, True, True],
                    'Age': [32, 31, 32, 34]})

df_new = pd.get_dummies(df)
