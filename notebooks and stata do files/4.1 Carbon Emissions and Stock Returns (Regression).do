clear

cd "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\regression output"

import delimited "https://raw.githubusercontent.com/connorpn/cnolan-thesis/main/output/carbon_emissions_stock_returns_vars.csv"


label variable ticker "ticker"
sort ticker
encode ticker, gen(ticker_encode)

ssc install numdate
numdate monthly date = yearmonth, p(YM)

ssc install winsor
winsor bm, gen(winsor_bm) p(0.025)
winsor leverage, gen(winsor_leverage) p(0.025)
winsor mom, gen(winsor_mom) p(0.005)
winsor investa, gen(winsor_investa) p(0.025)
winsor roe, gen(winsor_roe) p(0.025)
winsor volat, gen(winsor_volat) p(0.005)
winsor salesgr, gen(winsor_salesgr) p(0.005)
winsor epsgr, gen(winsor_epsgr) p(0.005)

ssc install ftools
ssc install reghdfe
ssc install estout

destring log_scope2, replace force

eststo clear

eststo: reghdfe ret log_scope1 logsize winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe logppe winsor_volat winsor_salesgr winsor_epsgr, absorb(date industry) vce(cluster ticker_encode year)
predict coeff_log_scope1_y, xb
sort date
by date: egen _b_log_scope1_y = mean(coeff_log_scope1_y)
estadd local year_month_fe "yes" , replace
estadd local industry_fe "yes" , replace

eststo: reghdfe ret log_scope2 logsize winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe logppe winsor_volat winsor_salesgr winsor_epsgr, absorb(date industry) vce(cluster ticker_encode year)
predict coeff_log_scope2_y, xb
sort date
by date: egen _b_log_scope2_y = mean(coeff_log_scope2_y)
estadd local year_month_fe "yes" , replace
estadd local industry_fe "yes" , replace

eststo: reghdfe ret log_total_emissions logsize winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe logppe winsor_volat winsor_salesgr winsor_epsgr, absorb(date industry) vce(cluster ticker_encode year)
predict coeff_log_total_emissions_y, xb
sort date
by date: egen _b_log_total_emissions_y = mean(coeff_log_total_emissions_y)
estadd local year_month_fe "yes" , replace
estadd local industry_fe "yes" , replace

eststo: reghdfe ret log_energy_consumption logsize winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe logppe winsor_volat winsor_salesgr winsor_epsgr, absorb(date industry) vce(cluster ticker_encode year)
predict coeff_log_energy_y, xb
sort date
by date: egen _b_log_energy_y = mean(coeff_log_energy_y)
estadd local year_month_fe "yes" , replace
estadd local industry_fe "yes" , replace


eststo: reghdfe ret log_scope1 logsize winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe logppe winsor_volat winsor_salesgr winsor_epsgr, absorb(date) vce(cluster ticker_encode year)
predict coeff_log_scope1_n, xb
sort date
by date: egen _b_log_scope1_n = mean(coeff_log_scope1_n)
estadd local year_fe "yes" , replace
estadd local industry_fe "no" , replace

eststo: reghdfe ret log_scope2 logsize winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe logppe winsor_volat winsor_salesgr winsor_epsgr, absorb(date) vce(cluster ticker_encode year)
predict coeff_log_scope2_n, xb
sort date
by date: egen _b_log_scope2_n = mean(coeff_log_scope2_n)
estadd local year_fe "yes" , replace
estadd local industry_fe "no" , replace

eststo: reghdfe ret log_total_emissions logsize winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe logppe winsor_volat winsor_salesgr winsor_epsgr, absorb(date) vce(cluster ticker_encode year)
predict coeff_log_total_emissions_n, xb
sort date
by date: egen _b_log_total_emissions_n = mean(coeff_log_total_emissions_n)
estadd local year_fe "yes" , replace
estadd local industry_fe "no" , replace

eststo: reghdfe ret log_energy_consumption logsize winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe logppe winsor_volat winsor_salesgr winsor_epsgr, absorb(date) vce(cluster ticker_encode year)
predict coeff_log_energy_n, xb
sort date
by date: egen _b_log_energy_n = mean(coeff_log_energy_n)
estadd local year_fe "yes" , replace
estadd local industry_fe "no" , replace

cd "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\regression output"

esttab using "regression output - carbon emissions and stock returns (log emissions).csv", r2 ar2 star(* 0.1 ** 0.05 *** 0.01) replace


eststo clear

eststo: reghdfe ret change_scope1 logsize winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe logppe winsor_volat winsor_salesgr winsor_epsgr, absorb(date industry) vce(cluster ticker_encode year)
predict coeff_change_scope1_y, xb
sort date
by date: egen _b_change_scope1_y = mean(coeff_change_scope1_y)
estadd local year_month_fe "yes" , replace
estadd local industry_fe "yes" , replace

eststo: reghdfe ret change_scope2 logsize winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe logppe winsor_volat winsor_salesgr winsor_epsgr, absorb(date industry) vce(cluster ticker_encode year)
predict coeff_change_scope2_y, xb
sort date
by date: egen _b_change_scope2_y = mean(coeff_change_scope2_y)
estadd local year_month_fe "yes" , replace
estadd local industry_fe "yes" , replace

eststo: reghdfe ret change_total_emissions logsize winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe logppe winsor_volat winsor_salesgr winsor_epsgr, absorb(date industry) vce(cluster ticker_encode year)
predict coeff_change_total_emissions_y, xb
sort date
by date: egen _b_change_total_emissions_y = mean(coeff_change_total_emissions_y)
estadd local year_month_fe "yes" , replace
estadd local industry_fe "yes" , replace

