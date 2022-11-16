clear

import delimited "https://raw.githubusercontent.com/connorpn/cnolan-thesis/main/output/emissions_determinants_vars.csv"


label variable ticker "ticker"
sort ticker
encode ticker, gen(ticker_encode)

ssc install numdate
numdate yearly date = year, p(Y)



save regression - determinants of carbon emissions.do, replace