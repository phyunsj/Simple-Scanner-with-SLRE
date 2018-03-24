#!/usr/bin/env python

import unittest
import requests
import json
import xmlrpclib
import pexpect
import sys, getopt, pprint

import sqlite3
from sqlite3 import Error

def create_table():
    db_file = './hadoop.db'
    
    sql_create_user_table = '''CREATE TABLE IF NOT EXISTS MAPREDUCE (
        TASK_IO_SORT_MB INTEGER ,
        MAP_SORT_SPILL_PERCENT INTEGER ,
        TASK_IO_SORT_FACTOR INTEGER ,
        MAP_COMBINE_MINSPILLS INTEGER ,
        CLUSTER_LOCAL_DIR TEXT ,
        REDUCE_MERGE_MEMTOMEM_ENABLED INTEGER ,
        FRAMEWORK_NAME TEXT ,
        REDUCE_SHUFFLE_PARALLELCOPIES INTEGER ,
        REDUCE_MEMORY_TOTALBYTES INTEGER ,
        REDUCE_SHUFFLE_MEMORY_LIMIT_PERCENT INTEGER ,
        JOB_UBERTASK_MAXMAPS INTEGER ,
        JOB_UBERTASK_ENABLE INTEGER ,
        JOB_UBERTASK_MAXBYTES INTEGER ,
        MAP_MEMORY_MB INTEGER ,
        REDUCE_MEMORY_MB  INTEGER );

    '''

    sql_insert_user_table = ''' INSERT INTO MAPREDUCE ( 
        TASK_IO_SORT_MB ,
        MAP_SORT_SPILL_PERCENT ,
        TASK_IO_SORT_FACTOR ,
        MAP_COMBINE_MINSPILLS ,
        CLUSTER_LOCAL_DIR ,
        REDUCE_MERGE_MEMTOMEM_ENABLED ,
        FRAMEWORK_NAME ,
        REDUCE_SHUFFLE_PARALLELCOPIES ,
        REDUCE_MEMORY_TOTALBYTES ,
        REDUCE_SHUFFLE_MEMORY_LIMIT_PERCENT ,
        JOB_UBERTASK_MAXMAPS ,
        JOB_UBERTASK_ENABLE ,
        JOB_UBERTASK_MAXBYTES ,
        MAP_MEMORY_MB ,
        REDUCE_MEMORY_MB )
        VALUES( ?,?,?,?,? ,?,?,?,?,? ,?,?,?,?,? );
'''

 
    
    try:
        conn = sqlite3.connect(db_file)
        print '> Open hadoop.db'
    except Error as e:
        print(e)
        sys.exit(-1)

    if conn is not None:
        try:
            c = conn.cursor()
            c.execute(sql_create_user_table)
            print '> Create MAPREDUCE table'
        except Error as e:
            print(e)
            sys.exit(-1)

        
        mapreduce_config =  ( 100, 80, 100, 4, "/mapred/local",  1, "yarn/remote", 30 , 1024, 70, 9, 1, 256, 1024, 1024 )
 
        c.execute(sql_insert_user_table, mapreduce_config)
        print '> Insert MAPREDUCE entries'
     
    conn.commit()
    conn.close()

###################################################################################################
# 
#  __main__  UnitTest Runner
#
if __name__ == '__main__':
    create_table()
    
