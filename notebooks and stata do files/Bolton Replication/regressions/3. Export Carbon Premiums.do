/*
ssc install winsor
ssc install numdate
ssc install asreg
*/

clear


cd "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\regression\regression outputs\bolton replications\carbon premiums"

import delimited "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\regression\regression variables\br_carbon_emissions_and_stock_returns.csv"


label variable ticker "ticker"
sort ticker 	
encode ticker, gen(ticker_encode)


numdate monthly date = yearmonth, p(YM)

winsor bm, gen(winsor_bm) p(0.025)
winsor leverage, gen(winsor_leverage) p(0.025)
winsor mom, gen(winsor_mom) p(0.005)
winsor investa, gen(winsor_investa) p(0.025)
winsor roe, gen(winsor_roe) p(0.025)
winsor volat, gen(winsor_volat) p(0.005)
winsor salesgr, gen(winsor_salesgr) p(0.005)
winsor epsgr, gen(winsor_epsgr) p(0.005)


destring log_scope2, replace force



*	WITHOUT INDUSTRY FE

*log emissions

bys date: asreg ret log_scope1 logsize winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe logppe beta winsor_volat winsor_salesgr winsor_epsgr
drop  _Nobs _R2 _adjR2 _b_logsize _b_winsor_bm _b_winsor_leverage _b_winsor_mom _b_winsor_investa _b_winsor_roe _b_logppe _b_beta _b_winsor_volat _b_winsor_salesgr _b_winsor_epsgr _b_cons

bys date: asreg ret log_scope2 logsize winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe logppe beta winsor_volat winsor_salesgr winsor_epsgr
drop  _Nobs _R2 _adjR2 _b_logsize _b_winsor_bm _b_winsor_leverage _b_winsor_mom _b_winsor_investa _b_winsor_roe _b_logppe _b_beta _b_winsor_volat _b_winsor_salesgr _b_winsor_epsgr _b_cons

bys date: asreg ret log_total_emissions logsize winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe logppe beta winsor_volat winsor_salesgr winsor_epsgr
drop  _Nobs _R2 _adjR2 _b_logsize _b_winsor_bm _b_winsor_leverage _b_winsor_mom _b_winsor_investa _b_winsor_roe _b_logppe _b_beta _b_winsor_volat _b_winsor_salesgr _b_winsor_epsgr _b_cons

bys date: asreg ret log_energy_consumption logsize winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe logppe beta winsor_volat winsor_salesgr winsor_epsgr
drop  _Nobs _R2 _adjR2 _b_logsize _b_winsor_bm _b_winsor_leverage _b_winsor_mom _b_winsor_investa _b_winsor_roe _b_logppe _b_beta _b_winsor_volat _b_winsor_salesgr _b_winsor_epsgr _b_cons




*change emissions
bys date: asreg ret change_scope1 logsize winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe logppe beta winsor_volat winsor_salesgr winsor_epsgr
drop  _Nobs _R2 _adjR2 _b_logsize _b_winsor_bm _b_winsor_leverage _b_winsor_mom _b_winsor_investa _b_winsor_roe _b_logppe _b_beta _b_winsor_volat _b_winsor_salesgr _b_winsor_epsgr _b_cons

bys date: asreg ret change_scope2 logsize winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe logppe beta winsor_volat winsor_salesgr winsor_epsgr
drop  _Nobs _R2 _adjR2 _b_logsize _b_winsor_bm _b_winsor_leverage _b_winsor_mom _b_winsor_investa _b_winsor_roe _b_logppe _b_beta _b_winsor_volat _b_winsor_salesgr _b_winsor_epsgr _b_cons

bys date: asreg ret change_total_emissions logsize winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe logppe beta winsor_volat winsor_salesgr winsor_epsgr
drop  _Nobs _R2 _adjR2 _b_logsize _b_winsor_bm _b_winsor_leverage _b_winsor_mom _b_winsor_investa _b_winsor_roe _b_logppe _b_beta _b_winsor_volat _b_winsor_salesgr _b_winsor_epsgr _b_cons

bys date: asreg ret change_energy_consumption logsize winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe logppe beta winsor_volat winsor_salesgr winsor_epsgr
drop  _Nobs _R2 _adjR2 _b_logsize _b_winsor_bm _b_winsor_leverage _b_winsor_mom _b_winsor_investa _b_winsor_roe _b_logppe _b_beta _b_winsor_volat _b_winsor_salesgr _b_winsor_epsgr _b_cons



* emissions int
bys date: asreg ret scope1_int logsize winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe logppe beta winsor_volat winsor_salesgr winsor_epsgr
drop  _Nobs _R2 _adjR2 _b_logsize _b_winsor_bm _b_winsor_leverage _b_winsor_mom _b_winsor_investa _b_winsor_roe _b_logppe _b_beta _b_winsor_volat _b_winsor_salesgr _b_winsor_epsgr _b_cons

bys date: asreg ret scope2_int logsize winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe logppe beta winsor_volat winsor_salesgr winsor_epsgr
drop  _Nobs _R2 _adjR2 _b_logsize _b_winsor_bm _b_winsor_leverage _b_winsor_mom _b_winsor_investa _b_winsor_roe _b_logppe _b_beta _b_winsor_volat _b_winsor_salesgr _b_winsor_epsgr _b_cons

bys date: asreg ret total_emissions_int logsize winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe logppe beta winsor_volat winsor_salesgr winsor_epsgr
drop  _Nobs _R2 _adjR2 _b_logsize _b_winsor_bm _b_winsor_leverage _b_winsor_mom _b_winsor_investa _b_winsor_roe _b_logppe _b_beta _b_winsor_volat _b_winsor_salesgr _b_winsor_epsgr _b_cons

bys date: asreg ret energy_consumption_int logsize winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe logppe beta winsor_volat winsor_salesgr winsor_epsgr
drop  _Nobs _R2 _adjR2 _b_logsize _b_winsor_bm _b_winsor_leverage _b_winsor_mom _b_winsor_investa _b_winsor_roe _b_logppe _b_beta _b_winsor_volat _b_winsor_salesgr _b_winsor_epsgr _b_cons


drop ticker industry ret log_scope1 log_scope2 log_total_emissions log_energy_consumption change_scope1 change_scope2 change_total_emissions change_energy_consumption scope1_int scope2_int total_emissions_int energy_consumption_int logsize bm leverage mom investa roe logppe beta volat salesgr epsgr ticker_encode date winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe winsor_volat winsor_salesgr winsor_epsgr

export delimited "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\regression\regression outputs\bolton replications\br_carbon_premium_ts", replace
