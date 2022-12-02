
/*
ssc install numdate
ssc install winsor
ssc install ftools
ssc install estout
ssc install erepost
*/


clear
eststo clear

import delimited "https://raw.githubusercontent.com/connorpn/cnolan-thesis/main/output/carbon_premium_risk_factors_vars.csv"
numdate monthly date = yearmonth, p(YM)
tsset date





eststo: newey _b_log_scope1, lag(12) force
eststo: newey _b_log_scope1 mktrf hml smb cma mom bab, lag(12) force

eststo: newey _b_log_scope2, lag(12) force
eststo: newey _b_log_scope2 mktrf hml smb cma mom bab, lag(12) force

eststo: newey _b_log_total_emissions, lag(12) force
eststo: newey _b_log_total_emissions mktrf hml smb cma mom bab, lag(12) force

eststo: newey _b_log_energy_consumption, lag(12) force
eststo: newey _b_log_energy_consumption mktrf hml smb cma mom bab, lag(12) force



cd "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\regression output\5.2 Carbon Premium and Traditional Risk Factors"

#delimit ;
esttab  using "log_emissions.tex", 
	label se star(* 0.10 ** 0.05 *** 0.01)
	s(N r2_a,
	label("Observations" "R2-Adj"))
	title(Carbon Premium and Risk Factors: log emissions)
	nomtitles
	mgroups("LN S1" "LN S2" "LN TOTAL" "LN ENERGY",
	pattern(1 0 1 0 1 0 1 0) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}))
	replace;
#delimit cr

eststo clear


eststo: newey _b_change_scope1, lag(12) force
eststo: newey _b_change_scope1 mktrf hml smb cma mom bab, lag(12) force

eststo: newey _b_change_scope2, lag(12) force
eststo: newey _b_change_scope2 mktrf hml smb cma mom bab, lag(12) force

eststo: newey _b_change_total_emissions, lag(12) force
eststo: newey _b_change_total_emissions mktrf hml smb cma mom bab, lag(12) force

eststo: newey _b_change_energy_consumption, lag(12) force
eststo: newey _b_change_energy_consumption mktrf hml smb cma mom bab, lag(12) force


cd "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\regression output\5.2 Carbon Premium and Traditional Risk Factors"

#delimit ;
esttab  using "change_emissions.tex", 
	label se star(* 0.10 ** 0.05 *** 0.01)
	s(N r2_a,
	label("Observations" "R2-Adj"))
	title(Carbon Premium and Risk Factors: log emissions)
	nomtitles
	mgroups("\$\Delta\$ S1" "\$\Delta\$ S2" "\$\Delta\$ TOTAL" "\$\Delta\$ ENERGY",
	pattern(1 0 1 0 1 0 1 0)
	span prefix(\multicolumn{@span}{c}{) suffix(})
	erepeat(\cmidrule(lr){@span}))
	replace;
#delimit cr

eststo clear

eststo: newey _b_scope1_int, lag(12) force
eststo: newey _b_scope1_int mktrf hml smb cma mom bab, lag(12) force

eststo: newey _b_scope2_int, lag(12) force
eststo: newey _b_scope2_int mktrf hml smb cma mom bab, lag(12) force

eststo: newey _b_total_emissions_int, lag(12) force
eststo: newey _b_total_emissions_int mktrf hml smb cma mom bab, lag(12) force

eststo: newey _b_energy_consumption_int, lag(12) force
eststo: newey _b_energy_consumption_int mktrf hml smb cma mom bab, lag(12) force

cd "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\regression output\5.2 Carbon Premium and Traditional Risk Factors"

#delimit ;
esttab  using "emissions_int.tex", 
	label se star(* 0.10 ** 0.05 *** 0.01)
	s(N r2_a,
	label("Observations" "R2-Adj"))
	title(Carbon Premium and Risk Factors: log emissions)
	mgroups("S1 INT" "S2 INT" "TOTAL INT" "ENERGY INT",
	pattern(1 0 1 0 1 0 1 0)
	span prefix(\multicolumn{@span}{c}{) suffix(})
	erepeat(\cmidrule(lr){@span}))
	nomtitles
	replace;
#delimit cr


*END