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

cross_sectional_returns_data = pd.read_csv ('https://raw.githubusercontent.com/connorpn/cnolan-thesis/main/output/carbon_emissions_stock_returns_vars.csv')
ms_data = pd.read_csv ('https://raw.githubusercontent.com/connorpn/cnolan-thesis/main/output/ms_data.csv')
asx500_filtered = pd.read_csv ('https://raw.githubusercontent.com/connorpn/cnolan-thesis/main/output/asx500_filtered.csv')

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
asx500 = asx500.drop_duplicates(subset=['yearmonth'])

asx500 = asx500['yearmonth'] > 200906
asx500 = asx500['yearmonth'] < 202
#%%


#%%

#calculate monthly return
asx500_ret = asx500.resample('M').ffill()
asx500_ret = asx500_ret / asx500_ret.shift(1) - 1 

asx500_ret['asx500'] = asx500_ret['asx500'].replace(0, np.nan)

#reformat to multi column (year, month) index
asx500_ret = asx500_ret.reset_index()
asx500_ret['year'] = asx500_ret['date'].dt.strftime('%Y')
asx500_ret['month'] = asx500_ret['date'].dt.strftime('%m')


asx500_ret['asx500'] = asx500_ret.asx500.astype(float)

asx500_ret = asx500_ret.reset_index(drop=True)

asx500_ret['year'] = asx500_ret['year'].astype(int)
asx500_ret['month'] = asx500_ret['month'].astype(int)


#%%
pmc = pd.merge(pmc, asx500_ret[['year','month','asx500']], how='left', on=['year','month'])
pmc = pd.merge(pmc, marketcap, how='left', on=['ticker','year']) #add marketcap (end of year) to ret observations


'''
construct pmc for log_scope1
'''

pmc_log_scope1 = pmc[['ticker_year_month', 'ticker', 'year', 'month', 'marketcap','industry', 'ret', 'asx500', 'log_scope1', 'logsize', 'bm', 'leverage', 'mom', 'investa', 'roe', 'logppe', 'beta', 'volat', 'salesgr', 'epsgr']]

'''
note it says value wieghted portfolios
>this could be based on daily/monthly market cap
>will use the end of year market cap values for now
'''

pmc_log_scope1['weighted_returns'] =  pmc_log_scope1['ret'] * (pmc_log_scope1['marketcap'] / pmc_log_scope1.groupby(['year', 'month'])['marketcap'].transform('sum'))


pmc_log_scope1['portfolio_ret'] = pmc_log_scope1.groupby(['year', 'month'])['weighted_returns'].transform('sum')

pmc_log_scope1 = pmc_log_scope1[['year', 'month','portfolio_ret','asx500']]

pmc_log_scope1 = pmc_log_scope1.drop_duplicates(ignore_index=True)

#pmc_log_scope1 = pmc_log_scope1.pivot(index=['year','month'], columns='portfolio', values = 'portfolio_ret')

#pmc_log_scope1['pmc'] = ((pmc_log_scope1['sp'] + pmc_log_scope1['bp']) / 2) - ((pmc_log_scope1['sc'] + pmc_log_scope1['bc']) / 2)

pmc_log_scope1['pmc'] = pmc_log_scope1['portfolio_ret'] - pmc_log_scope1['asx500']

pmc_log_scope1 = pmc_log_scope1.reset_index()



'''
construct pmc for log_scope2
'''

pmc_log_scope2 = pmc[['ticker_year_month', 'ticker', 'year', 'month', 'marketcap','industry', 'ret', 'asx500', 'log_scope2', 'logsize', 'bm', 'leverage', 'mom', 'investa', 'roe', 'logppe', 'beta', 'volat', 'salesgr', 'epsgr']]

'''
note it says value wieghted portfolios
>this could be based on daily/monthly market cap
>will use the end of year market cap values for now
'''

pmc_log_scope2['weighted_returns'] =  pmc_log_scope2['ret'] * (pmc_log_scope2['marketcap'] / pmc_log_scope2.groupby(['year', 'month'])['marketcap'].transform('sum'))


pmc_log_scope2['portfolio_ret'] = pmc_log_scope2.groupby(['year', 'month'])['weighted_returns'].transform('sum')

