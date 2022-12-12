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

"IMPORT DATA"

nger_data_matched = pd.read_csv('C:/Users/conno/OneDrive/University Study/Honours Thesis/cnolan-thesis/output/nger_data_matched.csv',encoding = "ISO-8859-1")
ms_data = pd.read_csv ('C:/Users/conno/OneDrive/University Study/Honours Thesis/cnolan-thesis/output/ms_data.csv', encoding='latin1')

price_data = pd.read_csv('C:/Users/conno/OneDrive/University Study/Honours Thesis/cnolan-thesis/data/ds_matched_dailyprice.csv')
marketcap = pd.read_csv('C:/Users/conno/OneDrive/University Study/Honours Thesis/cnolan-thesis/data/ds_marketcap.csv')
beta = pd.read_csv('C:/Users/conno/OneDrive/University Study/Honours Thesis/cnolan-thesis/data/ds_beta.csv')
industry = pd.read_csv ('C:/Users/conno/OneDrive/University Study/Honours Thesis/cnolan-thesis/data/ds_ticker_industry.csv')

matched_tickers = pd.read_csv("C:/Users/conno/OneDrive/University Study/Honours Thesis/cnolan-thesis/output/matched_tickers.csv")
matched_tickers_list = matched_tickers['ticker'].tolist()


#%%

"ADD TICKER YEAR ID"

nger_data_matched['year'] = nger_data_matched['year'].astype(str)
ms_data['year'] = ms_data['year'].astype(str)

nger_data_matched['ticker_year'] = nger_data_matched['ticker'] + '_' + nger_data_matched['year']
ms_data['ticker_year'] = ms_data['ticker'] + '_' + ms_data['year']

#%%

"CONSTRUCT RETURNS"

#format date
price_data['Date'] = pd.to_datetime(price_data['Date'], format='%d/%m/%Y')
price_data.set_index('Date',inplace=True)


#calculate monthly return
monthly_price_data = price_data.resample('M').ffill()
monthly_price_change = monthly_price_data / monthly_price_data.shift(1) - 1 
columns = ['29M', 'ARI', 'ABB1', 'ABC', 'ABY1', 'AIS', 'AGL', 'ALK', 'AQZ', 'AMP', 'ALD', 'ALG', 'AOE', 'AHY', 'AIO', 'AGO', 'AMI', 'AZJ', 'AST', 'AQC', 'AHG', 'BPT', 'BGA', 'BHP', 'BIN', 'BSL', 'BLD', 'B2Y', 'BKN', 'BKW', 'BRS', 'CAA', 'CBH1', 'CEY', 'CTP', 'CHC', 'CIM', 'CWY', 'CCL', 'CGJ', 'CBA', 'CWN', 'CSL', 'CSR', 'CDU', 'CEP', 'CER', 'CRG', 'DCN', 'DJS', 'DXS', 'DOW', 'APE', 'ENV1', 'EPW', 'EVT', 'EVN', 'ESG', 'ELD', 'ENE1', 'FMG', 'FGL1', 'FXJ', 'FLX1', 'FML', 'GCY', 'GFF', 'GNC', 'GRR', 'GCL', 'GNS', 'HVN', 'HSO', 'HGO', 'HRL', 'IGO', 'ILU', 'IMA', 'IPL', 'ING', 'IVA', 'IGR', 'IPG2', 'JBH', 'KZL', 'LLC', 'LAU', 'AEJ']
for i in columns:
    monthly_price_change[i] = monthly_price_change[i].replace(0, np.nan)

#reformat to multi column (year, month) index
monthly_price_change = monthly_price_change.reset_index()
monthly_price_change['year'] = monthly_price_change['Date'].dt.strftime('%Y')
monthly_price_change['month'] = monthly_price_change['Date'].dt.strftime('%m')

