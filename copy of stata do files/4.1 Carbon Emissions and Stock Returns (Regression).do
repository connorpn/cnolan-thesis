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


import delimited "https://raw.githubusercontent.com/connorpn/cnolan-thesis/main/output/carbon_emissions_stock_returns_vars.csv"


label variable ticker "ticker"
sort ticker 	
encode ticker, gen(ticker_encode)


numdate monthly date = yearmonth, p(YM)

winsor bm, gen(winsor_bm) p(0.025)
winsor leverage, gen(winsor_leverage) p(0.025)
winsor mom, gen(winsor_mom) p(0.005)
winsor investa, gen(winsor_investa) p(0.025)
winsor roe, gen(winsor_roe) p(0.025)
winsor volat, gen(winsor_volat) p(0.005)
winsor salesgr, gen(winsor_salesgr) p(0.005)
winsor epsgr, gen(winsor_epsgr) p(0.005)


destring log_scope2, replace force


*log emissions

eststo clear

eststo: reghdfe ret log_scope1 logsize winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe logppe beta winsor_volat winsor_salesgr winsor_epsgr, absorb(date industry) vce(cluster ticker_encode year)
predict coeff_log_scope1_y, xb
sort date
by date: egen _b_log_scope1_y = mean(coeff_log_scope1_y)
estadd local ym_fe "yes" , replace
estadd local industry_fe "yes" , replace

eststo: reghdfe ret log_scope2 logsize winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe logppe beta winsor_volat winsor_salesgr winsor_epsgr, absorb(date industry) vce(cluster ticker_encode year)
predict coeff_log_scope2_y, xb
sort date
by date: egen _b_log_scope2_y = mean(coeff_log_scope2_y)
estadd local ym_fe "yes" , replace
estadd local industry_fe "yes" , replace

eststo: reghdfe ret log_total_emissions logsize winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe logppe beta winsor_volat winsor_salesgr winsor_epsgr, absorb(date industry) vce(cluster ticker_encode year)
predict coeff_log_total_emissions_y, xb
sort date
by date: egen _b_log_total_emissions_y = mean(coeff_log_total_emissions_y)
estadd local ym_fe "yes" , replace
estadd local industry_fe "yes" , replace

eststo: reghdfe ret log_energy_consumption logsize winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe logppe beta winsor_volat winsor_salesgr winsor_epsgr, absorb(date industry) vce(cluster ticker_encode year)
predict coeff_log_energy_y, xb
sort date
by date: egen _b_log_energy_y = mean(coeff_log_energy_y)
estadd local ym_fe "yes" , replace
estadd local industry_fe "yes" , replace

eststo: reghdfe ret log_scope1 logsize winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe logppe beta winsor_volat winsor_salesgr winsor_epsgr, absorb(date) vce(cluster ticker_encode year)
predict coeff_log_scope1_n, xb
sort date
by date: egen _b_log_scope1_n = mean(coeff_log_scope1_n)
estadd local ym_fe "yes" , replace
estadd local industry_fe "no" , replace

eststo: reghdfe ret log_scope2 logsize winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe logppe beta winsor_volat winsor_salesgr winsor_epsgr, absorb(date) vce(cluster ticker_encode year)
predict coeff_log_scope2_n, xb
sort date
by date: egen _b_log_scope2_n = mean(coeff_log_scope2_n)
estadd local ym_fe "yes" , replace
estadd local industry_fe "no" , replace

eststo: reghdfe ret log_total_emissions logsize winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe logppe beta winsor_volat winsor_salesgr winsor_epsgr, absorb(date) vce(cluster ticker_encode year)
predict coeff_log_total_emissions_n, xb
sort date
by date: egen _b_log_total_emissions_n = mean(coeff_log_total_emissions_n)
estadd local ym_fe "yes" , replace
estadd local industry_fe "no" , replace

eststo: reghdfe ret log_energy_consumption logsize winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe logppe beta winsor_volat winsor_salesgr winsor_epsgr, absorb(date) vce(cluster ticker_encode year)
predict coeff_log_energy_n, xb
sort date
by date: egen _b_log_energy_n = mean(coeff_log_energy_n)
estadd local ym_fe "yes" , replace
estadd local industry_fe "no" , replace

