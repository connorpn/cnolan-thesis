clear
eststo clear

import delimited "https://raw.githubusercontent.com/connorpn/cnolan-thesis/main/regression/regression%20variables/pricing_carbon_risk.csv"

/*
label variable ticker "ticker"
sort ticker
encode ticker, gen(ticker_encode)
*/

destring log_scope2, replace force
destring change_scope2, replace force

winsor bm, gen(winsor_bm) p(0.025)
winsor leverage, gen(winsor_leverage) p(0.025)
winsor mom, gen(winsor_mom) p(0.005)
winsor investa, gen(winsor_investa) p(0.025)
winsor roe, gen(winsor_roe) p(0.025)
winsor volat, gen(winsor_volat) p(0.005)
winsor salesgr, gen(winsor_salesgr) p(0.005)
winsor epsgr, gen(winsor_epsgr) p(0.005)


drop bm leverage mom investa roe volat salesgr epsgr
rename ret ret
rename logsize logsize
rename winsor_bm bm
rename winsor_leverage leverage
rename winsor_mom mom
rename winsor_investa investa
rename winsor_roe roe
rename logppe logppe
rename beta beta
rename winsor_volat volat
rename winsor_salesgr salesgr
rename winsor_epsgr epsgr

drop yearmonth ticker industry 

logout, save(cb_summarize.tex) tex replace: tabstat log_scope1 log_scope2 log_total_emissions log_energy_consumption change_scope1 change_scope2 change_total_emissions change_energy_consumption scope1_int scope2_int total_emissions_int energy_consumption_int ret carbon_beta logsize bm leverage mom investa roe logppe beta volat salesgr epsgr, statistics(n mean sd min max p1 p5 p10 p25 p50 p75 p90 p95 p99 skewness kurtosis) columns(statistics)