pmc_log_scope2 = pmc_log_scope2[['year', 'month','portfolio_ret','asx500']]

pmc_log_scope2 = pmc_log_scope2.drop_duplicates(ignore_index=True)

#pmc_log_scope2 = pmc_log_scope2.pivot(index=['year','month'], columns='portfolio', values = 'portfolio_ret')

#pmc_log_scope2['pmc'] = ((pmc_log_scope2['sp'] + pmc_log_scope2['bp']) / 2) - ((pmc_log_scope2['sc'] + pmc_log_scope2['bc']) / 2)

pmc_log_scope2['pmc'] = pmc_log_scope2['portfolio_ret'] - pmc_log_scope2['asx500']

pmc_log_scope2 = pmc_log_scope2.reset_index()


'''
construct pmc for log_total_emissions
'''

pmc_log_total_emissions = pmc[['ticker_year_month', 'ticker', 'year', 'month', 'marketcap','industry', 'ret', 'asx500', 'log_total_emissions', 'logsize', 'bm', 'leverage', 'mom', 'investa', 'roe', 'logppe', 'beta', 'volat', 'salesgr', 'epsgr']]

'''
note it says value wieghted portfolios
>this could be based on daily/monthly market cap
>will use the end of year market cap values for now
'''

pmc_log_total_emissions['weighted_returns'] =  pmc_log_total_emissions['ret'] * (pmc_log_total_emissions['marketcap'] / pmc_log_total_emissions.groupby(['year', 'month'])['marketcap'].transform('sum'))


pmc_log_total_emissions['portfolio_ret'] = pmc_log_total_emissions.groupby(['year', 'month'])['weighted_returns'].transform('sum')

pmc_log_total_emissions = pmc_log_total_emissions[['year', 'month','portfolio_ret','asx500']]

pmc_log_total_emissions = pmc_log_total_emissions.drop_duplicates(ignore_index=True)

#pmc_log_total_emissions = pmc_log_total_emissions.pivot(index=['year','month'], columns='portfolio', values = 'portfolio_ret')

#pmc_log_total_emissions['pmc'] = ((pmc_log_total_emissions['sp'] + pmc_log_total_emissions['bp']) / 2) - ((pmc_log_total_emissions['sc'] + pmc_log_total_emissions['bc']) / 2)

pmc_log_total_emissions['pmc'] = pmc_log_total_emissions['portfolio_ret'] - pmc_log_total_emissions['asx500']

pmc_log_total_emissions = pmc_log_total_emissions.reset_index()


'''
construct pmc for log_energy_consumption
'''

pmc_log_energy_consumption = pmc[['ticker_year_month', 'ticker', 'year', 'month', 'marketcap','industry', 'ret', 'asx500', 'log_energy_consumption', 'logsize', 'bm', 'leverage', 'mom', 'investa', 'roe', 'logppe', 'beta', 'volat', 'salesgr', 'epsgr']]

'''
note it says value wieghted portfolios
>this could be based on daily/monthly market cap
>will use the end of year market cap values for now
'''

pmc_log_energy_consumption['weighted_returns'] =  pmc_log_energy_consumption['ret'] * (pmc_log_energy_consumption['marketcap'] / pmc_log_energy_consumption.groupby(['year', 'month'])['marketcap'].transform('sum'))


pmc_log_energy_consumption['portfolio_ret'] = pmc_log_energy_consumption.groupby(['year', 'month'])['weighted_returns'].transform('sum')

pmc_log_energy_consumption = pmc_log_energy_consumption[['year', 'month','portfolio_ret','asx500']]

pmc_log_energy_consumption = pmc_log_energy_consumption.drop_duplicates(ignore_index=True)

#pmc_log_energy_consumption = pmc_log_energy_consumption.pivot(index=['year','month'], columns='portfolio', values = 'portfolio_ret')

#pmc_log_energy_consumption['pmc'] = ((pmc_log_energy_consumption['sp'] + pmc_log_energy_consumption['bp']) / 2) - ((pmc_log_energy_consumption['sc'] + pmc_log_energy_consumption['bc']) / 2)

pmc_log_energy_consumption['pmc'] = pmc_log_energy_consumption['portfolio_ret'] - pmc_log_energy_consumption['asx500']

