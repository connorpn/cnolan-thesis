clear
eststo clear
ssc install logout

import delimited "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\summary stats\summ_stats.csv"


destring log_scope2, replace force
destring change_scope2, replace force

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

drop scope1_int scope2_int total_emissions_int energy_consumption

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

cd "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\summary stats"

logout, save("cb_summarize.tex") tex replace: tabstat log_scope1 log_scope2 log_total_emissions log_energy_consumption change_scope1 change_scope2 change_total_emissions change_energy_consumption scope1_int scope2_int total_emissions_int energy_consumption_int ret carbon_beta logsize bm leverage mom investa roe logppe beta volat salesgr epsgr, c(stat) stat(n mean sd min max p1 p5 p10 p25 p50 p75 p90 p95 p99 skewness kurtosis)

/*
foreach var of varlist _all {
	label var `var' `var'
}

estpost tabstat log_scope1 log_scope2 log_total_emissions log_energy_consumption change_scope1 change_scope2 change_total_emissions change_energy_consumption scope1_int scope2_int total_emissions_int energy_consumption_int ret carbon_beta logsize bm leverage mom investa roe logppe beta volat salesgr epsgr, c(stat) stat(sum mean sd min max n)

*stat(n mean sd min max p1 p5 p10 p25 p50 p75 p90 p95 p99 skewness kurtosis)

esttab using "cb_summarize.tex", replace ////
cells("sum mean sd min max n")

*collabels("Sum" "Mean" "SD" "Min" "Max" "N")


esttab using "cb_summarize.tex", replace ////
 cells("n sum(fmt(%6.0fc)) mean(fmt(%6.2fc)) sd(fmt(%6.2fc)) min max p1 p5 p10 p25 p50 p75 p90 p95 p99 skewness kurtosis")   nonumber ///
  nomtitle nonote noobs label booktabs ///
  collabels("N" "Sum" "Mean" "SD" "Min" "Max" "p1" "p5" "p10" "p25" "p50" "p75" "p90" "p95" "p99" "skewness" "kurtosis")  ///
  title("Summary Statistics \label{summarystats}")

  
esttab using "cb_summarize.tex", replace ////
cells("n sum(fmt(%6.0fc)) mean(fmt(%6.2fc)) sd(fmt(%6.2fc)) min max p1 p5 p10 p25 p50 p75 p90 p95 p99 skewness kurtosis")   nonumber ///
nomtitle nonote noobs nolabel

  */