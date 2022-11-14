clear

import delimited "https://raw.githubusercontent.com/connorpn/cnolan-thesis/main/output/carbon_beta_log_scope1_vars.csv"

ssc install winsor

winsor ret, gen(winsor_ret) p(0.02)
winsor mktrf, gen(winsor_mktrf) p(0.02)
winsor smb, gen(winsor_smb) p(0.02)
winsor hml, gen(winsor_hml) p(0.02)
winsor wml, gen(winsor_wml) p(0.02)
winsor pmc, gen(winsor_pmc) p(0.02)


label variable ticker "ticker"
sort ticker
encode ticker, gen(ticker_encode)

ssc install numdate
numdate monthly date = yearmonth, p(YM)


ssc install asreg
bys ticker_encode: asreg winsor_ret winsor_mktrf winsor_smb winsor_hml winsor_wml winsor_pmc


export delimited using "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\output\carbon_beta_log_scope1.csv", replace