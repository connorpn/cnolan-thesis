/*
ssc install numdate
ssc install winsor
ssc install ftools
ssc install reghdfe
ssc install estout
ssc install erepost
net install regsave, from("https://raw.githubusercontent.com/reifjulian/regsave/master") replace
*/


clear
eststo clear

*import data
import delimited "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\regression\regression variables\br_carbon_emissions_and_stock_returns.csv"

*encode ticker
label variable ticker "ticker"
sort ticker 	
encode ticker, gen(ticker_encode)

*datetime
numdate monthly date = yearmonth, p(YM)

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
winsor leverage, gen(winsor_leverage) p(0.025)
winsor mom, gen(winsor_mom) p(0.005)
winsor investa, gen(winsor_investa) p(0.025)
winsor roe, gen(winsor_roe) p(0.025)
winsor volat, gen(winsor_volat) p(0.005)
winsor salesgr, gen(winsor_salesgr) p(0.005)
winsor epsgr, gen(winsor_epsgr) p(0.005)



*regressions

*log emissions

eststo clear

eststo: reghdfe ret log_scope1 logsize winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe logppe beta winsor_volat winsor_salesgr winsor_epsgr, absorb(date industry) vce(cluster ticker_encode year)
estadd local ym_fe "yes" , replace
estadd local industry_fe "yes" , replace

eststo: reghdfe ret log_scope2 logsize winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe logppe beta winsor_volat winsor_salesgr winsor_epsgr, absorb(date industry) vce(cluster ticker_encode year)
estadd local ym_fe "yes" , replace
estadd local industry_fe "yes" , replace

eststo: reghdfe ret log_total_emissions logsize winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe logppe beta winsor_volat winsor_salesgr winsor_epsgr, absorb(date industry) vce(cluster ticker_encode year)
estadd local ym_fe "yes" , replace
estadd local industry_fe "yes" , replace

eststo: reghdfe ret log_energy_consumption logsize winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe logppe beta winsor_volat winsor_salesgr winsor_epsgr, absorb(date industry) vce(cluster ticker_encode year)
estadd local ym_fe "yes" , replace
estadd local industry_fe "yes" , replace

eststo: reghdfe ret log_scope1 logsize winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe logppe beta winsor_volat winsor_salesgr winsor_epsgr, absorb(date) vce(cluster ticker_encode year)
predict coeff_log_scope1_n, xb
sort date
by date: egen _b_log_scope1_n = mean(coeff_log_scope1_n)
estadd local ym_fe "yes" , replace
estadd local industry_fe "no" , replace

eststo: reghdfe ret log_scope2 logsize winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe logppe beta winsor_volat winsor_salesgr winsor_epsgr, absorb(date) vce(cluster ticker_encode year)
estadd local ym_fe "yes" , replace
estadd local industry_fe "no" , replace

eststo: reghdfe ret log_total_emissions logsize winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe logppe beta winsor_volat winsor_salesgr winsor_epsgr, absorb(date) vce(cluster ticker_encode year)
estadd local ym_fe "yes" , replace
estadd local industry_fe "no" , replace

eststo: reghdfe ret log_energy_consumption logsize winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe logppe beta winsor_volat winsor_salesgr winsor_epsgr, absorb(date) vce(cluster ticker_encode year)
estadd local ym_fe "yes" , replace
estadd local industry_fe "no" , replace

estfe, labels(date "Year/Month FE" industry "Industry FE")

cd "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\regression\regression outputs\bolton replications"

