#!/usr/bin/python3
__author__ = 'Keith Hoyle, Snowflake Computing'
import cx_Oracle

##############################################################################################################################
# SQL Function Migration Mappings
##############################################################################################################################
# KeyWord:   ['Function Type', 'getSrcFunction', #Arguments, 'Snowflake Function']
kwSQL  = [   #['String Math', '', 2, '<1> || <2>)'],
             ['Function', 'APPENDCHILDXML(', 0, '???(<2>, <1>)'],
             ['Function', 'ASCIISTR(', 1, '<1>::varchar'],
             ['Function', 'BFILENAME(', 0, '???(<2>, <1>)'],
             ['Function', 'BIN_TO_NUM(', 0, '???(<2>, <1>)'],
             ['Function', 'CARDINALITY(', 0, '???(<2>, <1>)'],
             ['Function', 'CHARTOROWID(', 0, '0'],
             ['Function', 'CLUSTER_ID(', 0, '0'],
             ['Function', 'CLUSTER_PROBABILITY(', 0, '???(<2>, <1>)'],
             ['Function', 'CLUSTER_SET(', 0, '???(<2>, <1>)'],
             ['Function', 'COLLECT(', 0, '???(<2>, <1>)'],
             ['Function', 'COMPOSE(', 0, '???(<2>, <1>)'],
             ['Function', 'CONVERT(', 0, '???(<2>, <1>)'],
             ['Function', 'DBTIMEZONE(', 0, '???(<2>, <1>)'],
             ['Function', 'DECOMPOSE(', 0, '???(<2>, <1>)'],
             ['Function', 'DELETEXML(', 0, '???(<2>, <1>)'],
             ['Function', 'DEPTH(', 0, '???(<2>, <1>)'],
             ['Function', 'EMPTY_BLOB(', 0, '???(<2>, <1>)'],
             ['Function', 'EMPTY_CLOB(', 0, '???(<2>, <1>)'],
             ['Function', 'EXISTSNODE(', 0, '???(<2>, <1>)'],
             ['Function', 'EXTRACT (XML)(', 0, '???(<2>, <1>)'],
             ['Function', 'EXTRACTVALUE(', 0, '???(<2>, <1>)'],
             ['Function', 'FEATURE_ID(', 0, '???(<2>, <1>)'],
             ['Function', 'FEATURE_SET(', 0, '???(<2>, <1>)'],
             ['Function', 'FEATURE_VALUE(', 0, '???(<2>, <1>)'],
             ['Function', 'FIRST(', 0, '???(<2>, <1>)'],
             ['Function', 'FROM_TZ(', 0, '???(<2>, <1>)'],
             ['Function', 'GROUP_ID(', 0, '???(<2>, <1>)'],
             ['Function', 'GROUPING(', 0, '???(<2>, <1>)'],
             ['Function', 'HEXTORAW(', 0, '???(<2>, <1>)'],
             ['Function', 'INSERTXMLBEFORE(', 0, '???(<2>, <1>)'],
             ['Function', 'INSTR(', 2, 'charindex(<2>, <1>)'],
             ['Function', 'LNNVL(', 0, '???(<2>, <1>)'],
             ['Function', 'MONTHS_BETWEEN(', 2, 'date_diff(month, <1>, <2>)'],
             ['Function', 'NANVL(', 0, '???(<2>, <1>)'],
             ['Function', 'NEW_TIME(', 0, '???(<2>, <1>)'],
             ['Function', 'NLS_INITCAP(', 1, 'initcap(<1>)'],
             ['Function', 'NLS_LOWER(', 1, 'lower(<1>)'],
             ['Function', 'NLS_UPPER(', 1, 'upper(<1>)'],
             ['Function', 'NLSSORT(', 0, '???(<2>, <1>)'],
             ['Function', 'NUMTODSINTERVAL(', 0, '???(<2>, <1>)'],
             ['Function', 'NUMTODSINTERVAL(', 0, '???(<2>, <1>)'],
             ['Function', 'NUMTOYMINTERVAL(', 0, '???(<2>, <1>)'],
             ['Function', 'NUMTOYMINTERVAL(', 0, '???(<2>, <1>)'],
             ['Function', 'PATH(', 0, '???(<2>, <1>)'],
             ['Function', 'POWERMULTISET(', 0, '???(<2>, <1>)'],
             ['Function', 'POWERMULTISET_BY_CARDINALITY(', 0, '???(<2>, <1>)'],
             ['Function', 'PREDICTION(', 0, '???(<2>, <1>)'],
             ['Function', 'PREDICTION_COST(', 0, '???(<2>, <1>)'],
             ['Function', 'PREDICTION_DETAILS(', 0, '???(<2>, <1>)'],
             ['Function', 'PREDICTION_PROBABILITY(', 0, '???(<2>, <1>)'],
             ['Function', 'PREDICTION_SET(', 0, '???(<2>, <1>)'],
             ['Function', 'RAWTOHEX(', 1, 'hex_encode(<1>)'],
             ['Function', 'RAWTONHEX(', 1, 'hex_encode(<1>)'],
             ['Function', 'REMAINDER(', 0, '???(<2>, <1>)'],
             ['Function', 'ROWIDTOCHAR(', 0, '???(<2>, <1>)'],
             ['Function', 'ROWIDTONCHAR(', 0, '???(<2>, <1>)'],
             ['Function', 'SCN_TO_TIMESTAMP(', 0, '???(<2>, <1>)'],
             ['Function', 'SESSIONTIMEZONE(', 0, '???(<2>, <1>)'],
             ['Function', 'SOUNDEX(', 0, '???(<2>, <1>)'],
             ['Function', 'STATS_BINOMIAL_TEST(', 0, '???(<2>, <1>)'],
             ['Function', 'STATS_CROSSTAB(', 0, '???(<2>, <1>)'],
             ['Function', 'STATS_F_TEST(', 0, '???(<2>, <1>)'],
             ['Function', 'STATS_KS_TEST(', 0, '???(<2>, <1>)'],
             ['Function', 'STATS_MODE(', 0, '???(<2>, <1>)'],
             ['Function', 'STATS_MW_TEST(', 0, '???(<2>, <1>)'],
             ['Function', 'STATS_ONE_WAY_ANOVA(', 0, '???(<2>, <1>)'],
             ['Function', 'STATS_T_TEST_*(', 0, '???(<2>, <1>)'],
             ['Function', 'STATS_WSR_TEST(', 0, '???(<2>, <1>)'],
             ['Function', 'SYS_CONTEXT(', 0, '???(<2>, <1>)'],
             ['Function', 'SYS_DBURIGEN(', 0, '???(<2>, <1>)'],
             ['Function', 'SYS_EXTRACT_UTC(', 0, '???(<2>, <1>)'],
             ['Function', 'SYS_GUID', 0, 'md5(random())'],
             ['Function', 'SYS_TYPEID(', 0, '???(<2>, <1>)'],
             ['Function', 'SYS_XMLAGG(', 0, '???(<2>, <1>)'],
             ['Function', 'SYS_XMLGEN(', 0, '???(<2>, <1>)'],
             ['Function', 'SYSDATE', 0, 'current_date()'],
             ['Function', 'SYSTIMESTAMP', 0, 'current_timestamp()'],
             ['Function', 'TIMESTAMP_TO_SCN(', 0, '???(<2>, <1>)'],
             ['Function', 'TO_BINARY_DOUBLE(', 0, '???(<2>, <1>)'],
             ['Function', 'TO_BINARY_FLOAT(', 0, '???(<2>, <1>)'],
             ['Function', 'TO_CLOB(', 1, '<1>::variant'],
             ['Function', 'TO_DSINTERVAL(', 1, '<1>::variant'],
             ['Function', 'TO_LOB(', 1, '<1>::variant'],
             ['Function', 'TO_MULTI_BYTE(', 0, '???(<2>, <1>)'],
             ['Function', 'TO_NCHAR(', 1, '<1>::varchar'],
             ['Function', 'TO_NCLOB(', 1, '<1>::variant'],
             ['Function', 'TO_SINGLE_BYTE(', 0, '???(<2>, <1>)'],
             ['Function', 'TO_YMINTERVAL(', 1, '<1>::variant'],
             ['Function', 'TRANSLATE ... USING(', 0, '???(<2>, <1>)'],
             ['Function', 'TREAT(', 0, '???(<2>, <1>)'],
             ['Function', 'TZ_OFFSET(', 0, '???(<2>, <1>)'],
             ['Function', 'UID(', 0, 'current_session()'],
             ['Function', 'UNISTR(', 0, '???(<2>, <1>)'],
             ['Function', 'UPDATEXML(', 0, '???(<2>, <1>)'],
             ['Function', 'USER', 0, 'current_user()'],
             ['Function', 'USERENV(', 0, 'current_schema()'],
             ['Function', 'XMLAGG(', 0, '???(<2>, <1>)'],
             ['Function', 'XMLCDATA(', 0, '???(<2>, <1>)'],
             ['Function', 'XMLCOLATTVAL(', 0, '???(<2>, <1>)'],
             ['Function', 'XMLCOMMENT(', 0, '???(<2>, <1>)'],
             ['Function', 'XMLCONCAT(', 0, '???(<2>, <1>)'],
             ['Function', 'XMLFOREST(', 0, '???(<2>, <1>)'],
             ['Function', 'XMLPARSE(', 0, '???(<2>, <1>)'],
             ['Function', 'XMLPI(', 0, '???(<2>, <1>)'],
             ['Function', 'XMLQUERY(', 0, '???(<2>, <1>)'],
             ['Function', 'XMLROOT(', 0, '???(<2>, <1>)'],
             ['Function', 'XMLSEQUENCE(', 0, '???(<2>, <1>)'],
             ['Function', 'XMLSERIALIZE(', 0, '???(<2>, <1>)'],
             ['Function', 'XMLTABLE(', 0, '???(<2>, <1>)']
           ]
