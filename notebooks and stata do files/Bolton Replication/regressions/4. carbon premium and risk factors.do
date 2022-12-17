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

*regress log emissions

eststo clear
qui regress log_scope1
local r2_a = e(r2_a)
eststo: newey log_scope1, lag(12) force
estadd local industry_fe "no" , replace
estadd scalar r2_a = `r2_a'

qui regress log_scope1 rmrf smb hml rmw cma wml
local r2_a = e(r2_a)
eststo: newey log_scope1 rmrf smb hml rmw cma wml, lag(12) force
estadd local industry_fe "no" , replace
estadd scalar r2_a = `r2_a'


qui regress log_scope2
local r2_a = e(r2_a)
eststo: newey log_scope2, lag(12) force
estadd local industry_fe "no" , replace
estadd scalar r2_a = `r2_a'

qui regress log_scope2 rmrf smb hml rmw cma wml
local r2_a = e(r2_a)
eststo: newey log_scope2 rmrf smb hml rmw cma wml, lag(12) force
estadd local industry_fe "no" , replace
estadd scalar r2_a = `r2_a'

qui regress log_total_emissions
local r2_a = e(r2_a)
eststo: newey log_total_emissions, lag(12) force
estadd local industry_fe "no" , replace
estadd scalar r2_a = `r2_a'

qui regress log_total_emissions rmrf smb hml rmw cma wml
local r2_a = e(r2_a)
eststo: newey log_total_emissions rmrf smb hml rmw cma wml, lag(12) force
estadd local industry_fe "no" , replace
estadd scalar r2_a = `r2_a'

qui regress log_energy_consumption
local r2_a = e(r2_a)
eststo: newey log_energy_consumption, lag(12) force
estadd local industry_fe "no" , replace
estadd scalar r2_a = `r2_a'

qui regress log_energy_consumption rmrf smb hml rmw cma wml
local r2_a = e(r2_a)
eststo: newey log_energy_consumption rmrf smb hml rmw cma wml, lag(12) force
estadd local industry_fe "no" , replace
estadd scalar r2_a = `r2_a'

*estfe, labels(industry "Industry FE")

*export regression table
cd "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\regression\regression outputs\bolton replications"

#delimit ;
esttab using "br_carbon_premium_and_risk_factors_log.tex", 
	label se star(* 0.10 ** 0.05 *** 0.01)
	s(industry_fe N r2_a,
	label("Industry adj." "Observations" "Adj, R2"))
	varlabels(
	rmrf "RMRF"
	smb "SMB"
	hml "HML"
	rmw "RMW"
	cma "CMA"
	wml "WML"
	_cons Constant
	)
	order(rmrf smb hml rmw cma wml _cons)
	mtitles("LN S1" "LN S1" "LN S2" "LN S2" "LN TOT" "LN TOT" "LN ENG" "LN ENG")
	mgroups("Monthly Carbon Premium", pattern(1 0 0 0 0 0 0 0) ///
prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}))
	replace;
#delimit cr



*regress change emissions

eststo clear
qui regress change_scope1
local r2_a = e(r2_a)
eststo: newey change_scope1, lag(12) force
estadd local industry_fe "no" , replace
estadd scalar r2_a = `r2_a'

qui regress change_scope1 rmrf smb hml rmw cma wml
local r2_a = e(r2_a)
eststo: newey change_scope1 rmrf smb hml rmw cma wml, lag(12) force
estadd local industry_fe "no" , replace
estadd scalar r2_a = `r2_a'


qui regress change_scope2
local r2_a = e(r2_a)
eststo: newey change_scope2, lag(12) force
estadd local industry_fe "no" , replace
estadd scalar r2_a = `r2_a'

qui regress change_scope2 rmrf smb hml rmw cma wml
local r2_a = e(r2_a)
eststo: newey change_scope2 rmrf smb hml rmw cma wml, lag(12) force
estadd local industry_fe "no" , replace
estadd scalar r2_a = `r2_a'

qui regress change_total_emissions
local r2_a = e(r2_a)
eststo: newey change_total_emissions, lag(12) force
estadd local industry_fe "no" , replace
estadd scalar r2_a = `r2_a'

qui regress change_total_emissions rmrf smb hml rmw cma wml
local r2_a = e(r2_a)
eststo: newey change_total_emissions rmrf smb hml rmw cma wml, lag(12) force
estadd local industry_fe "no" , replace
estadd scalar r2_a = `r2_a'

