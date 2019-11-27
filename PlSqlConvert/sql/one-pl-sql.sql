PROCEDURE SALES_ASSETS_DLY_EDR (p_date date) IS
-- MODIFICATION HISTORY
-- Person      Date    Comments
-- ---------   ------  --------------------------------------------
---- Esha Sardana March 2019 CM00105952 -Added new column COMP_GRID_SEGMENT in ip_foff_dly_trd_asset_snpsht
-------------------------------------------------------------------------------------------------------------------------

   d_process_dt    date;
   i_rpt_month_sid  NUMBER(10);
   d_as_of_dt      date;
   d_snpsht_run_dt  date;
   d_last_run_dt    date;


   BEGIN
        g_proc_nm := 'SALES_ASSETS_DLY_EDR';

        g_section := 'S100';
        if p_date is null then
           select src_extract_dt
             into d_snpsht_run_dt
           from dw_extract_dt_ctl;
        else
          d_snpsht_run_dt := p_date;
        end if;

        g_section := 'S120';
        select run_dt
        into d_last_run_dt
        from dw_score_crd_ctl s;


        g_section := 'S150';
        select distinct bus_process_dt into d_as_of_dt
        from etl_ip_foff_dly_trd_asset_tmp;

        g_section := 'S170';
        select m.month_sid into i_rpt_month_sid
        from month m where m.first_clnd_day_in_month_dt = trunc(d_as_of_dt,'MONTH');

        if trunc(d_snpsht_run_dt,'MONTH') = trunc(d_last_run_dt,'MONTH') then
          delete from dwedr.ip_foff_dly_trd_asset_snpsht;
        else
            delete from ip_foff_dly_trd_asset_snpsht where
              month_sid = i_rpt_month_sid;
        end if;

        g_section := 'S200';
        if p_date is null then
           select src_extract_dt
             into d_process_dt
           from dw_extract_dt_ctl;
        else
           d_process_dt := p_date;
        end if;

        g_section := 'S280';
        -- insert to EDR, SF contacts
        insert into ip_foff_dly_trd_asset_snpsht (
                          ip_sid, bus_process_dt, month_sid, sf_contact_id,
                          fund_offering_sid, line_of_bus_sid, accnt_func_ty_sid,
                          accnt_prog_sid, year_sid,
                          program_sid, mf_long_term_ind, mf_corp_class_ind, related_trd_fund_offering_sid,
                          whlslr_sid, territory_sid,  sls_rvp_emp_sid, iw_emp_sid,
                          focus_initiative_txt, adv_classf_ds, adv_sales_classf_ds, allnc_classf_ds, ip_sub_classf_ds, ip_chnl_cd, actv_ind,
                          ws_mtg_svc_std_cnt, iw_call_svc_std_cnt,
                          tot_asset_mkt_val_amt, stl_asset_mkt_val_amt,
                          mtd_purch_amt, mtd_rdmptn_amt, mtd_xchgin_amt, mtd_xchgout_amt, mtd_net_xchg_amt,
                          mtd_lt_purch_amt, mtd_lt_rdmptn_amt, mtd_st_purch_amt, mtd_st_rdmptn_amt,
                          mtd_allnc_purch_amt, mtd_allnc_rdmptn_amt, mtd_wrap_purch_amt, mtd_wrap_rdmptn_amt,
                          mtd_prspct_purch_amt, mtd_prspct_rdmptn_amt, mtd_hnw_purch_amt, mtd_hnw_rdmptn_amt,
                          mtd_mm_tot_xchgin_amt, mtd_mm_tot_xchgout_amt, mtd_mm_net_xchg_amt,
                          mtd_prspct_tot_xchgin_amt, mtd_prspct_tot_xchgout_amt, mtd_prspct_net_xchg_amt,
                          mtd_tax_eff_purch_amt, mtd_tax_eff_rdmptn_amt,
                          mtd_clearplan_tot_xchgin_amt, mtd_clearplan_tot_xchgout_amt, mtd_clearplan_net_xchg_amt,
                          lm_mtd_purch_amt, lm_mtd_rdmptn_amt,
                          lm_mtd_xchgin_amt, lm_mtd_xchgout_amt, lm_mtd_net_xchg_amt,
                          ytd_purch_amt, ytd_rdmptn_amt,
                          ytd_xchgin_amt, ytd_xchgout_amt, ytd_net_xchg_amt,
                          ly_mtd_purch_amt, ly_mtd_rdmptn_amt,
                          ly_mtd_xchgin_amt, ly_mtd_xchgout_amt, ly_mtd_net_xchg_amt,
                          ly_mtd_lt_purch_amt, ly_mtd_lt_rdmptn_amt, ly_mtd_st_purch_amt, ly_mtd_st_rdmptn_amt,
                          ly_ytd_purch_amt, ly_ytd_rdmptn_amt,
                          ly_ytd_xchgin_amt, ly_ytd_xchgout_amt, ly_ytd_net_xchg_amt,
                          mtd_purch_rke_amt, mtd_rdmptn_rke_amt,
                          mtd_purch_top10_prspct_amt, mtd_rdmptn_top10_prspct_amt,
                          sf_contact_record_ty_nm, brnch_advc_ip_ind, excluded_from_commsn_ind,
                          cvrg_drvr_txt, ws_cvrg_drvr_txt, iw_cvrg_drvr_txt, dflt_ws_svc_std_cnt, dflt_iw_svc_std_cnt,
                          bdm_sr_cvg_ind, bdm_sr_svc_std_cnt,comp_grid_segment)
        select          ip_to_use.ip_sid, a.bus_process_dt, i_rpt_month_sid , ip_to_use.sf_contact_id,
                          a.fund_offering_sid, a.line_of_bus_sid, a.accnt_func_ty_sid,
                          a.accnt_prog_sid, a.yr_sid,
                          a.program_sid, a.mf_long_term_ind, a.mf_corp_class_ind, a.related_trd_fund_offering_sid,
                          ss.whlslr_sid, ip_to_use.territory_sid,
                          ss.rvp_emp_sid, nvl(ss.inside_sales_emp_sid, -1),
                          ip_to_use.focus_initiative_txt, ip_to_use.adv_classf_ds, ip_to_use.adv_sales_classf_ds, ip_to_use.allnc_classf_ds, ip_to_use.ip_sub_classf_ds, ip_to_use.ip_chnl_cd, ip_to_use.actv_ind,
                          nvl(ip_to_use.ws_mtg_svc_std_cnt,0) ws_mtg_svc_std_cnt, nvl(ip_to_use.iw_call_svc_std_cnt,0) iw_call_svc_std_cnt,
                          sum(nvl(tot_asset_mkt_val_amt,0)) tot_asset_mkt_val_amt, sum(nvl(stl_asset_mkt_val_amt,0)) stl_asset_mkt_val_amt,
                          sum(nvl(mtd_purch_amt,0)) mtd_purch_amt, sum(nvl(mtd_rdmptn_amt,0)) mtd_rdmptn_amt, sum(nvl(mtd_xchgin_amt,0)) mtd_xchgin_amt, sum(nvl(mtd_xchgout_amt,0)) mtd_xchgout_amt, sum(nvl(mtd_net_xchg_amt,0)) mtd_net_xchg_amt,
                          sum(nvl(mtd_lt_purch_amt,0)) mtd_lt_purch_amt, sum(nvl(mtd_lt_rdmptn_amt,0)) mtd_lt_rdmptn_amt, sum(nvl(mtd_st_purch_amt,0)) mtd_st_purch_amt, sum(nvl(mtd_st_rdmptn_amt,0)) mtd_st_rdmptn_amt,
                          sum(nvl(mtd_allnc_purch_amt,0)) mtd_allnc_purch_amt, sum(nvl(mtd_allnc_rdmptn_amt,0)) mtd_allnc_rdmptn_amt, sum(nvl(mtd_wrap_purch_amt,0)) mtd_wrap_purch_amt, sum(nvl(mtd_wrap_rdmptn_amt,0)) mtd_wrap_rdmptn_amt,
                          sum(nvl(mtd_prspct_purch_amt,0)) mtd_prspct_purch_amt, sum(nvl(mtd_prspct_rdmptn_amt,0)) mtd_prspct_rdmptn_amt, sum(nvl(mtd_hnw_purch_amt,0)) mtd_hnw_purch_amt, sum(nvl(mtd_hnw_rdmptn_amt,0)) mtd_hnw_rdmptn_amt,
                          sum(nvl(mtd_mm_tot_xchgin_amt,0)) mtd_mm_tot_xchgin_amt, sum(nvl(mtd_mm_tot_xchgout_amt,0)) mtd_mm_tot_xchgout_amt, sum(nvl(mtd_mm_net_xchg_amt,0)) mtd_mm_net_xchg_amt,
                          sum(nvl(mtd_prspct_tot_xchgin_amt,0)) mtd_prspct_tot_xchgin_amt, sum(nvl(mtd_prspct_tot_xchgout_amt,0)) mtd_prspct_tot_xchgout_amt, sum(nvl(mtd_prspct_net_xchg_amt,0)) mtd_prspct_net_xchg_amt,
                          sum(nvl(mtd_tax_eff_purch_amt,0)) mtd_tax_eff_purch_amt, sum(nvl(mtd_tax_eff_rdmptn_amt,0)) mtd_tax_eff_rdmptn_amt,
                          sum(nvl(mtd_clearplan_tot_xchgin_amt,0)) mtd_clearplan_tot_xchgin_amt, sum(nvl(mtd_clearplan_tot_xchgout_amt,0)) mtd_clearplan_tot_xchgout_amt, sum(nvl(mtd_clearplan_net_xchg_amt,0)) mtd_clearplan_net_xchg_amt,
                          sum(nvl(lm_mtd_purch_amt,0)) lm_mtd_purch_amt, sum(nvl(lm_mtd_rdmptn_amt,0)) lm_mtd_rdmptn_amt,
                          sum(nvl(lm_mtd_xchgin_amt,0)) lm_mtd_xchgin_amt, sum(nvl(lm_mtd_xchgout_amt,0)) lm_mtd_xchgout_amt, sum(nvl(lm_mtd_net_xchg_amt,0)) lm_mtd_net_xchg_amt,
                          sum(nvl(ytd_purch_amt,0)) ytd_purch_amt, sum(nvl(ytd_rdmptn_amt,0)) ytd_rdmptn_amt,
                          sum(nvl(ytd_xchgin_amt,0)) ytd_xchgin_amt, sum(nvl(ytd_xchgout_amt,0)) ytd_xchgout_amt, sum(nvl(ytd_net_xchg_amt,0)) ytd_net_xchg_amt,
                          sum(nvl(ly_mtd_purch_amt,0)) ly_mtd_purch_amt, sum(nvl(ly_mtd_rdmptn_amt,0)) ly_mtd_rdmptn_amt,
                          sum(nvl(ly_mtd_xchgin_amt,0)) ly_mtd_xchgin_amt, sum(nvl(ly_mtd_xchgout_amt,0)) ly_mtd_xchgout_amt, sum(nvl(ly_mtd_net_xchg_amt,0)) ly_mtd_net_xchg_amt,
                          sum(nvl(ly_mtd_lt_purch_amt,0)) ly_mtd_lt_purch_amt, sum(nvl(ly_mtd_lt_rdmptn_amt,0)) ly_mtd_lt_rdmptn_amt, sum(nvl(ly_mtd_st_purch_amt,0)) ly_mtd_st_purch_amt, sum(nvl(ly_mtd_st_rdmptn_amt,0)) ly_mtd_st_rdmptn_amt,
                          sum(nvl(ly_ytd_purch_amt,0)) ly_ytd_purch_amt, sum(nvl(ly_ytd_rdmptn_amt,0)) ly_ytd_rdmptn_amt,
                          sum(nvl(ly_ytd_xchgin_amt,0)) ly_ytd_xchgin_amt, sum(nvl(ly_ytd_xchgout_amt,0)) ly_ytd_xchgout_amt, sum(nvl(ly_ytd_net_xchg_amt,0)) ly_ytd_net_xchg_amt,
                          sum(nvl(mtd_purch_rke_amt,0)) mtd_purch_rke_amt, sum(nvl(mtd_rdmptn_rke_amt,0)) mtd_rdmptn_rke_amt,
                          sum(nvl(mtd_purch_top10_prspct_amt,0)) mtd_purch_top10_prspct_amt, sum(nvl(mtd_rdmptn_top10_prspct_amt,0)) mtd_rdmptn_top10_prspct_amt,
                          ip_to_use.sf_contact_record_ty_nm, ip_to_use.brnch_advc_ip_ind,
                          ip_to_use.excluded_from_commsn_ind, ip_to_use.cvrg_drvr_txt, ip_to_use.ws_cvrg_drvr_txt,
                          ip_to_use.iw_cvrg_drvr_txt, nvl(ip_to_use.dflt_ws_svc_std_cnt,0) dflt_ws_svc_std_cnt, nvl(ip_to_use.dflt_iw_svc_std_cnt,0) dflt_iw_svc_std_cnt,
                          nvl(ip_to_use.bdm_sr_cvg_ind,'N') bdm_sr_cvg_ind, nvl(ip_to_use.bdm_sr_svc_std_cnt,0) bdm_sr_svc_std_cnt,ip_to_use.comp_grid_segment
        from investment_professional ip, etl_ip_foff_dly_trd_asset_tmp a, investment_professional ip_to_use, sales_territory_dly_snpsht ss
        where ip.ip_sid = a.ip_sid
            and ip.fsa_ip_id <> -10
            and ip.fsa_ip_id <> -1
            and ip.fsa_ip_id = ip_to_use.fsa_ip_id
            and d_process_dt >= ip_to_use.sid_start_dt
            and d_process_dt < nvl(ip_to_use.sid_end_dt, to_date('31-DEC-9999', 'DD-MON-YYYY'))
           and ip_to_use.territory_sid = ss.territory_sid
            and a.bus_process_dt = ss.bus_process_dt
        group by    ip_to_use.ip_sid, a.bus_process_dt, i_rpt_month_sid ,ip_to_use.sf_contact_id, a.fund_offering_sid, a.line_of_bus_sid, a.accnt_func_ty_sid, /*a.accnt_tax_ty_cd, a.accnt_regstr_ty_cd,*/
                        accnt_prog_sid, yr_sid,
                        a.program_sid, a.mf_long_term_ind, a.mf_corp_class_ind, a.related_trd_fund_offering_sid,
                        ss.whlslr_sid, ip_to_use.territory_sid,
                        ss.rvp_emp_sid, nvl(ss.inside_sales_emp_sid, -1),
                        ip_to_use.focus_initiative_txt, ip_to_use.adv_classf_ds, ip_to_use.adv_sales_classf_ds, ip_to_use.allnc_classf_ds, ip_to_use.ip_sub_classf_ds, ip_to_use.ip_chnl_cd, ip_to_use.actv_ind,
                        ip_to_use.ws_mtg_svc_std_cnt, ip_to_use.iw_call_svc_std_cnt,
                        ip_to_use.sf_contact_record_ty_nm, ip_to_use.brnch_advc_ip_ind,
                        ip_to_use.excluded_from_commsn_ind, ip_to_use.cvrg_drvr_txt, ip_to_use.ws_cvrg_drvr_txt,
                        ip_to_use.iw_cvrg_drvr_txt, ip_to_use.dflt_ws_svc_std_cnt, ip_to_use.dflt_iw_svc_std_cnt,
                        ip_to_use.bdm_sr_cvg_ind, ip_to_use.bdm_sr_svc_std_cnt,ip_to_use.comp_grid_segment;

        g_section := 'S300';
        -- insert to EDR, AXIS only IPs/DRs
        insert into ip_foff_dly_trd_asset_snpsht (
                          ip_sid, bus_process_dt, month_sid,
                          fund_offering_sid, line_of_bus_sid, accnt_func_ty_sid,
                          accnt_prog_sid, year_sid,
                          program_sid, mf_long_term_ind, mf_corp_class_ind, related_trd_fund_offering_sid,
                          whlslr_sid, territory_sid,
                          sls_rvp_emp_sid, iw_emp_sid,
                          focus_initiative_txt, adv_classf_ds, adv_sales_classf_ds, allnc_classf_ds, ip_sub_classf_ds, ip_chnl_cd, actv_ind,
                          ws_mtg_svc_std_cnt, iw_call_svc_std_cnt,
                          tot_asset_mkt_val_amt, stl_asset_mkt_val_amt,
                          mtd_purch_amt, mtd_rdmptn_amt, mtd_xchgin_amt, mtd_xchgout_amt, mtd_net_xchg_amt,
                          mtd_lt_purch_amt, mtd_lt_rdmptn_amt, mtd_st_purch_amt, mtd_st_rdmptn_amt,
                          mtd_allnc_purch_amt, mtd_allnc_rdmptn_amt, mtd_wrap_purch_amt, mtd_wrap_rdmptn_amt,
                          mtd_prspct_purch_amt, mtd_prspct_rdmptn_amt, mtd_hnw_purch_amt, mtd_hnw_rdmptn_amt,
                          mtd_mm_tot_xchgin_amt, mtd_mm_tot_xchgout_amt, mtd_mm_net_xchg_amt,
                          mtd_prspct_tot_xchgin_amt, mtd_prspct_tot_xchgout_amt, mtd_prspct_net_xchg_amt,
                          mtd_tax_eff_purch_amt, mtd_tax_eff_rdmptn_amt,
                          mtd_clearplan_tot_xchgin_amt, mtd_clearplan_tot_xchgout_amt, mtd_clearplan_net_xchg_amt,
                          lm_mtd_purch_amt, lm_mtd_rdmptn_amt,
                          lm_mtd_xchgin_amt, lm_mtd_xchgout_amt, lm_mtd_net_xchg_amt,
                          ytd_purch_amt, ytd_rdmptn_amt,
                          ytd_xchgin_amt, ytd_xchgout_amt, ytd_net_xchg_amt,
                          ly_mtd_purch_amt, ly_mtd_rdmptn_amt,
                          ly_mtd_xchgin_amt, ly_mtd_xchgout_amt, ly_mtd_net_xchg_amt,
                          ly_mtd_lt_purch_amt, ly_mtd_lt_rdmptn_amt, ly_mtd_st_purch_amt, ly_mtd_st_rdmptn_amt,
                          ly_ytd_purch_amt, ly_ytd_rdmptn_amt,
                          ly_ytd_xchgin_amt, ly_ytd_xchgout_amt, ly_ytd_net_xchg_amt,
                          mtd_purch_rke_amt, mtd_rdmptn_rke_amt,
                          mtd_purch_top10_prspct_amt, mtd_rdmptn_top10_prspct_amt,
                          sf_contact_record_ty_nm, brnch_advc_ip_ind,
                          excluded_from_commsn_ind, cvrg_drvr_txt, ws_cvrg_drvr_txt,
                          iw_cvrg_drvr_txt, dflt_ws_svc_std_cnt, dflt_iw_svc_std_cnt,
                          bdm_sr_cvg_ind, bdm_sr_svc_std_cnt,comp_grid_segment)
        select ip_to_use.ip_sid, a.bus_process_dt, i_rpt_month_sid ,
                          a.fund_offering_sid, a.line_of_bus_sid, a.accnt_func_ty_sid,
                          a.accnt_prog_sid, a.yr_sid,
                          a.program_sid, a.mf_long_term_ind, a.mf_corp_class_ind, a.related_trd_fund_offering_sid,
                          ss.whlslr_sid, ip_to_use.territory_sid,
                          ss.rvp_emp_sid, nvl(ss.inside_sales_emp_sid, -1),
                          ip_to_use.focus_initiative_txt, ip_to_use.adv_classf_ds, ip_to_use.adv_sales_classf_ds, ip_to_use.allnc_classf_ds, ip_to_use.ip_sub_classf_ds, ip_to_use.ip_chnl_cd, ip_to_use.actv_ind,
                          nvl(ip_to_use.ws_mtg_svc_std_cnt,0) ws_mtg_svc_std_cnt, nvl(ip_to_use.iw_call_svc_std_cnt,0) iw_call_svc_std_cnt,
                          sum(nvl(tot_asset_mkt_val_amt,0)) tot_asset_mkt_val_amt, sum(nvl(stl_asset_mkt_val_amt,0)) stl_asset_mkt_val_amt,
                          sum(nvl(mtd_purch_amt,0)) mtd_purch_amt, sum(nvl(mtd_rdmptn_amt,0)) mtd_rdmptn_amt, sum(nvl(mtd_xchgin_amt,0)) mtd_xchgin_amt, sum(nvl(mtd_xchgout_amt,0)) mtd_xchgout_amt, sum(nvl(mtd_net_xchg_amt,0)) mtd_net_xchg_amt,
                          sum(nvl(mtd_lt_purch_amt,0)) mtd_lt_purch_amt, sum(nvl(mtd_lt_rdmptn_amt,0)) mtd_lt_rdmptn_amt, sum(nvl(mtd_st_purch_amt,0)) mtd_st_purch_amt, sum(nvl(mtd_st_rdmptn_amt,0)) mtd_st_rdmptn_amt,
                          sum(nvl(mtd_allnc_purch_amt,0)) mtd_allnc_purch_amt, sum(nvl(mtd_allnc_rdmptn_amt,0)) mtd_allnc_rdmptn_amt, sum(nvl(mtd_wrap_purch_amt,0)) mtd_wrap_purch_amt, sum(nvl(mtd_wrap_rdmptn_amt,0)) mtd_wrap_rdmptn_amt,
                          sum(nvl(mtd_prspct_purch_amt,0)) mtd_prspct_purch_amt, sum(nvl(mtd_prspct_rdmptn_amt,0)) mtd_prspct_rdmptn_amt, sum(nvl(mtd_hnw_purch_amt,0)) mtd_hnw_purch_amt, sum(nvl(mtd_hnw_rdmptn_amt,0)) mtd_hnw_rdmptn_amt,
                          sum(nvl(mtd_mm_tot_xchgin_amt,0)) mtd_mm_tot_xchgin_amt, sum(nvl(mtd_mm_tot_xchgout_amt,0)) mtd_mm_tot_xchgout_amt, sum(nvl(mtd_mm_net_xchg_amt,0)) mtd_mm_net_xchg_amt,
                          sum(nvl(mtd_prspct_tot_xchgin_amt,0)) mtd_prspct_tot_xchgin_amt, sum(nvl(mtd_prspct_tot_xchgout_amt,0)) mtd_prspct_tot_xchgout_amt, sum(nvl(mtd_prspct_net_xchg_amt,0)) mtd_prspct_net_xchg_amt,
                          sum(nvl(mtd_tax_eff_purch_amt,0)) mtd_tax_eff_purch_amt, sum(nvl(mtd_tax_eff_rdmptn_amt,0)) mtd_tax_eff_rdmptn_amt,
                          sum(nvl(mtd_clearplan_tot_xchgin_amt,0)) mtd_clearplan_tot_xchgin_amt, sum(nvl(mtd_clearplan_tot_xchgout_amt,0)) mtd_clearplan_tot_xchgout_amt, sum(nvl(mtd_clearplan_net_xchg_amt,0)) mtd_clearplan_net_xchg_amt,
                          sum(nvl(lm_mtd_purch_amt,0)) lm_mtd_purch_amt, sum(nvl(lm_mtd_rdmptn_amt,0)) lm_mtd_rdmptn_amt,
                          sum(nvl(lm_mtd_xchgin_amt,0)) lm_mtd_xchgin_amt, sum(nvl(lm_mtd_xchgout_amt,0)) lm_mtd_xchgout_amt, sum(nvl(lm_mtd_net_xchg_amt,0)) lm_mtd_net_xchg_amt,
                          sum(nvl(ytd_purch_amt,0)) ytd_purch_amt, sum(nvl(ytd_rdmptn_amt,0)) ytd_rdmptn_amt,
                          sum(nvl(ytd_xchgin_amt,0)) ytd_xchgin_amt, sum(nvl(ytd_xchgout_amt,0)) ytd_xchgout_amt, sum(nvl(ytd_net_xchg_amt,0)) ytd_net_xchg_amt,
                          sum(nvl(ly_mtd_purch_amt,0)) ly_mtd_purch_amt, sum(nvl(ly_mtd_rdmptn_amt,0)) ly_mtd_rdmptn_amt,
                          sum(nvl(ly_mtd_xchgin_amt,0)) ly_mtd_xchgin_amt, sum(nvl(ly_mtd_xchgout_amt,0)) ly_mtd_xchgout_amt, sum(nvl(ly_mtd_net_xchg_amt,0)) ly_mtd_net_xchg_amt,
                          sum(nvl(ly_mtd_lt_purch_amt,0)) ly_mtd_lt_purch_amt, sum(nvl(ly_mtd_lt_rdmptn_amt,0)) ly_mtd_lt_rdmptn_amt, sum(nvl(ly_mtd_st_purch_amt,0)) ly_mtd_st_purch_amt, sum(nvl(ly_mtd_st_rdmptn_amt,0)) ly_mtd_st_rdmptn_amt,
                          sum(nvl(ly_ytd_purch_amt,0)) ly_ytd_purch_amt, sum(nvl(ly_ytd_rdmptn_amt,0)) ly_ytd_rdmptn_amt,
                          sum(nvl(ly_ytd_xchgin_amt,0)) ly_ytd_xchgin_amt, sum(nvl(ly_ytd_xchgout_amt,0)) ly_ytd_xchgout_amt, sum(nvl(ly_ytd_net_xchg_amt,0)) ly_ytd_net_xchg_amt,
                          sum(nvl(mtd_purch_rke_amt,0)) mtd_purch_rke_amt, sum(nvl(mtd_rdmptn_rke_amt,0)) mtd_rdmptn_rke_amt,
                          sum(nvl(mtd_purch_top10_prspct_amt,0)) mtd_purch_top10_prspct_amt, sum(nvl(mtd_rdmptn_top10_prspct_amt,0)) mtd_rdmptn_top10_prspct_amt,
                          ip_to_use.sf_contact_record_ty_nm, ip_to_use.brnch_advc_ip_ind,
                          ip_to_use.excluded_from_commsn_ind, ip_to_use.cvrg_drvr_txt, ip_to_use.ws_cvrg_drvr_txt,
                          ip_to_use.iw_cvrg_drvr_txt, nvl(ip_to_use.dflt_ws_svc_std_cnt,0) dflt_ws_svc_std_cnt, nvl(ip_to_use.dflt_iw_svc_std_cnt,0) dflt_iw_svc_std_cnt,
                          nvl(ip_to_use.bdm_sr_cvg_ind,'N') bdm_sr_cvg_ind, nvl(ip_to_use.bdm_sr_svc_std_cnt,0) bdm_sr_svc_std_cnt,ip_to_use.comp_grid_segment
        from investment_professional ip, etl_ip_foff_dly_trd_asset_tmp a, investment_professional ip_to_use, sales_territory_dly_snpsht ss
        where ip.ip_sid = a.ip_sid
            and ip.fsa_ip_id = -1
            and ip.fsa_ip_id = ip_to_use.fsa_ip_id
            and ip.prim_firm_cd = ip_to_use.prim_firm_cd
            and ip.prim_rep_cd = ip_to_use.prim_rep_cd
            and d_process_dt >= ip_to_use.sid_start_dt
            and d_process_dt < nvl(ip_to_use.sid_end_dt, TO_DATE('31-DEC-9999', 'DD-MON-YYYY'))
            and ip_to_use.territory_sid = ss.territory_sid
            and a.bus_process_dt = ss.bus_process_dt
        group by    ip_to_use.ip_sid, a.bus_process_dt, i_rpt_month_sid ,a.fund_offering_sid, a.line_of_bus_sid, a.accnt_func_ty_sid,
                        a.accnt_prog_sid, a.yr_sid,
                        a.program_sid, a.mf_long_term_ind, a.mf_corp_class_ind, a.related_trd_fund_offering_sid,
                        ss.whlslr_sid, ip_to_use.territory_sid,
                        ss.rvp_emp_sid, nvl(ss.inside_sales_emp_sid, -1),
                        ip_to_use.focus_initiative_txt, ip_to_use.adv_classf_ds, ip_to_use.adv_sales_classf_ds, ip_to_use.allnc_classf_ds, ip_to_use.ip_sub_classf_ds, ip_to_use.ip_chnl_cd, ip_to_use.actv_ind,
                        ip_to_use.ws_mtg_svc_std_cnt, ip_to_use.iw_call_svc_std_cnt,
                        ip_to_use.sf_contact_record_ty_nm, ip_to_use.brnch_advc_ip_ind,
                        ip_to_use.excluded_from_commsn_ind, ip_to_use.cvrg_drvr_txt, ip_to_use.ws_cvrg_drvr_txt,
                        ip_to_use.iw_cvrg_drvr_txt, ip_to_use.dflt_ws_svc_std_cnt, ip_to_use.dflt_iw_svc_std_cnt,
                        ip_to_use.bdm_sr_cvg_ind, ip_to_use.bdm_sr_svc_std_cnt,ip_to_use.comp_grid_segment;

        commit;

        DBMS_OUTPUT.put_line (g_section ||' '|| to_char(sysdate, 'YYYY-MM-DD HH24:MI:SS'));

   EXCEPTION
      when others then
            raise_application_error (SP_ERROR, g_proc_nm || ' Section: ' || g_section ||' ' || sqlerrm);
   END SALES_ASSETS_DLY_EDR;
