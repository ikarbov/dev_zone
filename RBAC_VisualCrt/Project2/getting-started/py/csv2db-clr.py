#!/usr/bin/env python
#import numpy as np
#import pandas as pd
#from sqlalchemy import create_engine
#from snowflake.sqlalchemy import URL
import snowflake.connector
import os, sys
import json
import csv


rolesDict = {} 
dbSchema = {}

with open('elems_s.json') as json_file:
    data = json.load(json_file)
    #print(data)
    #result = data['elements']
    #for value_dict in result:
    #    print ('{0}, {1}'.format(value['total'], value['_id']))

    #for key, value in data.items():
     #   print( key, value)

    #rolesDict = {} 
    rolesSchemas = {} 

    for item  in data['elements']['nodes']:
        print(item['group'])
        print(item['data']['id'])
        print(item['data']['label'])
        if item['data']['label'] == 'role':
            #if item['data']['id'] != 'rl_sysadmin':
            rolesDict[item['data']['id']] = '???'#item['data']['id'] rl_sysadmin
        if item['data']['label'] == 'schema':
            rolesSchemas[item['data']['id']] = item['data']['parent'] + '.' + item['data']['id']
            
        #for nod in item['data']:   parent
        #    print(item['data'][nod])
        #   print('--')
    
    #dbSchema = {}
    print('--Edges--')
    for item  in data['elements']['edges']:
        if item['data']['label'] == 'H':
            print(rolesDict[item['data']['source']])
            print(rolesDict[item['data']['target']])
            rolesDict[item['data']['source']] = item['data']['target']
            print(rolesDict)


        if item['data']['label'] != 'H':
            print(rolesSchemas[item['data']['target']])
            #dbSchema[item['data']['target']] = dbSchema[item['data']['target']] + '#' + item['data']['source']
            if item['data']['target'] not in dbSchema:
                dbSchema[item['data']['target']] = ',' + item['data']['source'] + '#' + item['data']['label']
            else:
                dbSchema[item['data']['target']] = dbSchema[item['data']['target']] + ',' +  item['data']['source'] + '#' + item['data']['label']
    
    rolesDict.pop("rl_sysadmin", None)
      
    print(rolesDict)
    print(dbSchema)  

#con = snowflake.connector.connect(
#  user='user---name',
#  password='pass******',
#  account='aws_cas2',
#)

#cur = con.cursor()
#cur.execute("USE ROLE SYSADMIN;")
#cur.execute("USE DATABASE IKARBOV_DB;")
#cur.execute("USE schema RBAC_PS;")
#cur.execute("USE warehouse IGORKA_WH;")

header_in = 0 #No HEADER in FILE
try:

    table1 = "create or replace TABLE ROLE_RBAC_MAIN_PY ( \
                ROLE VARCHAR, \
                GRANTED_TO VARCHAR, \
                ASSIGNED_WAREHOUSE VARCHAR \
            );"
    #cur.execute(table1)


    #process MAIN table as table1 // LINE: dynamic_prod_admin,WH_PROD_SMALL,SYSADMIN
    roles_to_sql = ''
    roles_to_hdr = ''
    line_count = 0

    for row in rolesDict:
        line_count += 1
        #sql_cmd = "INSERT INTO ROLE_RBAC_MAIN_PY(ROLE, GRANTED_TO, ASSIGNED_WAREHOUSE) VALUES  ('"+ row[0]+"','"+ row[2] +"','"+ row[1] +"')"
        sql_cmd = "INSERT INTO ROLE_RBAC_MAIN_PY(ROLE, GRANTED_TO, ASSIGNED_WAREHOUSE) VALUES  ('"+ row +"','"+ rolesDict[row] +"','"+ 'WH_SMALL' +"')"
        
        roles_to_sql = roles_to_sql + ', ' + row + ' VARCHAR'
        roles_to_hdr = roles_to_hdr + ', ' + row
        print(sql_cmd)
        #cur.execute(sql_cmd)
    
    print(f'Table1 - Processed {line_count} lines.')


    
    #process databse names to the script from table-2
    table2 = "create or replace TABLE  RBAC_DB_ACCESS_MNG (DB_NAME VARCHAR, SCHEMA_NAME VARCHAR, SCHEMA_MNGR VARCHAR " + roles_to_sql + " );"
    print(table2)
    ##cur.execute(table2)


#process ACCESS table as table2
    sql_cmd_cols = ""
    sql_cmd_cols_val = ""
    sql_cmd_cols_w_mngd_roles = ""
    db_w_schema_mngd = ''

    with open('../table-2.csv', encoding='utf-8-sig') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        
        for row in csv_reader:
            if line_count == 0 and header_in == 1:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                line_count += 1
                print(len(row))
                cnt_cols = len(row)
                ind_cols = 0
                sql_cmd = "INSERT INTO RBAC_DB_ACCESS_MNG(DB_NAME, SCHEMA_NAME, SCHEMA_MNGR "+roles_to_hdr+") VALUES  ("
                for colmn in row:
                    print(colmn)
                    if ind_cols == 0:
                        #ind_cols = ind_cols + 1
                        res_start = row[0].index('(')
                        res_end = row[0].index(')')
                        sql_role_for_mngd_schema = row[0][res_start+1:res_end]
                        sql_columnname = row[0][0:res_start].split('.')

                        sql_dbname = sql_columnname[0]
                        sql_schemanname = sql_columnname[1]

                        sql_cmd = sql_cmd +  "'" + sql_dbname + "', '" + sql_schemanname + "', '" + sql_role_for_mngd_schema + "', '"
                    if ind_cols != 0:
                        #ind_cols = ind_cols + 1
                        if ind_cols == (cnt_cols - 1):
                            sql_cmd = sql_cmd + colmn
                        else:
                            sql_cmd = sql_cmd + colmn + "', '"
                    ind_cols = ind_cols + 1
                    print(sql_cmd)
                  
                sql_cmd = sql_cmd + "')"
                print(sql_cmd)
                cur.execute(sql_cmd)
        print(f'Table2 - Processed {line_count} lines.')

#1.Main Stored Procedure execution
###### SP Run

#try SP

    sql_sp = "call SP_RBAC_PROCESSOR();"
    exec = cur.execute(sql_sp)
    sql_script = exec.fetchone()
    sql_str =  ''.join(sql_script)
    print('{0}'.format(sql_str))
    file = open("sql_script.sql","w") 
    file.write(sql_str) 
    file.close() 
#
#2. Call App for visualization, Users to Roles, Roles to DB Objects
###### Call Python app for Visualization
#
    print('Successfully Finished ')
except BaseException as e:
  print("An exception occurred") 
  print(str(e)) 
  cur.close()
finally:
    cur.close()
    