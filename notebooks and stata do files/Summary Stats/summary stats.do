/*
ssc install estout
ssc install winsor
*/

clear
eststo clear


  
**************************		
* Descriptive Statistics *
**************************



**************************		
* BOLTON REPLICATION
**************************
/*
*import data
import delimited "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\summary stats\br_summary_stats.csv"

*winsorization

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

drop bm leverage mom investa roe volat salesgr epsgr
rename winsor_bm bm
rename winsor_leverage leverage
rename winsor_mom mom
rename winsor_investa investa
rename winsor_roe roe
rename winsor_volat volat
rename winsor_salesgr salesgr
rename winsor_epsgr epsgr


eststo br_vars: estpost summ log_scope1 log_scope2 log_total_emissions log_energy_consumption change_scope1 change_scope2 change_total_emissions change_energy_consumption scope1_int scope2_int total_emissions_int energy_consumption_int ret logsize bm leverage mom investa roe logppe beta volat salesgr epsgr rmrf smb hml rmw cma wml, detail


cd "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\summary stats"

#delimit ;
esttab br_vars using "summ_stats_bolton.tex",
cells("count mean(fmt(2)) sd(fmt(2))  p1(fmt(2)) p5(fmt(2)) p25(fmt(2)) p50(fmt(2)) p75(fmt(2)) p95(fmt(2)) p99(fmt(2))")
nonumber nomtitle nonote noobs label booktabs
collabels("N" "Mean" "SD"  "1" "5" "25" "Median" "75" "95" "99")
refcat(log_scope1 "\newline{\textbf{Emissions Variables}}" ret "\newline{\textbf{Cross-sectional Variables}}" rmrf "\newline{\textbf{Time-series Variables}}", nolabel)
coefl(
log_scope1 "Log (Scope 1 Carbon Emissions)"
log_scope2 "Log (Scope 2 Carbon Emissions)"
log_total_emissions "Log (Total Carbon Emissions)"
log_energy_consumption "Log (Energy Consumption)"
change_scope1 "Change in Scope 1 Emissions"
change_scope2 "Change in Scope 2 Emissions"
change_total_emissions "Change in Total Emissions"
change_energy_consumption "Change in Energy Consumption"
scope1_int "Intensity of Scope 1 Emissions"
scope2_int "Intensity of Scope 2 Emission"
total_emissions_int "Intensity of Total Emission"
energy_consumption_int "Intensity of Energy Consumption"
ret "RET - Monthly Returns"
logsize "LOGSIZE"
bm "BM"
leverage "LEVERAGE"
mom "MOM"
investa "INVEST/A"
roe "ROE"
logppe "LOGPPE"
beta "BETA"
volat "VOLAT"
salesgr "SALESGR"
epsgr "EPSGR"
rmrf "MKTRF"
smb "SMB"
hml "HML"
rmw "RMW"
cma "CMA"
wml "WML"
)
replace ;
#delimit cr
*/


**************************		
* CARBON BETA
**************************
/*
clear
eststo clear

*import data
import delimited "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\summary stats\pricing_carbon_risk_out.csv"


*winsorization

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

*summary stats
eststo cb_vars: estpost summ ret carbon_beta ln_marketcap bm roe leverage investa logppe ppea beta mom, detail

*export to latex
cd "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\summary stats"

#delimit ;
esttab cb_vars using "summ_stats_carbon_beta.tex",
cells("count mean(fmt(2)) sd(fmt(2))  p1(fmt(2)) p5(fmt(2)) p25(fmt(2)) p50(fmt(2)) p75(fmt(2)) p95(fmt(2)) p99(fmt(2))")
nonumber nomtitle nonote noobs label booktabs
collabels("N" "Mean" "SD"  "1" "5" "25" "Median" "75" "95" "99")
coefl(
ret "Monthly Returns"
carbon_beta "Carbon Beta"
ln_marketcap "ln(Market Cap.)"
bm "Book/Market"
roe "Return on Equity"
leverage "Leverage"
investa "Capex/Assets"
logppe "ln(PPE)"
ppea "PPE/Assets"
beta "CAPM Beta"
mom "Momentum"
)
replace ;
#delimit cr
*/

**************************		
* YEARLY FIRMS AND EMISSIONS
**************************

clear
eststo clear

*import data
import delimited "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\summary stats\yearly_stats.csv"

*encode ticker
label variable ticker "ticker"
sort ticker
encode ticker, gen(ticker_encode)

*datetime 
numdate yearly date = year, p(Y)

*filter date
drop if year < 2008
drop if year > 2021

*winsorization

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

*summary stats
eststo cb_vars: estpost summ ret carbon_beta ln_marketcap bm roe leverage investa logppe ppea beta mom, detail

*export to latex
cd "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\summary stats"

#delimit ;
esttab cb_vars using "summ_stats_carbon_beta.tex",
cells("count mean(fmt(2)) sd(fmt(2))  p1(fmt(2)) p5(fmt(2)) p25(fmt(2)) p50(fmt(2)) p75(fmt(2)) p95(fmt(2)) p99(fmt(2))")
nonumber nomtitle nonote noobs label booktabs
collabels("N" "Mean" "SD"  "1" "5" "25" "Median" "75" "95" "99")
coefl(
ret "Monthly Returns"
carbon_beta "Carbon Beta"
ln_marketcap "ln(Market Cap.)"
bm "Book/Market"
roe "Return on Equity"
leverage "Leverage"
investa "Capex/Assets"
logppe "ln(PPE)"
ppea "PPE/Assets"
beta "CAPM Beta"
mom "Momentum"
)
replace ;
#delimit cr
*/

