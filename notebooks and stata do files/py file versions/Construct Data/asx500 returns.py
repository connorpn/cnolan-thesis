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
os.chdir('C:/Users/conno/OneDrive/University Study/Honours Thesis/cnolan-thesis/output')

asx500_all = pd.read_csv ('asx500_all.csv')


#%%

"monthly asx500 returns"

asx500 = asx500_all[['Ticker', 'Name', 'yearmonth', 'Market Cap\n','monthly return']]
asx500 

asx500 = asx500.rename(columns={'Market Cap\n': 'marketcap', 'monthly return':'ret'})

asx500['ret'] = asx500['ret'].replace({'--':np.nan})
asx500['marketcap'] = asx500['marketcap'].replace({'--':np.nan})

asx500['ret'] = asx500['ret'].astype(float)
asx500['marketcap'] = asx500['marketcap'].astype(float)


asx500['weighted_returns'] =  asx500['ret'] * (asx500['marketcap'] / asx500.groupby(['yearmonth'])['marketcap'].transform('sum'))
asx500['asx500_ret'] = asx500.groupby(['yearmonth'])['weighted_returns'].transform('sum')

asx500 = asx500[['yearmonth','asx500_ret']]
asx500 = asx500.drop_duplicates(subset=['yearmonth']).reset_index(drop=True)

asx500 = asx500.loc[(asx500['yearmonth'] >= 200807) & (asx500['yearmonth'] <= 202206)]

#%%

"Save asx_returns"
output_filename = 'asx500_returns.csv'
outputname = output_path + output_filename
asx500.to_csv(outputname, mode='w', index=False)
print("Exported File: " + outputname)
