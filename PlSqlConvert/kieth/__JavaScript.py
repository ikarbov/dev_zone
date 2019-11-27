#!/usr/bin/python3
__author__ = 'Keith Hoyle, Snowflake Computing'
##############################################################################################################################
# JavaScript constants........................................................................................................
##############################################################################################################################
header = f"""CREATE OR REPLACE PROCEDURE <procName>
(<procArgs>)
RETURNS VARCHAR
LANGUAGE JAVASCRIPT
AS
$$
// begin SPConversion ......................................................................................
"""
footer = f"""// end SPConversion ........................................................................................
return ''
$$
;"""
indent = f"""   """
exit = '}'
exitErr = f"""<indent>sys.exit(2)"""

##############################################################################################################################
# KeyWord:         ['Label'              , 'getTgtKeyWord'                                   , indent]
kw             = [ # Comments..........................................................
                   ['Single-Line Comment', '// '                                             , 0],
                   ['Comment Begin'      , '/*'                                              , 0], 
                   ['Comment End'        , '*/'                                              , 0],
                   ['Indent'             , '   '                                             , 0],
                   ['Command Terminator' , ';'                                               , 0],
                   # Branching Logic...................................................
                   ['If Begin'           , '<indent><ifString> {'                            , 1], 
                   ['Then'               , ''                                                , 0],
                   ['Else If'            , '<indent>} <elIfString> {'                        , 0],
                   ['Else'               , '<indent>} else {'                                , 0], 
                   ['If End'             , '<indent>}'                                       ,-1],
                   # Looping Logic.....................................................
                   ['For Begin'          , '<indent>for <forStmt> {'                         , 1], 
                   ['For End'            , '<indent>}'                                       , 0],
                   ['While Begin'        , '<indent>while <whileStmt> {'                     , 0], 
                   ['While End'          , '<indent>}'                                       ,-1],
                   # Procedural Variables..............................................
                   ['Variable Create'    , '<indent>var <varName> = <value>;'                , 0], 
                   ['Variable Drop'      , ''                                                , 0],
                   ['Variable Assign'    , '='                                               , 0],
                   # Procedural Layers/Navigation......................................
                   ['Sub-Routine Call'   , '<indent><defName>()'                             , 0], 
                   ['Sub-Routine Begin'  , 'def <defName>'                                   , 1], 
                   ['Sub-Routine End'    , ''                                                ,-1],
                   # Connection Activities..............................................
                   ['Logon'              , ''                                                , 0], 
                   ['Logoff'             , ''                                                , 0],
                   ['Warehouse'          , f"""<indent>use warehouse <sqlWarehouse>;"""      , 0], 
                   ['Database'           , """<indent>use database <sqlDatabase>;"""         , 0], 
                   ['Schema'             , f"""<indent>use schema <sqlSchema>;"""            , 0],
                   # SQL (DML/DDL).....................................................
                   ['SQL'                , '<indent>var stmt = snowflake.createStatement({sqlText: "<sqlStmt>;"});\n' +
                                           '<indent>stmt.execute();'                         , 0] ]