#reshape df into time series format
monthly_price_change = pd.melt(monthly_price_change, id_vars = ['Date', 'year', 'month'], value_vars= ['29M', 'ARI', 'ABB1', 'ABC', 'ABY1', 'AIS', 'AGL', 'ALK', 'AQZ', 'AMP', 'ALD', 'ALG', 'AOE', 'AHY', 'AIO', 'AGO', 'AMI', 'AZJ', 'AST', 'AQC', 'AHG', 'BPT', 'BGA', 'BHP', 'BIN', 'BSL', 'BLD', 'B2Y', 'BKN', 'BKW', 'BRS', 'CAA', 'CBH1', 'CEY', 'CTP', 'CHC', 'CIM', 'CWY', 'CCL', 'CGJ', 'CBA', 'CWN', 'CSL', 'CSR', 'CDU', 'CEP', 'CER', 'CRG', 'DCN', 'DJS', 'DXS', 'DOW', 'APE', 'ENV1', 'EPW', 'EVT', 'EVN', 'ESG', 'ELD', 'ENE1', 'FMG', 'FGL1', 'FXJ', 'FLX1', 'FML', 'GCY', 'GFF', 'GNC', 'GRR', 'GCL', 'GNS', 'HVN', 'HSO', 'HGO', 'HRL', 'IGO', 'ILU', 'IMA', 'IPL', 'ING', 'IVA', 'IGR', 'IPG2', 'JBH', 'KZL', 'LLC', 'LAU', 'AEJ'], var_name = 'ticker', value_name='monthly_return',col_level=None)
monthly_price_change['monthly_return'] = monthly_price_change.monthly_return.astype(float)


ret = monthly_price_change[['Date','year','month','ticker','monthly_return']]
ret = ret.rename(columns={'monthly_return':'ret'})
ret = ret.reset_index(drop=True)
ret['ticker_year_month'] = ret['ticker'] + '_' + ret['year'] + '_' + ret ['month']

ret_merge = ret[['ticker_year_month','ticker','year','month','ret']]

#%%

"CONSTRUCT EMISSIONS VARIABLES"

independent_vars = nger_data_matched
independent_vars = pd.merge(independent_vars, ms_data[['ticker_year','revenue']], how='left', on=['ticker_year'])

"LOG EMISSIONS"

#log scope1, scope2, total_emissions, and energy consumption
independent_vars['log_scope1'] = np.log(independent_vars['scope1'])
independent_vars['log_scope2'] = np.log(independent_vars['scope2'])
independent_vars['log_total_emissions'] = np.log(independent_vars['total_emissions'])
independent_vars['log_energy_consumption'] = np.log(independent_vars['energy_consumption'])

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
independent_vars["dummy_index"] = independent_vars["dummy_index"] = 1
firms_allyears['dummy_index'] = firms_allyears['dummy_index'] = 2

#concenate cloned firm years with main data file
independent_vars = pd.concat([independent_vars, firms_allyears]).reset_index(drop=True)

#sort dataframe by corporation name and year
independent_vars = independent_vars.sort_values(by=['ticker', 'year','ticker']).reset_index(drop=True)

#drop duplicates keeping first row (main  data file) as by dummy_index sorting
independent_vars = independent_vars.drop_duplicates(['ticker', 'year','ticker'], keep='first').reset_index(drop=True)


independent_vars['year'] =  pd.to_datetime(independent_vars['year'], format='%Y').dt.to_period("Y")

independent_vars = independent_vars.sort_values(by=['year'])
#calculate yearly change in emissions by corporation for scope1, scope2, total_emissions, and energy consumption
independent_vars['change_scope1'] = independent_vars.groupby(['ticker'])['scope1'].diff()
independent_vars['change_scope2'] = independent_vars.groupby(['ticker'])['scope2'].diff()
independent_vars['change_total_emissions'] = independent_vars.groupby(['ticker'])['total_emissions'].diff()
independent_vars['change_energy_consumption'] = independent_vars.groupby(['ticker'])['energy_consumption'].diff()

'''
CALCULATE LOG CHANGE EMISSIONS
'''
independent_vars['change_scope1'] = np.log(independent_vars['change_scope1'])
independent_vars['change_scope2'] = np.log(independent_vars['change_scope2'])
independent_vars['change_total_emissions'] = np.log(independent_vars['change_scope2'])
independent_vars['change_energy_consumption'] = np.log(independent_vars['change_scope2'])



'''
X
'''
#%%
"EMISSIONS INTENSITY"

