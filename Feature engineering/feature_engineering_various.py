
# coding: utf-8

# This script is a practice of feature engineering using sklearn and pandas, converting
# raw data in text to numerical features for next step. A few methods are experimented:
#     1. sklearn's DictVectorizer, converts list of key-value mappings to an array
#     2. pandas' get_dummies, converts raw data to features including dummy variables
#     3. sklearn.preprocessing.OneHotEncoder, converts array to features

# In[1]:

from IPython.display import display


# ### 1. DictVectorizer
# #### sklearn.feature_extraction.DictVectorizer

# In[2]:

from sklearn.feature_extraction import DictVectorizer
import pandas as pd

# input is a list of dictionaries, where each dict is a mapping of (k,v) where
# k is the feature name, v is the raw value
measurements = [
                {'Sex': 'Male', 'Nationality':'Indonesia', 'Wear Glasses':False, 'Age': 32},
                {'Sex': 'Male', 'Nationality':'China', 'Wear Glasses':True, 'Age': 31},
                {'Sex': 'Female', 'Nationality':'US', 'Wear Glasses':True, 'Age': 32},
                {'Sex': 'Female', 'Nationality':'Unknown', 'Wear Glasses':True, 'Age': 34},
                ]

# DictVectorizer defines the method to convert to a sparse matrix
vec = DictVectorizer(sparse=True)
# the fit_transform method converts list of dictionary to the matrix
data_sparse = vec.fit_transform(measurements)
# converts sparse matrix to an array
data = data_sparse.toarray()

# Code below denies conversion to a sparse matrix, rather it directly converts to a matrix
vec = DictVectorizer(sparse=False)
data = vec.fit_transform(measurements)

# generate dataframe. vec.get_feature_names gives the feature names
df1 = pd.DataFrame(data = data, columns = vec.get_feature_names())

display(df1)


# ### 2. get_dummies
# #### pandas.get_dummies

# In[3]:

import pandas as pd
from sklearn.ensemble import RandomForestClassifier as rf_c

# input is a dataframe already
df = pd.DataFrame({'Sex': ['Male', 'Male', 'Female', 'Female'],
                   'Nationality': ['Indonesia', 'China', 'US', 'Unkown'],
                    'Wear Glasses': [False, True, True, True],
                    'Age': [32, 31, 32, 34]})

# a random forest classifier is used to test if the algorithm takes raw data as input
clf = rf_c(n_estimators=5)

features = ['Sex', 'Nationality', 'Age']
target = ['Wear Glasses']

X = df[features].values
Y = df[target].values

try:
    clf.fit(X,Y)
except Exception as e:
    print e

# per error below, it does not take raw data


# In[4]:

# get_dummies method directly takes the dataframe in
df_new = pd.get_dummies(df)
# display shows the new dataframe, identicial to method 1 with DictVectorizer
display(df_new)

# Random forest classifier was able to run
features_new = [k for k in df_new.columns if k != 'Wear Glasses']
X_new = df_new[features_new].values
Y_new = df[target].values.reshape(-1,)

clf.fit(X_new, Y_new)


# #### Be cautious using dummy variables in regression (i.e. dummy variable trap). Drop one variable in each category, or remove intercept when fitting a regression function.
# #### Reference here (http://www.algosome.com/articles/dummy-variable-trap-regression.html)

# ### 3. OneHotEncoder
# #### sklearn.preprocessing.OneHotEncoder

# In[5]:

from sklearn import preprocessing

# input is a list of lists, containing raw data
array = [['Male', 'Indonesia', 32, False], 
         ['Male', 'China', 31, True], 
         ['Female', 'US', 32, True], 
         ['Female', 'Unknown', 34, True]]

enc = preprocessing.OneHotEncoder()

try:
    enc.fit(array)
except Exception as e:
    print e
    
# Unfortunately, OHE from sklearn does not take string data!


# In[6]:

# input is changed to numerical & boolean values
array = [[1, 0, 32, False], 
         [1, 1, 31, True], 
         [0, 2, 32, True], 
         [0, 3, 34, True]]

# added feature names..
features = ['Sex', 'Nationality', 'Age', 'Wear Glasses']

# removed the 2nd column as categorical features, because it is numerical
enc = preprocessing.OneHotEncoder(categorical_features=[0,1,3])
enc.fit(array) # code ran without problem

# n_values: the number of values per feature after OHE
print enc.n_values_

# feature_indices: indicies of features
print enc.feature_indices_

# active_features: features
print enc.active_features_

# transform method converts input to an array. Note Age is still there, only moved to the last column
print enc.transform(array).toarray()


# In[7]:

# going back to raw data, LabelEncoder could be used to 
# convert raw data to numerical classes

le = preprocessing.LabelEncoder()
le.fit(['Indonesia', 'China', 'US', 'Unknown'])

# classes_: attribute that records the actual classes
print list(le.classes_)

# transform: method that converts raw data to class labels
print le.transform(['Indonesia', 'China', 'US', 'Unknown'])

# trying an unseen class
try:
    print le.transform(['US', 'Canada'])
except Exception as e:
    print e


# In[8]:

# LabelEncoder can also directly convert dataframe columns
# However this assumes the values have an order

array = [['Male', 'Indonesia', 32, False], 
         ['Male', 'China', 31, True], 
         ['Female', 'US', 32, True], 
         ['Female', 'Unknown', 34, True]]

df = pd.DataFrame(data = array, columns = features)
display(df)

# fit_transform: directly fit the data and transform the data
df['Sex'] = le.fit_transform(df['Sex'].astype('str'))
df['Nationality'] = le.fit_transform(df['Nationality'].astype('str'))
df['Wear Glasses'] = le.fit_transform(df['Wear Glasses'].astype('bool'))
display(df)

