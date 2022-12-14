#%%
"IMPORT MODULES"
import os
import pandas as pd
import numpy as np
from fuzzywuzzy import process


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

#THIS DATA IS COLLATED AND PROCESSED FROM NOTEBOOK: 1. Collate Data
ms_data = pd.read_csv ('C:/Users/conno/OneDrive/University Study/Honours Thesis/cnolan-thesis/output/ms_data.csv', encoding='latin1')
asx500 = pd.read_csv("C:/Users/conno/OneDrive/University Study/Honours Thesis/cnolan-thesis/output/asx500_all.csv")

#%%

asx500_firms = asx500[['Ticker', 'Name']]
asx500_firms = asx500_firms.drop_duplicates(subset=['Name']).reset_index(drop=True)

"FORMAT NGER COMPANY NAMES FOR MATCHING"

asx500_firms['asx500_name'] = asx500_firms['Name']

asx500_firms['asx500_name']=asx500_firms['asx500_name'].str.lower()
asx500_firms['asx500_name']=asx500_firms['asx500_name'].str.replace('pty ltd','',regex=True)
asx500_firms['asx500_name']=asx500_firms['asx500_name'].str.replace('limited group','',regex=True)
asx500_firms['asx500_name']=asx500_firms['asx500_name'].str.replace('limited','',regex=True)
asx500_firms['asx500_name']=asx500_firms['asx500_name'].str.replace('group','',regex=True)
asx500_firms['asx500_name']=asx500_firms['asx500_name'].str.replace('ltd','',regex=True)
asx500_firms['asx500_name']=asx500_firms['asx500_name'].str.replace('holdings','',regex=True)
asx500_firms['asx500_name']=asx500_firms['asx500_name'].str.replace('holding','',regex=True)
asx500_firms['asx500_name']=asx500_firms['asx500_name'].str.replace('pty','',regex=True)
asx500_firms['asx500_name']=asx500_firms['asx500_name'].str.replace('proprietary','',regex=True)
asx500_firms['asx500_name']=asx500_firms['asx500_name'].str.replace('corporation','',regex=True)
asx500_firms['asx500_name']=asx500_firms['asx500_name'].str.rstrip('.')
asx500_firms['asx500_name']=asx500_firms['asx500_name'].str.strip()

asx500_firms_list = []
asx500_firms_list = asx500_firms['asx500_name'].unique().tolist()



ms_list = []
ms_list = ms_data['morningstar_name'].unique().tolist()

#%%
'''
print('starting fuzzy matching')

threshold = 95 #note: in preliminary analysis a threshold of 95 provided matching without mismatching 
names_response = []
for name in asx500_firms_list:
    resp_match =  process.extractOne(name,ms_list)
    if resp_match[1] > threshold:
         row = {'asx500_name':name,'morningstar_name':resp_match[0], 'match_score':resp_match[1]}
         names_response.append(row)
         
print('finish fuzzy matching')

"Save fuzzed_matched_asx500"
fuzzy_matched_asx500_save = pd.DataFrame(names_response)
output_filename = 'fuzzy_matched_asx500_save.csv'
outputname = output_path + output_filename
fuzzy_matched_asx500_save.to_csv(outputname, mode='w', index=False)
print("Exported File: " + outputname)
'''

#%%
#import saved fuzzy match
matched_asx500 = pd.read_csv('C:/Users/conno/OneDrive/University Study/Honours Thesis/cnolan-thesis/regression/regression variables/fuzzy_matched_asx500_save.csv')
matched_asx500['fuzzy_matched'] = 1
matched_asx500 = pd.merge(matched_asx500, ms_data[['morningstar_name', 'ticker']], how='left', on=['morningstar_name'])
matched_asx500 = pd.merge(matched_asx500,asx500_firms[['Name', 'asx500_name']], how='left', on=['asx500_name'])

#%%

