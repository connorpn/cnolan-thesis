clear

ssc install numdate
ssc install winsor
ssc install ftools
ssc install reghdfe
ssc install estout


import delimited "https://raw.githubusercontent.com/connorpn/cnolan-thesis/main/output/log_scope1_carbon_beta_firm_characteristics.csv"

label variable ticker "ticker"
sort ticker
encode ticker, gen(ticker_encode)

numdate monthly date = yearmonth, p(YM)

destring log_scope2, replace force

*REGRESSIONS 

eststo clear

EST