create or replace procedure SP_RBAC_PROCESSOR()
 returns string
    language javascript
    strict
    execute as caller
    as
    $$
    
    var EXECUTE_Script = false;
    var SQL_ACCESS = "select role, granted_to, ASSIGNED_WAREHOUSE, true  from ROLE_RBAC_MAIN_PY";
   
        var result_set_main = snowflake.execute ({sqlText: SQL_ACCESS});
 
        var forReturnt = "";
        var retValueGrant = "";
        var forReturntAll = "";
        var create_role = "";
        var retCrtRole = "";
        
        while (result_set_main.next())  {

          var sp_caller = "call SP_ROLE_ASSIGNER";

           var ROLE_NAME = result_set_main.getColumnValue(1);
           var GRANTED_TO = result_set_main.getColumnValue(2);
           var ASSIGNED_WAREHOUSE = result_set_main.getColumnValue(3);
           var NEED_ON_FUTURE_TBLS = result_set_main.getColumnValue(4);
           
           create_role = "CREATE ROLE IF NOT EXISTS " + ROLE_NAME + ";";
             
           retCrtRole = retCrtRole + "\n" + create_role;
           //var result_set = snowflake.execute ({sqlText: create_role});
           
           if (GRANTED_TO != '') //if no role to grant, just Functional Role
            {
              //Granting to Role
              var sql_cmd_role_grantedto = "GRANT ROLE " + ROLE_NAME + " TO ROLE " + GRANTED_TO + ";";

              retValueGrant = retValueGrant + "\n" + sql_cmd_role_grantedto;
              if (EXECUTE_Script) snowflake.execute ({sqlText: sql_cmd_role_grantedto});
            }

           sp_caller = sp_caller + "('" + ROLE_NAME + "','" + ASSIGNED_WAREHOUSE + "','" + GRANTED_TO + "'," + NEED_ON_FUTURE_TBLS + ");"

           forReturnt = forReturnt + "\n" +  sp_caller;
           //Call SP from here --> 
           /* */
           var result_set1 = snowflake.execute ({sqlText: sp_caller});
            while (result_set1.next()) 
            {
                forReturntAll = forReturntAll + "\n" + result_set1.getColumnValue(1);   
            } 
            
         }
         return "--Create Roles as !Securityadmin!: \n USE ROLE SECURITYADMIN; \n " + retCrtRole + "\n \n --Grant role to Parent Role " + retValueGrant + "\n \n -- RBAC script: \n" + forReturntAll;  
    $$;
 