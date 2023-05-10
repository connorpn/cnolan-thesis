#%%
"IMPORT MODULES"
import os
import pandas as pd
import numpy as np


"SET THE WORKING DIRECTORY BELOW TO THE LOCATION OF DATA FILES"

working_directory = 'C:/Users/conno/OneDrive/University Study/Honours Thesis/cnolan-thesis' #set location using back slashes

os.chdir(working_directory)

print("Current working directory: {0}".format(os.getcwd()))


def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
            output_path = os.makedirs(directory)
            print(output_path)
    except OSError:
        print ('Error: Creating directory. ' +  directory)
        

# Folder where outputs will be saved (by default a folder within the working directory) 
createFolder('./output/') 
output_path = working_directory +'./output/'

print('Set WD: Done')
#%%

'''
BOLTON REPLICATIONS
'''

"IMPORT DATA"

csr = pd.read_csv('C:/Users/conno/OneDrive/University Study/Honours Thesis/cnolan-thesis/regression/regression variables/br_carbon_emissions_and_stock_returns.csv')
famafrench_factors = pd.read_csv ('C:/Users/conno/OneDrive/University Study/Honours Thesis/cnolan-thesis/output/famafrench_factors.csv')
rmrf = pd.read_csv("C:/Users/conno/OneDrive/University Study/Honours Thesis/cnolan-thesis./output/rmrf.csv")


factors = pd.merge(rmrf[['yearmonth','rmrf']], famafrench_factors[['yearmonth','smb', 'hml', 'rmw', 'cma', 'wml']], how='inner', on=['yearmonth'])
factors = factors.loc[(factors['yearmonth'] >= 200807) & (factors['yearmonth'] <= 202106)]
factors = factors[['rmrf', 'smb', 'hml', 'rmw', 'cma', 'wml']]

csr_br = csr
csr_br = csr_br.loc[(csr_br['yearmonth'] >= 200807) & (csr_br['yearmonth'] <= 202106)]
csr_br = csr_br[['ret', 'log_scope1', 'log_scope2', 'log_total_emissions', 'log_energy_consumption', 'change_scope1', 'change_scope2', 'change_total_emissions', 'change_energy_consumption', 'scope1_int', 'scope2_int', 'total_emissions_int', 'energy_consumption_int', 'logsize', 'bm', 'leverage', 'mom', 'investa', 'roe', 'logppe', 'beta', 'volat', 'salesgr', 'epsgr']]

br_summary_stats = pd.concat([csr_br, factors], axis="columns").reset_index(drop=True)

"Save br_summary_stats"
output_filename = 'br_summary_stats.csv'
output_path = 'C:/Users/conno/OneDrive/University Study/Honours Thesis/cnolan-thesis/summary stats/'
outputname = output_path + output_filename
br_summary_stats.to_csv(outputname, mode='w', index=False)
print("Exported File: " + outputname)
#%%
'''
CARBON BETA
'''
pricing_carbon_risk = pd.read_csv('C:/Users/conno/OneDrive/University Study/Honours Thesis/cnolan-thesis/regression/regression variables/cb_asx500_pricing_carbon_risk.csv')
#carbon_beta = pd.read_csv("C:/Users/conno/OneDrive/University Study/Honours Thesis/cnolan-thesis/regression/regression outputs/carbon beta/carbon_beta_regression_output.csv")
pricing_carbon_risk = pricing_carbon_risk.loc[(pricing_carbon_risk['yearmonth'] >= 200807) & (pricing_carbon_risk['yearmonth'] <= 202106)]
pricing_carbon_risk_out = pricing_carbon_risk[['ret', 'ln_marketcap', 'bm', 'roe', 'leverage', 'investa', 'logppe', 'ppea', 'beta', 'mom', 'carbon_beta']].reset_index(drop=True)

"Save pricing_carbon_risk_out"
output_filename = 'pricing_carbon_risk_out.csv'
output_path = 'C:/Users/conno/OneDrive/University Study/Honours Thesis/cnolan-thesis/summary stats/'
outputname = output_path + output_filename
pricing_carbon_risk_out.to_csv(outputname, mode='w', index=False)
print("Exported File: " + outputname)

