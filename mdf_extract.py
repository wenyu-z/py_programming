# -*- coding: utf-8 -*-
"""
Created on Fri Feb 12 09:53:54 2016

"""

import pyodbc, os, time, shutil
import pandas as pd
from matplotlib import pyplot as plt

#cnxn = pyodbc.connect('DRIVER={SQL Server}; SERVER=US1153APP249', autocommit=True)
cnxn = pyodbc.connect('DRIVER={SQL Server}; SERVER=SLB-5GDN482\SQLEXPRESS', autocommit=True)
cursor = cnxn.cursor()

def db_create(db_name, mdf_path, ldf_path):
    cnxn = pyodbc.connect('DRIVER={SQL Server}; SERVER=SLB-5GDN482\SQLEXPRESS', autocommit=True)
    cursor = cnxn.cursor()
    db_exist = pd.read_sql("SELECT * FROM master.dbo.sysdatabases WHERE name = '{0}'".format(db_name), cnxn)
    if len(db_exist)>0:
        db_offline(db_name)
        db_drop(db_name)
        
    sql_command = """
    CREATE DATABASE {0}
    ON ( FILENAME = '{1}'),
    	 ( FILENAME = '{2}')
    FOR ATTACH
    """.format(db_name, mdf_path, ldf_path)
    cursor.execute(sql_command)
    

def db_query_table_names(db_name):
    cnxn = pyodbc.connect('DRIVER={SQL Server}; SERVER=SLB-5GDN482\SQLEXPRESS', autocommit=True)
    cursor = cnxn.cursor()
    sql_command = """
    SELECT TABLE_NAME FROM {0}.INFORMATION_SCHEMA.Tables
    """.format(db_name)
    table_names = pd.read_sql(sql_command,cnxn)
    return table_names
    
    
def db_offline(db_name):
    cnxn = pyodbc.connect('DRIVER={SQL Server}; SERVER=SLB-5GDN482\SQLEXPRESS', autocommit=True)
    cursor = cnxn.cursor()
    sql_command = """
    ALTER DATABASE {0} 
    SET OFFLINE WITH ROLLBACK IMMEDIATE
    """.format(db_name)
    cursor.execute(sql_command)


def db_drop(db_name):
    cnxn = pyodbc.connect('DRIVER={SQL Server}; SERVER=SLB-5GDN482\SQLEXPRESS', autocommit=True)
    cursor = cnxn.cursor()
    sql_command = """
    DROP DATABASE {0}
    """.format(db_name)
    cursor.execute(sql_command)


#%% Testing create, query, offline, drop a DB

db_name = 'MyDB1'

mdf_dir = 'C:\SLR_Temp' 
mdf_name = '20160316025554-20160317025550.mdf'
mdf_path = os.path.join(mdf_dir, mdf_name)

ldf_dir = mdf_dir
ldf_name = '20160316025554-20160317025550.ldf'
ldf_path = os.path.join(ldf_dir, ldf_name)  

db_create(db_name, mdf_path, ldf_path)
table_names = db_query_table_names(db_name)
db_offline(db_name)
db_drop(db_name)

#%% Testing query all tables from 1 file

db_name = 'MyDB1'

mdf_dir = 'D:\SLR\SWCS-Rig3\VFD-1\History_Ziped' 
mdf_name = '20151221034039-20151222023338.mdf'
mdf_path = os.path.join(mdf_dir, mdf_name)

ldf_dir = 'D:\SLR\SWCS-Rig3\VFD-1\History_Ziped\log'
ldf_name = '20151221034039-20151222023338.ldf'
ldf_path = os.path.join(ldf_dir, ldf_name)

db_create(db_name, mdf_path, ldf_path)
table_names = db_query_table_names(db_name)

tb_list = [pd.read_sql("SELECT * FROM [{0}].[dbo].[{1}]".format(db_name, tb), cnxn) for tb in table_names.TABLE_NAME]

db_offline(db_name)
db_drop(db_name)

#%% Testing concatenating all tables from all files..

mdf_names = [f.split('.')[0] for f in os.listdir(mdf_dir) if f.endswith('.mdf')]
ldf_names = [f.split('.')[0] for f in os.listdir(ldf_dir) if f.endswith('.ldf')]

if set(mdf_names) != set(ldf_names):
    both_names = list(set(mdf_names) & set(ldf_names))
else:
    both_names = mdf_names