qui regress change_energy_consumption
local r2_a = e(r2_a)
eststo: newey change_energy_consumption, lag(12) force
estadd local industry_fe "no" , replace
estadd scalar r2_a = `r2_a'

qui regress change_energy_consumption rmrf smb hml rmw cma wml
local r2_a = e(r2_a)
eststo: newey change_energy_consumption rmrf smb hml rmw cma wml, lag(12) force
estadd local industry_fe "no" , replace
estadd scalar r2_a = `r2_a'

*estfe, labels(industry "Industry FE")

*export regression table
cd "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\regression\regression outputs\bolton replications"

#delimit ;
esttab using "br_carbon_premium_and_risk_factors_change.tex", 
	label se star(* 0.10 ** 0.05 *** 0.01)
	s(industry_fe N r2_a,
	label("Industry adj." "Observations" "Adj, R2"))
	varlabels(
	rmrf "RMRF"
	smb "SMB"
	hml "HML"
	rmw "RMW"
	cma "CMA"
	wml "WML"
	_cons Constant
	)
	order(rmrf smb hml rmw cma wml _cons)
	mtitles("\$\Delta\$ S1" "\$\Delta\$ S1" "\$\Delta\$ S2" "\$\Delta\$ S2" "\$\Delta\$ TOT" "\$\Delta\$ TOT" "\$\Delta\$ ENG" "\$\Delta\$ ENG" )
	mgroups("Monthly Carbon Premium", pattern(1 0 0 0 0 0 0 0) ///
prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}))
	replace;
#delimit cr





*regress emissions int

eststo clear
qui regress scope1_int
local r2_a = e(r2_a)
eststo: newey scope1_int, lag(12) force
estadd local industry_fe "no" , replace
estadd scalar r2_a = `r2_a'

qui regress scope1_int rmrf smb hml rmw cma wml
local r2_a = e(r2_a)
eststo: newey scope1_int rmrf smb hml rmw cma wml, lag(12) force
estadd local industry_fe "no" , replace
estadd scalar r2_a = `r2_a'


qui regress scope2_int
local r2_a = e(r2_a)
eststo: newey scope2_int, lag(12) force
estadd local industry_fe "no" , replace
estadd scalar r2_a = `r2_a'

qui regress change_scope2 rmrf smb hml rmw cma wml
local r2_a = e(r2_a)
eststo: newey change_scope2 rmrf smb hml rmw cma wml, lag(12) force
estadd local industry_fe "no" , replace
estadd scalar r2_a = `r2_a'

qui regress change_total_emissions
local r2_a = e(r2_a)
eststo: newey change_total_emissions, lag(12) force
estadd local industry_fe "no" , replace
estadd scalar r2_a = `r2_a'

qui regress change_total_emissions rmrf smb hml rmw cma wml
local r2_a = e(r2_a)
eststo: newey change_total_emissions rmrf smb hml rmw cma wml, lag(12) force
estadd local industry_fe "no" , replace
estadd scalar r2_a = `r2_a'

qui regress change_energy_consumption
local r2_a = e(r2_a)
eststo: newey change_energy_consumption, lag(12) force
estadd local industry_fe "no" , replace
estadd scalar r2_a = `r2_a'

qui regress change_energy_consumption rmrf smb hml rmw cma wml
local r2_a = e(r2_a)
eststo: newey change_energy_consumption rmrf smb hml rmw cma wml, lag(12) force
estadd local industry_fe "no" , replace
estadd scalar r2_a = `r2_a'

*estfe, labels(industry "Industry FE")

*export regression table
cd "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\regression\regression outputs\bolton replications"

#delimit ;
esttab using "br_carbon_premium_and_risk_factors_int.tex", 
	label se star(* 0.10 ** 0.05 *** 0.01)
	s(industry_fe N r2_a,
	label("Industry adj." "Observations" "Adj, R2"))
	varlabels(
	rmrf "RMRF"
	smb "SMB"
	hml "HML"
	rmw "RMW"
	cma "CMA"
	wml "WML"
	_cons Constant
	)
	order(rmrf smb hml rmw cma wml _cons)
	mtitles("S1 INT" "S1 INT" "S2 INT" "S2 INT" "TOT INT" "TOT INT" "ENG INT" "ENG INT")
	mgroups("Monthly Carbon Premium", pattern(1 0 0 0 0 0 0 0) ///
prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}))
	replace;
#delimit cr