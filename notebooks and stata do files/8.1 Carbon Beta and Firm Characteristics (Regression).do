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

*log_scope1

import delimited "https://raw.githubusercontent.com/connorpn/cnolan-thesis/main/output/log_scope1_carbon_beta_firm_characteristics.csv"

label variable ticker "ticker"
sort ticker
encode ticker, gen(ticker_encode)

numdate monthly date = yearmonth, p(YM)

* Run and store regressions


eststo log_scope1: ///
reghdfe carbon_beta  logsize bm leverage mom investa roe logppe beta volat salesgr epsgr, ///
absorb(date) ///
vce(cluster ticker_encode)
estadd local date_fe "yes" , replace
estadd local industry_fe "no" , replace

eststo log_scope1_emiss: ///
reghdfe carbon_beta  logsize bm leverage mom investa roe logppe beta volat salesgr epsgr log_scope1, absorb(date) ///
vce(cluster ticker_encode)
estadd local date_fe "yes" , replace
estadd local industry_fe "no" , replace

eststo log_scope1_ind: ///
reghdfe carbon_beta  logsize bm leverage mom investa roe logppe beta volat salesgr epsgr, ///
absorb(date industry) ///
vce(cluster ticker_encode)
estadd local date_fe "yes" , replace
estadd local industry_fe "yes" , replace

eststo log_scope1_emiss_ind: /// 
reghdfe carbon_beta  logsize bm leverage mom investa roe logppe beta volat salesgr epsgr log_scope1, absorb(date industry) ///
vce(cluster ticker_encode)
estadd local date_fe "yes" , replace
estadd local industry_fe "yes" , replace


estfe, labels(date "Year/Month FE" industry "Industry FE")
*estadd scalar r2_adjusted = e(r2_a)

cd "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\regression output\8.1"

#delimit ;
esttab log_scope1 log_scope1_emiss log_scope1_ind log_scope1_emiss_ind using "log_scope1.tex", 
	indicate(`r(indicate_fe)')
	label se star(* 0.10 ** 0.05 *** 0.01)
	s(date_fe industry_fe N r2_a,
	label("Year/Month FE" "Industry FE" "Observations" "R2-Adj"))
	title("Carbon Beta and Firm Characteristics:" {bf: "log_scope1 emissions"})
	replace;
#delimit cr


save "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\notebooks and stata do files\8.1 Carbon Beta and Firm Characteristics (Regression).do", replace


