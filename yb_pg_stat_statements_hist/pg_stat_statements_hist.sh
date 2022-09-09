#!/usr/bin/env bash

EXPECTED_USERNAME=yugabyte
db=yb_stats_db
pg_stat_statements_hist=pg_stat_statements_hist
pg_stat_statements_hist_seq=pg_stat_statements_hist_seq

if [ "$(whoami)" != "$EXPECTED_USERNAME" ]; then
  printf "Script must be run as user: $EXPECTED_USERNAME"
  exit -1
fi


get_ysqlsh_binary_location()
{
	# Need to find out the ysqlsh binary location. Keeping manual for now
	file=$(ps -efwH | grep -i yb-tserver | grep -v grep | tr -s ' ' | cut -d ' ' -f 8 | xargs dirname)/ysqlsh
	if [ ! -f $file ]; then
		printf "Unable to locate ysqlsh binary"
		exit 1
	fi
	printf "$file"
}

get_ysqlsh_cmd()
{
	ysqlsh_cmd="`get_ysqlsh_binary_location` -h `hostname -i` -U $EXPECTED_USERNAME"
	
	#Checking ysqlsh connectivity
	today_date=$($ysqlsh_cmd -Atc "select current_date")
	
	if [ $? -ne 0 ]; then 
		printf "Unable to connect with ysqlsh"
		exit 1
	fi
	echo $ysqlsh_cmd
}

check_database()
{
	ysqlsh_cmd=$(get_ysqlsh_cmd)
	var=$($ysqlsh_cmd  -ltq | cut -d \| -f 1 | grep -w $db | xargs)
	# xargs to remove the empty space here

	if [ "$var" != "$db" ]; then
		printf "$db does not exist \n"
		exit 1
	fi

	printf "$db exist"
}

check_table()
{
	ysqlsh_cmd=$(get_ysqlsh_cmd)
        var=$($ysqlsh_cmd  -d $db -c "\d" | cut -d "|"  -f2 | grep -w $pg_stat_statements_hist | xargs)
        # xargs to remove the empty space here

        if [ "$var" != "$pg_stat_statements_hist" ]; then
                printf "$pg_stat_statements_hist does not exist in $db database\n"
                exit 1
        fi

        printf "$pg_stat_statements_hist exist"
}

check_pg_stat_statements_seq()
{
        ysqlsh_cmd=$(get_ysqlsh_cmd)
        var=$($ysqlsh_cmd  -d $db -c "\d" | cut -d "|"  -f2 | grep -w $pg_stat_statements_hist_seq | xargs)
        # xargs to remove the empty space here

        if [ "$var" != "$pg_stat_statements_hist_seq" ]; then
                printf "$pg_stat_statements_hist_seq does not exist in $db database\n"
                exit 1
        fi

        printf "$pg_stat_statements_hist_seq exist"
}

get_next_seq_value()
{
	ysqlsh_cmd=$(get_ysqlsh_cmd)
        next_seq=$($ysqlsh_cmd  -d $db -Atc "select nextval('pg_stat_statements_hist_seq')")
	echo $next_seq
}

get_current_date()
{
        ysqlsh_cmd=$(get_ysqlsh_cmd)
        insert_date=$($ysqlsh_cmd  -d $db -Atc "select current_date")
        echo $insert_date
}

get_current_host_ip_addr()
{
        ysqlsh_cmd=$(get_ysqlsh_cmd)
        ip_addr=$($ysqlsh_cmd  -d $db -Atc "select inet_server_addr()")
        echo $ip_addr
}


load_pg_stat_statements_data()
{
	run_id=$(get_next_seq_value)
	ysqlsh_cmd=$(get_ysqlsh_cmd)
        run_id=$(get_next_seq_value)
	
	status=$($ysqlsh_cmd -d $db -c "insert into pg_stat_statements_hist  select $run_id,host(inet_server_addr()),current_date ,userid,dbid,queryid,query,calls,total_time,min_time,max_time,mean_time,stddev_time,rows,shared_blks_hit,shared_blks_read,shared_blks_dirtied,shared_blks_written,local_blks_hit,local_blks_read,local_blks_dirtied,local_blks_written,temp_blks_read,temp_blks_written,blk_read_time,blk_write_time from pg_stat_statements")
}

a=`load_pg_stat_statements_data`
echo $a
