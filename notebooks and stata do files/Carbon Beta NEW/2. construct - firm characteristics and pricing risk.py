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
#FROM REGRESSION ON CARBON BETA VARS
asx500_carbon_beta = pd.read_csv ("C:/Users/conno/OneDrive/University Study/Honours Thesis/cnolan-thesis/regression/regression outputs/carbon beta/cb_asx500_carbon_beta_regression_output.csv")
nger_carbon_beta = pd.read_csv ("C:/Users/conno/OneDrive/University Study/Honours Thesis/cnolan-thesis/regression/regression outputs/carbon beta/carbon_beta_regression_output.csv")
asx500_csr = pd.read_csv ('C:/Users/conno/OneDrive/University Study/Honours Thesis/cnolan-thesis/output/asx500_csr.csv')
cb_nger_csr = pd.read_csv('C:/Users/conno/OneDrive/University Study/Honours Thesis/cnolan-thesis/output/cb_csr_nger.csv')
cross_sectional_returns_data = pd.read_csv ('C:/Users/conno/OneDrive/University Study/Honours Thesis/cnolan-thesis/output/cross_sectional_returns_data.csv')
industry = pd.read_csv ('C:/Users/conno/OneDrive/University Study/Honours Thesis/cnolan-thesis/data/ds_ticker_industry.csv')
#%%
'''
FORMATE ESTIMATION OF CARBON BETA ASX 500
'''


"Format Data"

asx500_carbon_beta = asx500_carbon_beta[['yearmonth','ticker', '_b_winsor_pmc']].dropna(subset=['_b_winsor_pmc'])
asx500_carbon_beta = asx500_carbon_beta.rename(columns={'_b_winsor_pmc': 'carbon_beta'})
asx500_carbon_beta = asx500_carbon_beta.sort_values(by=['carbon_beta']).reset_index(drop=True)

'''
NOTE: FOR SOME REASON THERE ARE 9 FIRMS THAT DONT OUTPUT REGRESSION RESULTS I.E. GIVE US A CARBON BETA
'''



carbon_beta_csr = pd.merge(asx500_csr, asx500_carbon_beta, on=['yearmonth','ticker'], how ='left')

len_before = len(carbon_beta_csr)
carbon_beta_csr = carbon_beta_csr.dropna(subset=['carbon_beta'])
print('[dropna carbon_beta] Dropped: '+ str(len_before-len(carbon_beta_csr))+' From : '+ str(len_before)+' to ' + str(len(carbon_beta_csr)))

len_before = len(carbon_beta_csr)
carbon_beta_csr = carbon_beta_csr.dropna(subset=['ret', 'ln_marketcap', 'bm', 'roe', 'leverage', 'investa', 'logppe', 'ppea','beta','mom'])
print('[other variables] Dropped: '+ str(len_before-len(carbon_beta_csr))+' From : '+ str(len_before)+' to ' + str(len(carbon_beta_csr)))

#%%
'''
FORMATE ESTIMATION OF CARBON BETA NGER
'''


"Format Data"

nger_carbon_beta = nger_carbon_beta[['yearmonth','ticker', '_b_winsor_pmc']].dropna(subset=['_b_winsor_pmc'])
nger_carbon_beta = nger_carbon_beta.rename(columns={'_b_winsor_pmc': 'carbon_beta'})
nger_carbon_beta = nger_carbon_beta.sort_values(by=['carbon_beta']).reset_index(drop=True)

'''
NOTE: FOR SOME REASON THERE ARE 9 FIRMS THAT DONT OUTPUT REGRESSION RESULTS I.E. GIVE US A CARBON BETA
'''


nger_carbon_beta_csr = pd.merge(cb_nger_csr, nger_carbon_beta, on=['yearmonth','ticker'], how ='left')

len_before = len(nger_carbon_beta_csr)
nger_carbon_beta_csr = nger_carbon_beta_csr.dropna(subset=['carbon_beta'])
print('[dropna carbon_beta] Dropped: '+ str(len_before-len(nger_carbon_beta_csr))+' From : '+ str(len_before)+' to ' + str(len(nger_carbon_beta_csr)))

len_before = len(nger_carbon_beta_csr)
nger_carbon_beta_csr = nger_carbon_beta_csr.dropna(subset=['ln_marketcap', 'bm', 'roe', 'leverage', 'investa', 'logppe', 'ppea'])
print('[other variables] Dropped: '+ str(len_before-len(nger_carbon_beta_csr))+' From : '+ str(len_before)+' to ' + str(len(nger_carbon_beta_csr)))


#%%
"carbon beta and firrm characteristics "


cb_firm_characteristics = pd.merge(nger_carbon_beta_csr, cross_sectional_returns_data[['yearmonth','ticker','industry','log_scope1', 'log_scope2', 'log_total_emissions', 'log_energy_consumption', 'change_scope1', 'change_scope2', 'change_total_emissions', 'change_energy_consumption', 'scope1_int', 'scope2_int', 'total_emissions_int', 'energy_consumption_int']],
                                   how='left',
                                   on=['yearmonth','ticker'])
cb_firm_characteristics = cb_firm_characteristics.rename(columns={"carbon_beta": "nger_carbon_beta"})

merge_nger_carbon_beta_csr = carbon_beta_csr
merge_nger_carbon_beta_csr = merge_nger_carbon_beta_csr.rename(columns={"carbon_beta":"asx500_carbon_beta"})


cb_firm_characteristics_merged = pd.concat([cb_firm_characteristics, merge_nger_carbon_beta_csr], axis=0, ignore_index=True)

cb_firm_characteristics_output = cb_firm_characteristics_merged[['yearmonth', 'ticker','industry','nger_carbon_beta','asx500_carbon_beta', 
                                   'ln_marketcap','bm', 'leverage', 'investa', 'logppe', 'ppea', 'roe',
                                   'log_scope1', 'log_scope2', 'log_total_emissions', 'log_energy_consumption', 'change_scope1', 'change_scope2', 'change_total_emissions', 'change_energy_consumption', 'scope1_int', 'scope2_int', 'total_emissions_int', 'energy_consumption_int']]


"Save cb_firm_characteristics_merged"
output_filename = 'cb_firm_characteristics_vars.csv'
output_path = 'C:/Users/conno/OneDrive/University Study/Honours Thesis/cnolan-thesis/regression/regression variables/'
outputname = output_path + output_filename
cb_firm_characteristics_output.to_csv(outputname, mode='w', index=False)
print("Exported File: " + outputname)



#%%

'''
pricing of carbon risk : using monthly returns + bolton controls
'''


asx500_pricing_carbon_risk = carbon_beta_csr

"Save pricing_carbon_risk"
output_filename = 'cb_asx500_pricing_carbon_risk.csv'
output_path = 'C:/Users/conno/OneDrive/University Study/Honours Thesis/cnolan-thesis/regression/regression variables/'
outputname = output_path + output_filename
asx500_pricing_carbon_risk.to_csv(outputname, mode='w', index=False)
print("Exported File: " + outputname)




