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
import delimited "Z:/OneDrive/University Study/Honours Thesis/cnolan-thesis/regression/regression variables/cb_asx500_pricing_carbon_risk.csv"

*encode ticker
label variable ticker "ticker"
sort ticker
encode ticker, gen(ticker_encode)

*datetime
numdate monthly date = yearmonth, p(YM)

*filter date
drop if date < tm(2008m7)
drop if date > tm(2021m6)


*winsorize

winsor ret, gen(winsor_ret) p(0.005)
winsor ln_marketcap, gen(winsor_ln_marketcap) p(0.025)
winsor bm, gen(winsor_bm) p(0.025)
winsor roe, gen(winsor_roe) p(0.025) 
winsor leverage, gen(winsor_leverage) p(0.025)
winsor investa, gen(winsor_investa) p(0.025)
winsor logppe, gen(winsor_logppe) p(0.025)
winsor ppea, gen(winsor_ppea) p(0.025)
winsor carbon_beta, gen(winsor_carbon_beta) p(0.025)
winsor beta, gen(winsor_beta) p(0.005)
winsor mom, gen(winsor_mom) p(0.005)


drop ret ln_marketcap bm roe leverage investa logppe ppea carbon_beta beta mom
rename winsor_ret ret
rename winsor_ln_marketcap ln_marketcap
rename winsor_bm bm
rename winsor_roe roe
rename winsor_leverage leverage
rename winsor_investa investa
rename winsor_logppe logppe
rename winsor_ppea ppea
rename winsor_carbon_beta carbon_beta
rename winsor_beta beta
rename winsor_mom mom



* Run and store regressions


eststo clear

eststo cb: ///
reghdfe ret carbon_beta, ///
absorb(date) ///
vce(cluster ticker_encode)
estadd local date_fe "yes" , replace
estadd local industry_fe "no" , replace

eststo cb_vars: ///
reghdfe ret carbon_beta ln_marketcap bm roe leverage investa logppe ppea beta mom, ///
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
reghdfe ret carbon_beta ln_marketcap bm roe leverage investa logppe ppea beta mom, ///
absorb(date industry) ///
vce(cluster ticker_encode)
estadd local date_fe "yes" , replace
estadd local industry_fe "yes" , replace



estfe, labels(date "Year/Month FE" industry "Industry FE")
*estadd scalar r2_adjusted = e(r2_a)

cd "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\regression\regression outputs\carbon beta\"

/*
#delimit ;
esttab cb cb_vars cb_ind cb_vars_ind using "cb_asx500_pricing_risk.tex", 
	indicate(`r(indicate_fe)')
	label se star(* 0.10 ** 0.05 *** 0.01)
	s(date_fe industry_fe N r2_a,
	label("Year/Month FE" "Industry FE" "Observations" "R2-Adj"))
	varlabels(
	carbon_beta "Carbon Beta"
	ln_marketcap "ln(Market Cap.)"
	bm Book/Market
	roe "Return on Equity"
	leverage LEVERAGE
	investa Capex/Assets
	logppe "ln(PPE)"
	ppea PPE/Assets
	beta "CAPM Beta"
	mom Momentum
	)
	order(carbon_beta ln_marketcap bm roe leverage investa logppe ppea beta mom _cons)
	compress
	nomtitles
	nogaps
	mgroups("Dependent Variable: Monthly Stock Returns") ", pattern(1 0 0 0) ///
prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}))
	noconstant
	replace;
#delimit cr
*/

