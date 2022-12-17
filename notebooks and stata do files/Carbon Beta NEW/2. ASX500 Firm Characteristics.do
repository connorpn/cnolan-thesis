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
import delimited "Z:/OneDrive/University Study/Honours Thesis/cnolan-thesis/regression/regression variables/cb_firm_characteristics_vars.csv"

*encode ticker
label variable ticker "ticker"
sort ticker
encode ticker, gen(ticker_encode)

*datetime
numdate monthly date = yearmonth, p(YM)

*filter date
drop if date < tm(2008m7)
drop if date > tm(2021m6)


*winsorize firm variables
winsor ln_marketcap, gen(winsor_ln_marketcap) p(0.025)
winsor bm, gen(winsor_bm) p(0.025)
winsor roe, gen(winsor_roe) p(0.025) 
winsor leverage, gen(winsor_leverage) p(0.025)
winsor investa, gen(winsor_investa) p(0.025)
winsor logppe, gen(winsor_logppe) p(0.025)
winsor ppea, gen(winsor_ppea) p(0.025)

drop ln_marketcap bm roe leverage investa logppe ppea
rename winsor_ln_marketcap ln_marketcap
rename winsor_bm bm
rename winsor_roe roe
rename winsor_leverage leverage
rename winsor_investa investa
rename winsor_logppe logppe
rename winsor_ppea ppea

*winsor ret, gen(winsor_ret) p(0.025)
*drop ret
*rename winsor_ret ret

*winsor carbon_beta, gen(winsor_carbon_beta) p(0.025)
*drop carbon_beta
*rename winsor_carbon_beta carbon_beta

*winsorize emissions variables

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



* Run and store regressions


eststo clear


eststo cb_vars: ///
reghdfe asx500_carbon_beta ln_marketcap bm roe leverage investa logppe ppea, ///
absorb(date) ///
vce(cluster ticker_encode)
estadd local ym_fe "yes" , replace
estadd local industry_fe "no" , replace

eststo cb_vars: ///
reghdfe nger_carbon_beta ln_marketcap bm roe leverage investa logppe ppea, ///
absorb(date) ///
vce(cluster ticker_encode)
estadd local ym_fe "yes" , replace
estadd local industry_fe "no" , replace

eststo cb_vars: ///
reghdfe nger_carbon_beta ln_marketcap bm roe leverage investa logppe ppea log_scope1, ///
absorb(date) ///
vce(cluster ticker_encode)
estadd local ym_fe "yes" , replace
estadd local industry_fe "no" , replace

eststo cb_vars: ///
reghdfe nger_carbon_beta ln_marketcap bm roe leverage investa logppe ppea log_scope2, ///
absorb(date) ///
vce(cluster ticker_encode)
estadd local ym_fe "yes" , replace
estadd local industry_fe "no" , replace

eststo cb_vars: ///
reghdfe nger_carbon_beta ln_marketcap bm roe leverage investa logppe ppea log_total_emissions, ///
absorb(date) ///
vce(cluster ticker_encode)
estadd local ym_fe "yes" , replace
estadd local industry_fe "no" , replace

eststo cb_vars: ///
reghdfe nger_carbon_beta ln_marketcap bm roe leverage investa logppe ppea log_energy_consumption, ///
absorb(date) ///
vce(cluster ticker_encode)
estadd local ym_fe "yes" , replace
estadd local industry_fe "no" , replace

eststo cb_vars: ///
reghdfe asx500_carbon_beta ln_marketcap bm roe leverage investa logppe ppea, ///
absorb(date industry) ///
vce(cluster ticker_encode)
estadd local ym_fe "yes" , replace
estadd local industry_fe "yes", replace

eststo cb_vars: ///
reghdfe nger_carbon_beta ln_marketcap bm roe leverage investa logppe ppea, ///
absorb(date industry) ///
vce(cluster ticker_encode)
estadd local ym_fe "yes" , replace
estadd local industry_fe "yes", replace

eststo cb_vars: ///
reghdfe nger_carbon_beta ln_marketcap bm roe leverage investa logppe ppea log_scope1, ///
absorb(date industry) ///
vce(cluster ticker_encode)
estadd local ym_fe "yes" , replace
estadd local industry_fe "yes", replace

eststo cb_vars: ///
reghdfe nger_carbon_beta ln_marketcap bm roe leverage investa logppe ppea log_scope2, ///
absorb(date industry) ///
vce(cluster ticker_encode)
estadd local ym_fe "yes" , replace
estadd local industry_fe "yes", replace

eststo cb_vars: ///
reghdfe nger_carbon_beta ln_marketcap bm roe leverage investa logppe ppea log_total_emissions, ///
absorb(date industry) ///
vce(cluster ticker_encode)
estadd local ym_fe "yes" , replace
estadd local industry_fe "yes", replace

eststo cb_vars: ///
reghdfe nger_carbon_beta ln_marketcap bm roe leverage investa logppe ppea log_energy_consumption, ///
absorb(date industry) ///
vce(cluster ticker_encode)
estadd local ym_fe "yes" , replace
estadd local industry_fe "yes", replace


estfe, labels(date "Year/Month FE" industry "Industry FE")
*estadd scalar r2_adjusted = e(r2_a)

cd "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\regression\regression outputs\carbon beta"


esttab using "cb_determinants_log.tex", 
	varlabels(
	log_scope1 "LN S1"
	log_scope2 "LN S2"
	log_total_emissions "LN TOT"
	log_energy_consumption "LN ENG"
	ln_marketcap "ln(Market Cap.)"
	bm Book/Market
	roe "Return on Equity"
	leverage LEVERAGE
	investa Capex/Assets
	logppe "ln(PPE)"
	ppea PPE/Assets
	)
	indicate(`r(indicate_fe)')
	order(log_scope1 log_scope2 log_total_emissions log_energy_consumption ln_marketcap bm roe leverage investa logppe ppea )
	label se star(* 0.10 ** 0.05 *** 0.01)
	s(ym_fe industry_fe N r2_a,
	label("Year FE" "Industry FE" "Observations" "R2-Adj"))
	nomtitles
	mgroups("Dependent Variable: Carbon Beta) ", pattern(1 0 0 0 0 0 0 0 0 0 0 0) ///
prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}))
	noconstant
	replace;
#delimit cr
