clear

ssc install winsor
ssc install numdate
ssc install asreg

import delimited "https://raw.githubusercontent.com/connorpn/cnolan-thesis/main/output/carbon_beta_log_scope1_vars.csv"

winsor ret, gen(winsor_ret) p(0.02)
winsor mktrf, gen(winsor_mktrf) p(0.02)
winsor smb, gen(winsor_smb) p(0.02)
winsor hml, gen(winsor_hml) p(0.02)
winsor wml, gen(winsor_wml) p(0.02)
winsor pmc, gen(winsor_pmc) p(0.02)

label variable ticker "ticker"
sort ticker
encode ticker, gen(ticker_encode)

numdate monthly date = yearmonth, p(YM)

bys ticker_encode: asreg winsor_ret winsor_mktrf winsor_smb winsor_hml winsor_wml winsor_pmc

export delimited using "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\output\carbon_beta_log_scope1.csv", replace




clear

import delimited "https://raw.githubusercontent.com/connorpn/cnolan-thesis/main/output/carbon_beta_log_scope2_vars.csv"

winsor ret, gen(winsor_ret) p(0.02)
winsor mktrf, gen(winsor_mktrf) p(0.02)
winsor smb, gen(winsor_smb) p(0.02)
winsor hml, gen(winsor_hml) p(0.02)
winsor wml, gen(winsor_wml) p(0.02)
winsor pmc, gen(winsor_pmc) p(0.02)

label variable ticker "ticker"
sort ticker
encode ticker, gen(ticker_encode)

numdate monthly date = yearmonth, p(YM)

bys ticker_encode: asreg winsor_ret winsor_mktrf winsor_smb winsor_hml winsor_wml winsor_pmc

export delimited using "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\output\carbon_beta_log_scope2.csv", replace

clear




import delimited "https://raw.githubusercontent.com/connorpn/cnolan-thesis/main/output/carbon_beta_log_total_emissions_vars.csv"

winsor ret, gen(winsor_ret) p(0.02)
winsor mktrf, gen(winsor_mktrf) p(0.02)
winsor smb, gen(winsor_smb) p(0.02)
winsor hml, gen(winsor_hml) p(0.02)
winsor wml, gen(winsor_wml) p(0.02)
winsor pmc, gen(winsor_pmc) p(0.02)


label variable ticker "ticker"
sort ticker
encode ticker, gen(ticker_encode)


numdate monthly date = yearmonth, p(YM)



bys ticker_encode: asreg winsor_ret winsor_mktrf winsor_smb winsor_hml winsor_wml winsor_pmc


export delimited using "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\output\carbon_beta_log_total_emissions.csv", replace


clear

import delimited "https://raw.githubusercontent.com/connorpn/cnolan-thesis/main/output/carbon_beta_log_energy_consumption_vars.csv"



winsor ret, gen(winsor_ret) p(0.02)
winsor mktrf, gen(winsor_mktrf) p(0.02)
winsor smb, gen(winsor_smb) p(0.02)
winsor hml, gen(winsor_hml) p(0.02)
winsor wml, gen(winsor_wml) p(0.02)
winsor pmc, gen(winsor_pmc) p(0.02)


label variable ticker "ticker"
sort ticker
encode ticker, gen(ticker_encode)


numdate monthly date = yearmonth, p(YM)



bys ticker_encode: asreg winsor_ret winsor_mktrf winsor_smb winsor_hml winsor_wml winsor_pmc


export delimited using "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\output\carbon_beta_log_energy_consumption.csv", replace

clear

import delimited "https://raw.githubusercontent.com/connorpn/cnolan-thesis/main/output/carbon_beta_change_scope1_vars.csv"



winsor ret, gen(winsor_ret) p(0.02)
winsor mktrf, gen(winsor_mktrf) p(0.02)
winsor smb, gen(winsor_smb) p(0.02)
winsor hml, gen(winsor_hml) p(0.02)
winsor wml, gen(winsor_wml) p(0.02)
winsor pmc, gen(winsor_pmc) p(0.02)


label variable ticker "ticker"
sort ticker
encode ticker, gen(ticker_encode)


numdate monthly date = yearmonth, p(YM)



bys ticker_encode: asreg winsor_ret winsor_mktrf winsor_smb winsor_hml winsor_wml winsor_pmc


export delimited using "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\output\carbon_beta_change_scope1.csv", replace


clear

import delimited "https://raw.githubusercontent.com/connorpn/cnolan-thesis/main/output/carbon_beta_change_scope2_vars.csv"



winsor ret, gen(winsor_ret) p(0.02)
winsor mktrf, gen(winsor_mktrf) p(0.02)
winsor smb, gen(winsor_smb) p(0.02)
winsor hml, gen(winsor_hml) p(0.02)
winsor wml, gen(winsor_wml) p(0.02)
winsor pmc, gen(winsor_pmc) p(0.02)


label variable ticker "ticker"
sort ticker
encode ticker, gen(ticker_encode)


numdate monthly date = yearmonth, p(YM)



bys ticker_encode: asreg winsor_ret winsor_mktrf winsor_smb winsor_hml winsor_wml winsor_pmc


export delimited using "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\output\carbon_beta_change_scope2.csv", replace


clear