#delimit ;
esttab * using "cb_asx500_pricing_risk.tex", 
	varlabels(
	carbon_beta "Carbon Beta"
	ln_marketcap "ln(Market Cap.)"
	bm Book/Market
	roe "Return on Equity"
	leverage Leverage
	investa Capex/Assets
	logppe "ln(PPE)"
	ppea PPE/Assets
	beta "CAPM Beta"
	mom Momentum
	)
	indicate(`r(indicate_fe)')
	order(carbon_beta ln_marketcap bm roe leverage investa logppe ppea beta mom)
	label se star(* 0.10 ** 0.05 *** 0.01)
	s(date_fe industry_fe N r2_a,
	label("Year/Month FE" "Industry FE" "Observations" "R2-Adj"))
	nomtitles
	mgroups("Dependent Variable: Monthly Stock Returns", pattern(1 0 0 0 ) ///
prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}))
	noconstant
	replace;
#delimit cr


clear
eststo clear

*import data
import delimited "Z:/OneDrive/University Study/Honours Thesis/cnolan-thesis/regression/regression variables/cb_asx500_pricing_carbon_risk.csv"

*encode ticker
label variable ticker "ticker"
sort ticker
encode ticker, gen(ticker_encode)

*datetime
numdate monthly date = yearmonth, p(YM)

*filter date
drop if date < tm(2009m7)
drop if date > tm(2021m6)


*winsorize

winsor ret, gen(winsor_ret) p(0.005)
winsor ln_marketcap, gen(winsor_ln_marketcap) p(0.025)
winsor bm, gen(winsor_bm) p(0.025)
winsor roe, gen(winsor_roe) p(0.025) 
winsor leverage, gen(winsor_leverage) p(0.025)
winsor investa, gen(winsor_investa) p(0.025)
winsor logppe, gen(winsor_logppe) p(0.025)
winsor ppea, gen(winsor_ppea) p(0.025)
winsor carbon_beta, gen(winsor_carbon_beta) p(0.025)
winsor beta, gen(winsor_beta) p(0.005)
winsor mom, gen(winsor_mom) p(0.005)


drop ret ln_marketcap bm roe leverage investa logppe ppea carbon_beta beta mom
rename winsor_ret ret
rename winsor_ln_marketcap ln_marketcap
rename winsor_bm bm
rename winsor_roe roe
rename winsor_leverage leverage
rename winsor_investa investa
rename winsor_logppe logppe
rename winsor_ppea ppea
rename winsor_carbon_beta carbon_beta
rename winsor_beta beta
rename winsor_mom mom



* Run and store regressions


eststo clear

eststo cb: ///
reghdfe ret carbon_beta, ///
absorb(date) ///
vce(cluster ticker_encode)
estadd local date_fe "yes" , replace
estadd local industry_fe "no" , replace

eststo cb_vars: ///
reghdfe ret carbon_beta ln_marketcap bm roe leverage investa logppe ppea beta mom, ///
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
reghdfe ret carbon_beta ln_marketcap bm roe leverage investa logppe ppea beta mom, ///
absorb(date industry) ///
vce(cluster ticker_encode)
estadd local date_fe "yes" , replace
estadd local industry_fe "yes" , replace



estfe, labels(date "Year/Month FE" industry "Industry FE")
*estadd scalar r2_adjusted = e(r2_a)

cd "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\regression\regression outputs\carbon beta\"

/*
#delimit ;
esttab cb cb_vars cb_ind cb_vars_ind using "cb_asx500_pricing_risk.tex", 
	indicate(`r(indicate_fe)')
	label se star(* 0.10 ** 0.05 *** 0.01)
	s(date_fe industry_fe N r2_a,
	label("Year/Month FE" "Industry FE" "Observations" "R2-Adj"))
	varlabels(
	carbon_beta "Carbon Beta"
	ln_marketcap "ln(Market Cap.)"
	bm Book/Market
	roe "Return on Equity"
	leverage LEVERAGE
	investa Capex/Assets
	logppe "ln(PPE)"
	ppea PPE/Assets
	beta "CAPM Beta"
	mom Momentum
	)
	order(carbon_beta ln_marketcap bm roe leverage investa logppe ppea beta mom _cons)
	compress
	nomtitles
	nogaps
	mgroups("Dependent Variable: Monthly Stock Returns") ", pattern(1 0 0 0) ///
prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}))
	noconstant
	replace;
#delimit cr
*/

