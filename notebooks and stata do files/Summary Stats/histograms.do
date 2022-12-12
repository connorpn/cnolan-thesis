clear
eststo clear

cd "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\regression\regression variables"

import delimited "br_carbon_emissions_and_stock_returns.csv"

destring log_scope2, replace force
destring change_scope2, replace force

histogram log_scope1, percent normal
graph export "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\summary stats\histogram_log_scope1.png", replace as(png) name("Graph")

histogram log_scope2, percent normal
graph export "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\summary stats\histogram_log_scope2.png", replace as(png) name("Graph")

histogram log_total_emissions, percent normal
graph export "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\summary stats\histogram_log_total_emissions.png", replace as(png) name("Graph")

histogram log_energy_consumption, percent normal
graph export "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\summary stats\histogram_log_energy_consumption.png", replace as(png) name("Graph")


histogram change_scope1, percent normal
graph export "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\summary stats\histogram_change_scope1.png", replace as(png) name("Graph")

histogram change_scope2, percent normal
graph export "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\summary stats\histogram_change_scope2.png", replace as(png) name("Graph")

histogram change_total_emissions, percent normal
graph export "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\summary stats\histogram_change_total_emissions.png", replace as(png) name("Graph")

histogram change_energy_consumption, percent normal
graph export "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\summary stats\histogram_change_energy_consumption.png", replace as(png) name("Graph")


histogram scope1_int, percent normal
graph export "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\summary stats\histogram_scope1_int.png", replace as(png) name("Graph")

histogram scope2_int, percent normal
graph export "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\summary stats\histogram_scope2_int.png", replace as(png) name("Graph")

histogram total_emissions_int, percent normal
graph export "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\summary stats\histogram_total_emissions_int.png", replace as(png) name("Graph")

histogram energy_consumption_int, percent normal
graph export "Z:\OneDrive\University Study\Honours Thesis\cnolan-thesis\summary stats\histogram_energy_consumption_int.png", replace as(png) name("Graph")