asx500_to_merge = asx500[['yearmonth','Name','GICS Ind\n','Market Cap\n','monthly return']]
asx500_to_merge = asx500_to_merge.rename(columns={'GICS Ind\n':'industry','Market Cap\n':'marketcap_month'})
asx500_to_merge = asx500_to_merge.drop_duplicates(subset=['yearmonth', 'Name'])                             

matched_asx500 = pd.merge(asx500_to_merge, matched_asx500[['fuzzy_matched', 'ticker', 'Name']], how='left', on=['Name'])
matched_asx500 = matched_asx500.drop_duplicates(subset=['yearmonth', 'Name'])   

len_before = len(matched_asx500)
matched_asx500 = matched_asx500.loc[matched_asx500['fuzzy_matched'] == 1]
len_after = len(matched_asx500)
print('Dropped:' + str(len_before-len_after))

matched_asx500 = matched_asx500[['yearmonth','ticker','industry', 'marketcap_month', 'monthly return']]
matched_asx500['asx_500'] = 1
matched_asx500['year'] =  pd.to_datetime(matched_asx500['yearmonth'], format='%Y%M').dt.to_period("Y")
matched_asx500['year'] = matched_asx500['year'].dt.strftime('%Y')
matched_asx500['year'] = matched_asx500['year'].astype(int)
matched_asx500 = pd.merge(matched_asx500,ms_data[['ticker', 'year', 'capex', 'eoy_price', 'eps', 'ltdebt', 'marketcap', 'ppe', 'revenue', 'roe', 'stdebt', 'assets', 'liabilities']],how='left',on=['year','ticker'])



#%%
"drop if assets less than 10million"
asx500_csr = matched_asx500.loc[matched_asx500["assets"] >= 10000000 ]
asx500_csr = asx500_csr.dropna(subset=['monthly return'])
asx500_csr = asx500_csr[['yearmonth', 'year','ticker', 'industry', 'marketcap_month', 'monthly return', 'capex', 'eoy_price', 'eps', 'ltdebt', 'marketcap', 'ppe', 'revenue', 'roe', 'stdebt', 'assets', 'liabilities']]



#%%
"construct variables"

#ln(marketcap)
asx500_csr['ln_marketcap'] = np.log(asx500_csr['marketcap'])

#book/market
asx500_csr['bm'] = (asx500_csr['assets'] - asx500_csr['liabilities']) / asx500_csr['marketcap']

#ROE (already included)

#debt/assets
asx500_csr['totaldebt'] = asx500_csr.stdebt.fillna(0) + asx500_csr.ltdebt.fillna(0) #calculate total debt, skipping nan values (this means total debt can be constructed from ltdebt, stdebt, or both)
asx500_csr['leverage'] = asx500_csr.totaldebt / asx500_csr.assets #calculate leverage

#Investment/Assets
asx500_csr['investa'] = asx500_csr.capex / asx500_csr.assets

#LOGPPE
asx500_csr['logppe'] = np.log(asx500_csr['ppe'])

#ppe/assets
asx500_csr['ppea'] = asx500_csr.ppe / asx500_csr.assets

#r&d / assets 
#cant get r&d


#replace -inf with nan
asx500_csr = asx500_csr.replace([np.inf, -np.inf], np.nan)

'''
#MOM
mom['lag_monthly_return'] = mom.monthly_return.shift(1)
mom['mom'] = mom.lag_monthly_return.rolling(12).mean()
mom = mom.reset_index(drop=True)
mom['ticker_year_month'] = mom['ticker'] + '_' + mom['year'] + '_' + mom['month']
mom_merge = mom[['ticker_year_month','mom']]
'''

'''
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
'''

#%%


"save asx500 csr"
asx500_csr_output = asx500_csr[['yearmonth', 'ticker', 'industry', 'monthly return', 'ln_marketcap', 'bm', 'roe','leverage', 'investa', 'logppe', 'ppea']]
asx500_csr_output = asx500_csr_output.dropna(subset=['monthly return', 'ln_marketcap', 'bm', 'roe','leverage', 'investa', 'logppe', 'ppea'], how ='any').reset_index(drop=True)
asx500_csr_output = asx500_csr_output.rename(columns={'monthly return':'ret'})
"Save asx500"
output_filename = 'asx500_csr.csv'
outputname = output_path + output_filename
asx500_csr_output.to_csv(outputname, mode='w', index=False)
print("Exported File: " + outputname)


