import os
import pandas as pd
import numpy as np
from fuzzywuzzy import process

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

#THIS DATA IS COLLATED AND PROCESSED FROM NOTEBOOK: 1. Collate Data
nger_data = pd.read_csv('C:/Users/conno/OneDrive/University Study/Honours Thesis/cnolan-thesis/output/nger_data.csv',encoding = "ISO-8859-1")
ms_data = pd.read_csv ('C:/Users/conno/OneDrive/University Study/Honours Thesis/cnolan-thesis/output/ms_data.csv', encoding='latin1')


#%%

"FUZZY MATCH NGER AND MORNINGSTAR FIRMS NAMES (TAKES A LONG TIME)"

print("STARTING FUZZY MATCHING")

ms_firms = ms_data[['ticker', 'morningstar_name']]
ms_firms = ms_firms.drop_duplicates(subset=['morningstar_name'])

ms_firms_list = []
ms_firms_list = ms_data['morningstar_name'].unique().tolist()

nger_firms_list = []
nger_firms_list = nger_data['nger_name'].unique().tolist()


threshold = 95 #note: in preliminary analysis a threshold of 95 provided matching without mismatching 
names_response = []
for name in nger_firms_list:
    resp_match =  process.extractOne(name,ms_firms_list)
    if resp_match[1] > threshold:
         row = {'nger_name':name,'morningstar_name':resp_match[0], 'match_score':resp_match[1]}
         names_response.append(row)

print("FINISHED FUZZY MATCHING")
#%%

matched_firms = pd.DataFrame(names_response)

matched_firms_tickers = pd.merge(matched_firms[['nger_name', 'morningstar_name', 'match_score']],
                            ms_firms[['ticker', 'morningstar_name']],
                                          on = ['morningstar_name'],
                                          how = 'left')

matched_firms_tickers["matched"] = 1
matched_firms_tickers = matched_firms_tickers.reindex(columns=['nger_name', 'morningstar_name', 'ticker','matched','match_score'])

"Save Matched Firms File"
output_filename = 'matched_firms_tickers.csv'
outputname = output_path + output_filename
matched_firms_tickers.to_csv(outputname, mode='w')
print("Exported File: " + outputname)

#ticker list for datastream series search
matched_tickers = matched_firms_tickers['ticker']

"Save Matched Firms List File"
output_filename = 'matched_tickers.csv'
outputname = output_path + output_filename
matched_tickers.to_csv(outputname, mode='w', index=False)
print("Exported File: " + outputname)

#%%

"APPEND MATCHED DATA TO NGER DATA AND FILTER (MATCHED ONLY NGER DATA)"

nger_data_matched = pd.merge(nger_data[['year', 'nger_name', 'scope1', 'scope2', 'energy_consumption', 'total_emissions']], matched_firms_tickers[['nger_name', 'morningstar_name', 'match_score', 'ticker','matched']], on = ['nger_name'], how = 'left')
nger_data_matched = nger_data_matched.dropna(axis=0, how= 'any', subset=['matched'])
print(list(nger_data_matched))

nger_data_matched = nger_data_matched.reindex(columns=['year', 'nger_name', 'morningstar_name', 'ticker', 'match_score', 'matched', 'scope1', 'scope2', 'energy_consumption', 'total_emissions'])
nger_data_matched = nger_data_matched.reset_index(drop=True)

"Save Matched NGER Data"
output_filename = 'nger_data_matched.csv'
outputname = output_path + output_filename
nger_data_matched.to_csv(outputname, mode='w', index=False)
print("Exported File: " + outputname)

print('Number of Matched Firms:')
print(len(matched_firms_tickers))

#%%
print("CONSTRUCT SAMPLE (MATCH NGER FIRMS) DONE")
print("RUN - 3. CONSTRUCT CROSS SECTIONAL RETURNS")