#for tb in table_names.TABLE_NAME:
tb = 'tbDB51'
print tb

df_list = []
for f in both_names:
    mdf_path = os.path.join(mdf_dir, f+'.mdf')
    ldf_path = os.path.join(ldf_dir, f+'.ldf')
    
    db_create(db_name, mdf_path, ldf_path)
    
    df = pd.read_sql("SELECT * FROM [{0}].[dbo].[{1}]".format(db_name, tb), cnxn)
    df['AcqTime'] = [time.mktime(k.timetuple()) for k in df.T51Date]
    df.sort_values(by='AcqTime', ascending=True, inplace=True)
    df.reset_index(inplace=True, drop=True)
    df_list.append(df)
    
    db_offline(db_name)
    db_drop(db_name)
    
df_list = pd.concat(df_list)
df_list.reset_index(inplace=True, drop=True)
plt.plot(df_list.T51Date)
plt.plot(df_list.AcqTime)

    
#%% Convert MDF files to folders of csv's, which are tables in each MDF
    
#mdf_dir = 'D:\SLR\SWCS-Rig3\VFD-1\History_Ziped' 
#ldf_dir = 'D:\SLR\SWCS-Rig3\VFD-1\History_Ziped\log'
#csv_dir = 'D:\SLR\SWCS-Rig3\VFD-1\CSV'

mdf_dir = 'D:\SLR\SWCS-Rig4\VFD-4\History' 
ldf_dir = 'D:\SLR\SWCS-Rig4\VFD-4\History\log'
csv_dir = 'D:\SLR\SWCS-Rig4\VFD-4\CSV'

mdf_names = [f.split('.')[0] for f in os.listdir(mdf_dir) if f.endswith('.mdf')]
ldf_names = [f.split('.')[0] for f in os.listdir(ldf_dir) if f.endswith('.ldf')]

if set(mdf_names) != set(ldf_names):
    both_names = list(set(mdf_names) & set(ldf_names))
else:
    both_names = mdf_names

db_name = 'MyDB1'

for f in both_names:
    mdf_path = os.path.join(mdf_dir, f+'.mdf')
    ldf_path = os.path.join(ldf_dir, f+'.ldf')
    
    db_create(db_name, mdf_path, ldf_path)
    table_names = db_query_table_names(db_name)
    tb_list = [pd.read_sql("SELECT * FROM [{0}].[dbo].[{1}]".format(db_name, tb), cnxn) for tb in table_names.TABLE_NAME]
    
    os.mkdir(os.path.join(csv_dir, f))
    for (k, df) in enumerate(tb_list):
        df.to_csv(os.path.join(csv_dir, f, table_names.TABLE_NAME.iloc[k]+'.csv'), index=False)
        
    print "\n{}".format(f)
    db_offline(db_name)
    db_drop(db_name)
    



#%% Convert HTData1 for Rig 5 (VFD1 & VFD2)

mdf_dir = 'D:\SLR\SWCS-Rig5\VFD1' 
ldf_dir = 'D:\SLR\SWCS-Rig5\VFD1'
csv_dir = 'D:\SLR\SWCS-Rig5\VFD1\CSV\HTData1'

db_name = 'MyDB3'

mdf_names = [f.split('.')[0] for f in os.listdir(mdf_dir) if f.endswith('.mdf')]
ldf_names = [f.split('.')[0] for f in os.listdir(ldf_dir) if f.endswith('.ldf')]


mdf_path = os.path.join(mdf_dir, 'HTData1.mdf')
ldf_path = os.path.join(ldf_dir, 'HTData1Log.ldf')

db_create(db_name, mdf_path, ldf_path)
table_names = db_query_table_names(db_name)
tb_list = [pd.read_sql("SELECT * FROM [{0}].[dbo].[{1}]".format(db_name, tb), cnxn) for tb in table_names.TABLE_NAME]

for (k, df) in enumerate(tb_list):
    df.to_csv(os.path.join(csv_dir, table_names.TABLE_NAME.iloc[k]+'.csv'), index=False)
    
db_offline(db_name)
db_drop(db_name)


#%% (Rig 5, VFD1) Check date & time of HTData, and if it's duplicate of other data

import os, re, time, datetime
import pandas as pd

dir_vfd = 'D:\SLR\SWCS-Rig5\VFD1\CSV\HTData1'
files_db = [f for f in os.listdir(dir_vfd) if f.startswith('tbDB')]

