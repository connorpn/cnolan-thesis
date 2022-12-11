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
'IMPORT DATA'

cross_sectional_returns_data = pd.read_csv ('C:/Users/conno/OneDrive/University Study/Honours Thesis/cnolan-thesis/output/cross_sectional_returns_data.csv')
ms_data = pd.read_csv ('C:/Users/conno/OneDrive/University Study/Honours Thesis/cnolan-thesis/output/ms_data.csv')
asx500_filtered = pd.read_csv ('C:/Users/conno/OneDrive/University Study/Honours Thesis/cnolan-thesis/output/asx500_filtered.csv')
monthly_marketcap = pd.read_csv ('C:/Users/conno/OneDrive/University Study/Honours Thesis/cnolan-thesis/data/ds_marketcap_monthly.csv')
asx500_returns = pd.read_csv ('C:/Users/conno/OneDrive/University Study/Honours Thesis/cnolan-thesis/output/asx500_returns.csv')
famafrench_factors = pd.read_csv ('C:/Users/conno/OneDrive/University Study/Honours Thesis/cnolan-thesis/output/famafrench_factors.csv')

#%% create seperate portfolios 

'''
create the seperate portfolios that construct the pmc portfolio

pmc = ((SP+BP)/2) - ((SC+BC)/2)

SP = Small Pollutive 
BP = Big Polluive
SC = Small Clean
BC = Big Clean

PMC is long on the top 30% most pollutivng firms and short on the least 30% pollutive firms

Adjust for Size bias by creating seperate clean and pollutive for firms valued below and above the MEDIAN Sample Firm
>paper uses median NYSE firm and we should ideally use median ASX firm but using median sample firm for simplistic sakes at this point in time

'''

'''
How to do it 

group by year/month
calculate emissions percentile
assign p/c for top/bottom 30%
assign s/b for firms above or below median
'''


pmc = cross_sectional_returns_data

marketcap = ms_data[['ticker','year','marketcap']].dropna(subset='marketcap').reset_index(drop=True)

#%%
"monthly asx500 returns"

asx500 = asx500_filtered
asx500 = asx500.rename(columns={'Market Cap\n': 'marketcap', 'monthly return':'ret'})

asx500['ret'] = asx500['ret'].replace({'--':np.nan})
asx500['marketcap'] = asx500['marketcap'].replace({'--':np.nan})

asx500['ret'] = asx500['ret'].astype(float)
asx500['marketcap'] = asx500['marketcap'].astype(float)


asx500['weighted_returns'] =  asx500['ret'] * (asx500['marketcap'] / asx500.groupby(['yearmonth'])['marketcap'].transform('sum'))
asx500['asx500_ret'] = asx500.groupby(['yearmonth'])['weighted_returns'].transform('sum')
asx500['median_marketcap'] = asx500.groupby(['yearmonth'])['marketcap'].transform('median')

asx500 = asx500[['yearmonth','asx500_ret','median_marketcap']]
asx500 = asx500.drop_duplicates(subset=['yearmonth']).reset_index(drop=True)

asx500 = asx500.loc[(asx500['yearmonth'] >= 200807) & (asx500['yearmonth'] <= 202206)]

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

pmc_factor = pd.merge(pmc, asx500, how='left',on=['yearmonth'])

pmc_factor['pmc'] = pmc_factor.nger_ret - pmc_factor.asx500_ret


#%% 
"set up cross sectional variables for regression" 

pmc_factor_vars = pmc_factor[['yearmonth','pmc']]

pmc_factor_vars = pd.merge(pmc_factor_vars, famafrench_factors, how='left', on=['yearmonth'])
pmc_factor_vars = pd.merge(pmc_factor_vars, asx500_returns, how='left', on=['yearmonth'])

pmc_factor_vars = pmc_factor_vars.rename(columns={'asx500_ret': 'rmrf'})

pmc_factor_vars = pmc_factor_vars[['yearmonth','rmrf','smb','hml','rmw','cma','wml','pmc']]

carbon_beta_vars = pd.merge(cross_sectional_returns_data [['yearmonth','ticker','industry', 'ret']], pmc_factor_vars, how = 'left', on =['yearmonth'])

#%%

len_before = len(carbon_beta_vars)
carbon_beta_vars = carbon_beta_vars.dropna(subset=['ret', 'rmrf', 'smb', 'hml', 'rmw', 'cma', 'wml', 'pmc'], how='any')
print('Dropped: '+str(len_before-len(carbon_beta_vars)))


#%%
"Save carbon_beta_vars"
output_filename = 'cb_carbon_beta_vars.csv'
output_path = 'C:/Users/conno/OneDrive/University Study/Honours Thesis/cnolan-thesis/regression/regression variables/'
outputname = output_path + output_filename
carbon_beta_vars.to_csv(outputname, mode='w', index=False)
print("Exported File: " + outputname)

print("PMC - DONE")
print("RUN REGRESSION ON CARBON BETA VARS")

"RUN REGRESSION ON CARBON BETA VARS"