#%%
"save asx500 estimate carbon beta"

asx500_cb_output = asx500_csr[['yearmonth', 'ticker', 'monthly return']]
asx500_cb_output = asx500_cb_output.rename(columns={'monthly return':'ret'})
"Save asx500"
output_filename = 'cb_asx500_vars.csv'
outputname = output_path + output_filename
asx500_cb_output.to_csv(outputname, mode='w', index=False)
print("Exported File: " + outputname)


#%%
'''

CREATE PMC 

'''
"IMPORT DATA"
cross_sectional_returns_data = pd.read_csv ('C:/Users/conno/OneDrive/University Study/Honours Thesis/cnolan-thesis/output/cross_sectional_returns_data.csv')
ms_data = pd.read_csv ('C:/Users/conno/OneDrive/University Study/Honours Thesis/cnolan-thesis/output/ms_data.csv')
asx500_filtered = pd.read_csv ('C:/Users/conno/OneDrive/University Study/Honours Thesis/cnolan-thesis/output/asx500_filtered.csv')
monthly_marketcap = pd.read_csv ('C:/Users/conno/OneDrive/University Study/Honours Thesis/cnolan-thesis/data/ds_marketcap_monthly.csv')
famafrench_factors = pd.read_csv ('C:/Users/conno/OneDrive/University Study/Honours Thesis/cnolan-thesis/output/famafrench_factors.csv')
rmrf = pd.read_csv("C:/Users/conno/OneDrive/University Study/Honours Thesis/cnolan-thesis./output/rmrf.csv")


pmc = cross_sectional_returns_data
marketcap = ms_data[['ticker','year','marketcap']].dropna(subset='marketcap').reset_index(drop=True)

#%%

"monthly asx500 returns"

asx500_pmc = asx500_filtered
asx500_pmc = asx500_pmc.rename(columns={'Market Cap\n': 'marketcap', 'monthly return':'ret'})

asx500_pmc['ret'] = asx500_pmc['ret'].replace({'--':np.nan})
asx500_pmc['marketcap'] = asx500_pmc['marketcap'].replace({'--':np.nan})

asx500_pmc['ret'] = asx500_pmc['ret'].astype(float)
asx500_pmc['marketcap'] = asx500_pmc['marketcap'].astype(float)


asx500_pmc['weighted_returns'] =  asx500_pmc['ret'] * (asx500_pmc['marketcap'] / asx500_pmc.groupby(['yearmonth'])['marketcap'].transform('sum'))
asx500_pmc['asx500_ret'] = asx500_pmc.groupby(['yearmonth'])['weighted_returns'].transform('sum')
asx500_pmc['median_marketcap'] = asx500_pmc.groupby(['yearmonth'])['marketcap'].transform('median')

asx500_pmc = asx500_pmc[['yearmonth','asx500_ret','median_marketcap']]
asx500_pmc = asx500_pmc.drop_duplicates(subset=['yearmonth']).reset_index(drop=True)

asx500_pmc = asx500_pmc.loc[(asx500_pmc['yearmonth'] >= 200807) & (asx500_pmc['yearmonth'] <= 202206)]

#%%
"monthly marketcap"
marketcap = monthly_marketcap
marketcap['yearmonth'] = marketcap['yearmonth'].astype(int)