pmc_log_energy_consumption = pmc_log_energy_consumption.reset_index()


'''
construct pmc for change_scope1
'''

pmc_change_scope1 = pmc[['ticker_year_month', 'ticker', 'year', 'month', 'marketcap','industry', 'ret', 'asx500', 'change_scope1', 'logsize', 'bm', 'leverage', 'mom', 'investa', 'roe', 'logppe', 'beta', 'volat', 'salesgr', 'epsgr']]

'''
note it says value wieghted portfolios
>this could be based on daily/monthly market cap
>will use the end of year market cap values for now
'''

pmc_change_scope1['weighted_returns'] =  pmc_change_scope1['ret'] * (pmc_change_scope1['marketcap'] / pmc_change_scope1.groupby(['year', 'month'])['marketcap'].transform('sum'))


pmc_change_scope1['portfolio_ret'] = pmc_change_scope1.groupby(['year', 'month'])['weighted_returns'].transform('sum')

pmc_change_scope1 = pmc_change_scope1[['year', 'month','portfolio_ret','asx500']]

pmc_change_scope1 = pmc_change_scope1.drop_duplicates(ignore_index=True)

#pmc_change_scope1 = pmc_change_scope1.pivot(index=['year','month'], columns='portfolio', values = 'portfolio_ret')

#pmc_change_scope1['pmc'] = ((pmc_change_scope1['sp'] + pmc_change_scope1['bp']) / 2) - ((pmc_change_scope1['sc'] + pmc_change_scope1['bc']) / 2)

pmc_change_scope1['pmc'] = pmc_change_scope1['portfolio_ret'] - pmc_change_scope1['asx500']

pmc_change_scope1 = pmc_change_scope1.reset_index()



'''
construct pmc for change_scope2
'''

pmc_change_scope2 = pmc[['ticker_year_month', 'ticker', 'year', 'month', 'marketcap','industry', 'ret', 'asx500', 'change_scope2', 'logsize', 'bm', 'leverage', 'mom', 'investa', 'roe', 'logppe', 'beta', 'volat', 'salesgr', 'epsgr']]

'''
note it says value wieghted portfolios
>this could be based on daily/monthly market cap
>will use the end of year market cap values for now
'''

pmc_change_scope2['weighted_returns'] =  pmc_change_scope2['ret'] * (pmc_change_scope2['marketcap'] / pmc_change_scope2.groupby(['year', 'month'])['marketcap'].transform('sum'))


pmc_change_scope2['portfolio_ret'] = pmc_change_scope2.groupby(['year', 'month'])['weighted_returns'].transform('sum')

pmc_change_scope2 = pmc_change_scope2[['year', 'month','portfolio_ret','asx500']]

pmc_change_scope2 = pmc_change_scope2.drop_duplicates(ignore_index=True)

#pmc_change_scope2 = pmc_change_scope2.pivot(index=['year','month'], columns='portfolio', values = 'portfolio_ret')

#pmc_change_scope2['pmc'] = ((pmc_change_scope2['sp'] + pmc_change_scope2['bp']) / 2) - ((pmc_change_scope2['sc'] + pmc_change_scope2['bc']) / 2)

pmc_change_scope2['pmc'] = pmc_change_scope2['portfolio_ret'] - pmc_change_scope2['asx500']

pmc_change_scope2 = pmc_change_scope2.reset_index()




'''
construct pmc for change_total_emissions
'''

pmc_change_total_emissions = pmc[['ticker_year_month', 'ticker', 'year', 'month', 'marketcap','industry', 'ret', 'asx500', 'change_total_emissions', 'logsize', 'bm', 'leverage', 'mom', 'investa', 'roe', 'logppe', 'beta', 'volat', 'salesgr', 'epsgr']]

'''
note it says value wieghted portfolios
>this could be based on daily/monthly market cap
>will use the end of year market cap values for now
'''

pmc_change_total_emissions['weighted_returns'] =  pmc_change_total_emissions['ret'] * (pmc_change_total_emissions['marketcap'] / pmc_change_total_emissions.groupby(['year', 'month'])['marketcap'].transform('sum'))


