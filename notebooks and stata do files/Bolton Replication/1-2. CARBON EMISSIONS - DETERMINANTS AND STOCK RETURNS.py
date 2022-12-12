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

cross_sectional_returns_data = pd.read_csv ('C:/Users/conno/OneDrive/University Study/Honours Thesis/cnolan-thesis/output/cross_sectional_returns_data.csv')

#%%
"regression variables for bolton replication- determinants of carbon emissions"

br_determinants_of_carbon_emissions = cross_sectional_returns_data[['year','ticker', 'industry',
                                                                    'log_scope1', 'log_scope2', 'log_total_emissions', 'log_energy_consumption', 'change_scope1', 'change_scope2', 'change_total_emissions', 'change_energy_consumption', 'scope1_int', 'scope2_int', 'total_emissions_int', 'energy_consumption_int',
                                                                    'logsize', 'bm', 'roe','leverage', 'investa','logppe','salesgr', 'epsgr']]

"Save br_determinants_of_carbon_emissions"
output_filename = 'br_determinants_of_carbon_emissions.csv'
output_path = 'C:/Users/conno/OneDrive/University Study/Honours Thesis/cnolan-thesis/regression/regression variables/'
outputname = output_path + output_filename
br_determinants_of_carbon_emissions.to_csv(outputname, mode='w', index=False)
print("Exported File: " + outputname)

#%%
"regression variables for bolton replication - carbon emissions and stock returns"

br_carbon_emissions_and_stock_returns = cross_sectional_returns_data [['yearmonth','ticker', 'industry',
                                                                       'ret',
                                                                       'log_scope1', 'log_scope2', 'log_total_emissions', 'log_energy_consumption', 'change_scope1', 'change_scope2', 'change_total_emissions', 'change_energy_consumption', 'scope1_int', 'scope2_int', 'total_emissions_int', 'energy_consumption_int',
                                                                       'logsize', 'bm', 'leverage', 'mom','investa','roe','logppe','beta','volat','salesgr', 'epsgr']]


"Save br_carbon_emissions_and_stock_returns"
output_filename = 'br_carbon_emissions_and_stock_returns.csv'
output_path = 'C:/Users/conno/OneDrive/University Study/Honours Thesis/cnolan-thesis/regression/regression variables/'
outputname = output_path + output_filename
br_carbon_emissions_and_stock_returns.to_csv(outputname, mode='w', index=False)
print("Exported File: " + outputname)