estfe, labels(date "Year/Month FE" industry "Industry FE")

cd "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\regression output\4.1 Carbon Emissions and Stock Returns"

#delimit ;
esttab using "4.1 Carbon Emissions and Stock Returns (log emissions).tex", 
	varlabels(
	log_scope1 "LN SCOPE1"
	log_scope2 "LN SCOPE2"
	log_total_emissions "LN TOTAL"
	log_energy_consumption "LN ENERGY"
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
	nomtitles
	replace;
#delimit cr

eststo clear

eststo: reghdfe ret change_scope1 logsize winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe logppe beta winsor_volat winsor_salesgr winsor_epsgr, absorb(date industry) vce(cluster ticker_encode year)
predict coeff_change_scope1_y, xb
sort date
by date: egen _b_change_scope1_y = mean(coeff_change_scope1_y)
estadd local ym_fe "yes" , replace
estadd local industry_fe "yes" , replace

eststo: reghdfe ret change_scope2 logsize winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe logppe beta winsor_volat winsor_salesgr winsor_epsgr, absorb(date industry) vce(cluster ticker_encode year)
predict coeff_change_scope2_y, xb
sort date
by date: egen _b_change_scope2_y = mean(coeff_change_scope2_y)
estadd local ym_fe "yes" , replace
estadd local industry_fe "yes" , replace

eststo: reghdfe ret change_total_emissions logsize winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe logppe beta winsor_volat winsor_salesgr winsor_epsgr, absorb(date industry) vce(cluster ticker_encode year)
predict coeff_change_total_emissions_y, xb
sort date
by date: egen _b_change_total_emissions_y = mean(coeff_change_total_emissions_y)
estadd local ym_fe "yes" , replace
estadd local industry_fe "yes" , replace

eststo: reghdfe ret change_energy_consumption logsize winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe logppe beta winsor_volat winsor_salesgr winsor_epsgr, absorb(date industry) vce(cluster ticker_encode year)
predict coeff_change_energy_y, xb
sort date
by date: egen _b_change_energy_y = mean(coeff_change_energy_y)
estadd local ym_fe "yes" , replace
estadd local industry_fe "yes" , replace


eststo: reghdfe ret change_scope1 logsize winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe logppe beta winsor_volat winsor_salesgr winsor_epsgr, absorb(date) vce(cluster ticker_encode year)
predict coeff_change_scope1_n, xb
sort date
by date: egen _b_change_scope1_n = mean(coeff_change_scope1_n)
estadd local ym_fe "yes" , replace
estadd local industry_fe "no" , replace

eststo: reghdfe ret change_scope2 logsize winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe logppe beta winsor_volat winsor_salesgr winsor_epsgr, absorb(date) vce(cluster ticker_encode year)
predict coeff_change_scope2_n, xb
sort date
by date: egen _b_change_scope2_n = mean(coeff_change_scope2_n)
estadd local ym_fe "yes" , replace
estadd local industry_fe "no" , replace

eststo: reghdfe ret change_total_emissions logsize winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe logppe beta winsor_volat winsor_salesgr winsor_epsgr, absorb(date) vce(cluster ticker_encode year)
predict coeff_change_total_emissions_n, xb
sort date
by date: egen _b_change_total_emissions_n = mean(coeff_change_total_emissions_n)
estadd local ym_fe "yes" , replace
estadd local industry_fe "no" , replace

eststo: reghdfe ret change_energy_consumption logsize winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe logppe beta winsor_volat winsor_salesgr winsor_epsgr, absorb(date) vce(cluster ticker_encode year)
predict coeff_change_energy_n, xb
sort date
by date: egen _b_change_energy_n = mean(coeff_change_energy_n)
estadd local ym_fe "yes" , replace
estadd local industry_fe "no" , replace

estfe, labels(date "Year/Month FE" industry "Industry FE")

cd "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\regression output\4.1 Carbon Emissions and Stock Returns"

#delimit ;
esttab using "4.1 Carbon Emissions and Stock Returns (change emissions).tex", 
	varlabels(
	change_scope1 "\$\Delta\$ SCOPE1"
	change_scope2 "\$\Delta\$ SCOPE2"
	change_total_emissions "\$\Delta\$ TOTAL"
	change_energy_consumption "\$\Delta\$ ENERGY"
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
	nomtitles
	replace;
#delimit cr

eststo clear


eststo: reghdfe ret scope1_int logsize winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe logppe beta winsor_volat winsor_salesgr winsor_epsgr, absorb(date industry) vce(cluster ticker_encode year)
predict coeff_scope1_int_y, xb
sort date
by date: egen _b_scope1_int_y = mean(coeff_scope1_int_y)
estadd local ym_fe "yes" , replace
estadd local industry_fe "yes" , replace

eststo: reghdfe ret scope2_int logsize winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe logppe beta winsor_volat winsor_salesgr winsor_epsgr, absorb(date industry) vce(cluster ticker_encode year)
predict coeff_scope2_int_y, xb
sort date
by date: egen _b_scope2_int_y = mean(coeff_scope2_int_y)
estadd local ym_fe "yes" , replace
estadd local industry_fe "yes" , replace

eststo: reghdfe ret total_emissions_int logsize winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe logppe beta winsor_volat winsor_salesgr winsor_epsgr, absorb(date industry) vce(cluster ticker_encode year)
predict coeff_total_emissions_int_y, xb
sort date
by date: egen _b_total_emissions_int_y = mean(coeff_total_emissions_int_y)
estadd local ym_fe "yes" , replace
estadd local industry_fe "yes" , replace

eststo: reghdfe ret energy_consumption_int logsize winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe logppe beta winsor_volat winsor_salesgr winsor_epsgr, absorb(date industry) vce(cluster ticker_encode year)
predict coeff_energy_consumption_int_y, xb
sort date
by date: egen _b_energy_consumption_int_y = mean(coeff_energy_consumption_int_y)
estadd local ym_fe "yes" , replace
estadd local industry_fe "yes" , replace


eststo: reghdfe ret scope1_int logsize winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe logppe beta winsor_volat winsor_salesgr winsor_epsgr, absorb(date) vce(cluster ticker_encode year)
predict coeff_scope1_int_n, xb
sort date
by date: egen _b_scope1_int_n = mean(coeff_scope1_int_n)
estadd local ym_fe "yes" , replace
estadd local industry_fe "no" , replace

eststo: reghdfe ret scope2_int logsize winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe logppe beta winsor_volat winsor_salesgr winsor_epsgr, absorb(date) vce(cluster ticker_encode year)
predict coeff_scope2_int_n, xb
sort date
by date: egen _b_scope2_int_n = mean(coeff_scope2_int_n)
estadd local ym_fe "yes" , replace
estadd local industry_fe "no" , replace

eststo: reghdfe ret total_emissions_int logsize winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe logppe beta winsor_volat winsor_salesgr winsor_epsgr, absorb(date) vce(cluster ticker_encode year)
predict coeff_total_emissions_int_n, xb
sort date
by date: egen _b_total_emissions_int_n = mean(coeff_total_emissions_int_n)
estadd local ym_fe "yes" , replace
estadd local industry_fe "no" , replace

eststo: reghdfe ret energy_consumption_int logsize winsor_bm winsor_leverage winsor_mom winsor_investa winsor_roe logppe beta winsor_volat winsor_salesgr winsor_epsgr, absorb(date) vce(cluster ticker_encode year)
estadd local ym_fe "yes" , replace
estadd local industry_fe "no" , replace

estfe, labels(date "Year/Month FE" industry "Industry FE")

cd "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\regression output\4.1 Carbon Emissions and Stock Returns"

#delimit ;
esttab using "4.1 Carbon Emissions and Stock Returns (emissions int).tex", 
	varlabels(
	scope1_int "SCOPE1 INT"
	scope2_int "SCOPE2 INT"
	total_emissions_int "TOTAL INT"
	energy_consumption_int "ENERGY INT"
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
	nomtitles
	replace;
#delimit cr

eststo clear


*END