pattern = '%Y-%m-%d %H:%M:%S'
for f in files_db:
    no_db = re.split('[tbDB.csv]',f)[4]
    col_time = no_db.join(('T','Date'))
    df = pd.read_csv(os.path.join(dir_vfd, f))
    if len(df)>0:
        df['AcqTime'] = [int(time.mktime(time.strptime(k, pattern))) for k in df[col_time]]
        time_min = str(datetime.datetime.fromtimestamp(df.AcqTime.min()))
        time_max = str(datetime.datetime.fromtimestamp(df.AcqTime.max()))
        print "{0}: {1} - {2}".format(col_time, time_min, time_max)
    
#HTData is not a duplicate; it is data after the history.
#CSV file folder is renamed to 20160122022442-20160122093739


#%% (Rig 5, VFD2) Check date & time of HTData

import os, re, time, datetime
import pandas as pd

dir_vfd = 'D:\SLR\SWCS-Rig5\VFD2\CSV'
files_db = [f for f in os.listdir(dir_vfd) if f.startswith('tbDB')]

pattern = '%Y-%m-%d %H:%M:%S'
for f in files_db:
    no_db = re.split('[tbDB.csv]',f)[4]
    col_time = no_db.join(('T','Date'))
    df = pd.read_csv(os.path.join(dir_vfd, f))
    if len(df)>0:
        df['AcqTime'] = [int(time.mktime(time.strptime(k, pattern))) for k in df[col_time]]
        time_min = str(datetime.datetime.fromtimestamp(df.AcqTime.min()))
        time_max = str(datetime.datetime.fromtimestamp(df.AcqTime.max()))
        print "{0}: {1} - {2}".format(col_time, time_min, time_max)
        

#CSV file folder is renamed to 20160122022457-20160122105611

#%% Convert MDF's to CSV's, which are tables in each MDF
#When CSV folder is the same location with the MDF's

vfd_dir = ['D:\SLR\Iraq Rig\Rig 201\database files vfd1\SQLHTData',
           'D:\SLR\Iraq Rig\Rig 201\database files VFD2\SQLHTData',
           'D:\SLR\Iraq Rig\Rig 202\Rig 102 VFD 1 SQLHTData\SQLHTData',
           'D:\SLR\Iraq Rig\Rig 202\Rig 102 VFD 2 SQLHTData\SQLHTData']
c_dir = 'C:\Program Files\Microsoft SQL Server'

for vfd in vfd_dir:
    if 'CSV' in os.listdir(vfd):
        pass
    else:
        os.mkdir(os.path.join(vfd, 'CSV'))
        
    csv_dir = os.path.join(vfd, 'CSV')
    
    shutil.copytree(os.path.join(vfd, 'History'), os.path.join(c_dir, 'History'))
    
    mdf_dir = os.path.join(c_dir, 'History')
    ldf_dir = os.path.join(c_dir, 'History', 'log')
#    csv_dir = 'D:\SLR\Iraq Rig\Rig 201\database files vfd1\SQLHTData\CSV'
    
    mdf_names = [f.split('.')[0] for f in os.listdir(mdf_dir) if f.endswith('.mdf')]
    ldf_names = [f.split('.')[0] for f in os.listdir(ldf_dir) if f.endswith('.ldf')]
    
    if set(mdf_names) != set(ldf_names):
        both_names = list(set(mdf_names) & set(ldf_names))
    else:
        both_names = mdf_names
    
    db_name = 'MyDB1'
    
    for f in both_names:
        mdf_path = os.path.join(mdf_dir, f+'.mdf')
        ldf_path = os.path.join(ldf_dir, f+'.ldf')
        
        db_create(db_name, mdf_path, ldf_path)
        table_names = db_query_table_names(db_name)
        tb_list = [pd.read_sql("SELECT * FROM [{0}].[dbo].[{1}]".format(db_name, tb), cnxn) for tb in table_names.TABLE_NAME]
        
        os.mkdir(os.path.join(csv_dir, f))
        for (k, df) in enumerate(tb_list):
            df.to_csv(os.path.join(csv_dir, f, table_names.TABLE_NAME.iloc[k]+'.csv'), index=False)
            
        print "\n{}".format(f)
        db_offline(db_name)
        db_drop(db_name)
    
    shutil.rmtree(os.path.join(c_dir, 'History'))
    