eststo: reghdfe ret change_energy_consumption logsize winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe logppe winsor_volat winsor_salesgr winsor_epsgr, absorb(date industry) vce(cluster ticker_encode year)
predict coeff_change_energy_y, xb
sort date
by date: egen _b_change_energy_y = mean(coeff_change_energy_y)
estadd local year_month_fe "yes" , replace
estadd local industry_fe "yes" , replace


eststo: reghdfe ret change_scope1 logsize winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe logppe winsor_volat winsor_salesgr winsor_epsgr, absorb(date) vce(cluster ticker_encode year)
predict coeff_change_scope1_n, xb
sort date
by date: egen _b_change_scope1_n = mean(coeff_change_scope1_n)
estadd local year_fe "yes" , replace
estadd local industry_fe "no" , replace

eststo: reghdfe ret change_scope2 logsize winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe logppe winsor_volat winsor_salesgr winsor_epsgr, absorb(date) vce(cluster ticker_encode year)
predict coeff_change_scope2_n, xb
sort date
by date: egen _b_change_scope2_n = mean(coeff_change_scope2_n)
estadd local year_fe "yes" , replace
estadd local industry_fe "no" , replace

eststo: reghdfe ret change_total_emissions logsize winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe logppe winsor_volat winsor_salesgr winsor_epsgr, absorb(date) vce(cluster ticker_encode year)
predict coeff_change_total_emissions_n, xb
sort date
by date: egen _b_change_total_emissions_n = mean(coeff_change_total_emissions_n)
estadd local year_fe "yes" , replace
estadd local industry_fe "no" , replace

eststo: reghdfe ret change_energy_consumption logsize winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe logppe winsor_volat winsor_salesgr winsor_epsgr, absorb(date) vce(cluster ticker_encode year)
predict coeff_change_energy_n, xb
sort date
by date: egen _b_change_energy_n = mean(coeff_change_energy_n)
estadd local year_fe "yes" , replace
estadd local industry_fe "no" , replace

cd "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\regression output"

esttab using "regression output - carbon emissions and stock returns (change emissions).csv", r2 ar2 star(* 0.1 ** 0.05 *** 0.01) replace


eststo clear

eststo: reghdfe ret scope1_int logsize winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe logppe winsor_volat winsor_salesgr winsor_epsgr, absorb(date industry) vce(cluster ticker_encode year)
predict coeff_scope1_int_y, xb
sort date
by date: egen _b_scope1_int_y = mean(coeff_scope1_int_y)
estadd local year_month_fe "yes" , replace
estadd local industry_fe "yes" , replace

eststo: reghdfe ret scope2_int logsize winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe logppe winsor_volat winsor_salesgr winsor_epsgr, absorb(date industry) vce(cluster ticker_encode year)
predict coeff_scope2_int_y, xb
sort date
by date: egen _b_scope2_int_y = mean(coeff_scope2_int_y)
estadd local year_month_fe "yes" , replace
estadd local industry_fe "yes" , replace

eststo: reghdfe ret total_emissions_int logsize winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe logppe winsor_volat winsor_salesgr winsor_epsgr, absorb(date industry) vce(cluster ticker_encode year)
predict coeff_total_emissions_int_y, xb
sort date
by date: egen _b_total_emissions_int_y = mean(coeff_total_emissions_int_y)
estadd local year_month_fe "yes" , replace
estadd local industry_fe "yes" , replace

eststo: reghdfe ret energy_consumption_int logsize winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe logppe winsor_volat winsor_salesgr winsor_epsgr, absorb(date industry) vce(cluster ticker_encode year)
predict coeff_energy_consumption_int_y, xb
sort date
by date: egen _b_energy_consumption_int_y = mean(coeff_energy_consumption_int_y)
estadd local year_month_fe "yes" , replace
estadd local industry_fe "yes" , replace


eststo: reghdfe ret scope1_int logsize winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe logppe winsor_volat winsor_salesgr winsor_epsgr, absorb(date) vce(cluster ticker_encode year)
predict coeff_scope1_int_n, xb
sort date
by date: egen _b_scope1_int_n = mean(coeff_scope1_int_n)
estadd local year_fe "yes" , replace
estadd local industry_fe "no" , replace

eststo: reghdfe ret scope2_int logsize winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe logppe winsor_volat winsor_salesgr winsor_epsgr, absorb(date) vce(cluster ticker_encode year)
predict coeff_scope2_int_n, xb
sort date
by date: egen _b_scope2_int_n = mean(coeff_scope2_int_n)
estadd local year_fe "yes" , replace
estadd local industry_fe "no" , replace

eststo: reghdfe ret total_emissions_int logsize winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe logppe winsor_volat winsor_salesgr winsor_epsgr, absorb(date) vce(cluster ticker_encode year)
predict coeff_total_emissions_int_n, xb
sort date
by date: egen _b_total_emissions_int_n = mean(coeff_total_emissions_int_n)
estadd local year_fe "yes" , replace
estadd local industry_fe "no" , replace

eststo: reghdfe ret energy_consumption_int logsize winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe logppe winsor_volat winsor_salesgr winsor_epsgr, absorb(date) vce(cluster ticker_encode year)
predict coeff_energy_consumption_int_n, xb
sort date
by date: egen _b_energy_consumption_int_n = mean(coeff_energy_consumption_int_n)
estadd local year_fe "yes" , replace
estadd local industry_fe "no" , replace

cd "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\regression output"

esttab using "regression output - carbon emissions and stock returns (int emissions).csv", r2 ar2 star(* 0.1 ** 0.05 *** 0.01) replace

eststo clear

cd "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\output"

export delimited using "csr_carbon_premium.csv", replace

cd "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\notebooks and stata do files"

save "4.1 Carbon Emissions and Stock Returns (Regression).do", replace