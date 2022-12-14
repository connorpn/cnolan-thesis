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
asx500_carbon_beta = pd.read_csv ('C:/Users/conno/OneDrive/University Study/Honours Thesis/cnolan-thesis/regression/regression outputs/carbon beta/asx500_carbon_beta_regression_output.csv')

asx500_csr = pd.read_csv ('C:/Users/conno/OneDrive/University Study/Honours Thesis/cnolan-thesis./output/asx500_csr.csv')

#%%
'''
FORMATE ESTIMATION OF CARBON BETA
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
carbon_beta_csr = carbon_beta_csr.dropna(subset=['ret', 'ln_marketcap', 'bm', 'roe', 'leverage', 'investa', 'logppe', 'ppea'])
print('[other variables] Dropped: '+ str(len_before-len(carbon_beta_csr))+' From : '+ str(len_before)+' to ' + str(len(carbon_beta_csr)))

#%%
'''
carbon_beta_firm_characteristics_vars = carbon_beta_csr[['yearmonth','ticker','industry',
                                        'carbon_beta',
                                        'logsize', 'bm', 'leverage', 'mom', 'investa', 'roe', 'logppe', 'beta', 'volat', 'salesgr', 'epsgr',
                                        'log_scope1', 'log_scope2', 'log_total_emissions', 'log_energy_consumption', 'change_scope1', 'change_scope2', 'change_total_emissions', 'change_energy_consumption', 'scope1_int', 'scope2_int', 'total_emissions_int', 'energy_consumption_int',
                                        ]]

"Save carbon_beta_vars"
output_filename = 'carbon_beta_firm_characteristics_vars.csv'
output_path = 'C:/Users/conno/OneDrive/University Study/Honours Thesis/cnolan-thesis/regression/regression variables/'
outputname = output_path + output_filename
carbon_beta_firm_characteristics_vars.to_csv(outputname, mode='w', index=False)

'''
#%%

'''
pricing of carbon risk : using monthly returns + bolton controls
'''


asx500_pricing_carbon_risk = carbon_beta_csr

"Save pricing_carbon_risk"
output_filename = 'asx500_pricing_carbon_risk.csv'
output_path = 'C:/Users/conno/OneDrive/University Study/Honours Thesis/cnolan-thesis/regression/regression variables/'
outputname = output_path + output_filename
asx500_pricing_carbon_risk.to_csv(outputname, mode='w', index=False)