pmc_change_total_emissions['portfolio_ret'] = pmc_change_total_emissions.groupby(['year', 'month'])['weighted_returns'].transform('sum')

pmc_change_total_emissions = pmc_change_total_emissions[['year', 'month','portfolio_ret','asx500']]

pmc_change_total_emissions = pmc_change_total_emissions.drop_duplicates(ignore_index=True)

#pmc_change_total_emissions = pmc_change_total_emissions.pivot(index=['year','month'], columns='portfolio', values = 'portfolio_ret')

#pmc_change_total_emissions['pmc'] = ((pmc_change_total_emissions['sp'] + pmc_change_total_emissions['bp']) / 2) - ((pmc_change_total_emissions['sc'] + pmc_change_total_emissions['bc']) / 2)

pmc_change_total_emissions['pmc'] = pmc_change_total_emissions['portfolio_ret'] - pmc_change_total_emissions['asx500']

pmc_change_total_emissions = pmc_change_total_emissions.reset_index()



'''
construct pmc for change_energy_consumption
'''

pmc_change_energy_consumption = pmc[['ticker_year_month', 'ticker', 'year', 'month', 'marketcap','industry', 'ret', 'asx500', 'change_energy_consumption', 'logsize', 'bm', 'leverage', 'mom', 'investa', 'roe', 'logppe', 'beta', 'volat', 'salesgr', 'epsgr']]

'''
note it says value wieghted portfolios
>this could be based on daily/monthly market cap
>will use the end of year market cap values for now
'''

pmc_change_energy_consumption['weighted_returns'] =  pmc_change_energy_consumption['ret'] * (pmc_change_energy_consumption['marketcap'] / pmc_change_energy_consumption.groupby(['year', 'month'])['marketcap'].transform('sum'))


pmc_change_energy_consumption['portfolio_ret'] = pmc_change_energy_consumption.groupby(['year', 'month'])['weighted_returns'].transform('sum')

pmc_change_energy_consumption = pmc_change_energy_consumption[['year', 'month','portfolio_ret','asx500']]

pmc_change_energy_consumption = pmc_change_energy_consumption.drop_duplicates(ignore_index=True)

#pmc_change_energy_consumption = pmc_change_energy_consumption.pivot(index=['year','month'], columns='portfolio', values = 'portfolio_ret')

#pmc_change_energy_consumption['pmc'] = ((pmc_change_energy_consumption['sp'] + pmc_change_energy_consumption['bp']) / 2) - ((pmc_change_energy_consumption['sc'] + pmc_change_energy_consumption['bc']) / 2)

pmc_change_energy_consumption['pmc'] = pmc_change_energy_consumption['portfolio_ret'] - pmc_change_energy_consumption['asx500']

pmc_change_energy_consumption = pmc_change_energy_consumption.reset_index()


'''
construct pmc for scope1_int
'''

pmc_scope1_int = pmc[['ticker_year_month', 'ticker', 'year', 'month', 'marketcap','industry', 'ret', 'asx500', 'scope1_int', 'logsize', 'bm', 'leverage', 'mom', 'investa', 'roe', 'logppe', 'beta', 'volat', 'salesgr', 'epsgr']]

'''
note it says value wieghted portfolios
>this could be based on daily/monthly market cap
>will use the end of year market cap values for now
'''

pmc_scope1_int['weighted_returns'] =  pmc_scope1_int['ret'] * (pmc_scope1_int['marketcap'] / pmc_scope1_int.groupby(['year', 'month'])['marketcap'].transform('sum'))


pmc_scope1_int['portfolio_ret'] = pmc_scope1_int.groupby(['year', 'month'])['weighted_returns'].transform('sum')

pmc_scope1_int = pmc_scope1_int[['year', 'month','portfolio_ret','asx500']]

pmc_scope1_int = pmc_scope1_int.drop_duplicates(ignore_index=True)

#pmc_scope1_int = pmc_scope1_int.pivot(index=['year','month'], columns='portfolio', values = 'portfolio_ret')

#pmc_scope1_int['pmc'] = ((pmc_scope1_int['sp'] + pmc_scope1_int['bp']) / 2) - ((pmc_scope1_int['sc'] + pmc_scope1_int['bc']) / 2)

