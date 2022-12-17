/*
ssc install winsor
ssc install numdate
ssc install asreg
*/

clear

*import data
import delimited "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\regression\regression variables\cb_asx_500_carbon_beta_vars.csv"

*encode ticker
label variable ticker "ticker"
sort ticker
encode ticker, gen(ticker_encode)

*datetime
numdate monthly date = yearmonth, p(YM)


*winsorize
winsor ret, gen(winsor_ret) p(0.02)
winsor rmrf, gen(winsor_rmrf) p(0.02)
winsor smb, gen(winsor_smb) p(0.02)
winsor hml, gen(winsor_hml) p(0.02)
winsor rmw, gen(winsor_rmw) p(0.02)
winsor cma, gen(winsor_cma) p(0.02)
winsor wml, gen(winsor_wml) p(0.02)
winsor pmc, gen(winsor_pmc) p(0.02)


*regression to estimate carbon beta
bys ticker_encode: asreg winsor_ret winsor_rmrf winsor_smb winsor_hml winsor_rmw winsor_cma winsor_wml winsor_pmc, wind (date 36) fitted


/*
*regression to estimate carbon beta
bys ticker_encode: asreg ret rmrf smb hml rmw cma wml pmc, wind (date 36) fitted
*/

*export estimated carbon beta
cd "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\regression\regression outputs\carbon beta"
export delimited using "cb_asx500_carbon_beta_regression_output.csv", replace


clear

**
** estimate beta for nger firms 
**
*import data
import delimited "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\regression\regression variables\cb_carbon_beta_vars.csv"

*encode ticker
label variable ticker "ticker"
sort ticker
encode ticker, gen(ticker_encode)

*datetime
numdate monthly date = yearmonth, p(YM)


*winsorize
winsor ret, gen(winsor_ret) p(0.02)
winsor rmrf, gen(winsor_rmrf) p(0.02)
winsor smb, gen(winsor_smb) p(0.02)
winsor hml, gen(winsor_hml) p(0.02)
winsor rmw, gen(winsor_rmw) p(0.02)
winsor cma, gen(winsor_cma) p(0.02)
winsor wml, gen(winsor_wml) p(0.02)
winsor pmc, gen(winsor_pmc) p(0.02)


*regression to estimate carbon beta
bys ticker_encode: asreg winsor_ret winsor_rmrf winsor_smb winsor_hml winsor_rmw winsor_cma winsor_wml winsor_pmc, wind (date 36) fitted

*export estimated carbon beta
export delimited using "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\regression\regression outputs\carbon beta\carbon_beta_regression_output.csv", replace


*END
*END

display "RUN PY - 2. CONSTRUCT FIRM CHARACTERISTICS AND PRICING RISK"