## int = (tons CO 2 e/AUD m.)
independent_vars['revenue(m)'] = independent_vars['revenue'] / 1000000
independent_vars['scope1_int'] = independent_vars['scope1'] /  independent_vars['revenue(m)']
independent_vars['scope2_int'] = independent_vars['scope2'] /  independent_vars['revenue(m)']
independent_vars['total_emissions_int'] = independent_vars['total_emissions'] /  independent_vars['revenue(m)']
independent_vars['energy_consumption_int'] = independent_vars['energy_consumption'] / independent_vars['revenue(m)']


"DROP BLANK OBSERVATIONS"
independent_vars = independent_vars.dropna(subset=['scope1', 'scope2', 'energy_consumption', 'total_emissions'],how='any').reset_index(drop=True)
independent_vars = independent_vars[['year', 'ticker', 'ticker_year', 'log_scope1', 'log_scope2', 'log_total_emissions', 'log_energy_consumption', 'change_scope1', 'change_scope2', 'change_total_emissions', 'change_energy_consumption', 'scope1_int', 'scope2_int', 'total_emissions_int', 'energy_consumption_int']]

independent_vars_merge = independent_vars[['ticker_year','year','ticker','log_scope1', 'log_scope2', 'log_total_emissions', 'log_energy_consumption', 'change_scope1', 'change_scope2', 'change_total_emissions', 'change_energy_consumption', 'scope1_int', 'scope2_int', 'total_emissions_int', 'energy_consumption_int']]


#%%

"CONSTRUCT CONTROL VARIABLES"

control_vars = ms_data

#LOGSIZE
control_vars['logsize'] = np.log(control_vars['marketcap'])

#B/M
control_vars['bm'] = (control_vars['assets'] - control_vars['liabilities']) / control_vars['marketcap']

#LEVERAGE
control_vars['totaldebt'] = control_vars.stdebt.fillna(0) + control_vars.ltdebt.fillna(0) #calculate total debt, skipping nan values (this means total debt can be constructed from ltdebt, stdebt, or both)
control_vars['leverage'] = control_vars.totaldebt / control_vars.assets #calculate leverage

#MOM
mom = monthly_price_change.reset_index(drop=True)
mom = mom.set_index('Date')
mom = mom.to_period(freq="M")
mom['lag_monthly_return'] = mom.monthly_return.shift(1)
mom['mom'] = mom.lag_monthly_return.rolling(12).mean()
mom = mom.reset_index(drop=True)
mom['ticker_year_month'] = mom['ticker'] + '_' + mom['year'] + '_' + mom['month']
mom_merge = mom[['ticker_year_month','mom']]

#INVEST/A
control_vars['investa'] = control_vars.capex / control_vars.assets

#ROE
#control_vars['roe'] #already have

# HHI (ignore: unable to source firm revenues by busniess segement - limitation)

#LOGPPE
control_vars['logppe'] = np.log(control_vars['ppe'])

#BETA
beta = beta.drop('CEP', axis = 1)
beta['year'] = pd.to_datetime(beta['year'], format='%Y')
beta['year'] = beta['year'].dt.strftime('%Y')
beta = beta.set_index('year')
beta_cols = list(beta)
beta = beta.reset_index()
beta = pd.melt(beta, id_vars = ['year'], value_vars = beta_cols, var_name = 'ticker', value_name='beta',col_level=None)
beta['ticker_year'] = beta['ticker'] + '_' + beta['year']
beta_merge = beta[['ticker_year','beta']]

#VOLAT
volat = price_data
volat = volat.drop('CEP', axis = 1)
volat = volat.resample('M').ffill()
volat_cols = list(volat)
volat = volat.reset_index()
volat = pd.melt(volat, id_vars = ['Date'], value_vars = volat_cols, var_name = 'ticker', value_name='price',col_level=None)
volat['price'] = volat.price.astype(float)
volat = volat.set_index('Date').sort_values('ticker')
volat['pct'] = volat.groupby('ticker')['price'].pct_change()
volat['volat'] = volat['pct'].rolling(12).std()
volat = volat.reset_index()
volat['year'] = volat['Date'].dt.strftime('%Y')
volat['month'] = volat['Date'].dt.strftime('%m')
volat['ticker_year_month'] = volat['ticker'] + '_' + volat['year'] + '_' + volat['month']

volat_merge = volat[['ticker_year_month','volat']]