pmc_scope1_int['pmc'] = pmc_scope1_int['portfolio_ret'] - pmc_scope1_int['asx500']

pmc_scope1_int = pmc_scope1_int.reset_index()



'''
construct pmc for scope2_int
'''

pmc_scope2_int = pmc[['ticker_year_month', 'ticker', 'year', 'month', 'marketcap','industry', 'ret', 'asx500', 'scope2_int', 'logsize', 'bm', 'leverage', 'mom', 'investa', 'roe', 'logppe', 'beta', 'volat', 'salesgr', 'epsgr']]

'''
note it says value wieghted portfolios
>this could be based on daily/monthly market cap
>will use the end of year market cap values for now
'''

pmc_scope2_int['weighted_returns'] =  pmc_scope2_int['ret'] * (pmc_scope2_int['marketcap'] / pmc_scope2_int.groupby(['year', 'month'])['marketcap'].transform('sum'))


pmc_scope2_int['portfolio_ret'] = pmc_scope2_int.groupby(['year', 'month'])['weighted_returns'].transform('sum')

pmc_scope2_int = pmc_scope2_int[['year', 'month','portfolio_ret','asx500']]

pmc_scope2_int = pmc_scope2_int.drop_duplicates(ignore_index=True)

#pmc_scope2_int = pmc_scope2_int.pivot(index=['year','month'], columns='portfolio', values = 'portfolio_ret')

#pmc_scope2_int['pmc'] = ((pmc_scope2_int['sp'] + pmc_scope2_int['bp']) / 2) - ((pmc_scope2_int['sc'] + pmc_scope2_int['bc']) / 2)

pmc_scope2_int['pmc'] = pmc_scope2_int['portfolio_ret'] - pmc_scope2_int['asx500']

pmc_scope2_int = pmc_scope2_int.reset_index()




'''
construct pmc for total_emissions_int
'''

pmc_total_emissions_int = pmc[['ticker_year_month', 'ticker', 'year', 'month', 'marketcap','industry', 'ret', 'asx500', 'total_emissions_int', 'logsize', 'bm', 'leverage', 'mom', 'investa', 'roe', 'logppe', 'beta', 'volat', 'salesgr', 'epsgr']]

'''
note it says value wieghted portfolios
>this could be based on daily/monthly market cap
>will use the end of year market cap values for now
'''

pmc_total_emissions_int['weighted_returns'] =  pmc_total_emissions_int['ret'] * (pmc_total_emissions_int['marketcap'] / pmc_total_emissions_int.groupby(['year', 'month'])['marketcap'].transform('sum'))


pmc_total_emissions_int['portfolio_ret'] = pmc_total_emissions_int.groupby(['year', 'month'])['weighted_returns'].transform('sum')

pmc_total_emissions_int = pmc_total_emissions_int[['year', 'month','portfolio_ret','asx500']]

pmc_total_emissions_int = pmc_total_emissions_int.drop_duplicates(ignore_index=True)

#pmc_total_emissions_int = pmc_total_emissions_int.pivot(index=['year','month'], columns='portfolio', values = 'portfolio_ret')

#pmc_total_emissions_int['pmc'] = ((pmc_total_emissions_int['sp'] + pmc_total_emissions_int['bp']) / 2) - ((pmc_total_emissions_int['sc'] + pmc_total_emissions_int['bc']) / 2)

pmc_total_emissions_int['pmc'] = pmc_total_emissions_int['portfolio_ret'] - pmc_total_emissions_int['asx500']

pmc_total_emissions_int = pmc_total_emissions_int.reset_index()



'''
construct pmc for energy_consumption_int
'''

pmc_energy_consumption_int = pmc[['ticker_year_month', 'ticker', 'year', 'month', 'marketcap','industry', 'ret', 'asx500', 'energy_consumption_int', 'logsize', 'bm', 'leverage', 'mom', 'investa', 'roe', 'logppe', 'beta', 'volat', 'salesgr', 'epsgr']]

'''
note it says value wieghted portfolios
>this could be based on daily/monthly market cap
>will use the end of year market cap values for now
'''

pmc_energy_consumption_int['weighted_returns'] =  pmc_energy_consumption_int['ret'] * (pmc_energy_consumption_int['marketcap'] / pmc_energy_consumption_int.groupby(['year', 'month'])['marketcap'].transform('sum'))


