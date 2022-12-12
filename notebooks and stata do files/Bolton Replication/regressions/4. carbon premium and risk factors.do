clear 


ssc install numdate


import delimited "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\regression\regression variables\br_carbon_premium_risk_factors.csv"


numdate monthly date = yearmonth, p(YM)

tsset date, monthly

eststo: newey log_scope1, lag(12) force
eststo: newey log_scope1 smb hml rmw cma wml, lag(12) force
estadd local industry_fe "no" , replace

eststo: newey log_scope2, lag(12) force
eststo: newey log_scope2 smb hml rmw cma wml, lag(12) force
estadd local industry_fe "no" , replace

eststo: newey log_total_emissions, lag(12) force
eststo: newey log_total_emissions smb hml rmw cma wml, lag(12) force
estadd local industry_fe "no" , replace

eststo: newey log_energy_consumption, lag(12) force
eststo: newey log_energy_consumption smb hml rmw cma wml, lag(12) force
estadd local industry_fe "no" , replace

estfe, labels(industry "Industry FE")

cd "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\regression\regression outputs\bolton replications"

#delimit ;
esttab using "br_carbon_premium_and_risk_factors.tex", 
	label se star(* 0.10 ** 0.05 *** 0.01)
	s(industry_fe N r2_a,
	label("Industry FE" "Observations" "R2-Adj"))
	title("Carbon Premium and Traditional Risk Factors")
	nomtitles
	nodepvars
	indicate(
	`r(indicate_fe)'
	)
	replace;
#delimit cr