#%%
'''
#############YEARLY FIRM OBSERVATIONS
'''
#%%
'''
log emissions
'''
"import data"
yearly_stats = pd.read_csv ("C:/Users/conno/OneDrive/University Study/Honours Thesis/cnolan-thesis/regression/regression variables/br_determinants_of_carbon_emissions.csv")
yearly_stats = yearly_stats[['year','ticker','log_scope1', 'log_scope2', 'log_total_emissions', 'log_energy_consumption', 'change_scope1', 'change_scope2', 'change_total_emissions', 'change_energy_consumption', 'scope1_int', 'scope2_int', 'total_emissions_int', 'energy_consumption_int']]
yearly_stats_out = yearly_stats

"Save yearly_stats_out"
output_filename = 'yearly_stats_out.csv'
output_path = 'C:/Users/conno/OneDrive/University Study/Honours Thesis/cnolan-thesis/summary stats/'
outputname = output_path + output_filename
yearly_stats_out.to_csv(outputname, mode='w', index=False)
print("Exported File: " + outputname)
#%%

'''
EXP EMISSIONS
'''

nger_data_matched = pd.read_csv('C:/Users/conno/OneDrive/University Study/Honours Thesis/cnolan-thesis/output/nger_data_matched.csv',encoding = "ISO-8859-1")
matched_tickers = pd.read_csv("C:/Users/conno/OneDrive/University Study/Honours Thesis/cnolan-thesis/output/matched_tickers.csv")
matched_tickers_list = matched_tickers['ticker'].tolist()
ms_data = pd.read_csv ('C:/Users/conno/OneDrive/University Study/Honours Thesis/cnolan-thesis/output/ms_data.csv', encoding='latin1')

"ADD TICKER YEAR ID"

nger_data_matched['year'] = nger_data_matched['year'].astype(str)
ms_data['year'] = ms_data['year'].astype(str)

nger_data_matched['ticker_year'] = nger_data_matched['ticker'] + '_' + nger_data_matched['year']
ms_data['ticker_year'] = ms_data['ticker'] + '_' + ms_data['year']


"CONSTRUCT EMISSIONS VARIABLES"

independent_vars_exp = nger_data_matched
independent_vars_exp = pd.merge(independent_vars_exp, ms_data[['ticker_year','revenue']], how='left', on=['ticker_year'])
independent_vars_exp = independent_vars_exp.replace([np.inf, -np.inf], np.nan)


"YEAR BY YEAR CHANGE IN EMISSIONS"

#clone each unique company for each observation year (2009-2021)
firms_2009 = pd.DataFrame({'ticker':matched_tickers_list, 'year': '2009'})
firms_2010 = pd.DataFrame({'ticker':matched_tickers_list, 'year': '2010'})
firms_2011 = pd.DataFrame({'ticker':matched_tickers_list, 'year': '2011'})
firms_2012 = pd.DataFrame({'ticker':matched_tickers_list, 'year': '2012'})
firms_2013 = pd.DataFrame({'ticker':matched_tickers_list, 'year': '2013'})
firms_2014 = pd.DataFrame({'ticker':matched_tickers_list, 'year': '2014'})
firms_2015 = pd.DataFrame({'ticker':matched_tickers_list, 'year': '2015'})
firms_2016 = pd.DataFrame({'ticker':matched_tickers_list, 'year': '2016'})
firms_2017 = pd.DataFrame({'ticker':matched_tickers_list, 'year': '2017'})
firms_2018 = pd.DataFrame({'ticker':matched_tickers_list, 'year': '2018'})
firms_2019 = pd.DataFrame({'ticker':matched_tickers_list, 'year': '2019'})
firms_2020 = pd.DataFrame({'ticker':matched_tickers_list, 'year': '2020'})
firms_2021 = pd.DataFrame({'ticker':matched_tickers_list, 'year': '2021'})

#create dataframe to add all cloned firm years
firms_allyears = pd.DataFrame(columns = ['ticker', 'year'])

