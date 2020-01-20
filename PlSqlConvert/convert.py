import re

def script_to_list(file_path, delimiter = ';'):
    line = []
    with open(file_path, 'r', encoding = 'utf-8') as file:
        #content = file.read()
        # remove end line characters
        ##content = content.replace("\n", "")
        # split by lines
        ##lines = re.compile("(\[[0-9//, :\]]+)").split(content)
        # clean "" elements
        ##lines = [x for x in lines if x != ""]
        #line = file.read().split(delimiter)

        #print(line)
        return (
           file.read().split(delimiter)
           #... ... 
          )# 


def main():

    #script_to_list()
    print('// Start')
    statements_sql = script_to_list('sql/one-pl-sql.sql')
    outputSql = ""
    for lnTxt in statements_sql: 
        #if lnTxt == 'BEGIN':
        sp_state = ''
        #lnTxt = lnTxt.replace('\n','')
        if len(lnTxt) == 1 and lnTxt == ';':
            lnTxt = lnTxt
            continue

        if 'PROCEDURE' in lnTxt:
            #sp_state = lnTxt
            outputSql = outputSql +  lnTxt
        if 'if' in lnTxt:
            if (lnTxt.find('select') != -1) or (lnTxt.find('delete') != -1):
                lnTxt =   lnTxt.replace('then', 'then \nvar rs = snowflake.execute( {sqlText: "') +  ';"} );'
            else:
                lnTxt = lnTxt
            outputSql = outputSql +  lnTxt.replace('end if',';') # + ';'
            continue
        if 'else' in lnTxt:
            if (lnTxt.find('select') != -1) or (lnTxt.find('delete') != -1):
                lnTxt =   lnTxt.replace('else', ' else\nvar rs = snowflake.execute( {sqlText: "') +  ';"} );'
            else:
                lnTxt = lnTxt
            outputSql = outputSql +  lnTxt.replace('end if',';') # + ';'
            continue
        if 'BEGIN' in lnTxt:
            lnTxt =   lnTxt.replace('BEGIN', '')
        if 'END' in lnTxt:
            lnTxt = lnTxt.replace('END','$$; \n //')
            continue
        if ':=' in lnTxt:
            lnTxt = 'SET ' + lnTxt.replace(':=', '=')
            #lnTxt = '\n var rs = snowflake.execute( {sqlText: "' + lnTxt.replace('\n','') + '"} );'
            #outputSql = outputSql EXCEPTION
        if 'commit' in lnTxt:
            lnTxt =  lnTxt.replace('commit', '// commit')
            continue
        if 'EXCEPTION' in lnTxt:
            lnTxt =  lnTxt.replace('EXCEPTION', '// EXCEPTION')
            continue
        if 'DBMS_OUTPUT' in lnTxt:
            lnTxt =  lnTxt.replace('DBMS_OUTPUT', '// DBMS_OUTPUT')
            continue
        if 'PROCEDURE' not in lnTxt:
            lnTxt = '\nvar rs = snowflake.execute( {sqlText: "' + lnTxt.replace('\n','') + ';"} );'
            outputSql = outputSql +  lnTxt # + ';'
        #print(outputSql) 
        #commit;
    #outputSql = outputSql + ' \n// End'
    outputSql = outputSql + '\n $$;'
    print(outputSql)


    print('// End')

    wfile = open('procs.sql', 'w')
    wfile.write(outputSql)
    wfile.close()

if __name__ == '__main__':
    main()