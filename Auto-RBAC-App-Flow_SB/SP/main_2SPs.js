create or replace procedure SP_ROLE_ASSIGNER
    (ROLE_NAME VARCHAR, WAREHOUSE_NAME VARCHAR, GRANT_ONFUTURE BOOLEAN)
returns string
language javascript
strict
execute as caller
as
$$

//Parameter that allows CMD Execution, 'false' => just text, no execution
var EXECUTE_Script = false

var retValueFrom = "";
var SQL_ACCESS =
    "select ROLES, DB_NAME, SCHEMA_NAME, SCHEMA_MNGR,PRIVILEGE from RBAC_DB_ACCESS_MNG unpivot(privilege for ROLES in (" + ROLE_NAME + ")) WHERE PRIVILEGE <> ''";

var result_set_access = snowflake.execute({ sqlText: SQL_ACCESS });
var retValueFromIf = "";
var schema = "";

while (result_set_access.next()) {
   
    var ROLE_NAME = result_set_access.getColumnValue(1);
    var DB_NAME = result_set_access.getColumnValue(2);
    var SCHEMA_NAME = result_set_access.getColumnValue(3);
    var ROLE_MNGD_SCHEMA = result_set_access.getColumnValue(4).toUpperCase(); 
    var ACCESS_CODE = result_set_access.getColumnValue(5).toUpperCase(); 
        
    retValueFrom = retValueFrom + "\n" + "--New Schema: " + SCHEMA_NAME;

    var checkAccessCode = ACCESS_CODE.charAt(0);//check if the first letter A or S

    if (checkAccessCode == 'S') {
        //retValueFromIf = "Security Only";
        var sql_cmd_for_skrt =
            "USE ROLE SECURITYADMIN; \n GRANT CREATE USER, CREATE ROLE, MANAGE GRANTS TO ROLE " + ROLE_NAME + ";";
        if (EXECUTE_Script) snowflake.execute ({sqlText: sql_cmd_for_skrt});

        retValueFrom = sql_cmd_for_skrt + "\n";

    } else if (checkAccessCode == 'A') {
        retValueFromIf = "Sys Only";
        //grant CREATE DATABASE on account to sysadmin;
        var sql_cmd_for_acc =
            "USE ROLE SYSADMIN; \n " + 
            "GRANT CREATE DATABASE, CREATE WAREHOUSE ON ACCOUNT TO " + ROLE_NAME + ";";
        if (EXECUTE_Script) snowflake.execute ({sqlText: sql_cmd_for_acc});
        var sql_cmd_for_db =
            "GRANT ALL ON DATABASE " + DB_NAME + " TO ROLE " + ROLE_NAME + ";";
        if (EXECUTE_Script) snowflake.execute ({sqlText: sql_cmd_for_db});
        
        var sql_cmd_for_schema =
            "GRANT ALL ON ALL SCHEMAS IN DATABASE " + DB_NAME + " TO ROLE " + ROLE_NAME + ";";
        if (EXECUTE_Script) snowflake.execute ({sqlText: sql_cmd_for_schema});
        retValueFrom = retValueFrom + "\n" + sql_cmd_for_acc + "\n" + sql_cmd_for_db + "\n" + sql_cmd_for_schema + "\n";

    } 
    if ((checkAccessCode == 'A' || checkAccessCode == 'S')) //Checks, it is NOT Admin nor Security
        {
            //Admin or Security
        }
        else 
        {
            //retValueFromIf = retValueFromIf + "::RWO+not Sec or Sys ";
            var sql_cmd_for_db =
                "USE ROLE SYSADMIN;-- Or role assigned to perform this \n " +
                "GRANT USAGE ON DATABASE " + DB_NAME + " TO ROLE " + ROLE_NAME + " ;"; //?? ONLY USAGE on DB or need CREATE SCHEMA ???
            if (EXECUTE_Script) snowflake.execute ({sqlText: sql_cmd_for_db});
            
            var sql_cmd_mngd_schema_role_set = '';

            if (ROLE_MNGD_SCHEMA.length != 0)
            {
                sql_cmd_mngd_schema_role_set = 'USE ROLE ' + ROLE_MNGD_SCHEMA + ';'
                if (EXECUTE_Script) snowflake.execute ({sqlText: sql_cmd_mngd_schema_role_set});
            }

            if (ACCESS_CODE.includes("O")) //in a case 'RWO' Operate: Create, Delete, Modify
            {
                var sql_cmd_for_schema =
                    "GRANT ALL ON SCHEMA " + DB_NAME + "." + SCHEMA_NAME + " TO ROLE " + ROLE_NAME + ";";
                
                if (EXECUTE_Script) snowflake.execute ({sqlText: sql_cmd_for_schema});
                retValueFrom = retValueFrom + "\n" + sql_cmd_for_db + "\n" + sql_cmd_mngd_schema_role_set +  "\n" + sql_cmd_for_schema + "\n";
            }
            else 
            {
                //  add Granting on schema level...
                var sql_cmd_for_schema =
                    "GRANT USAGE ON SCHEMA " + DB_NAME + "." + SCHEMA_NAME + " TO ROLE " + ROLE_NAME + ";";
                
                if (EXECUTE_Script) snowflake.execute ({sqlText: sql_cmd_for_schema});
                retValueFrom = retValueFrom + "\n" + sql_cmd_for_db + "\n" + sql_cmd_mngd_schema_role_set +  "\n" + sql_cmd_for_schema + "\n";
            }

            {
                // Process ACCESS for Tables
                var sql_cmd_for_tables = "";
                var sql_cmd_grant_on_future = "";

                var ACCESS_CODE_stripped = ACCESS_CODE.replace("O", "");//remove 'Operation'
                
                switch (ACCESS_CODE_stripped) {
                    case "R":
                        // code block
                        sql_cmd_for_tables =
                            "GRANT SELECT ON ALL TABLES IN SCHEMA " + DB_NAME + "." + SCHEMA_NAME + " TO ROLE " + ROLE_NAME + ";";
                        if (GRANT_ONFUTURE == true)
                            sql_cmd_grant_on_future =
                                "GRANT SELECT ON FUTURE TABLES IN SCHEMA " + DB_NAME + "." + SCHEMA_NAME + " TO ROLE " + ROLE_NAME + ";";
                        break;
                    case "RW":
                        // code block
                        sql_cmd_for_tables =
                            "GRANT ALL ON ALL TABLES IN SCHEMA " + DB_NAME + "." + SCHEMA_NAME + " TO ROLE " + ROLE_NAME + ";";
                        if (GRANT_ONFUTURE == true)
                            sql_cmd_grant_on_future =
                                "GRANT ALL ON FUTURE TABLES IN SCHEMA " + DB_NAME + "." + SCHEMA_NAME + " TO ROLE " + ROLE_NAME + ";";
                        break;
                    case "W":
                        // code block
                        sql_cmd_for_tables =
                            "GRANT INSERT, UPDATE, DELETE, REFERENCES ON ALL TABLES IN SCHEMA " + DB_NAME + "." + SCHEMA_NAME + " TO ROLE " + ROLE_NAME + ";";
                            if (GRANT_ONFUTURE == true)
                            sql_cmd_grant_on_future =
                                "GRANT INSERT, UPDATE, DELETE on future tables in schema " + DB_NAME + "." + SCHEMA_NAME + " TO ROLE " + ROLE_NAME + ";";
                        break;
                    default:
                        // code block
                        var sql_cmd_for_tables = "";//Generate an error
                        sql_cmd_grant_on_future = "";
                }
                
                //Execute SQL to grant ACCESS on Databse.SCHEMA.TABLES
                if (EXECUTE_Script) snowflake.execute ({sqlText: sql_cmd_for_tables}); 
                
                //retValueFrom = retValueFrom + "\n" + sql_cmd_usedb  + "\n" + sql_cmd_for_tables;
                retValueFrom = retValueFrom + "\n" + sql_cmd_for_tables + "\n" + sql_cmd_grant_on_future + "\n";
            } 
        }   
}

// Assign a Warehouse to role // ?? Operate, ...???
var sql_cmd_for_warehouse = 
    "USE ROLE SYSADMIN; \n " + 
    "GRANT USAGE, OPERATE ON WAREHOUSES " + WAREHOUSE_NAME + " TO ROLE " + ROLE_NAME + ";";
    
if (EXECUTE_Script) snowflake.execute ({sqlText: sql_cmd_for_warehouse});

retValueFrom = retValueFrom + "\n" + sql_cmd_for_warehouse + "\n";

return "--New Role :::\n" + retValueFrom;
$$
;