#%% Convert MDF's in one folder to CSV's in a different location

vfd_dir = ['D:\SLR\SWCS-Rig3\VFD-1\History_Zipped2',
           ]
csv_dir = ['D:\SLR\SWCS-Rig3\VFD-1\CSV',
           ]
c_dir = 'C:\Program Files\Microsoft SQL Server'

db_name = 'MyDB1'

for (k, vfd) in enumerate(vfd_dir):
    
    csv = csv_dir[k]
    
    shutil.copytree(vfd, os.path.join(c_dir, 'History'))
    
    mdf_dir = os.path.join(c_dir, 'History')
    ldf_dir = os.path.join(c_dir, 'History', 'log')
    
#    mdf_dir = vfd
#    ldf_dir = os.path.join(vfd, 'log')
    
    mdf_names = [f.split('.')[0] for f in os.listdir(mdf_dir) if f.endswith('.mdf')]
    ldf_names = [f.split('.')[0] for f in os.listdir(ldf_dir) if f.endswith('.ldf')]
    
    if set(mdf_names) != set(ldf_names):
        both_names = list(set(mdf_names) & set(ldf_names))
    else:
        both_names = mdf_names
    
    for f in both_names:
        mdf_path = os.path.join(mdf_dir, f+'.mdf')
        ldf_path = os.path.join(ldf_dir, f+'.ldf')
        
        db_create(db_name, mdf_path, ldf_path)
        table_names = db_query_table_names(db_name)
        tb_list = [pd.read_sql("SELECT * FROM [{0}].[dbo].[{1}]".format(db_name, tb), cnxn) for tb in table_names.TABLE_NAME]
        
        os.mkdir(os.path.join(csv, f))
        for (k, df) in enumerate(tb_list):
            df.to_csv(os.path.join(csv, f, table_names.TABLE_NAME.iloc[k]+'.csv'), index=False)
            
        print "\n{}".format(f)
        db_offline(db_name)
        db_drop(db_name)
    
    shutil.rmtree(os.path.join(c_dir, 'History'))


#%% Convert MDF's in one folder to CSV's in a different location

vfd_dir = ['F:\SLR\SWCS-Rig3\VFD-1\History',
           'F:\SLR\SWCS-Rig4\VFD-4\History',
           'F:\SLR\SWCS-Rig5\VFD1\History'
           ]
csv_dir = ['F:\SLR\SWCS-Rig3\VFD-1\CSV',
           'F:\SLR\SWCS-Rig4\VFD-4\CSV',
           'F:\SLR\SWCS-Rig5\VFD1\CSV'
           ]
c_dir = 'C:\SLR_Temp'

db_name = 'HTData'

for (k, vfd) in enumerate(vfd_dir):
    
    csv = csv_dir[k]
    
#    mdf_dir = vfd
#    ldf_dir = os.path.join(vfd, 'log')
    
    
    shutil.copytree(vfd, os.path.join(c_dir, 'History'))
    mdf_dir = os.path.join(c_dir, 'History')
    ldf_dir = os.path.join(c_dir, 'History', 'log')
    
    mdf_names = [f.split('.')[0] for f in os.listdir(mdf_dir) if f.endswith('.mdf')]
    ldf_names = [f.split('.')[0] for f in os.listdir(ldf_dir) if f.endswith('.ldf')]
    
    if set(mdf_names) != set(ldf_names):
        both_names = list(set(mdf_names) & set(ldf_names))
    else:
        both_names = mdf_names
    both_names.sort()
    
    for f in both_names:
        mdf_path = os.path.join(mdf_dir, f+'.mdf')
        ldf_path = os.path.join(ldf_dir, f+'.ldf')
        
        try:
            db_create(db_name, mdf_path, ldf_path)
            table_names = db_query_table_names(db_name)
            tb_list = [pd.read_sql("SELECT * FROM [{0}].[dbo].[{1}]".format(db_name, tb), cnxn) for tb in table_names.TABLE_NAME]
            
            os.mkdir(os.path.join(csv, f))
            for (j, df) in enumerate(tb_list):
                df.to_csv(os.path.join(csv, f, table_names.TABLE_NAME.iloc[j]+'.csv'), index=False)
                
            print "\n{}".format(f)
            db_offline(db_name)
            db_drop(db_name)
        except:
            print "Error! {0}".format(f)
    
    shutil.rmtree(os.path.join(c_dir, 'History'))






