#delimit ;
esttab using "br_carbon_emissions_and_stock_returns_log_emissions.tex", 
	varlabels(
	log_scope1 "LN S1"
	log_scope2 "LN S2"
	log_total_emissions "LN TOT"
	log_energy_consumption "LN ENG"
	logsize LOGSIZE
	winsor_bm B/M
	winsor_leverage LEVERAGE
	winsor_mom MOM
	winsor_investa INVEST/A
	winsor_roe ROE
	logppe LOGPPE
	beta BETA
	winsor_volat VOLAT
	winsor_salesgr SALESGR
	winsor_epsgr EPSGR
	)
	indicate(
	`r(indicate_fe)'
	)
	order(log_scope1 log_scope2 log_total_emissions log_energy_consumption logsize winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe logppe beta winsor_volat winsor_salesgr winsor_epsgr _cons)
	label se star(* 0.10 ** 0.05 *** 0.01)
	s(ym_fe industry_fe N r2_a,
	label("Year FE" "Industry FE" "Observations" "R2-Adj"))
	title(Carbon Emissions and Stock Returns: LOG Emission)
	mtitles("RET" "RET" "RET" "RET" "RET" "RET" "RET" "RET")
	replace;
#delimit cr
*nomtitles

eststo clear

eststo: reghdfe ret change_scope1 logsize winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe logppe beta winsor_volat winsor_salesgr winsor_epsgr, absorb(date industry) vce(cluster ticker_encode year)
estadd local ym_fe "yes" , replace
estadd local industry_fe "yes" , replace

eststo: reghdfe ret change_scope2 logsize winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe logppe beta winsor_volat winsor_salesgr winsor_epsgr, absorb(date industry) vce(cluster ticker_encode year)
estadd local ym_fe "yes" , replace
estadd local industry_fe "yes" , replace

eststo: reghdfe ret change_total_emissions logsize winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe logppe beta winsor_volat winsor_salesgr winsor_epsgr, absorb(date industry) vce(cluster ticker_encode year)
estadd local ym_fe "yes" , replace
estadd local industry_fe "yes" , replace

eststo: reghdfe ret change_energy_consumption logsize winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe logppe beta winsor_volat winsor_salesgr winsor_epsgr, absorb(date industry) vce(cluster ticker_encode year)
estadd local ym_fe "yes" , replace
estadd local industry_fe "yes" , replace


eststo: reghdfe ret change_scope1 logsize winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe logppe beta winsor_volat winsor_salesgr winsor_epsgr, absorb(date) vce(cluster ticker_encode year)
estadd local ym_fe "yes" , replace
estadd local industry_fe "no" , replace

eststo: reghdfe ret change_scope2 logsize winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe logppe beta winsor_volat winsor_salesgr winsor_epsgr, absorb(date) vce(cluster ticker_encode year)
estadd local ym_fe "yes" , replace
estadd local industry_fe "no" , replace

eststo: reghdfe ret change_total_emissions logsize winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe logppe beta winsor_volat winsor_salesgr winsor_epsgr, absorb(date) vce(cluster ticker_encode year)
estadd local ym_fe "yes" , replace
estadd local industry_fe "no" , replace

eststo: reghdfe ret change_energy_consumption logsize winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe logppe beta winsor_volat winsor_salesgr winsor_epsgr, absorb(date) vce(cluster ticker_encode year)
estadd local ym_fe "yes" , replace
estadd local industry_fe "no" , replace

estfe, labels(date "Year/Month FE" industry "Industry FE")

cd "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\regression\regression outputs\bolton replications"

#delimit ;
esttab using "br_carbon_emissions_and_stock_returns_change_emissions.tex",
	varlabels(
	change_scope1 "\$\Delta\$ S1"
	change_scope2 "\$\Delta\$ S2"
	change_total_emissions "\$\Delta\$ TOT"
	change_energy_consumption "\$\Delta\$ ENG"
	logsize LOGSIZE
	winsor_bm B/M
	winsor_leverage LEVERAGE
	winsor_mom MOM
	winsor_investa INVEST/A
	winsor_roe ROE
	logppe LOGPPE
	beta BETA
	winsor_volat VOLAT
	winsor_salesgr SALESGR
	winsor_epsgr EPSGR
	)
	indicate(
	`r(indicate_fe)'
	)
	order(change_scope1 change_scope2 change_total_emissions change_energy_consumption logsize winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe logppe beta winsor_volat winsor_salesgr winsor_epsgr _cons)
	label se star(* 0.10 ** 0.05 *** 0.01)
	s(ym_fe industry_fe N r2_a,
	label("Year FE" "Industry FE" "Observations" "R2-Adj"))
	title(Carbon Emissions and Stock Returns: Yearly Change in Emissions)
	mtitles("RET" "RET" "RET" "RET" "RET" "RET" "RET" "RET")
	replace;
