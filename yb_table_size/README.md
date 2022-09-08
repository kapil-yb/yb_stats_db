# yb_table_size

DBA's need to understand keep a tab on the growing size of database and tables. This data can be helpful in ways such as:

1) Understand the table size growing over time for reporting purpose.
2) Developer might have miss to set the purging policies on the table and thus size will continously keep on increasing.
3) A sudden drop or increase could be due to accidental deletion or insertion
4) Management might want a utilization report for each Database in multi tennant environment.

This program aim to capture the table level metrics which should help to capture the details.

Note
1) Script can be deployed on platform server, or external servers as well
2) Install the dependent module require by this script
3) Schedule this script to run on daily basis ( Cron could be an option)

# Modules which are required for to run this program. This program is written and tested on:

Python 2.7.18
YB Anywhere 2.13.X
http                               0.2
jsonschema                         3.2.0
pandas                             0.24.2
psycopg2-binary                    2.8.6

DataBase Readiness:
#Create a database "yb_stats_db" and following object in the database:

1) create table table_stats (run_id bigint,current_dt date,tableUUID text, dbname text,tableType text,tableName text,relationType text,sizeBytes float,isIndexTable text, primary key((run_id,current_dt,tableUUID) ));

2) create sequence table_stats_run_id_sequence start 1 increment 1;
