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
RUN EXPORT CARBON PREMIUMS STATA FILE FIRST 
'''

#%%
"IMPORT DATA"

carbon_premium = pd.read_csv("C:/Users/conno/OneDrive/University Study/Honours Thesis/cnolan-thesis/regression/regression outputs/bolton replications/br_carbon_premium_ts.csv")
famafrench_factors = pd.read_csv ('C:/Users/conno/OneDrive/University Study/Honours Thesis/cnolan-thesis/output/famafrench_factors.csv')
rmrf = pd.read_csv("C:/Users/conno/OneDrive/University Study/Honours Thesis/cnolan-thesis./output/rmrf.csv")

#%%

carbon_premium_risk_factors = pd.merge(carbon_premium,famafrench_factors, how='left',on=['yearmonth'])


carbon_premium_risk_factors = carbon_premium_risk_factors.rename(columns = {'_b_log_scope1' :'log_scope1', '_b_log_scope2': 'log_scope2', '_b_log_total_emissions' : 'log_total_emissions', '_b_log_energy_consumption':'log_energy_consumption', '_b_change_scope1':'change_scope1', '_b_change_scope2':'change_scope2', '_b_change_total_emissions':'change_total_emissions', '_b_change_energy_consumption':'change_energy_consumption', '_b_scope1_int':'scope1_int', '_b_scope2_int':'scope2_int', '_b_total_emissions_int':'total_emissions_int', '_b_energy_consumption_int':'energy_consumption_int'})


carbon_premium_risk_factors = carbon_premium_risk_factors.drop_duplicates('yearmonth').reset_index(drop=True)

carbon_premium_risk_factors = pd.merge(carbon_premium_risk_factors, rmrf, on=['yearmonth'], how='left')
#%%

"Save carbon_premium_risk_factors"
output_filename = 'br_carbon_premium_risk_factors.csv'
output_path = 'C:/Users/conno/OneDrive/University Study/Honours Thesis/cnolan-thesis/regression/regression variables/'
outputname = output_path + output_filename
carbon_premium_risk_factors.to_csv(outputname, mode='w', index=False)
print("Exported File: " + outputname)

#%%
print("done")
print("RUN STATA - 4. CARBON PREMIUM AND RISK FACTORS")