##############################################################################################################################
# Stored Procedure Migration Mappings
##############################################################################################################################
# KeyWord:         ['Label'              , 'getSrcKeyWord' ]
kwSP  = [    # Procedure Begin/End...............................................
             ['Procedure Begin'    , 'create or replace procedure '], 
             ['Procedure Begin Alt', 'create procedure '], 
             ['Procedure End'      , 'end procedure;'],
             # Comments..........................................................
             ['Single-Line Comment', '--'            ],
             ['Comment Begin'      , '/*'            ], 
             ['Comment End'        , '*/'            ],
             # Branching Logic...................................................
             ['If Begin'           , 'if '           ], 
             ['Then'               , 'then '         ],
             ['Else If'            , 'else if '      ],
             ['Else'               , 'else '         ], 
             ['If End'             , 'end if'        ],
             # Looping Logic.....................................................
             ['For Begin'          , 'for '          ], 
             ['For End'            , ''              ],
             ['While Begin'        , 'while '        ], 
             ['While End'          , ''              ],
             # Procedural Variables..............................................
             ['Variable Create'    , 'declare '      ], 
             ['Variable Drop'      , 'drop variable '],
             ['Variable Assign'    , ':='            ],
             # Procedural Layers/Navigation......................................
             ['Sub-Routine Call'   , 'goto '         ], 
             ['Sub-Routine Begin'  , 'label '        ], 
             ['Sub-Routine End'    , 'exit'          ],
             # Connection Activities..............................................
             ['Logon'              , 'logon '        ], 
             ['Logoff'             , 'logoff'        ],
             ['Warehouse'          , 'warehouse '    ], 
             ['Database'           , 'database '     ], 
             ['Schema'             , 'schema '       ] ]