#SALESGR
marketcap = marketcap.dropna(how='all')
marketcap = marketcap.drop('CEP', axis = 1)
marketcap['Date'] = pd.to_datetime(marketcap['Date'], format='%d/%m/%Y')
marketcap = marketcap.set_index('Date')
marketcap_cols = list(marketcap)
marketcap = marketcap.reset_index()
marketcap = pd.melt(marketcap, id_vars = ['Date'], value_vars = marketcap_cols, var_name = 'ticker', value_name = 'marketcap', col_level = None)
marketcap['year'] = marketcap['Date'].dt.strftime('%Y')
marketcap['marketcap'] = marketcap['marketcap'].astype(float)
marketcap['marketcap'] = marketcap['marketcap'] * 1000000
marketcap['marketcap_lag'] = marketcap['marketcap'].shift(1)
marketcap['year'] = marketcap['Date'].dt.strftime('%Y')
marketcap['month'] = marketcap['Date'].dt.strftime('%m')
marketcap['ticker_year'] = marketcap['ticker'] + '_' + marketcap['year'] 
marketcap['ticker_year_month'] = marketcap['ticker'] + '_' + marketcap['year'] + '_' + marketcap['month']

revenue_change = ms_data[['ticker_year','year','ticker','revenue']]
revenue_change = revenue_change.sort_values(by=['ticker', 'year']) #sort dataframe by ticker and year
revenue_change['revenue_change'] = revenue_change.groupby(['ticker'])['revenue'].diff() #calculate yearly change in revenue by firm


salesgr = pd.merge(marketcap, revenue_change, how='left', on=['ticker_year'])

salesgr['salesgr'] = salesgr.revenue_change / salesgr.marketcap #salesgr = change in annual revenue normailzed by marketcap

salesgr_merge = salesgr[['ticker_year_month','salesgr']]


#EPSGR
eps_change = ms_data[['ticker_year','year','ticker','eps']]
eps_change = eps_change.sort_values(by=['ticker', 'year']) #sort dataframe by ticker and year
eps_change['eps'] = eps_change['eps'].astype(float)
eps_change['eps_change'] = eps_change.groupby(['ticker'])['eps'].diff() #calculate yearly change in eps by firm


monthly_price = monthly_price_data
monthly_price_cols = list(monthly_price)
monthly_price = monthly_price.reset_index()
monthly_price = pd.melt(monthly_price, id_vars = ['Date'], value_vars= monthly_price_cols, var_name = 'ticker', value_name='eom_price',col_level=None)
monthly_price['eom_price'] = monthly_price['eom_price'].astype(float)
monthly_price['year'] = monthly_price['Date'].dt.strftime('%Y')
monthly_price['month'] = monthly_price['Date'].dt.strftime('%m')
monthly_price['ticker_year'] = monthly_price['ticker'] + '_' + monthly_price['year'] 
monthly_price['ticker_year_month'] = monthly_price['ticker'] + '_' + monthly_price['year'] + '_' + monthly_price['month']

epsgr = pd.merge(monthly_price, eps_change[['ticker_year', 'eps', 'eps_change']], how = 'left', on =['ticker_year'])
epsgr['epsgr'] = epsgr.eps_change / epsgr.eom_price

epsgr_merge = epsgr[['ticker_year_month', 'epsgr']]

#%%
"MERGE MONTHLY VARIABLES TOGETHER"
# ret_merge
# mom_merge
# volat_merge
# salesgr_merge
# epsgr_merge

monthly_merge = pd.merge(ret_merge, mom_merge, on=['ticker_year_month'], how = 'outer')
monthly_merge = pd.merge(monthly_merge, volat_merge, on=['ticker_year_month'], how = 'outer')
monthly_merge = pd.merge(monthly_merge, salesgr_merge, on=['ticker_year_month'], how = 'outer')
monthly_merge = pd.merge(monthly_merge, epsgr_merge, on=['ticker_year_month'], how = 'outer')

monthly_merge['ticker_year'] = monthly_merge['ticker'] + '_' + monthly_merge['year']

"MERGE YEARLY VARIABLES TOGETHER"
# independent_vars_merge
# logsize_merge
# bm_merge
# leverage_merge
# investa_merge
# roe_merge
# logppe_merge
# beta_merge

