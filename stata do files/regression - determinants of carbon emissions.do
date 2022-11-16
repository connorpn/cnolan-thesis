clear

cd "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\regression output"

import delimited "https://raw.githubusercontent.com/connorpn/cnolan-thesis/main/output/emissions_determinants_vars.csv"


label variable ticker "ticker"
sort ticker
encode ticker, gen(ticker_encode)

ssc install numdate
numdate yearly date = year, p(Y)

ssc install winsor
winsor bm, gen(winsor_bm) p(0.025)
winsor roe, gen(winsor_roe) p(0.025)
winsor leverage, gen(winsor_leverage) p(0.025)
winsor investa, gen(winsor_investa) p(0.025)
winsor salesgr, gen(winsor_salesgr) p(0.005)
winsor epsgr, gen(winsor_epsgr) p(0.005)


ssc install ftools
ssc install reghdfe
ssc install estout

destring log_scope2, replace force

eststo clear

eststo: reghdfe log_scope1 logsize winsor_bm winsor_roe winsor_leverage winsor_investa logppe winsor_salesgr winsor_epsgr, absorb(date industry) vce(cluster ticker_encode date)
estadd local year_fe "yes" , replace
estadd local industry_fe "yes" , replace


eststo: reghdfe log_scope2 logsize winsor_bm winsor_roe winsor_leverage winsor_investa logppe winsor_salesgr winsor_epsgr, absorb(date industry) vce(cluster ticker_encode date)
estadd local year_fe "yes" , replace
estadd local industry_fe "yes" , replace

eststo: reghdfe log_total_emissions logsize winsor_bm winsor_roe winsor_leverage winsor_investa logppe winsor_salesgr winsor_epsgr, absorb(date industry) vce(cluster ticker_encode date)
estadd local year_fe "yes" , replace
estadd local industry_fe "yes" , replace

eststo: reghdfe log_energy_consumption logsize winsor_bm winsor_roe winsor_leverage winsor_investa logppe winsor_salesgr winsor_epsgr, absorb(date industry) vce(cluster ticker_encode date)
estadd local year_fe "yes" , replace
estadd local industry_fe "yes" , replace

eststo: reghdfe change_scope1 logsize winsor_bm winsor_roe winsor_leverage winsor_investa logppe winsor_salesgr winsor_epsgr, absorb(date industry) vce(cluster ticker_encode date)
estadd local year_fe "yes" , replace
estadd local industry_fe "yes" , replace

eststo: reghdfe change_scope2 logsize winsor_bm winsor_roe winsor_leverage winsor_investa logppe winsor_salesgr winsor_epsgr, absorb(date industry) vce(cluster ticker_encode date)
estadd local year_fe "yes" , replace
estadd local industry_fe "yes" , replace

eststo: reghdfe change_total_emissions logsize winsor_bm winsor_roe winsor_leverage winsor_investa logppe winsor_salesgr winsor_epsgr, absorb(date industry) vce(cluster ticker_encode date)
estadd local year_fe "yes" , replace
estadd local industry_fe "yes" , replace

eststo: reghdfe change_energy_consumption logsize winsor_bm winsor_roe winsor_leverage winsor_investa logppe winsor_salesgr winsor_epsgr, absorb(date industry) vce(cluster ticker_encode date)
estadd local year_fe "yes" , replace
estadd local industry_fe "yes" , replace

eststo: reghdfe scope1_int logsize winsor_bm winsor_roe winsor_leverage winsor_investa logppe winsor_salesgr winsor_epsgr, absorb(date industry) vce(cluster ticker_encode date)
estadd local year_fe "yes" , replace
estadd local industry_fe "yes" , replace

reghdfe scope2_int logsize winsor_bm winsor_roe winsor_leverage winsor_investa logppe winsor_salesgr winsor_epsgr, absorb(date industry) vce(cluster ticker_encode date)
estadd local year_fe "yes" , replace
estadd local industry_fe "yes" , replace

eststo: reghdfe total_emissions_int logsize winsor_bm winsor_roe winsor_leverage winsor_investa logppe winsor_salesgr winsor_epsgr, absorb(date industry) vce(cluster ticker_encode date)
estadd local year_fe "yes" , replace
estadd local industry_fe "yes" , replace

eststo: reghdfe energy_consumption_int logsize winsor_bm winsor_roe winsor_leverage winsor_investa logppe winsor_salesgr winsor_epsgr, absorb(date industry) vce(cluster ticker_encode date)
estadd local year_fe "yes" , replace
estadd local industry_fe "yes" , replace


cd "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\regression output"

esttab using "regression output - determinants of carbon emissions.csv", r2 ar2 star(* 0.1 ** 0.05 *** 0.01) replace





cd "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\stata do files"

save "regression - determinants of carbon emissions.do", replace