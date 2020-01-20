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