#delimit ;
esttab * using "cb_asx500_pricing_risk_12m.tex", 
	varlabels(
	carbon_beta "Carbon Beta"
	ln_marketcap "ln(Market Cap.)"
	bm Book/Market
	roe "Return on Equity"
	leverage Leverage
	investa Capex/Assets
	logppe "ln(PPE)"
	ppea PPE/Assets
	beta "CAPM Beta"
	mom Momentum
	)
	indicate(`r(indicate_fe)')
	order(carbon_beta ln_marketcap bm roe leverage investa logppe ppea beta mom)
	label se star(* 0.10 ** 0.05 *** 0.01)
	s(date_fe industry_fe N r2_a,
	label("Year/Month FE" "Industry FE" "Observations" "R2-Adj"))
	nomtitles
	mgroups("Dependent Variable: Monthly Stock Returns", pattern(1 0 0 0 ) ///
prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}))
	noconstant
	replace;
#delimit cr

clear
eststo clear

*import data
import delimited "Z:/OneDrive/University Study/Honours Thesis/cnolan-thesis/regression/regression variables/cb_asx500_pricing_carbon_risk.csv"

*encode ticker
label variable ticker "ticker"
sort ticker
encode ticker, gen(ticker_encode)

*datetime
numdate monthly date = yearmonth, p(YM)

*filter date
drop if date < tm(2010m7)
drop if date > tm(2021m6)


*winsorize

winsor ret, gen(winsor_ret) p(0.005)
winsor ln_marketcap, gen(winsor_ln_marketcap) p(0.025)
winsor bm, gen(winsor_bm) p(0.025)
winsor roe, gen(winsor_roe) p(0.025) 
winsor leverage, gen(winsor_leverage) p(0.025)
winsor investa, gen(winsor_investa) p(0.025)
winsor logppe, gen(winsor_logppe) p(0.025)
winsor ppea, gen(winsor_ppea) p(0.025)
winsor carbon_beta, gen(winsor_carbon_beta) p(0.025)
winsor beta, gen(winsor_beta) p(0.005)
winsor mom, gen(winsor_mom) p(0.005)


drop ret ln_marketcap bm roe leverage investa logppe ppea carbon_beta beta mom
rename winsor_ret ret
rename winsor_ln_marketcap ln_marketcap
rename winsor_bm bm
rename winsor_roe roe
rename winsor_leverage leverage
rename winsor_investa investa
rename winsor_logppe logppe
rename winsor_ppea ppea
rename winsor_carbon_beta carbon_beta
rename winsor_beta beta
rename winsor_mom mom



* Run and store regressions


eststo clear

eststo cb: ///
reghdfe ret carbon_beta, ///
absorb(date) ///
vce(cluster ticker_encode)
estadd local date_fe "yes" , replace
estadd local industry_fe "no" , replace

eststo cb_vars: ///
reghdfe ret carbon_beta ln_marketcap bm roe leverage investa logppe ppea beta mom, ///
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
reghdfe ret carbon_beta ln_marketcap bm roe leverage investa logppe ppea beta mom, ///
absorb(date industry) ///
vce(cluster ticker_encode)
estadd local date_fe "yes" , replace
estadd local industry_fe "yes" , replace



estfe, labels(date "Year/Month FE" industry "Industry FE")
*estadd scalar r2_adjusted = e(r2_a)

cd "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\regression\regression outputs\carbon beta\"

/*
#delimit ;
esttab cb cb_vars cb_ind cb_vars_ind using "cb_asx500_pricing_risk.tex", 
	indicate(`r(indicate_fe)')
	label se star(* 0.10 ** 0.05 *** 0.01)
	s(date_fe industry_fe N r2_a,
	label("Year/Month FE" "Industry FE" "Observations" "R2-Adj"))
	varlabels(
	carbon_beta "Carbon Beta"
	ln_marketcap "ln(Market Cap.)"
	bm Book/Market
	roe "Return on Equity"
	leverage LEVERAGE
	investa Capex/Assets
	logppe "ln(PPE)"
	ppea PPE/Assets
	beta "CAPM Beta"
	mom Momentum
	)
	order(carbon_beta ln_marketcap bm roe leverage investa logppe ppea beta mom _cons)
	compress
	nomtitles
	nogaps
	mgroups("Dependent Variable: Monthly Stock Returns") ", pattern(1 0 0 0) ///
prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}))
	noconstant
	replace;
#delimit cr
*/

