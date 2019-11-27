PROCEDURE SALES_ASSETS_DLY_EDR (p_date date) IS
-- MODIFICATION HISTORY
-- Person      Date    Comments
-- ---------   ------  --------------------------------------------
---- Esha Sardana March 2019 CM00105952 -Added new column COMP_GRID_SEGMENT in ip_foff_dly_trd_asset_snpsht
-------------------------------------------------------------------------------------------------------------------------

   d_process_dt    date
var rs = snowflake.execute( {sqlText: "   i_rpt_month_sid  NUMBER(10);"} );
var rs = snowflake.execute( {sqlText: "   d_as_of_dt      date;"} );
var rs = snowflake.execute( {sqlText: "   d_snpsht_run_dt  date;"} );
var rs = snowflake.execute( {sqlText: "   d_last_run_dt    date;"} );
var rs = snowflake.execute( {sqlText: "SET            g_proc_nm = 'SALES_ASSETS_DLY_EDR';"} );
var rs = snowflake.execute( {sqlText: "SET         g_section = 'S100';"} );
        if p_date is null then 
var rs = snowflake.execute( {sqlText: "
           select src_extract_dt
             into d_snpsht_run_dt
           from dw_extract_dt_ctl;"} );
        else
          d_snpsht_run_dt := p_date
        ;
var rs = snowflake.execute( {sqlText: "SET         g_section = 'S120';"} );
var rs = snowflake.execute( {sqlText: "        select run_dt        into d_last_run_dt        from dw_score_crd_ctl s;"} );
var rs = snowflake.execute( {sqlText: "SET         g_section = 'S150';"} );
var rs = snowflake.execute( {sqlText: "        select distinct bus_process_dt into d_as_of_dt        from etl_ip_foff_dly_trd_asset_tmp;"} );
var rs = snowflake.execute( {sqlText: "SET         g_section = 'S170';"} );
var rs = snowflake.execute( {sqlText: "        select m.month_sid into i_rpt_month_sid        from month m where m.first_clnd_day_in_month_dt = trunc(d_as_of_dt,'MONTH');"} );

        if trunc(d_snpsht_run_dt,'MONTH') = trunc(d_last_run_dt,'MONTH') then 
var rs = snowflake.execute( {sqlText: "
          delete from dwedr.ip_foff_dly_trd_asset_snpsht;"} );
         else
var rs = snowflake.execute( {sqlText: "
            delete from ip_foff_dly_trd_asset_snpsht where
              month_sid = i_rpt_month_sid;"} );
        ;
var rs = snowflake.execute( {sqlText: "SET         g_section = 'S200';"} );
        if p_date is null then 
var rs = snowflake.execute( {sqlText: "
           select src_extract_dt
             into d_process_dt
           from dw_extract_dt_ctl;"} );
        else
           d_process_dt := p_date
        ;
var rs = snowflake.execute( {sqlText: ";"} );
 $$;