/*
ssc install numdate
ssc install winsor
ssc install ftools
ssc install asreg
ssc install estout
ssc install erepost
*/


clear
eststo clear


import delimited "https://raw.githubusercontent.com/connorpn/cnolan-thesis/main/output/carbon_emissions_stock_returns_vars.csv"


label variable ticker "ticker"
sort ticker 	
encode ticker, gen(ticker_encode)


numdate monthly date = yearmonth, p(YM)
sort date

winsor bm, gen(winsor_bm) p(0.025)
winsor leverage, gen(winsor_leverage) p(0.025)
winsor mom, gen(winsor_mom) p(0.005)
winsor investa, gen(winsor_investa) p(0.025)
winsor roe, gen(winsor_roe) p(0.025)
winsor volat, gen(winsor_volat) p(0.005)
winsor salesgr, gen(winsor_salesgr) p(0.005)
winsor epsgr, gen(winsor_epsgr) p(0.005)


destring log_scope2, replace force


*log emissions

eststo clear




bys date: asreg ret log_scope1 logsize winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe logppe beta winsor_volat winsor_salesgr winsor_epsgr, 
drop _Nobs _R2 _adjR2 _b_logsize _b_winsor_bm _b_winsor_leverage _b_winsor_mom _b_winsor_investa _b_winsor_roe _b_logppe _b_beta _b_winsor_volat _b_winsor_salesgr _b_winsor_epsgr _b_cons

bys date: asreg ret log_scope2 logsize winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe logppe beta winsor_volat winsor_salesgr winsor_epsgr, 
drop _Nobs _R2 _adjR2 _b_logsize _b_winsor_bm _b_winsor_leverage _b_winsor_mom _b_winsor_investa _b_winsor_roe _b_logppe _b_beta _b_winsor_volat _b_winsor_salesgr _b_winsor_epsgr _b_cons

bys date: asreg ret log_total_emissions logsize winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe logppe beta winsor_volat winsor_salesgr winsor_epsgr, 
drop _Nobs _R2 _adjR2 _b_logsize _b_winsor_bm _b_winsor_leverage _b_winsor_mom _b_winsor_investa _b_winsor_roe _b_logppe _b_beta _b_winsor_volat _b_winsor_salesgr _b_winsor_epsgr _b_cons

bys date: asreg ret log_energy_consumption logsize winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe logppe beta winsor_volat winsor_salesgr winsor_epsgr, 
drop _Nobs _R2 _adjR2 _b_logsize _b_winsor_bm _b_winsor_leverage _b_winsor_mom _b_winsor_investa _b_winsor_roe _b_logppe _b_beta _b_winsor_volat _b_winsor_salesgr _b_winsor_epsgr _b_cons



bys date: asreg ret change_scope1 logsize winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe logppe beta winsor_volat winsor_salesgr winsor_epsgr, 
drop _Nobs _R2 _adjR2 _b_logsize _b_winsor_bm _b_winsor_leverage _b_winsor_mom _b_winsor_investa _b_winsor_roe _b_logppe _b_beta _b_winsor_volat _b_winsor_salesgr _b_winsor_epsgr _b_cons


bys date: asreg ret change_scope2 logsize winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe logppe beta winsor_volat winsor_salesgr winsor_epsgr, 
drop _Nobs _R2 _adjR2 _b_logsize _b_winsor_bm _b_winsor_leverage _b_winsor_mom _b_winsor_investa _b_winsor_roe _b_logppe _b_beta _b_winsor_volat _b_winsor_salesgr _b_winsor_epsgr _b_cons


bys date: asreg ret change_total_emissions logsize winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe logppe beta winsor_volat winsor_salesgr winsor_epsgr, 
drop _Nobs _R2 _adjR2 _b_logsize _b_winsor_bm _b_winsor_leverage _b_winsor_mom _b_winsor_investa _b_winsor_roe _b_logppe _b_beta _b_winsor_volat _b_winsor_salesgr _b_winsor_epsgr _b_cons


bys date: asreg ret change_energy_consumption logsize winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe logppe beta winsor_volat winsor_salesgr winsor_epsgr
drop _Nobs _R2 _adjR2 _b_logsize _b_winsor_bm _b_winsor_leverage _b_winsor_mom _b_winsor_investa _b_winsor_roe _b_logppe _b_beta _b_winsor_volat _b_winsor_salesgr _b_winsor_epsgr _b_cons








bys date: asreg ret scope1_int logsize winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe logppe beta winsor_volat winsor_salesgr winsor_epsgr, 
drop _Nobs _R2 _adjR2 _b_logsize _b_winsor_bm _b_winsor_leverage _b_winsor_mom _b_winsor_investa _b_winsor_roe _b_logppe _b_beta _b_winsor_volat _b_winsor_salesgr _b_winsor_epsgr _b_cons

bys date: asreg ret scope2_int logsize winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe logppe beta winsor_volat winsor_salesgr winsor_epsgr, 
drop _Nobs _R2 _adjR2 _b_logsize _b_winsor_bm _b_winsor_leverage _b_winsor_mom _b_winsor_investa _b_winsor_roe _b_logppe _b_beta _b_winsor_volat _b_winsor_salesgr _b_winsor_epsgr _b_cons

bys date: asreg ret total_emissions_int logsize winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe logppe beta winsor_volat winsor_salesgr winsor_epsgr, 
drop _Nobs _R2 _adjR2 _b_logsize _b_winsor_bm _b_winsor_leverage _b_winsor_mom _b_winsor_investa _b_winsor_roe _b_logppe _b_beta _b_winsor_volat _b_winsor_salesgr _b_winsor_epsgr _b_cons

bys date: asreg ret energy_consumption_int logsize winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe logppe beta winsor_volat winsor_salesgr winsor_epsgr, 
drop _Nobs _R2 _adjR2 _b_logsize _b_winsor_bm _b_winsor_leverage _b_winsor_mom _b_winsor_investa _b_winsor_roe _b_logppe _b_beta _b_winsor_volat _b_winsor_salesgr _b_winsor_epsgr _b_cons


cd "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\output"

export delimited csr_carbon_premium.csv, replace



cd "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\notebooks and stata do files"


save "5. Carbon Premium and Risk Factors (Constuct Carbon Premium).do", replace