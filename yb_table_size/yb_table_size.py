#!/usr/bin/env python
# coding: utf-8
DBA's need to understand keep a tab on the growing size of database and tables. This data can be helpful in ways such as:

1) Understand the table size growing over time for reporting purpose. 
2) Developer might have miss to set the purging policies on the table and thus size will continously keep on increasing.
3) A sudden drop or increase could be due to accidental deletion or insertion
4) Management might want a utilization report for each Database in multi tennant environment.

This program aim to capture the table level metrics which should help to capture the details.

Instructions:
1) This script can be deployed on platform server
2) Install the dependent module require by this script
3) Schedule this script to run on daily basis ( Cron could be an option)
# In[1]:


# Modules whcih are required for to run this program
# This program is written and tested on :
# Python 2.7.18
# YB Anywhere 2.13.X
# http                               0.2
# jsonschema                         3.2.0
# pandas                             0.24.2
# psycopg2-binary                    2.8.6

#import http.client (For python3)
import httplib 
import json
import pandas as pd
import psycopg2
from datetime import datetime


# In[2]:


#Define Variables

# YB Anywhere platform IP Address
yb_platform_addr="10.9.123.49"

# Replace Customer UUID
cUUID="3a69de7a-f74e-4124-adcd-de19484006da"

#Replace Universe UUID
uniUUID="7e848e2a-f7e1-47bc-8517-ec4a64b4e285"

yb_user_token="0d26d552-0b12-4ed6-869b-425972e6b398"

#Define Variables for connecting to YB Database

yb_db_addr="10.9.124.17"
yb_stats_db="yb_stats_db"
yb_db_port="5433"
yb_db_user="yugabyte"
yb_db_password=""
yb_db_ssl_path=""


# In[3]:


#Make a connection to the database

#conn = http.client.HTTPConnection("yb_platform_addr") -- (For python3)
conn = httplib.HTTPConnection(yb_platform_addr)

#For Https connection, use HTTPSConnection
#conn = http.client.HTTPSConnection("yb_platform_addr")

## Repalce your API Token
headers = {
    'Content-Type': "application/json",
    'X-AUTH-YW-API-TOKEN': yb_user_token
    }

conn.request("GET", "/api/v1/customers/"+cUUID+"/universes/"+uniUUID+"/tables", headers=headers)

res = conn.getresponse()
data = json.loads(res.read())

#data[0]['tableUUID']


# Notes:
# ======
# 
# "table_stats" table has primary key on run_id,current_dt,tableuuid
# 
# #Table and seq definition
# # Create a database "yb_stats_db" and following object in the database.
# create table table_stats (run_id bigint,current_dt date,tableUUID text, dbname text,tableType text,tableName text,relationType text,sizeBytes float,isIndexTable text, primary key((run_id,current_dt,tableUUID) ));
# 
# create sequence table_stats_run_id_sequence start 1 increment 1;
# # Sequence will help to create unique ID for every script execution. It will also help to create primary key for the table

# In[4]:


try:
# Connect to your postgres DB
    conn = psycopg2.connect(dbname=yb_stats_db,host=yb_db_addr,port=yb_db_port,user=yb_db_user)
#    conn = psycopg2.connect(dbname='northwind',host='us-west-2.6ae39e7c-660a-4a25-9c6a-a1276a635c06.aws.ybdb.io',port='5433',user='admin',password='44Rf_2yypKP-Qg1WypskRBm0eSQzSp',sslmode='verify-full', sslrootcert=yb_db_ssl_path)

# Open a cursor to perform database operations
    cur = conn.cursor()
except Exception as err:
    print ("Oops! An exception has occured:", error)
    print ("Exception TYPE:", type(error))


# In[5]:


select_sql="SELECT nextval('table_stats_run_id_sequence')"
cur.execute(select_sql)

# Retrieve query results
run_id = cur.fetchall()


# In[6]:


# Capture current date on whcih data was inserted into the table
now = datetime.now()

# convert to string
date_time_str = now.strftime("%Y-%m-%d")


# In[7]:


# Final data insertion in the table 
insert_sql="insert into table_stats values (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
for iter in data:
    params=(run_id[0][0],date_time_str,iter['tableUUID'],iter['keySpace'],iter['tableType'],iter['tableName'],iter['relationType'],iter['sizeBytes'],iter['isIndexTable'])
    cur.execute(insert_sql,params)
    conn.commit()


# In[17]:


conn.close()


# In[ ]:




