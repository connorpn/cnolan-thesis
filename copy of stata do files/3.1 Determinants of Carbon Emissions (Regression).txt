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


import delimited "https://raw.githubusercontent.com/connorpn/cnolan-thesis/main/output/emissions_determinants_vars.csv"

destring log_scope2, replace force

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

cd "Y:\OneDrive\University Study\Honours Thesis\cnolan-thesis\regression output\3.1 Determinants of Carbon Emissions"

*erase "3.1 determinants of carbon emissions.tex"

#delimit ;
esttab log_scope1 log_scope2 log_total_emissions log_energy_consumption
	using "3.1 determinants of carbon emissions (log emissions).tex", 
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
	replace;
#delimit cr

#delimit ;
esttab change_scope1 change_scope2 change_total_emissions change_energy_consumption
	using "3.1 determinants of carbon emissions (change emissions).tex", 
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
	title(Determinants of Carbon Emissions: Yearly Change in Emissions)
	nomtitles
	replace;
#delimit cr

#delimit ;
esttab scope1_int scope2_int total_emissions_int energy_consumption_int
	using "3.1 determinants of carbon emissions (emissions int).tex", 
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
	order(logsize winsor_bm winsor_roe winsor_leverage winsor_investa logppe 	winsor_salesgr winsor_epsgr _cons)
	label se star(* 0.10 ** 0.05 *** 0.01)
	s(year_fe industry_fe N r2_a,
	label("Year FE" "Industry FE" "Observations" "R2-Adj"))
	title(Determinants of Carbon Emissions: Emission Intensity)
	nomtitles
	replace;
#delimit cr

*mlabels(,none) collabels(,none)

save "Y:\OneDrive\University Study\Honours Thesis\cnolan-thesis\notebooks and stata do files\3.1 Determinants of Carbon Emissions (Regression).do", replace