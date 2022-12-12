/*
ssc install numdate
ssc install winsor
ssc install ftools
ssc install reghdfe
ssc install estout
ssc install erepost
*/

clear
eststo clear

cd "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\regression\regression variables"

import delimited "br_determinants_of_carbon_emissions.csv"

destring log_scope2, replace force
destring change_scope2, replace force

label variable ticker "ticker"
sort ticker
encode ticker, gen(ticker_encode)

numdate yearly date = year, p(Y)

winsor bm, gen(winsor_bm) p(0.025)
winsor roe, gen(winsor_roe) p(0.025)
winsor leverage, gen(winsor_leverage) p(0.025)
winsor investa, gen(winsor_investa) p(0.025)
winsor salesgr, gen(winsor_salesgr) p(0.005)
winsor epsgr, gen(winsor_epsgr) p(0.005)


*regressions

eststo log_scope1: reghdfe log_scope1 logsize winsor_bm winsor_roe winsor_leverage winsor_investa logppe winsor_salesgr winsor_epsgr, absorb(date industry) vce(cluster ticker_encode date)
estadd local year_fe "yes" , replace
estadd local industry_fe "yes" , replace


eststo log_scope2: reghdfe log_scope2 logsize winsor_bm winsor_roe winsor_leverage winsor_investa logppe winsor_salesgr winsor_epsgr, absorb(date industry) vce(cluster ticker_encode date)
estadd local year_fe "yes" , replace
estadd local industry_fe "yes" , replace

eststo log_total_emissions: reghdfe log_total_emissions logsize winsor_bm winsor_roe winsor_leverage winsor_investa logppe winsor_salesgr winsor_epsgr, absorb(date industry) vce(cluster ticker_encode date)
estadd local year_fe "yes" , replace
estadd local industry_fe "yes" , replace

eststo log_energy_consumption: reghdfe log_energy_consumption logsize winsor_bm winsor_roe winsor_leverage winsor_investa logppe winsor_salesgr winsor_epsgr, absorb(date industry) vce(cluster ticker_encode date)
estadd local year_fe "yes" , replace
estadd local industry_fe "yes" , replace

eststo change_scope1: reghdfe change_scope1 logsize winsor_bm winsor_roe winsor_leverage winsor_investa logppe winsor_salesgr winsor_epsgr, absorb(date industry) vce(cluster ticker_encode date)
estadd local year_fe "yes" , replace
estadd local industry_fe "yes" , replace

eststo change_scope2: reghdfe change_scope2 logsize winsor_bm winsor_roe winsor_leverage winsor_investa logppe winsor_salesgr winsor_epsgr, absorb(date industry) vce(cluster ticker_encode date)
estadd local year_fe "yes" , replace
estadd local industry_fe "yes" , replace

eststo change_total_emissions: reghdfe change_total_emissions logsize winsor_bm winsor_roe winsor_leverage winsor_investa logppe winsor_salesgr winsor_epsgr, absorb(date industry) vce(cluster ticker_encode date)
estadd local year_fe "yes" , replace
estadd local industry_fe "yes" , replace

eststo change_energy_consumption: reghdfe change_energy_consumption logsize winsor_bm winsor_roe winsor_leverage winsor_investa logppe winsor_salesgr winsor_epsgr, absorb(date industry) vce(cluster ticker_encode date)
estadd local year_fe "yes" , replace
estadd local industry_fe "yes" , replace

eststo scope1_int: reghdfe scope1_int logsize winsor_bm winsor_roe winsor_leverage winsor_investa logppe winsor_salesgr winsor_epsgr, absorb(date industry) vce(cluster ticker_encode date)
estadd local year_fe "yes" , replace
estadd local industry_fe "yes" , replace

eststo scope2_int: reghdfe scope2_int logsize winsor_bm winsor_roe winsor_leverage winsor_investa logppe winsor_salesgr winsor_epsgr, absorb(date industry) vce(cluster ticker_encode date)
estadd local year_fe "yes" , replace
estadd local industry_fe "yes" , replace

eststo total_emissions_int: reghdfe total_emissions_int logsize winsor_bm winsor_roe winsor_leverage winsor_investa logppe winsor_salesgr winsor_epsgr, absorb(date industry) vce(cluster ticker_encode date)
estadd local year_fe "yes" , replace
estadd local industry_fe "yes" , replace

eststo energy_consumption_int: reghdfe energy_consumption_int logsize winsor_bm winsor_roe winsor_leverage winsor_investa logppe winsor_salesgr winsor_epsgr, absorb(date industry) vce(cluster ticker_encode date)
estadd local year_fe "yes" , replace
estadd local industry_fe "yes" , replace



estfe, labels(date "Year/Month FE" industry "Industry FE")

cd "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\regression\regression outputs\bolton replications"



#delimit ;
esttab log_scope1 log_scope2 log_total_emissions log_energy_consumption change_scope1 change_scope2 change_total_emissions change_energy_consumption scope1_int scope2_int total_emissions_int energy_consumption_int
	using "br_determinants_of_carbon_emissions.tex", 
	varlabels(
	logsize LOGSIZE
	winsor_bm B/M
	winsor_roe ROE
	winsor_leverage LEVERAGE
	winsor_investa INVEST/A
	logppe LOGPPE
	winsor_salesgr SALESGR
	winsor_epsgr EPSGR
	)
	indicate(
	`r(indicate_fe)'
	)
	order(logsize winsor_bm winsor_roe winsor_leverage winsor_investa logppe winsor_salesgr winsor_epsgr _cons)
	label se star(* 0.10 ** 0.05 *** 0.01)
	s(year_fe industry_fe N r2_a,
	label("Year FE" "Industry FE" "Observations" "R2-Adj"))
	title(Determinants of Carbon Emissions: LOG EMISSIONS)
	nomtitles
	nodepvars
	replace;
#delimit cr

