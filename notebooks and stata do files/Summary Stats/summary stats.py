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

"IMPORT DATA"

csr = pd.read_csv("C:/Users/conno/OneDrive/University Study/Honours Thesis/cnolan-thesis/output/cross_sectional_returns_data.csv")
ff = pd.read_csv ("C:/Users/conno/OneDrive/University Study/Honours Thesis/cnolan-thesis/output/famafrench_factors.csv")
carbon_beta = pd.read_csv ('C:/Users/conno/OneDrive/University Study/Honours Thesis/cnolan-thesis/regression/regression outputs/carbon beta/carbon_beta_regression_output.csv')
#%%

csr_ff = pd.merge(csr, ff[['yearmonth','smb', 'hml', 'rmw', 'cma', 'wml']],how='outer',on=['yearmonth'])

carbon_beta = carbon_beta.rename(columns={'_b_winsor_pmc': 'carbon_beta'})
carbon_beta = carbon_beta[['carbon_beta']] 
carbon_beta = carbon_beta.drop_duplicates(subset=['carbon_beta']).dropna().reset_index(drop=True)


csr_ff_cb = csr_ff.join(carbon_beta)

summ_stats = csr_ff_cb[['log_scope1', 'log_scope2', 'log_total_emissions', 'log_energy_consumption', 'change_scope1', 'change_scope2', 'change_total_emissions', 'change_energy_consumption', 'scope1_int', 'scope2_int', 'total_emissions_int', 'energy_consumption_int',
                     'carbon_beta','ret','logsize', 'bm', 'leverage', 'mom', 'investa', 'roe', 'logppe', 'beta', 'volat', 'salesgr', 'epsgr',
                     'smb', 'hml', 'rmw', 'cma', 'wml']]

"Save summ_stats"
output_filename = 'summ_stats.csv'
output_path = 'C:/Users/conno/OneDrive/University Study/Honours Thesis/cnolan-thesis/summary stats/'
outputname = output_path + output_filename
summ_stats.to_csv(outputname, mode='w', index=False)