#add all clone firm year dataframes to a list
firm_years_list = [firms_2009, firms_2010, firms_2011, firms_2012, firms_2013, firms_2014, firms_2015, firms_2016, firms_2017, firms_2018, firms_2019, firms_2020, firms_2021]

#concatenate dataframes
firms_allyears = pd.concat(firm_years_list)

firms_allyears['ticker_year'] = firms_allyears['ticker'] + '_' + firms_allyears['year']

#create dummy level index
independent_vars_exp["dummy_index"] = independent_vars_exp["dummy_index"] = 1
firms_allyears['dummy_index'] = firms_allyears['dummy_index'] = 2

#concenate cloned firm years with main data file
independent_vars_exp = pd.concat([independent_vars_exp, firms_allyears]).reset_index(drop=True)

#sort dataframe by corporation name and year
independent_vars_exp = independent_vars_exp.sort_values(by=['ticker', 'year']).reset_index(drop=True)

#drop duplicates keeping first row (main  data file) as by dummy_index sorting
independent_vars_exp = independent_vars_exp.drop_duplicates(['ticker', 'year',], keep='first').reset_index(drop=True)


#independent_vars_exp['year'] =  pd.to_datetime(independent_vars_exp['year'], format='%Y').dt.to_period("Y")

independent_vars_exp = independent_vars_exp.sort_values(by=['ticker','year'])

#calculate yearly change in emissions by corporation for scope1, scope2, total_emissions, and energy consumption


#on log emissions

independent_vars_exp = independent_vars_exp.sort_values(by=['ticker','year'])
independent_vars_exp['change_scope1'] = independent_vars_exp.groupby(['ticker'])['scope1'].diff()
independent_vars_exp['change_scope2'] = independent_vars_exp.groupby(['ticker'])['scope2'].diff()
independent_vars_exp['change_total_emissions'] = independent_vars_exp.groupby(['ticker'])['total_emissions'].diff()
independent_vars_exp['change_energy_consumption'] = independent_vars_exp.groupby(['ticker'])['energy_consumption'].diff()

independent_vars_exp = independent_vars_exp.replace([np.inf, -np.inf], np.nan).reset_index(drop=True)


"EMISSIONS INTENSITY"

'''
## int = (tons CO 2 e/AUD m.)
independent_vars_exp['revenue(m)'] = independent_vars_exp['revenue'] / 1000000

independent_vars_exp['scope1_int'] = independent_vars_exp['scope1'] /  independent_vars_exp['revenue(m)']
independent_vars_exp['scope2_int'] = independent_vars_exp['scope2'] /  independent_vars_exp['revenue(m)']
independent_vars_exp['total_emissions_int'] = independent_vars_exp['total_emissions'] /  independent_vars_exp['revenue(m)']
independent_vars_exp['energy_consumption_int'] = independent_vars_exp['energy_consumption'] / independent_vars_exp['revenue(m)']

independent_vars_exp['scope1_int'] = independent_vars_exp['scope1_int']/100
independent_vars_exp['scope2_int'] = independent_vars_exp['scope2_int']/100
independent_vars_exp['total_emissions_int'] = independent_vars_exp['total_emissions_int']/100
independent_vars_exp['energy_consumption_int'] = independent_vars_exp['energy_consumption_int']/100
'''


"merge intensity"
independent_vars_exp['year'] = independent_vars_exp['year'].astype(int)
independent_vars_exp = pd.merge(independent_vars_exp, yearly_stats[['year', 'ticker', 'scope1_int', 'scope2_int', 'total_emissions_int', 'energy_consumption_int']], how='left', on=['year','ticker'])

"DROP BLANK OBSERVATIONS"
independent_vars_exp = independent_vars_exp.dropna(subset=['scope1', 'scope2', 'total_emissions', 'energy_consumption', 'change_scope1', 'change_scope2', 'change_total_emissions', 'change_energy_consumption', 'scope1_int', 'scope2_int', 'total_emissions_int', 'energy_consumption_int'],how='all').reset_index(drop=True)
independent_vars_exp = independent_vars_exp[['year', 'ticker', 'ticker_year', 'scope1', 'scope2', 'total_emissions', 'energy_consumption', 'change_scope1', 'change_scope2', 'change_total_emissions', 'change_energy_consumption', 'scope1_int', 'scope2_int', 'total_emissions_int', 'energy_consumption_int']]

