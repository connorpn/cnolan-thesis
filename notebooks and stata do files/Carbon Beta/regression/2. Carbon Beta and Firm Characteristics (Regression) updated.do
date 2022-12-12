/*
ssc install numdate
ssc install winsor
ssc install ftools
ssc install reghdfe
ssc install estout
ssc install erepost
*destring log_scope2, replace force
*/


clear
eststo clear

import delimited "Z:/OneDrive/University Study/Honours Thesis/cnolan-thesis/regression/regression variables/carbon_beta_firm_characteristics_vars.csv"


label variable ticker "ticker"
sort ticker
encode ticker, gen(ticker_encode)

numdate monthly date = yearmonth, p(YM)

destring log_scope2, replace force

winsor bm, gen(winsor_bm) p(0.025)
winsor leverage, gen(winsor_leverage) p(0.025)
winsor mom, gen(winsor_mom) p(0.005)
winsor investa, gen(winsor_investa) p(0.025)
winsor roe, gen(winsor_roe) p(0.025)
winsor volat, gen(winsor_volat) p(0.005)
winsor salesgr, gen(winsor_salesgr) p(0.005)
winsor epsgr, gen(winsor_epsgr) p(0.005)


drop bm leverage mom investa roe volat salesgr epsgr
rename winsor_bm bm
rename winsor_leverage leverage
rename winsor_mom mom
rename winsor_investa investa
rename winsor_roe roe
rename winsor_volat volat
rename winsor_salesgr salesgr
rename winsor_epsgr epsgr

* Run and store regressions





*	log_emissions


eststo cb_variables: ///
reghdfe carbon_beta  logsize bm leverage mom investa roe logppe beta volat salesgr epsgr,absorb(date) ///
vce(cluster ticker_encode)
estadd local date_fe "yes" , replace
estadd local industry_fe "no" , replace

eststo log_scope1: ///
reghdfe carbon_beta  logsize bm leverage mom investa roe logppe beta volat salesgr epsgr log_scope1, absorb(date) ///
vce(cluster ticker_encode)
estadd local date_fe "yes" , replace
estadd local industry_fe "no" , replace

eststo log_scope2: ///
reghdfe carbon_beta  logsize bm leverage mom investa roe logppe beta volat salesgr epsgr log_scope2, absorb(date) ///
vce(cluster ticker_encode)
estadd local date_fe "yes" , replace
estadd local industry_fe "no" , replace

eststo log_total_emissions: ///
reghdfe carbon_beta  logsize bm leverage mom investa roe logppe beta volat salesgr epsgr log_total_emissions, absorb(date) ///
vce(cluster ticker_encode)
estadd local date_fe "yes" , replace
estadd local industry_fe "no" , replace

eststo log_energy_consumption: ///
reghdfe carbon_beta  logsize bm leverage mom investa roe logppe beta volat salesgr epsgr log_energy_consumption, absorb(date) ///
vce(cluster ticker_encode)
estadd local date_fe "yes" , replace
estadd local industry_fe "no" , replace

eststo cb_variables_ind: ///
reghdfe carbon_beta  logsize bm leverage mom investa roe logppe beta volat salesgr epsgr, ///
absorb(date industry) ///
vce(cluster ticker_encode)
estadd local date_fe "yes" , replace
estadd local industry_fe "yes" , replace

eststo log_scope1_ind: /// 
reghdfe carbon_beta  logsize bm leverage mom investa roe logppe beta volat salesgr epsgr log_scope1, absorb(date industry) ///
vce(cluster ticker_encode)
estadd local date_fe "yes" , replace
estadd local industry_fe "yes" , replace

eststo log_scope2_ind: /// 
reghdfe carbon_beta  logsize bm leverage mom investa roe logppe beta volat salesgr epsgr log_scope2, absorb(date industry) ///
vce(cluster ticker_encode)
estadd local date_fe "yes" , replace
estadd local industry_fe "yes" , replace

eststo log_total_emissions_ind: /// 
reghdfe carbon_beta  logsize bm leverage mom investa roe logppe beta volat salesgr epsgr log_total_emissions, absorb(date industry) ///
vce(cluster ticker_encode)
estadd local date_fe "yes" , replace
estadd local industry_fe "yes" , replace

eststo log_energy_consumption_ind: /// 
reghdfe carbon_beta  logsize bm leverage mom investa roe logppe beta volat salesgr epsgr log_energy_consumption, absorb(date industry) ///
vce(cluster ticker_encode)
estadd local date_fe "yes" , replace
estadd local industry_fe "yes" , replace


estfe, labels(date "Year/Month FE" industry "Industry FE")
*estadd scalar r2_adjusted = e(r2_a)

cd "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\regression\regression outputs\carbon beta"

#delimit ;
esttab cb_variables log_scope1 log_scope2 log_total_emissions log_energy_consumption cb_variables_ind log_scope1_ind log_scope2_ind log_total_emissions_ind log_energy_consumption_ind using "cb_firm_characteristics.tex", 
	indicate(`r(indicate_fe)')
	label se star(* 0.10 ** 0.05 *** 0.01)
	s(date_fe industry_fe N r2_a,
	label("Year/Month FE" "Industry FE" "Observations" "R2-Adj"))
	rename(log_scope1 "LN S1" log_scope2 "LN S2" log_total_emissions "LN TOT" log_energy_consumption "LN ENG")
	varlabels(
	log_scope1 "LN SCOPE1"
	log_scope2 "LN SCOPE2"
	log_total_emissions "LN TOTAL"
	log_energy_consumption "LN ENERGY"
	logsize LOGSIZE
	bm B/M
	leverage LEVERAGE
	mom MOM
	investa INVEST/A
	roe ROE
	logppe LOGPPE
	beta BETA
	volat VOLAT
	salesgr SALESGR
	epsgr EPSGR
	)
	title(Carbon Beta and Firm Characteristics: Level of Emissions)
	nomtitles
	nodepvars
	compress
	nogaps
	replace;
#delimit cr


*posthead(note("test"))
*prehead(note("test"))


