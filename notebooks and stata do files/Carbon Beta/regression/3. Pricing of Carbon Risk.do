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

import delimited "https://raw.githubusercontent.com/connorpn/cnolan-thesis/main/regression/regression%20variables/pricing_carbon_risk.csv"

label variable ticker "ticker"
sort ticker
encode ticker, gen(ticker_encode)

numdate monthly date = yearmonth, p(YM)

destring log_scope2, replace force


* Run and store regressions


eststo clear

eststo cb: ///
reghdfe ret carbon_beta, ///
absorb(date) ///
vce(cluster ticker_encode)
estadd local date_fe "yes" , replace
estadd local industry_fe "no" , replace

eststo cb_vars: ///
reghdfe ret carbon_beta logsize bm leverage mom investa roe logppe beta volat salesgr epsgr, ///
absorb(date) ///
vce(cluster ticker_encode)
estadd local date_fe "yes" , replace
estadd local industry_fe "no" , replace

eststo cb_ind: ///
reghdfe ret carbon_beta, ///
absorb(date industry) ///
vce(cluster ticker_encode)
estadd local date_fe "yes" , replace
estadd local industry_fe "yes" , replace

eststo cb_vars_ind: ///
reghdfe ret carbon_beta  logsize bm leverage mom investa roe logppe beta volat salesgr epsgr , ///
absorb(date industry) ///
vce(cluster ticker_encode)
estadd local date_fe "yes" , replace
estadd local industry_fe "yes" , replace



estfe, labels(date "Year/Month FE" industry "Industry FE")
*estadd scalar r2_adjusted = e(r2_a)

cd "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\regression\regression outputs\carbon beta"

#delimit ;
esttab cb cb_vars cb_ind cb_vars_ind using "cb_pricing_risk.tex", 
	indicate(`r(indicate_fe)')
	label se star(* 0.10 ** 0.05 *** 0.01)
	s(date_fe industry_fe N r2_a,
	label("Year/Month FE" "Industry FE" "Observations" "R2-Adj"))
	varlabels(
	carbon_beta "CARBON BETA"
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
	title(Pricing of Carbon Risk: test2)
	order(ret carbon_beta logsize bm leverage mom investa roe logppe beta volat salesgr epsgr _cons)
	compress
	nomtitles
	nogaps
	mgroups("Returns i,t: (Monthly Stock Returns) ", pattern(0 0 0 0) ///
prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}))
	replace;
#delimit cr

