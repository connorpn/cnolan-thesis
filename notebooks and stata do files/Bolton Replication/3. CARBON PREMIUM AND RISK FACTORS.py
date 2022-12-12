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

os.chdir("C:/Users/conno/OneDrive/University Study/Honours Thesis/cnolan-thesis/regression/regression outputs/bolton replications/carbon premiums")

cp_log_scope1_noind = pd.read_csv("cp_log_scope1_noind.csv")
cp_log_scope2_noind = pd.read_csv("cp_log_scope2_noind.csv")
cp_log_total_emissions_noind = pd.read_csv("cp_log_total_emissions_noind.csv")
cp_log_energy_consumption_noind = pd.read_csv("cp_log_energy_consumption_noind.csv")

cp_change_scope1_noind = pd.read_csv("cp_change_scope1_noind.csv")
cp_change_scope2_noind = pd.read_csv("cp_change_scope2_noind.csv")
cp_change_total_emissions_noind = pd.read_csv("cp_change_total_emissions_noind.csv")
cp_change_energy_consumption_noind = pd.read_csv("cp_change_energy_consumption_noind.csv")

cp_scope1_int_noind = pd.read_csv("cp_scope1_int_noind.csv")
cp_scope2_int_noind = pd.read_csv("cp_scope2_int_noind.csv")
cp_total_emissions_int_noind = pd.read_csv("cp_total_emissions_int_noind.csv")
cp_energy_consumption_int_noind = pd.read_csv("cp_energy_consumption_int_noind.csv")

cp_log_scope1_ind = pd.read_csv("cp_log_scope1_ind.csv")
cp_log_scope2_ind = pd.read_csv("cp_log_scope2_ind.csv")
cp_log_total_emissions_ind = pd.read_csv("cp_log_total_emissions_ind.csv")
cp_log_energy_consumption_ind = pd.read_csv("cp_log_energy_consumption_ind.csv")

cp_change_scope1_ind = pd.read_csv("cp_change_scope1_ind.csv")
cp_change_scope2_ind = pd.read_csv("cp_change_scope2_ind.csv")
cp_change_total_emissions_ind = pd.read_csv("cp_change_total_emissions_ind.csv")
cp_change_energy_consumption_ind = pd.read_csv("cp_change_energy_consumption_ind.csv")

cp_scope1_int_ind = pd.read_csv("cp_scope1_int_ind.csv")
cp_scope2_int_ind = pd.read_csv("cp_scope2_int_ind.csv")
cp_total_emissions_int_ind = pd.read_csv("cp_total_emissions_int_ind.csv")
cp_energy_consumption_int_ind = pd.read_csv("cp_energy_consumption_int_ind.csv")

os.chdir("C:/Users/conno/OneDrive/University Study/Honours Thesis/cnolan-thesis/output")

famafrench_factors = pd.read_csv("famafrench_factors.csv")



#%%

"COLLATE NO IND FILES"


no_ind= [cp_log_scope1_noind,cp_log_scope2_noind,cp_log_total_emissions_noind,cp_log_energy_consumption_noind,
          cp_change_scope1_noind,cp_change_scope2_noind,cp_change_total_emissions_noind,cp_change_energy_consumption_noind,
          cp_scope1_int_noind,cp_scope2_int_noind,cp_total_emissions_int_noind,cp_energy_consumption_int_noind]

no_ind_df = pd.concat(no_ind, ignore_index=True, sort=False)
no_ind_df=no_ind_df[['var','coef']]
no_ind_df['di']=1
no_ind_df = pd.pivot_table(no_ind_df, values = 'coef', index=['di'], columns = 'var').reset_index()
no_ind_df = no_ind_df.drop(['di','_cons', 'beta','logppe', 'logsize', 'winsor_bm', 'winsor_epsgr', 'winsor_investa', 'winsor_leverage', 'winsor_mom', 'winsor_roe', 'winsor_salesgr', 'winsor_volat'], axis=1)
no_ind_df['ind'] = 'noind'


ind= [cp_log_scope1_ind,cp_log_scope2_ind,cp_log_total_emissions_ind,cp_log_energy_consumption_ind,
          cp_change_scope1_ind,cp_change_scope2_ind,cp_change_total_emissions_ind,cp_change_energy_consumption_ind,
          cp_scope1_int_ind,cp_scope2_int_ind,cp_total_emissions_int_ind,cp_energy_consumption_int_ind]

ind_df = pd.concat(ind, ignore_index=True, sort=False)
ind_df=ind_df[['var','coef']]
ind_df['di']=1
ind_df = pd.pivot_table(ind_df, values = 'coef', index=['di'], columns = 'var').reset_index()
ind_df = ind_df.drop(['di','_cons', 'beta','logppe', 'logsize', 'winsor_bm', 'winsor_epsgr', 'winsor_investa', 'winsor_leverage', 'winsor_mom', 'winsor_roe', 'winsor_salesgr', 'winsor_volat'], axis=1)
ind_df['ind'] = 'ind'

cp = pd.concat([no_ind_df,ind_df],ignore_index=True, sort=False)


#%%

"MERGE FAMA FRENCH FACTORS"