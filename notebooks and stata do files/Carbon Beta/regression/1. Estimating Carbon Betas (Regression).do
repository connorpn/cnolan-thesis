clear

ssc install winsor
ssc install numdate
ssc install asreg

import delimited "https://raw.githubusercontent.com/connorpn/cnolan-thesis/main/regression/regression%20variables/carbon_beta_vars.csv"

winsor ret, gen(winsor_ret) p(0.02)
winsor rmrf, gen(winsor_rmrf) p(0.02)
winsor smb, gen(winsor_smb) p(0.02)
winsor hml, gen(winsor_hml) p(0.02)
winsor rmw, gen(winsor_rmw) p(0.02)
winsor cma, gen(winsor_cma) p(0.02)
winsor wml, gen(winsor_wml) p(0.02)
winsor pmc, gen(winsor_pmc) p(0.02)

label variable ticker "ticker"
sort ticker
encode ticker, gen(ticker_encode)

numdate monthly date = yearmonth, p(YM)

bys ticker_encode: asreg winsor_ret winsor_rmrf winsor_smb winsor_hml winsor_rmw winsor_cma winsor_wml winsor_pmc

export delimited using "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\regression\regression outputs\carbon_beta_regression_output.csv", replace


*END