yearly_stats_exp_out = independent_vars_exp

"Save yearly_stats_exp_out"
output_filename = 'yearly_stats_exp_out.csv'
output_path = 'C:/Users/conno/OneDrive/University Study/Honours Thesis/cnolan-thesis/summary stats/'
outputname = output_path + output_filename
yearly_stats_exp_out.to_csv(outputname, mode='w', index=False)
print("Exported File: " + outputname)



#%%

"GROUP BY AGG"

"YEAERLY STATS TAB"
yearly_stats_out_winsor = pd.read_csv('C:/Users/conno/OneDrive/University Study/Honours Thesis/cnolan-thesis/summary stats/yearly_stats_out_winsor.csv')
yearly_stats_log_agg = yearly_stats_out_winsor.groupby("year").agg({"ticker": pd.Series.nunique, 'log_scope1': np.mean, 'log_scope2': np.mean, 'log_total_emissions': np.mean, 'log_energy_consumption': np.mean, 'change_scope1': np.mean, 'change_scope2': np.mean, 'change_total_emissions': np.mean, 'change_energy_consumption': np.mean, 'scope1_int': np.mean, 'scope2_int': np.mean, 'total_emissions_int': np.mean, 'energy_consumption_int': np.mean,})
yearly_stats_log_agg =yearly_stats_log_agg.assign(table="log")

"Save yearly_stats_log_agg"
output_filename = 'yearly_stats_log_agg.csv'
output_path = 'C:/Users/conno/OneDrive/University Study/Honours Thesis/cnolan-thesis/summary stats/'
outputname = output_path + output_filename
yearly_stats_log_agg.to_csv(outputname, mode='w', index=False)
print("Exported File: " + outputname)

"YEARLY STATS TAB E"
yearly_stats_exp_out_winsor = pd.read_csv('C:/Users/conno/OneDrive/University Study/Honours Thesis/cnolan-thesis/summary stats/yearly_stats_exp_out_winsor.csv')
yearly_stats_exp_agg = yearly_stats_exp_out_winsor.groupby("year").agg({"ticker": pd.Series.nunique, 'scope1': np.mean, 'scope2': np.mean, 'total_emissions': np.mean, 'energy_consumption': np.mean, 'change_scope1': np.mean, 'change_scope2': np.mean, 'change_total_emissions': np.mean, 'change_energy_consumption': np.mean, 'scope1_int': np.mean, 'scope2_int': np.mean, 'total_emissions_int': np.mean, 'energy_consumption_int': np.mean})
yearly_stats_exp_agg =yearly_stats_exp_agg.assign(table="exp")

"Save yearly_stats_exp_agg"
output_filename = 'yearly_stats_exp_agg.csv'
output_path = 'C:/Users/conno/OneDrive/University Study/Honours Thesis/cnolan-thesis/summary stats/'
outputname = output_path + output_filename
yearly_stats_exp_agg.to_csv(outputname, mode='w', index=False)
print("Exported File: " + outputname)


"YEARLY STATS CONACT"
yearly_stats_exp_agg = yearly_stats_exp_agg.rename(columns={'scope1': 'log_scope1', 'scope2':'log_scope2', 'total_emissions': 'log_total_emissions', 'energy_consumption': 'log_energy_consumption'})

yearly_stats_concat_agg = yearly_stats_log_agg.append(yearly_stats_exp_agg)
yearly_stats_concat_agg = yearly_stats_concat_agg.reset_index()
yearly_stats_concat_agg['year'] = yearly_stats_concat_agg['year'].astype(int)


"Save yearly_stats_concat_agg"
output_filename = 'yearly_stats_concat_agg.csv'
output_path = 'C:/Users/conno/OneDrive/University Study/Honours Thesis/cnolan-thesis/summary stats/'
outputname = output_path + output_filename
yearly_stats_concat_agg.to_csv(outputname, mode='w', index=False)
print("Exported File: " + outputname)
