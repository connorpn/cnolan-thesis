clear

import delimited "https://raw.githubusercontent.com/connorpn/cnolan-thesis/main/output/log_scope1_carbon_beta_firm_characteristics.csv"

label variable ticker "ticker"
sort ticker
encode ticker, gen(ticker_encode)

ssc install numdate
numdate monthly date = yearmonth, p(YM)


ssc install estout, replace

