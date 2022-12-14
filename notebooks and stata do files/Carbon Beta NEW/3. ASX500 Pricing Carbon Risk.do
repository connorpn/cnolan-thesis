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
drop if date < tm(2010m7)
drop if date > tm(2022m6)


*winsorize

winsor ret, gen(winsor_ret) p(0.025)
winsor ln_marketcap, gen(winsor_ln_marketcap) p(0.025)
winsor bm, gen(winsor_bm) p(0.025)
winsor roe, gen(winsor_roe) p(0.025) 
winsor leverage, gen(winsor_leverage) p(0.025)
winsor investa, gen(winsor_investa) p(0.025)
winsor logppe, gen(winsor_logppe) p(0.025)
winsor ppea, gen(winsor_ppea) p(0.025)
winsor carbon_beta, gen(winsor_carbon_beta) p(0.025)


drop ret ln_marketcap bm roe leverage investa logppe ppea carbon_beta
rename winsor_ret ret
rename winsor_ln_marketcap ln_marketcap
rename winsor_bm bm
rename winsor_roe roe
rename winsor_leverage leverage
rename winsor_investa investa
rename winsor_logppe logppe
rename winsor_ppea ppea
rename winsor_carbon_beta carbon_beta



* Run and store regressions


eststo clear

eststo cb: ///
reghdfe ret carbon_beta, ///
absorb(date) ///
vce(cluster ticker_encode)
estadd local date_fe "yes" , replace
estadd local industry_fe "no" , replace

eststo cb_vars: ///
reghdfe ret carbon_beta ln_marketcap bm roe leverage investa logppe ppea, ///
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
reghdfe ret carbon_beta ln_marketcap bm roe leverage investa logppe ppea, ///
absorb(date industry) ///
vce(cluster ticker_encode)
estadd local date_fe "yes" , replace
estadd local industry_fe "yes" , replace



estfe, labels(date "Year/Month FE" industry "Industry FE")
*estadd scalar r2_adjusted = e(r2_a)

cd "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\regression\regression outputs\carbon beta\asx500 estimation"

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
	)
	title(Pricing of Carbon Risk Using ASX500 SAMPLE)
	order(carbon_beta ln_marketcap bm roe leverage investa logppe ppea _cons)
	compress
	nomtitles
	nogaps
	mgroups("Returns i,t: (Monthly Stock Returns) ", pattern(1 0 0 0) ///
prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}))
	note("All Variables are Winsorized at 2.5%")
	replace;
#delimit cr

