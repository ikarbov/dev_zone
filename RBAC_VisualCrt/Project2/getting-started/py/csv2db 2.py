#!/usr/bin/env python
#import numpy as np
#import pandas as pd
#from sqlalchemy import create_engine
#from snowflake.sqlalchemy import URL
import snowflake.connector
import os, sys
#import json
import csv


con = snowflake.connector.connect(
  user='ikarbov',
  password='Passwordik_27',
  account='aws_cas2',
)

cur = con.cursor()
cur.execute("USE DATABASE IKARBOV_DB;")
cur.execute("USE schema RBAC_PS;")
cur.execute("USE warehouse IGORKA_WH;")

#cur_do = con.cursor()
#cur_do.execute("USE DATABASE IKARBOV_DB;")
#cur_do.execute("USE schema PUBLIC;")
#cur_do.execute("USE warehouse IGORKA_WH;")
header_in = 0 #No HEADER in FILE
try:

    #cur.execute("drop table IF EXISTS users1")
    #cur.execute("create or replace stage rbac_stage")
    #cur.execute("put file:///../table1.csv @~/rbac_stage;")
    table1 = "create or replace TABLE ROLE_RBAC_MAIN_PY ( \
                ROLE VARCHAR, \
                GRANTED_TO VARCHAR, \
                ASSIGNED_WAREHOUSE VARCHAR \
            );"
    cur.execute(table1)
    
    table2 = "create or replace TABLE  RBAC_DB_ACCESS_PY \
                ( \
                    NAME VARCHAR, \
                    PROD VARCHAR, \
                    QA VARCHAR, \
                    DEV VARCHAR \
                );"
    cur.execute(table2)

#process MAIN table as table1
    with open('../table1.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0 and header_in == 1:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                print(f'\t{row[0]} works in the {row[1]} department, and was born in {row[2]}.')
                line_count += 1
                sql_cmd = "INSERT INTO ROLE_RBAC_MAIN_PY(ROLE, GRANTED_TO, ASSIGNED_WAREHOUSE) VALUES  ('"+ row[0]+"','"+ row[2] +"','"+ row[1] +"')"
                #sql_cmd = "INSERT INTO ROLE_RBAC_MAIN_PY (ROLE, GRANTED_TO, ASSIGNED_WAREHOUSE) VALUES  ('data1','data2','data3')"
                
                cur.execute(sql_cmd)
                #print(sql_cmd)
        print(f'Table1 - Processed {line_count} lines.')

#process ACCESS table as table2
    with open('../table2.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0 and header_in == 1:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                print(f'\t{row[0]} works in the {row[1]} department, and was born in {row[2]}.')
                line_count += 1
                sql_cmd = "INSERT INTO RBAC_DB_ACCESS_PY(NAME, PROD, QA, DEV) VALUES  ('"+ row[0]+"','"+ row[1] +"','"+ row[2] +"','"+ row[3] +"')"
                #sql_cmd = "INSERT INTO ROLE_RBAC_MAIN_PY (ROLE, GRANTED_TO, ASSIGNED_WAREHOUSE) VALUES  ('data1','data2','data3')"
                
                cur.execute(sql_cmd)
                #print(sql_cmd)
        print(f'Table2 - Processed {line_count} lines.')

finally:
    cur.close()
    print('Successfully Finished ')