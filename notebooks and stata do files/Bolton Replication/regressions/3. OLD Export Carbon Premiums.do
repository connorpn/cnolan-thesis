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

export delimited using "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\regression\regression variables\br_carbon_emissions_and_stock_returns_winsor.csv", replace



*	WITHOUT INDUSTRY FE



*log emissions no ind

clear
import delimited using "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\regression\regression variables\br_carbon_emissions_and_stock_returns_winsor.csv"
reghdfe ret log_scope1 logsize winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe logppe beta winsor_volat winsor_salesgr winsor_epsgr, absorb(date) vce(cluster ticker_encode year)
regsave, tstat pval ci
export delimited using "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\regression\regression outputs\bolton replications\carbon premiums\cp_log_scope1_noind.csv", replace

clear
import delimited using "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\regression\regression variables\br_carbon_emissions_and_stock_returns_winsor.csv"
reghdfe ret log_scope2 logsize winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe logppe beta winsor_volat winsor_salesgr winsor_epsgr, absorb(date) vce(cluster ticker_encode year)
regsave, tstat pval ci
export delimited using "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\regression\regression outputs\bolton replications\carbon premiums\cp_log_scope2_noind.csv", replace

clear
import delimited using "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\regression\regression variables\br_carbon_emissions_and_stock_returns_winsor.csv"
reghdfe ret log_total_emissions logsize winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe logppe beta winsor_volat winsor_salesgr winsor_epsgr, absorb(date) vce(cluster ticker_encode year)
regsave, tstat pval ci
export delimited using "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\regression\regression outputs\bolton replications\carbon premiums\cp_log_total_emissions_noind.csv", replace

clear
import delimited using "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\regression\regression variables\br_carbon_emissions_and_stock_returns_winsor.csv"
reghdfe ret log_energy_consumption logsize winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe logppe beta winsor_volat winsor_salesgr winsor_epsgr, absorb(date) vce(cluster ticker_encode year)
regsave, tstat pval ci
export delimited using "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\regression\regression outputs\bolton replications\carbon premiums\cp_log_energy_consumption_noind.csv", replace


*change emissions no ind

clear
import delimited using "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\regression\regression variables\br_carbon_emissions_and_stock_returns_winsor.csv"
reghdfe ret change_scope1 logsize winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe logppe beta winsor_volat winsor_salesgr winsor_epsgr, absorb(date) vce(cluster ticker_encode year)
regsave, tstat pval ci
export delimited using "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\regression\regression outputs\bolton replications\carbon premiums\cp_change_scope1_noind.csv", replace

clear
import delimited using "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\regression\regression variables\br_carbon_emissions_and_stock_returns_winsor.csv"
reghdfe ret change_scope2 logsize winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe logppe beta winsor_volat winsor_salesgr winsor_epsgr, absorb(date) vce(cluster ticker_encode year)
regsave, tstat pval ci
export delimited using "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\regression\regression outputs\bolton replications\carbon premiums\cp_change_scope2_noind.csv", replace

clear
import delimited using "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\regression\regression variables\br_carbon_emissions_and_stock_returns_winsor.csv"
reghdfe ret change_total_emissions logsize winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe logppe beta winsor_volat winsor_salesgr winsor_epsgr, absorb(date) vce(cluster ticker_encode year)
regsave, tstat pval ci
export delimited using "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\regression\regression outputs\bolton replications\carbon premiums\cp_change_total_emissions_noind.csv", replace

clear
import delimited using "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\regression\regression variables\br_carbon_emissions_and_stock_returns_winsor.csv"
reghdfe ret change_energy_consumption logsize winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe logppe beta winsor_volat winsor_salesgr winsor_epsgr, absorb(date) vce(cluster ticker_encode year)
regsave, tstat pval ci
export delimited using "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\regression\regression outputs\bolton replications\carbon premiums\cp_change_energy_consumption_noind.csv", replace


*int emissions no ind

clear
import delimited using "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\regression\regression variables\br_carbon_emissions_and_stock_returns_winsor.csv"
reghdfe ret scope1_int logsize winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe logppe beta winsor_volat winsor_salesgr winsor_epsgr, absorb(date) vce(cluster ticker_encode year)
regsave, tstat pval ci
export delimited using "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\regression\regression outputs\bolton replications\carbon premiums\cp_scope1_int_noind.csv", replace

clear
import delimited using "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\regression\regression variables\br_carbon_emissions_and_stock_returns_winsor.csv"
reghdfe ret scope2_int logsize winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe logppe beta winsor_volat winsor_salesgr winsor_epsgr, absorb(date) vce(cluster ticker_encode year)
regsave, tstat pval ci
export delimited using "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\regression\regression outputs\bolton replications\carbon premiums\cp_scope2_int_noind.csv", replace

clear
import delimited using "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\regression\regression variables\br_carbon_emissions_and_stock_returns_winsor.csv"
reghdfe ret total_emissions_int logsize winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe logppe beta winsor_volat winsor_salesgr winsor_epsgr, absorb(date) vce(cluster ticker_encode year)
regsave, tstat pval ci
export delimited using "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\regression\regression outputs\bolton replications\carbon premiums\cp_total_emissions_int_noind.csv", replace

clear
import delimited using "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\regression\regression variables\br_carbon_emissions_and_stock_returns_winsor.csv"
reghdfe ret energy_consumption_int logsize winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe logppe beta winsor_volat winsor_salesgr winsor_epsgr, absorb(date) vce(cluster ticker_encode year)
regsave, tstat pval ci
export delimited using "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\regression\regression outputs\bolton replications\carbon premiums\cp_energy_consumption_int_noind.csv", replace


