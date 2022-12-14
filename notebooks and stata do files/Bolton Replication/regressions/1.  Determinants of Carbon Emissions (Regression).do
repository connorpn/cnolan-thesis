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

*import data
import delimited "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\regression\regression variables\br_determinants_of_carbon_emissions.csv"


*encode ticker
label variable ticker "ticker"
sort ticker
encode ticker, gen(ticker_encode)

*datetime 
numdate yearly date = year, p(Y)

*destring

destring log_scope2, replace force
destring change_scope2, replace force

*winsorize

winsor change_scope1, gen(winsor_change_scope1) p(0.025)
winsor change_scope2, gen(winsor_change_scope2) p(0.025)
winsor change_total_emissions, gen(winsor_change_total_emissions) p(0.025)
winsor change_energy_consumption, gen(winsor_change_energy_consumption) p(0.025)

drop change_scope1 change_scope2 change_total_emissions change_energy_consumption
rename winsor_change_scope1 change_scope1
rename winsor_change_scope2 change_scope2
rename winsor_change_total_emissions change_total_emissions
rename winsor_change_energy_consumption change_energy_consumption

winsor scope1_int, gen(winsor_scope1_int) p(0.025)
winsor scope2_int, gen(winsor_scope2_int) p(0.025)
winsor total_emissions_int, gen(winsor_total_emissions_int) p(0.025)
winsor energy_consumption_int, gen(winsor_energy_consumption_int) p(0.025)

drop scope1_int scope2_int total_emissions_int energy_consumption_int
rename winsor_scope1_int scope1_int
rename winsor_scope2_int scope2_int
rename winsor_total_emissions_int total_emissions_int
rename winsor_energy_consumption_int energy_consumption_int

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
	log_scope1 "LN S1"
	log_scope2 "LN S2"
	log_total_emissions "LN TOT"
	log_energy_consumption "LN ENG"
	change_scope1 "\$\Delta\$ S1"
	change_scope2 "\$\Delta\$ S2"
	change_total_emissions "\$\Delta\$ TOT"
	change_energy_consumption "\$\Delta\$ ENG"
	scope1_int "S1 INT"
	scope2_int "S2 INT"
	total_emissions_int "TOT INT"
	energy_consumption_int "ENG INT"
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
	title(Determinants of Carbon Emissions)
	mtitles("LN S1" "LN S2" "LN TOT" "LN ENG" "\$\Delta\$ S1" "\$\Delta\$ S2" "\$\Delta\$ TOT" "\$\Delta\$ ENG" "S1 INT" "S2 INT" "TOT INT" "ENG INT"
	)
	replace;
#delimit cr

*nomtitles
