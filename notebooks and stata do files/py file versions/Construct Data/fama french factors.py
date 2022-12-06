"collate fama french factors"

"IMPORT MODULES"
import os
import pandas as pd
import numpy as np

#%%

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
"import files"
os.chdir('C:/Users/conno/OneDrive/University Study/Honours Thesis/cnolan-thesis/data')

famafrench = pd.read_csv ('Asia_Pacific_ex_Japan_5_Factors.csv')
famafrench_wml = pd.read_csv ('Asia_Pacific_ex_Japan_MOM_Factor.csv')
exchange_rate = pd.read_csv ('usdaud_exchange_rate.csv')

#%%
famafrench = pd.merge(famafrench,famafrench_wml[['yearmonth','wml']], how = 'left', on=['yearmonth'])

famafrench = famafrench.loc[(famafrench['yearmonth'] >= 200807) & (famafrench['yearmonth'] <= 202206)]

famafrench = famafrench[['yearmonth', 'year', 'month', 'smb', 'hml', 'rmw', 'cma', 'wml']]

#%%
"convert to aud"

" = ( 1 + usd_returns) * (1 + (USD/AUD - 1)"

famafrench = pd.merge(famafrench,exchange_rate[['yearmonth','exchange_return']],how = 'left', on = 'yearmonth')


famafrench_factors = ['smb','hml','rmw','cma','wml']
for i in famafrench_factors:
    famafrench[i] = famafrench[i] / 100
    famafrench[i] = ((1 + famafrench[i]) * (1 + famafrench['exchange_return'])) - 1

famafrench = famafrench[['yearmonth', 'year', 'month', 'smb', 'hml', 'rmw', 'cma', 'wml']]

"Save famafrench"
output_filename = 'famafrench_factors.csv'
outputname = output_path + output_filename
famafrench.to_csv(outputname, mode='w', index=False)
print("Exported File: " + outputname)
