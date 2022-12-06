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
asx500 = asx500.drop_duplicates(subset=['yearmonth']).reset_index(drop=True)

asx500 = asx500.loc[(asx500['yearmonth'] >= 200807) & (asx500['yearmonth'] <= 202206)]

#%%

pmc = cross_sectional_returns_data[['ret', 'yearmonth']]