#delimit ;
esttab * using "cb_asx500_pricing_risk_24m.tex", 
	varlabels(
	carbon_beta "Carbon Beta"
	ln_marketcap "ln(Market Cap.)"
	bm Book/Market
	roe "Return on Equity"
	leverage Leverage
	investa Capex/Assets
	logppe "ln(PPE)"
	ppea PPE/Assets
	beta "CAPM Beta"
	mom Momentum
	)
	indicate(`r(indicate_fe)')
	order(carbon_beta ln_marketcap bm roe leverage investa logppe ppea beta mom)
	label se star(* 0.10 ** 0.05 *** 0.01)
	s(date_fe industry_fe N r2_a,
	label("Year/Month FE" "Industry FE" "Observations" "R2-Adj"))
	nomtitles
	mgroups("Dependent Variable: Monthly Stock Returns", pattern(1 0 0 0 ) ///
prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}))
	noconstant
	replace;
#delimit cr

clear
eststo clear

*import data
import delimited "Z:/OneDrive/University Study/Honours Thesis/cnolan-thesis/regression/regression variables/cb_asx500_pricing_carbon_risk.csv"

*encode ticker
label variable ticker "ticker"
sort ticker
encode ticker, gen(ticker_encode)

*datetime
numdate monthly date = yearmonth, p(YM)

*filter date
drop if date < tm(2011m7)
drop if date > tm(2021m6)


*winsorize

winsor ret, gen(winsor_ret) p(0.005)
winsor ln_marketcap, gen(winsor_ln_marketcap) p(0.025)
winsor bm, gen(winsor_bm) p(0.025)
winsor roe, gen(winsor_roe) p(0.025) 
winsor leverage, gen(winsor_leverage) p(0.025)
winsor investa, gen(winsor_investa) p(0.025)
winsor logppe, gen(winsor_logppe) p(0.025)
winsor ppea, gen(winsor_ppea) p(0.025)
winsor carbon_beta, gen(winsor_carbon_beta) p(0.025)
winsor beta, gen(winsor_beta) p(0.005)
winsor mom, gen(winsor_mom) p(0.005)


drop ret ln_marketcap bm roe leverage investa logppe ppea carbon_beta beta mom
rename winsor_ret ret
rename winsor_ln_marketcap ln_marketcap
rename winsor_bm bm
rename winsor_roe roe
rename winsor_leverage leverage
rename winsor_investa investa
rename winsor_logppe logppe
rename winsor_ppea ppea
rename winsor_carbon_beta carbon_beta
rename winsor_beta beta
rename winsor_mom mom



* Run and store regressions


eststo clear

eststo cb: ///
reghdfe ret carbon_beta, ///
absorb(date) ///
vce(cluster ticker_encode)
estadd local date_fe "yes" , replace
estadd local industry_fe "no" , replace

eststo cb_vars: ///
reghdfe ret carbon_beta ln_marketcap bm roe leverage investa logppe ppea beta mom, ///
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
reghdfe ret carbon_beta ln_marketcap bm roe leverage investa logppe ppea beta mom, ///
absorb(date industry) ///
vce(cluster ticker_encode)
estadd local date_fe "yes" , replace
estadd local industry_fe "yes" , replace



estfe, labels(date "Year/Month FE" industry "Industry FE")
*estadd scalar r2_adjusted = e(r2_a)

cd "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\regression\regression outputs\carbon beta\"

/*
#delimit ;
esttab cb cb_vars cb_ind cb_vars_ind using "cb_asx500_pricing_risk.tex", 
	indicate(`r(indicate_fe)')
	label se star(* 0.10 ** 0.05 *** 0.01)
	s(date_fe industry_fe N r2_a,
	label("Year/Month FE" "Industry FE" "Observations" "R2-Adj"))
	varlabels(
	carbon_beta "Carbon Beta"
	ln_marketcap "ln(Market Cap.)"
	bm Book/Market
	roe "Return on Equity"
	leverage LEVERAGE
	investa Capex/Assets
	logppe "ln(PPE)"
	ppea PPE/Assets
	beta "CAPM Beta"
	mom Momentum
	)
	order(carbon_beta ln_marketcap bm roe leverage investa logppe ppea beta mom _cons)
	compress
	nomtitles
	nogaps
	mgroups("Dependent Variable: Monthly Stock Returns") ", pattern(1 0 0 0) ///
prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}))
	noconstant
	replace;
#delimit cr
*/

#delimit ;
esttab * using "cb_asx500_pricing_risk_36m.tex", 
	varlabels(
	carbon_beta "Carbon Beta"
	ln_marketcap "ln(Market Cap.)"
	bm Book/Market
	roe "Return on Equity"
	leverage Leverage
	investa Capex/Assets
	logppe "ln(PPE)"
	ppea PPE/Assets
	beta "CAPM Beta"
	mom Momentum
	)
	indicate(`r(indicate_fe)')
	order(carbon_beta ln_marketcap bm roe leverage investa logppe ppea beta mom)
	label se star(* 0.10 ** 0.05 *** 0.01)
	s(date_fe industry_fe N r2_a,
	label("Year/Month FE" "Industry FE" "Observations" "R2-Adj"))
	nomtitles
	mgroups("Dependent Variable: Monthly Stock Returns", pattern(1 0 0 0 ) ///
prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}))
	noconstant
	replace;
#delimit cr


