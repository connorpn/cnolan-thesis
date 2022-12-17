/*
ssc install numdate
*/

clear 
eststo clear

*import data
import delimited "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\regression\regression variables\br_carbon_premium_risk_factors.csv"

*datetime
numdate monthly date = yearmonth, p(YM)

*filter date
drop if date < tm(2008m7)
drop if date > tm(2021m6)

*set date to lag on
tsset date, monthly

eststo: newey log_scope1, lag(12) force
eststo: newey log_scope1 rmrf rmrf smb hml rmw cma wml, lag(12) force
*estadd local industry_fe "no" , replace

eststo: newey log_scope2, lag(12) force
eststo: newey log_scope2 rmrf smb hml rmw cma wml, lag(12) force
*estadd local industry_fe "no" , replace

eststo: newey log_total_emissions, lag(12) force
eststo: newey log_total_emissions rmrf smb hml rmw cma wml, lag(12) force
#estadd local industry_fe "no" , replace

eststo: newey log_energy_consumption, lag(12) force
eststo: newey log_energy_consumption rmrf smb hml rmw cma wml, lag(12) force
*estadd local industry_fe "no" , replace

*estfe, labels(industry "Industry FE")

*export regression table
cd "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\regression\regression outputs\bolton replications"

#delimit ;
esttab using "br_carbon_premium_and_risk_factors_log.tex", 
	label se star(* 0.10 ** 0.05 *** 0.01)
	s(N r2,
	label("Observations" "R2"))
	title("Carbon Premium and Traditional Risk Factors: LOG EMISSIONS")
	varlabels(
	smb "SMB"
	hml "HML"
	rmw "RMW"
	cma "CMA"
	wml "WML"
	)
	order(rmrf smb hml rmw cma wml _cons)
	mtitles("LN S1" "LN S1" "LN S2" "LN S2" "LN TOT" "LN TOT" "LN ENG" "LN ENG")
	mgroups("Carbon Return Premium (Monthly)", pattern(0 0 0 0 0 0 0 0) ///
prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}))
	replace;
#delimit cr



/*
*regression change emission

eststo clear

eststo: newey change_scope1, lag(12) force
eststo: newey change_scope1 rmrf smb hml rmw cma wml, lag(12) force
*estadd local industry_fe "no" , replace

eststo: newey change_scope2, lag(12) force
eststo: newey change_scope2 rmrf smb hml rmw cma wml, lag(12) force
*estadd local industry_fe "no" , replace

eststo: newey change_total_emissions, lag(12) force
eststo: newey change_total_emissions rmrf smb hml rmw cma wml, lag(12) force
#estadd local industry_fe "no" , replace

eststo: newey change_energy_consumption, lag(12) force
eststo: newey change_energy_consumption rmrf smb hml rmw cma wml, lag(12) force
*estadd local industry_fe "no" , replace

*estfe, labels(industry "Industry FE")

*export regression table
cd "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\regression\regression outputs\bolton replications"

#delimit ;
esttab using "br_carbon_premium_and_risk_factors_change.tex", 
	label se star(* 0.10 ** 0.05 *** 0.01)
	s(N r2,
	label("Observations" "R2"))
	title("Carbon Premium and Traditional Risk Factors: CHANGE EMISSIONS")
	varlabels(
	smb "SMB"
	hml "HML"
	rmw "RMW"
	cma "CMA"
	wml "WML"
	)
	order(rmrf smb hml rmw cma wml _cons)
	mtitles("\$\Delta\$ S1" "\$\Delta\$ S1" "\$\Delta\$ S2" "\$\Delta\$ S2" "\$\Delta\$ TOT" "\$\Delta\$ TOT" "\$\Delta\$ ENG" "\$\Delta\$ ENG" )
	mgroups("Carbon Return Premium (Monthly)", pattern(0 0 0 0 0 0 0 0) ///
prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}))
	replace;
#delimit cr
*/


*regression emission int

eststo clear

eststo: newey scope1_int, lag(12) force
eststo: newey scope1_int rmrf smb hml rmw cma wml, lag(12) force
estadd local industry_fe "no" , replace


eststo: newey scope2_int, lag(12) force
eststo: newey scope2_int rmrf smb hml rmw cma wml, lag(12) force
estadd local industry_fe "no" , replace

eststo: newey total_emissions_int, lag(12) force
eststo: newey total_emissions_int rmrf smb hml rmw cma wml, lag(12) force
#estadd local industry_fe "no" , replace

eststo: newey energy_consumption_int, lag(12) force
eststo: newey energy_consumption_int rmrf smb hml rmw cma wml, lag(12) force
*estadd local industry_fe "no" , replace

*estfe, labels(industry "Industry FE")


*export regression table
cd "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\regression\regression outputs\bolton replications"

#delimit ;
esttab using "br_carbon_premium_and_risk_factors_int.tex", 
	label se star(* 0.10 ** 0.05 *** 0.01)
	s(N r2,
	label("Observations" "R2"))
	title("Carbon Premium and Traditional Risk Factors: EMISSIONS INT")
	varlabels(
	rmrf "RMRF"
	smb "SMB"
	hml "HML"
	rmw "RMW"
	cma "CMA"
	wml "WML"
	)
	order(rmrf smb hml rmw cma wml _cons)
	mtitles("S1 INT" "S1 INT" "S2 INT" "S2 INT" "TOT INT" "TOT INT" "ENG INT" "ENG INT")
	mgroups("Carbon Return Premium (Monthly)", pattern(0 0 0 0 0 0 0 0) ///
prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}))
	replace;
#delimit cr