#delimit cr
*nomtitles

eststo clear


eststo: reghdfe ret scope1_int logsize winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe logppe beta winsor_volat winsor_salesgr winsor_epsgr, absorb(date industry) vce(cluster ticker_encode year)
estadd local ym_fe "yes" , replace
estadd local industry_fe "yes" , replace

eststo: reghdfe ret scope2_int logsize winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe logppe beta winsor_volat winsor_salesgr winsor_epsgr, absorb(date industry) vce(cluster ticker_encode year)
estadd local ym_fe "yes" , replace
estadd local industry_fe "yes" , replace

eststo: reghdfe ret total_emissions_int logsize winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe logppe beta winsor_volat winsor_salesgr winsor_epsgr, absorb(date industry) vce(cluster ticker_encode year)
estadd local ym_fe "yes" , replace
estadd local industry_fe "yes" , replace

eststo: reghdfe ret energy_consumption_int logsize winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe logppe beta winsor_volat winsor_salesgr winsor_epsgr, absorb(date industry) vce(cluster ticker_encode year)
estadd local ym_fe "yes" , replace
estadd local industry_fe "yes" , replace


eststo: reghdfe ret scope1_int logsize winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe logppe beta winsor_volat winsor_salesgr winsor_epsgr, absorb(date) vce(cluster ticker_encode year)
estadd local ym_fe "yes" , replace
estadd local industry_fe "no" , replace

eststo: reghdfe ret scope2_int logsize winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe logppe beta winsor_volat winsor_salesgr winsor_epsgr, absorb(date) vce(cluster ticker_encode year)
estadd local ym_fe "yes" , replace
estadd local industry_fe "no" , replace

eststo: reghdfe ret total_emissions_int logsize winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe logppe beta winsor_volat winsor_salesgr winsor_epsgr, absorb(date) vce(cluster ticker_encode year)
estadd local ym_fe "yes" , replace
estadd local industry_fe "no" , replace

eststo: reghdfe ret energy_consumption_int logsize winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe logppe beta winsor_volat winsor_salesgr winsor_epsgr, absorb(date) vce(cluster ticker_encode year)
estadd local ym_fe "yes" , replace
estadd local industry_fe "no" , replace

estfe, labels(date "Year/Month FE" industry "Industry FE")

cd "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\regression\regression outputs\bolton replications"

#delimit ;
esttab using "br_carbon_emissions_and_stock_returns_emissions_int.tex", 
	varlabels(
	scope1_int "S1 INT"
	scope2_int "S2 INT"
	total_emissions_int "TOT INT"
	energy_consumption_int "ENG INT"
	logsize LOGSIZE
	winsor_bm B/M
	winsor_leverage LEVERAGE
	winsor_mom MOM
	winsor_investa INVEST/A
	winsor_roe ROE
	logppe LOGPPE
	beta BETA
	winsor_volat VOLAT
	winsor_salesgr SALESGR
	winsor_epsgr EPSGR
	)
	indicate(
	`r(indicate_fe)'
	)
	order(scope1_int scope2_int total_emissions_int energy_consumption_int logsize winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe logppe beta winsor_volat winsor_salesgr winsor_epsgr _cons)
	label se star(* 0.10 ** 0.05 *** 0.01)
	s(ym_fe industry_fe N r2_a,
	label("Year FE" "Industry FE" "Observations" "R2-Adj"))
	title(Carbon Emissions and Stock Returns: Emission Intensity)
	mtitles("RET" "RET" "RET" "RET" "RET" "RET" "RET" "RET")
	replace;
#delimit cr

*nomtitles