##############################################################################################################################
# RDBMS-specific Utilities
##############################################################################################################################
def connect(_account, _user, _password) :
   return cx_Oracle.connect(src_creds_dict['user'] + '/' + 
      src_creds_dict['password'] + '@' + 
      src_creds_dict['account']
   )
##############################################################################################################################
# Table Migration Constants
##############################################################################################################################
colFinder = f"""select case when column_id = 1 then case when row_number() over(order by 1) > 1 then ');' || chr(13) || chr(10) else '' end ||
                                                    'create table if not exists <database>.' || owner || '_LZ.' || table_name || ' (' || chr(13) || chr(10) ||
                                                    '    '
                            else '  , '
                       end
                       || column_name || ' ' ||
                       case when data_type =    'NUMBER' then 'NUMBER' || case when data_scale > 0 then '(' || data_precision || ', ' || data_scale || ')' else '' end
                            when data_type like 'BOOL%' then 'BOOLEAN'
                            when data_type like 'DATE%' then 'DATE'
                            when data_type like 'TIME%ZONE' then 'TIMESTAMP_LTZ' || case when data_scale > 0 then '(' || data_scale || ')' else '' end
                            when data_type like 'TIME%' then 'TIMESTAMP' || case when data_scale > 0 then '(' || data_scale || ')' else '' end
                            when data_type like '%CHAR%' then 'VARCHAR' --|| case when data_length is not null then '(' || data_length || ')' else '' end
                            when data_type like 'BINARY%' then 'BINARY'
                            when data_type =    'BLOB' then 'BINARY'
                            when data_type =    'FLOAT' then 'FLOAT'
                            else 'VARIANT'
                       end ddl_
                from all_tab_cols atc
                where lower(owner) = lower('<schema>')
                order by table_name, column_id
             """
idxFinder = """SELECT 'alter table ' || cons.owner || '_LZ.' || cols.table_name || ' add primary key (' || listagg(cols.column_name, ',') within group (order by cols.column_name) || ')' pk_ddl_lz
                      , 'alter table ' || cons.owner || '_PSA.' || cols.table_name || ' add primary key (' || listagg(cols.column_name, ',') within group (order by cols.column_name) || ')' pk_ddl_psa
               FROM all_constraints cons
               INNER JOIN all_cons_columns cols
                 ON  cons.constraint_name = cols.constraint_name
                 AND cons.owner = cols.owner
               WHERE lower(cons.owner) = lower('<schema>')
               AND   cons.constraint_type = 'P'
               GROUP BY cons.owner, cols.table_name
               ORDER BY cons.owner, cols.table_name
            """
##############################################################################################################################
# Data Migration Constants
##############################################################################################################################
cdcInsert  = f"""select view_definition
                        , table_catalog, replace(table_schema, '_PSA', '') table_schema, replace(table_name, '_LZ_CDC', '') table_name, table_name view_name
                 from information_schema.views
                 where charindex('_CDC', table_name) > 0
                 and   upper(table_schema) = '<schema>_PSA';
              """
exprInsert = f"""select view_definition
                        , table_catalog, replace(table_schema, '_PSA', '') table_schema, replace(table_name, '_LZ_EXPR', '') table_name, table_name view_name
                 from information_schema.views
                 where charindex('_EXPR', table_name) > 0
                 and   upper(table_schema) = '<schema>_PSA';
              """
