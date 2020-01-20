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

with open('elems_last.json') as json_file:
    data = json.load(json_file)

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
            rolesSchemas[item['data']['parent'] + '.' + item['data']['id']] =  'NaN'#item['data']['id']
            rolesSchemas[item['data']['id']] =  'NaN'#item['data']['id']
            
        #   print('--')
    print(rolesSchemas)
    print(rolesDict)
    #dbSchema = {}
    print('--Edges--')
    roleToMatchSchDict = rolesDict.copy()
    #clear Values newDict = wordsDict.copy()
    for k in roleToMatchSchDict:
        roleToMatchSchDict[k] = ''

    roleToMatchSchDict.pop("rl_sysadmin", None)

    dictSchemaWithRoles = {}

    for item  in data['elements']['edges']:
        if item['data']['label'] == 'H':
            print(rolesDict[item['data']['source']])
            print(rolesDict[item['data']['target']])
            rolesDict[item['data']['source']] = item['data']['target']
            print(rolesDict)


        if item['data']['label'] != 'H':
            print(item['data']['target'])
            print(rolesSchemas[item['data']['target']])
            #dbSchema[item['data']['target']] = dbSchema[item['data']['target']] + '#' + item['data']['source']
            #if item['data']['target'] not in dbSchema:
            print(item['data']['target'])
            print(item['data']['source'])
            #roleToMatchSchDict[item['data']['source']] = item['data']['source'] + '#' + item['data']['label']
            
            #dictSchemaWithRoles[item['data']['target']] = roleToMatchSchDict
            #roleToMatchSchDict[item['data']['source']] = item['data']['source'] + '#' + item['data']['label']
            print(roleToMatchSchDict)
            for k in roleToMatchSchDict:
                roleToMatchSchDict[k] = ''
            if item['data']['target'] not in dbSchema:
                roleToMatchSchDict[item['data']['source']] = item['data']['source'] + '#' + item['data']['label']
                dbSchema[item['data']['target']] = roleToMatchSchDict.copy()#[item['data']['source']]#',' + item['data']['source'] + '#' + item['data']['label']
                print(dbSchema)
            else:
                dictRolesLine = dbSchema[item['data']['target']]
                dictRolesLine[item['data']['source']] =  item['data']['source'] + '#' + item['data']['label']
                dbSchema[item['data']['target']] = dictRolesLine
                print(dbSchema)

            #else:
            #    dbSchema[item['data']['target']] = dbSchema[item['data']['target']] + ',' +  item['data']['source'] + '#' + item['data']['label']
    
    rolesDict.pop("rl_sysadmin", None)
      
    print(rolesDict)
    print(dbSchema)  

#con = snowflake.connector.connect(
#  user='user---name',
#  password='pass******',
#  account='aws_cas2',
#)

con = snowflake.connector.connect(
  user='i',
  password='',
  account='aws_cas2',
)

cur = con.cursor()
cur.execute("USE ROLE SYSADMIN;")
cur.execute("USE DATABASE IKARBOV_DB;")
cur.execute("USE schema RBAC_PS;")
cur.execute("USE warehouse IGORKA_WH;")

#header_in = 0 #No HEADER in FILE
try:

    table1 = "create or replace TABLE ROLE_RBAC_MAIN_PY ( \
                ROLE VARCHAR, \
                GRANTED_TO VARCHAR, \
                ASSIGNED_WAREHOUSE VARCHAR \
            );"
    cur.execute(table1)


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
        cur.execute(sql_cmd)
    
    print(f'Table1 - Processed {line_count} lines.')


    
    #process databse names to the script from table-2
    table2 = "create or replace TABLE  RBAC_DB_ACCESS_MNG (DB_NAME VARCHAR, SCHEMA_NAME VARCHAR, SCHEMA_MNGR VARCHAR " + roles_to_sql + " );"
    print(table2)
    cur.execute(table2)


#process ACCESS table as table2
    sql_cmd_cols = ""
    sql_cmd_cols_val = ""
    sql_cmd_cols_w_mngd_roles = ""
    db_w_schema_mngd = ''

    #with open('../table-2.csv', encoding='utf-8-sig') as csv_file:
        #csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
        
    for row in dbSchema:
        #if line_count == 0 and header_in == 1:
        #    print(f'Column names are {", ".join(row)}')
        #   line_count += 1
        #else:
        line_count += 1
        print(len(row))
        #cnt_cols = len(row)
        ind_cols = 0
        sql_cmd = "INSERT INTO RBAC_DB_ACCESS_MNG(DB_NAME, SCHEMA_NAME, SCHEMA_MNGR "+roles_to_hdr+") VALUES  ("
        ####for colmn in row:
        #print(colmn)
        #if ind_cols == 0:
        #ind_cols = ind_cols + 1
        #Fix MANAGED ROle later
        #res_start = row[0].index('(')
        #res_end = row[0].index(')')
        #sql_role_for_mngd_schema = row[0][res_start+1:res_end]
        #sql_columnname = row[0][0:res_start].split('.')
        sql_columnname = row.split('.')

        sql_dbname = sql_columnname[0]
        sql_schemanname = sql_columnname[1]

        ##sql_cmd = sql_cmd +  "'" + sql_dbname + "', '" + sql_schemanname + "', '" + sql_role_for_mngd_schema + "', '"
        sql_cmd = sql_cmd +  "'" + sql_dbname + "', '" + sql_schemanname + "', '" + 'mngd_schema' + "', '"
        #fixed = dbSchema[row][0:pos]+s[pos+1:]
        #vv = dbSchema[row]
        #fixed = ''.join(dbSchema[row].split(',', 1))
        #lines = fixed.split(',')
        cnt_cols = len(dbSchema[row])
        ind_cols = 0
        for ln in dbSchema[row]:
            print(dbSchema[row][ln])
            #if ind_cols != 0:
            if '#' in dbSchema[row][ln]:
                l = dbSchema[row][ln].split('#')[1]
            else:
                l = ' '
            if ind_cols == (cnt_cols - 1):
                sql_cmd = sql_cmd + l 
            else:
                sql_cmd = sql_cmd + l + "', '" #colmn
            ind_cols = ind_cols + 1
        #if ind_cols != 0:
            #ind_cols = ind_cols + 1
        #    if ind_cols == (cnt_cols - 1):
        #        sql_cmd = sql_cmd + dbSchema[row]#colmn
        #    else:
        #        sql_cmd = sql_cmd + dbSchema[row] + "', '"
        #ind_cols = ind_cols + 1
        #print(sql_cmd)
            
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
    