marketcap = pd.melt(marketcap, id_vars = ['yearmonth', 'year', 'month'], value_vars= ['29M', 'ARI', 'ABB1', 'ABC', 'ABY1', 'AIS', 'AGL', 'ALK', 'AQZ', 'AMP', 'ALD', 'ALG', 'AOE', 'AHY', 'AIO', 'AGO', 'AMI', 'AZJ', 'AST', 'AQC', 'AHG', 'BPT', 'BGA', 'BHP', 'BIN', 'BSL', 'BLD', 'B2Y', 'BKN', 'BKW', 'BRS', 'CAA', 'CBH1', 'CEY', 'CTP', 'CHC', 'CIM', 'CWY', 'CCL', 'CGJ', 'CBA', 'CWN', 'CSL', 'CSR', 'CDU', 'CER', 'CRG', 'DCN', 'DJS', 'DXS', 'DOW', 'APE', 'ENV1', 'EPW', 'EVT', 'EVN', 'ESG', 'ELD', 'ENE1', 'FMG', 'FGL1', 'FXJ', 'FLX1', 'FML', 'GCY', 'GFF', 'GNC', 'GRR', 'GCL', 'GNS', 'HVN', 'HSO', 'HGO', 'HRL', 'IGO', 'ILU', 'IMA', 'IPL', 'ING', 'IVA', 'IGR', 'IPG2', 'JBH', 'KZL', 'LLC', 'LAU', 'AEJ'], var_name = 'ticker', value_name='marketcap',col_level=None)
marketcap['marketcap'] = marketcap['marketcap'].astype(float)
marketcap['marketcap'] = marketcap['marketcap'] * 1000000

pmc = cross_sectional_returns_data[['yearmonth','ticker','ret']]

pmc = pd.merge(pmc, marketcap[['yearmonth','ticker','marketcap']], how='left', on=['ticker','yearmonth'])

pmc['weighted_returns'] =  pmc['ret'] * (pmc['marketcap'] / pmc.groupby(['yearmonth'])['marketcap'].transform('sum'))
pmc['nger_ret'] = pmc.groupby(['yearmonth'])['weighted_returns'].transform('sum')

pmc = pmc[['yearmonth','nger_ret']]
pmc = pmc.drop_duplicates(subset=['yearmonth']).reset_index(drop=True)

pmc = pmc.loc[(pmc['yearmonth'] >= 200807) & (pmc['yearmonth'] <= 202206)]

#%%

"calculate pmc"

pmc_factor = pd.merge(pmc, asx500_pmc, how='left',on=['yearmonth'])

pmc_factor['pmc'] = pmc_factor.nger_ret - pmc_factor.asx500_ret



#%% 
"set up cross sectional variables for regression" 

pmc_factor_vars = pmc_factor[['yearmonth','pmc']]

pmc_factor_vars = pd.merge(pmc_factor_vars, famafrench_factors, how='left', on=['yearmonth'])
pmc_factor_vars = pd.merge(pmc_factor_vars, rmrf, how='left', on=['yearmonth'])

pmc_factor_vars = pmc_factor_vars[['yearmonth','rmrf','smb','hml','rmw','cma','wml','pmc']]

asx_500_carbon_beta_vars = pd.merge(asx500_cb_output, pmc_factor_vars, how = 'left', on =['yearmonth'])

#%%

len_before = len(asx_500_carbon_beta_vars)
asx_500_carbon_beta_vars = asx_500_carbon_beta_vars.dropna(subset=['ret', 'rmrf', 'smb', 'hml', 'rmw', 'cma', 'wml', 'pmc'], how='any')
print('Dropped: '+str(len_before-len(asx_500_carbon_beta_vars)))

#%%
"Save asx_500_carbon_beta_vars"
output_filename = 'cb_asx_500_carbon_beta_vars.csv'
output_path = 'C:/Users/conno/OneDrive/University Study/Honours Thesis/cnolan-thesis/regression/regression variables/'
outputname = output_path + output_filename
asx_500_carbon_beta_vars.to_csv(outputname, mode='w', index=False)
print("Exported File: " + outputname)

print("PMC - DONE")
print("RUN REGRESSION ON CARBON BETA VARS")

"RUN REGRESSION ON CARBON BETA VARS"


