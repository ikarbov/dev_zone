ACCESS_CODE_stripped:RW:::

grant USAGE on database PROD to role dynamic_prod_devops ;
grant ALL on ALL schemas in database PROD to role dynamic_prod_devops;

GRANT ALL ON ALL TABLES IN SCHEMA PROD.INFORMATION_SCHEMA to role dynamic_prod_devops;
GRANT ALL ON ALL TABLES IN SCHEMA PROD.PUBLIC to role dynamic_prod_devops;
GRANT ALL ON ALL TABLES IN SCHEMA PROD.RBAC_DEV to role dynamic_prod_devops;
GRANT ALL ON ALL TABLES IN SCHEMA PROD.RBAC_PROD to role dynamic_prod_devops;
GRANT ALL ON ALL TABLES IN SCHEMA PROD.RBAC_PS to role dynamic_prod_devops;
GRANT ALL ON ALL TABLES IN SCHEMA PROD.RBAC_QA to role dynamic_prod_devops;
GRANT ALL ON ALL TABLES IN SCHEMA PROD.VISUALIZATION to role dynamic_prod_devops;
grant USAGE on database QA to role dynamic_prod_devops ;
grant ALL on ALL schemas in database QA to role dynamic_prod_devops;

GRANT ALL ON ALL TABLES IN SCHEMA QA.INFORMATION_SCHEMA to role dynamic_prod_devops;
GRANT ALL ON ALL TABLES IN SCHEMA QA.PUBLIC to role dynamic_prod_devops;
GRANT ALL ON ALL TABLES IN SCHEMA QA.RBAC_DEV to role dynamic_prod_devops;
GRANT ALL ON ALL TABLES IN SCHEMA QA.RBAC_PROD to role dynamic_prod_devops;
GRANT ALL ON ALL TABLES IN SCHEMA QA.RBAC_PS to role dynamic_prod_devops;
GRANT ALL ON ALL TABLES IN SCHEMA QA.RBAC_QA to role dynamic_prod_devops;
GRANT ALL ON ALL TABLES IN SCHEMA QA.VISUALIZATION to role dynamic_prod_devops;














grant USAGE on database QA to role dynamic_prod_devops ;
grant ALL on ALL schemas in database QA to role dynamic_prod_devops;

GRANT ALL ON ALL TABLES IN SCHEMA QA.INFORMATION_SCHEMA to role dynamic_prod_devops;
GRANT ALL ON ALL TABLES IN SCHEMA QA.PUBLIC to role dynamic_prod_devops;
GRANT ALL ON ALL TABLES IN SCHEMA QA.RBAC_DEV to role dynamic_prod_devops;
GRANT ALL ON ALL TABLES IN SCHEMA QA.RBAC_PROD to role dynamic_prod_devops;
GRANT ALL ON ALL TABLES IN SCHEMA QA.RBAC_PS to role dynamic_prod_devops;
GRANT ALL ON ALL TABLES IN SCHEMA QA.RBAC_QA to role dynamic_prod_devops;
GRANT ALL ON ALL TABLES IN SCHEMA QA.VISUALIZATION to role dynamic_prod_devops;
grant USAGE on database DEV to role dynamic_prod_devops ;
grant ALL on ALL schemas in database DEV to role dynamic_prod_devops;

GRANT ALL ON ALL TABLES IN SCHEMA DEV.INFORMATION_SCHEMA to role dynamic_prod_devops;
GRANT ALL ON ALL TABLES IN SCHEMA DEV.PUBLIC to role dynamic_prod_devops;
GRANT ALL ON ALL TABLES IN SCHEMA DEV.RBAC_DEV to role dynamic_prod_devops;
GRANT ALL ON ALL TABLES IN SCHEMA DEV.RBAC_PROD to role dynamic_prod_devops;
GRANT ALL ON ALL TABLES IN SCHEMA DEV.RBAC_PS to role dynamic_prod_devops;
GRANT ALL ON ALL TABLES IN SCHEMA DEV.RBAC_QA to role dynamic_prod_devops;
GRANT ALL ON ALL TABLES IN SCHEMA DEV.VISUALIZATION to role dynamic_prod_devops;
grant usage, operate on warehouse WAREHOUSE_2 to role dynamic_prod_devops;

grant role dynamic_prod_devops to role GRANT_TO_ROLE;