import delimited "https://raw.githubusercontent.com/connorpn/cnolan-thesis/main/output/carbon_beta_change_total_emissions_vars.csv"



winsor ret, gen(winsor_ret) p(0.02)
winsor mktrf, gen(winsor_mktrf) p(0.02)
winsor smb, gen(winsor_smb) p(0.02)
winsor hml, gen(winsor_hml) p(0.02)
winsor wml, gen(winsor_wml) p(0.02)
winsor pmc, gen(winsor_pmc) p(0.02)


label variable ticker "ticker"
sort ticker
encode ticker, gen(ticker_encode)


numdate monthly date = yearmonth, p(YM)



bys ticker_encode: asreg winsor_ret winsor_mktrf winsor_smb winsor_hml winsor_wml winsor_pmc


export delimited using "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\output\carbon_beta_change_total_emissions.csv", replace


clear

import delimited "https://raw.githubusercontent.com/connorpn/cnolan-thesis/main/output/carbon_beta_change_energy_consumption_vars.csv"



winsor ret, gen(winsor_ret) p(0.02)
winsor mktrf, gen(winsor_mktrf) p(0.02)
winsor smb, gen(winsor_smb) p(0.02)
winsor hml, gen(winsor_hml) p(0.02)
winsor wml, gen(winsor_wml) p(0.02)
winsor pmc, gen(winsor_pmc) p(0.02)


label variable ticker "ticker"
sort ticker
encode ticker, gen(ticker_encode)


numdate monthly date = yearmonth, p(YM)



bys ticker_encode: asreg winsor_ret winsor_mktrf winsor_smb winsor_hml winsor_wml winsor_pmc


export delimited using "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\output\carbon_beta_change_energy_consumption.csv", replace

clear

import delimited "https://raw.githubusercontent.com/connorpn/cnolan-thesis/main/output/carbon_beta_scope1_int_vars.csv"



winsor ret, gen(winsor_ret) p(0.02)
winsor mktrf, gen(winsor_mktrf) p(0.02)
winsor smb, gen(winsor_smb) p(0.02)
winsor hml, gen(winsor_hml) p(0.02)
winsor wml, gen(winsor_wml) p(0.02)
winsor pmc, gen(winsor_pmc) p(0.02)


label variable ticker "ticker"
sort ticker
encode ticker, gen(ticker_encode)


numdate monthly date = yearmonth, p(YM)



bys ticker_encode: asreg winsor_ret winsor_mktrf winsor_smb winsor_hml winsor_wml winsor_pmc


export delimited using "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\output\carbon_beta_scope1_int.csv", replace


clear

import delimited "https://raw.githubusercontent.com/connorpn/cnolan-thesis/main/output/carbon_beta_scope2_int_vars.csv"



winsor ret, gen(winsor_ret) p(0.02)
winsor mktrf, gen(winsor_mktrf) p(0.02)
winsor smb, gen(winsor_smb) p(0.02)
winsor hml, gen(winsor_hml) p(0.02)
winsor wml, gen(winsor_wml) p(0.02)
winsor pmc, gen(winsor_pmc) p(0.02)


label variable ticker "ticker"
sort ticker
encode ticker, gen(ticker_encode)


numdate monthly date = yearmonth, p(YM)



bys ticker_encode: asreg winsor_ret winsor_mktrf winsor_smb winsor_hml winsor_wml winsor_pmc


export delimited using "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\output\carbon_beta_scope2_int.csv", replace


clear

import delimited "https://raw.githubusercontent.com/connorpn/cnolan-thesis/main/output/carbon_beta_total_emissions_int_vars.csv"



winsor ret, gen(winsor_ret) p(0.02)
winsor mktrf, gen(winsor_mktrf) p(0.02)
winsor smb, gen(winsor_smb) p(0.02)
winsor hml, gen(winsor_hml) p(0.02)
winsor wml, gen(winsor_wml) p(0.02)
winsor pmc, gen(winsor_pmc) p(0.02)


label variable ticker "ticker"
sort ticker
encode ticker, gen(ticker_encode)


numdate monthly date = yearmonth, p(YM)



bys ticker_encode: asreg winsor_ret winsor_mktrf winsor_smb winsor_hml winsor_wml winsor_pmc


export delimited using "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\output\carbon_beta_total_emissions_int.csv", replace


clear

import delimited "https://raw.githubusercontent.com/connorpn/cnolan-thesis/main/output/carbon_beta_energy_consumption_int_vars.csv"



winsor ret, gen(winsor_ret) p(0.02)
winsor mktrf, gen(winsor_mktrf) p(0.02)
winsor smb, gen(winsor_smb) p(0.02)
winsor hml, gen(winsor_hml) p(0.02)
winsor wml, gen(winsor_wml) p(0.02)
winsor pmc, gen(winsor_pmc) p(0.02)


label variable ticker "ticker"
sort ticker
encode ticker, gen(ticker_encode)


numdate monthly date = yearmonth, p(YM)



bys ticker_encode: asreg winsor_ret winsor_mktrf winsor_smb winsor_hml winsor_wml winsor_pmc


export delimited using "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\output\carbon_beta_energy_consumption_int.csv", replace

save "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\notebooks and stata do files\7.1 Estimate Carbon Betas (Regression).do", replace