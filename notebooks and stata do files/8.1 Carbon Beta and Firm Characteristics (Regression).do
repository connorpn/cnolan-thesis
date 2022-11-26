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
estimates clear

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

eststo log_scope1_emiss: ///
reghdfe carbon_beta  logsize bm leverage mom investa roe logppe beta volat salesgr epsgr log_scope1, absorb(date) ///
vce(cluster ticker_encode)

eststo log_scope1_ind: ///
reghdfe carbon_beta  logsize bm leverage mom investa roe logppe beta volat salesgr epsgr, ///
absorb(date industry) ///
vce(cluster ticker_encode)

eststo log_scope1_emiss_ind: /// 
reghdfe carbon_beta  logsize bm leverage mom investa roe logppe beta volat salesgr epsgr log_scope1, absorb(date industry) ///
vce(cluster ticker_encode)



estfe, labels(date "Year/Month FE" industry "Industry FE")
estadd ar2, replace

cd "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\regression output\8.1"

#delimit ;
esttab log_scope1 log_scope1_emiss log_scope1_ind log_scope1_emiss_ind using "log_scope1.tex", 
	indicate(`r(indicate_fe)')
	label se star(* 0.10 ** 0.05 *** 0.01)
	s(N ar2,
	label("Observations" "R{superscript:2}-Adj."))
	keep(did treat post mat_hs_v pat_hs_v)
	replace;
#delimit cr


/*



* Prepare estimates for -estout-
	estfe, labels(date "Year/Month FE" industry "Industry FE")
	return list
/*
* Run estout/esttab
	esttab . log_scope1* , indicate(`r(indicate_fe)')
*/		

* Export to LaTex
	cd "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\regression output\8.1"
	esttab using log_scope1.tex, ar2 replace indicate(`r(indicate_fe)') label ///
	title(log_scope1 Carbon Beta and Firm Charateristics)
	
* Return stored estimates to their previous state
*	estfe . log_scope1*, restore

*eststo clear
*clear


*/


*save "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\notebooks and stata do files\8.1 Carbon Beta and Firm Characteristics (Regression).do", replace