*	WITH INDUSTRY FE


*log emissions with ind

clear
import delimited using "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\regression\regression variables\br_carbon_emissions_and_stock_returns_winsor.csv"
reghdfe ret log_scope1 logsize winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe logppe beta winsor_volat winsor_salesgr winsor_epsgr, absorb(date industry) vce(cluster ticker_encode year)
regsave, tstat pval ci
export delimited using "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\regression\regression outputs\bolton replications\carbon premiums\cp_log_scope1_ind.csv", replace

clear
import delimited using "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\regression\regression variables\br_carbon_emissions_and_stock_returns_winsor.csv"
reghdfe ret log_scope2 logsize winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe logppe beta winsor_volat winsor_salesgr winsor_epsgr, absorb(date industry) vce(cluster ticker_encode year)
regsave, tstat pval ci
export delimited using "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\regression\regression outputs\bolton replications\carbon premiums\cp_log_scope2_ind.csv", replace

clear
import delimited using "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\regression\regression variables\br_carbon_emissions_and_stock_returns_winsor.csv"
reghdfe ret log_total_emissions logsize winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe logppe beta winsor_volat winsor_salesgr winsor_epsgr, absorb(date industry) vce(cluster ticker_encode year)
regsave, tstat pval ci
export delimited using "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\regression\regression outputs\bolton replications\carbon premiums\cp_log_total_emissions_ind.csv", replace

clear
import delimited using "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\regression\regression variables\br_carbon_emissions_and_stock_returns_winsor.csv"
reghdfe ret log_energy_consumption logsize winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe logppe beta winsor_volat winsor_salesgr winsor_epsgr, absorb(date industry) vce(cluster ticker_encode year)
regsave, tstat pval ci
export delimited using "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\regression\regression outputs\bolton replications\carbon premiums\cp_log_energy_consumption_ind.csv", replace


*change emissions with ind

clear
import delimited using "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\regression\regression variables\br_carbon_emissions_and_stock_returns_winsor.csv"
reghdfe ret change_scope1 logsize winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe logppe beta winsor_volat winsor_salesgr winsor_epsgr, absorb(date industry) vce(cluster ticker_encode year)
regsave, tstat pval ci
export delimited using "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\regression\regression outputs\bolton replications\carbon premiums\cp_change_scope1_ind.csv", replace

clear
import delimited using "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\regression\regression variables\br_carbon_emissions_and_stock_returns_winsor.csv"
reghdfe ret change_scope2 logsize winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe logppe beta winsor_volat winsor_salesgr winsor_epsgr, absorb(date industry) vce(cluster ticker_encode year)
regsave, tstat pval ci
export delimited using "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\regression\regression outputs\bolton replications\carbon premiums\cp_change_scope2_ind.csv", replace

clear
import delimited using "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\regression\regression variables\br_carbon_emissions_and_stock_returns_winsor.csv"
reghdfe ret change_total_emissions logsize winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe logppe beta winsor_volat winsor_salesgr winsor_epsgr, absorb(date industry) vce(cluster ticker_encode year)
regsave, tstat pval ci
export delimited using "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\regression\regression outputs\bolton replications\carbon premiums\cp_change_total_emissions_ind.csv", replace

clear
import delimited using "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\regression\regression variables\br_carbon_emissions_and_stock_returns_winsor.csv"
reghdfe ret change_energy_consumption logsize winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe logppe beta winsor_volat winsor_salesgr winsor_epsgr, absorb(date industry) vce(cluster ticker_encode year)
regsave, tstat pval ci
export delimited using "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\regression\regression outputs\bolton replications\carbon premiums\cp_change_energy_consumption_ind.csv", replace


*int emissions with ind

clear
import delimited using "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\regression\regression variables\br_carbon_emissions_and_stock_returns_winsor.csv"
reghdfe ret scope1_int logsize winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe logppe beta winsor_volat winsor_salesgr winsor_epsgr, absorb(date industry) vce(cluster ticker_encode year)
regsave, tstat pval ci
export delimited using "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\regression\regression outputs\bolton replications\carbon premiums\cp_scope1_int_ind.csv", replace

clear
import delimited using "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\regression\regression variables\br_carbon_emissions_and_stock_returns_winsor.csv"
reghdfe ret scope2_int logsize winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe logppe beta winsor_volat winsor_salesgr winsor_epsgr, absorb(date industry) vce(cluster ticker_encode year)
regsave, tstat pval ci
export delimited using "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\regression\regression outputs\bolton replications\carbon premiums\cp_scope2_int_ind.csv", replace

clear
import delimited using "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\regression\regression variables\br_carbon_emissions_and_stock_returns_winsor.csv"
reghdfe ret total_emissions_int logsize winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe logppe beta winsor_volat winsor_salesgr winsor_epsgr, absorb(date industry) vce(cluster ticker_encode year)
regsave, tstat pval ci
export delimited using "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\regression\regression outputs\bolton replications\carbon premiums\cp_total_emissions_int_ind.csv", replace

clear
import delimited using "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\regression\regression variables\br_carbon_emissions_and_stock_returns_winsor.csv"
reghdfe ret energy_consumption_int logsize winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe logppe beta winsor_volat winsor_salesgr winsor_epsgr, absorb(date industry) vce(cluster ticker_encode year)
regsave, tstat pval ci
export delimited using "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\regression\regression outputs\bolton replications\carbon premiums\cp_energy_consumption_int_ind.csv", replace