pmc_energy_consumption_int['portfolio_ret'] = pmc_energy_consumption_int.groupby(['year', 'month'])['weighted_returns'].transform('sum')

pmc_energy_consumption_int = pmc_energy_consumption_int[['year', 'month','portfolio_ret','asx500']]

pmc_energy_consumption_int = pmc_energy_consumption_int.drop_duplicates(ignore_index=True)

#pmc_energy_consumption_int = pmc_energy_consumption_int.pivot(index=['year','month'], columns='portfolio', values = 'portfolio_ret')

#pmc_energy_consumption_int['pmc'] = ((pmc_energy_consumption_int['sp'] + pmc_energy_consumption_int['bp']) / 2) - ((pmc_energy_consumption_int['sc'] + pmc_energy_consumption_int['bc']) / 2)

pmc_energy_consumption_int['pmc'] = pmc_energy_consumption_int['portfolio_ret'] - pmc_energy_consumption_int['asx500']

pmc_energy_consumption_int = pmc_energy_consumption_int.reset_index()


"Save pmc_log_scope1 PMC factor"
output_filename = 'pmc_log_scope1.csv'
outputname = output_path + output_filename
pmc_log_scope1.to_csv(outputname, mode='w', index=False)
print("Exported File: " + outputname)


"Save pmc_log_scope2 PMC factor"
output_filename = 'pmc_log_scope2.csv'
outputname = output_path + output_filename
pmc_log_scope2.to_csv(outputname, mode='w', index=False)
print("Exported File: " + outputname)

"Save pmc_log_total_emissions PMC factor"
output_filename = 'pmc_log_total_emissions.csv'
outputname = output_path + output_filename
pmc_log_total_emissions.to_csv(outputname, mode='w', index=False)
print("Exported File: " + outputname)

"Save pmc_log_energy_consumption PMC factor"
output_filename = 'pmc_log_energy_consumption.csv'
outputname = output_path + output_filename
pmc_log_energy_consumption.to_csv(outputname, mode='w', index=False)
print("Exported File: " + outputname)


"Save pmc_change_scope1 PMC factor"
output_filename = 'pmc_change_scope1.csv'
outputname = output_path + output_filename
pmc_change_scope1.to_csv(outputname, mode='w', index=False)
print("Exported File: " + outputname)

"Save pmc_change_scope2 PMC factor"
output_filename = 'pmc_change_scope2.csv'
outputname = output_path + output_filename
pmc_change_scope2.to_csv(outputname, mode='w', index=False)
print("Exported File: " + outputname)

"Save pmc_change_total_emissions PMC factor"
output_filename = 'pmc_change_total_emissions.csv'
outputname = output_path + output_filename
pmc_change_total_emissions.to_csv(outputname, mode='w', index=False)
print("Exported File: " + outputname)

"Save pmc_change_energy_consumption PMC factor"
output_filename = 'pmc_change_energy_consumption.csv'
outputname = output_path + output_filename
pmc_change_energy_consumption.to_csv(outputname, mode='w', index=False)
print("Exported File: " + outputname)


"Save pmc_scope1_int PMC factor"
output_filename = 'pmc_scope1_int.csv'
outputname = output_path + output_filename
pmc_scope1_int.to_csv(outputname, mode='w', index=False)
print("Exported File: " + outputname)

"Save pmc_scope2_int PMC factor"
output_filename = 'pmc_scope2_int.csv'
outputname = output_path + output_filename
pmc_scope2_int.to_csv(outputname, mode='w', index=False)
print("Exported File: " + outputname)

"Save pmc_total_emissions_int PMC factor"
output_filename = 'pmc_total_emissions_int.csv'
outputname = output_path + output_filename
pmc_total_emissions_int.to_csv(outputname, mode='w', index=False)
print("Exported File: " + outputname)

"Save pmc_energy_consumption_int PMC factor"
output_filename = 'pmc_energy_consumption_int.csv'
outputname = output_path + output_filename
pmc_energy_consumption_int.to_csv(outputname, mode='w', index=False)
print("Exported File: " + outputname)

print('Notebook Finish')