# pg_stat_statements_hist

This script will capture pg_stat_statements for analysis. 

Yugabyte run independent postgres entity on individual DB node (Tserver). This make it difficult to analyze the queries on Yugabyte as a whole. With the help of this solution, we want to capture pg_stat_statements data from all the DB nodes at central location for analysis.

This solution is written in Shell script and need to be deployed on all the host running DB nodes. 

Steps of deployment:
1) Create a database "yb_stats_db" 
2) Create a table "pg_stat_statements_hist" in database "yb_stats_db" with following DDL
```
create table pg_stat_statements_hist (
 run_id bigint,   // run_id is unique ID for every instance of script execution
 host_ip_addr text, // IP address of host to which data belongs
 insert_date date, // Date when the records are inserted 
  userid integer,
  dbid integer,
  queryid bigint,
  query text,
  calls integer,
  total_time float,
  min_time float,
  max_time float,
  mean_time float,
  stddev_time float,
  rows bigint,
  shared_blks_hit float,
  shared_blks_read float,
  shared_blks_dirtied float,
  shared_blks_written float,
  local_blks_hit float,
  local_lks_read float,
  local_blks_dirtied float,
  local_blks_written float,
  temp_blks_read float,
  temp_blks_written float,
  blk_read_time float,
  blk_write_time float
);
```
3) Create a sequence "pg_stat_statements_hist_seq" required for run_id 

create sequence pg_stat_statements_hist_seq start 1 increment 1;

4) Copy the script on all the DB nodes in "yugabyte" home directory. This script assume that the script will run as "yugabyte" ( default install user)

5) Provide execute permission to the script

6) Edit the crontab to schedule the script at a fixed frequency. 

Depending upon system utilization (i.e. number of queries execution), script run schedule need to be defined. "pg_stat_statements" store information for latest queries only and old queries will get rolled over. 

To schedule every 6 hours:
0 */6 * * * /home/yugabyte/yb_query_history.sh