#Merge on the yearly emissions variables
yearly_merge = pd.merge(independent_vars_merge, control_vars[['ticker_year','logsize','bm','leverage','investa','roe','logppe']], on=['ticker_year'], how = 'outer')
yearly_merge = pd.merge(yearly_merge, beta_merge, on=['ticker_year'], how = 'outer')


#Explode yearly data so that the yearly observation is duplicated for each month 01-12

months_list_df = pd.DataFrame({'month':[['01','02','03','04','05','06','07','08','09','10','11','12']]})
len_yearly_merge = len(yearly_merge)
months_list_df = pd.concat([months_list_df]*len_yearly_merge, ignore_index=True)
yearly_merge = yearly_merge.join(months_list_df)

yearly_merge = yearly_merge.explode('month')
#.reset_index(drop=True)
yearly_merge['ticker_year_month'] = yearly_merge['ticker_year'] + '_' + yearly_merge['month']
yearly_merge = yearly_merge.sort_values(by=['ticker_year_month']).reset_index(drop=True)

#%%
"MERGE MONTHLY AND YEARLY VARIABLES TOGETHER + ADD INDUSTRY"

data_cross_sectional_returns = pd.merge(monthly_merge[['ticker_year_month', 'ticker', 'year', 'month', 'ret', 'mom', 'volat', 'salesgr', 'epsgr']],
                      yearly_merge[['ticker_year_month','log_scope1', 'log_scope2', 'log_total_emissions', 'log_energy_consumption', 'change_scope1', 'change_scope2', 'change_total_emissions', 'change_energy_consumption', 'scope1_int', 'scope2_int', 'total_emissions_int', 'energy_consumption_int', 'logsize', 'bm', 'leverage', 'investa', 'roe', 'logppe', 'beta']],
                      how = 'outer',
                      on=['ticker_year_month'])

data_cross_sectional_returns= pd.merge(data_cross_sectional_returns, industry, on=['ticker'], how='left')

data_cross_sectional_returns = data_cross_sectional_returns.reindex(columns=['ticker_year_month', 'ticker', 'industry', 'year', 'month', 'ret', 'log_scope1', 'log_scope2', 'log_total_emissions', 'log_energy_consumption', 'change_scope1', 'change_scope2', 'change_total_emissions', 'change_energy_consumption', 'scope1_int', 'scope2_int', 'total_emissions_int', 'energy_consumption_int', 'logsize', 'bm', 'leverage', 'mom', 'investa', 'roe', 'logppe', 'beta', 'volat', 'salesgr', 'epsgr'])


#%%

"DROP MISSING OBSERVATIONS"

data_cross_sectional_returns = data_cross_sectional_returns.dropna(how = 'any', subset=['ret', 'logsize', 'bm', 'leverage', 'mom', 'investa', 'roe', 'logppe', 'beta', 'volat', 'salesgr', 'epsgr'])
data_cross_sectional_returns = data_cross_sectional_returns.dropna(how = 'all', subset=['log_scope1', 'log_scope2', 'log_total_emissions', 'log_energy_consumption', 'change_scope1', 'change_scope2', 'change_total_emissions', 'change_energy_consumption', 'scope1_int', 'scope2_int', 'total_emissions_int', 'energy_consumption_int'])

obs_prev = len(data_cross_sectional_returns)
data_cross_sectional_returns = data_cross_sectional_returns.dropna(subset=['industry'])
obs_after = len(data_cross_sectional_returns)
print('obs dropped from industry dropna: '+ str(obs_prev-obs_after))

data_cross_sectional_returns = data_cross_sectional_returns.sort_values(by=['year','month','ticker']).reset_index(drop=True)

data_cross_sectional_returns['yearmonth'] = data_cross_sectional_returns['year'].astype(str) + data_cross_sectional_returns['month'].astype(str)
data_cross_sectional_returns['yearmonth'] = data_cross_sectional_returns['yearmonth'].astype(int)

#%%

"Save Cabron Emissions and Stock Returns Data"
output_filename = 'cross_sectional_returns_data.csv'
outputname = output_path + output_filename
data_cross_sectional_returns.to_csv(outputname, mode='w', index=False)
print("Exported File: " + outputname)

#%%
print("CONSTRUCT CROSS SECTIONAL RETURNS - DONE")