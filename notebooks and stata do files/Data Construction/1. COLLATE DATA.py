import pandas as pd
import numpy as np
import os
import requests
import io
import re
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

'''
    NGER EMISSIONS DATA
'''

"IMPORT DATA"
#NGER Greenhouse Gas and Energy Information by Corporation
nger_2009 = pd.read_csv('C:/Users/conno/OneDrive/University Study/Honours Thesis/cnolan-thesis/data/NGER_GHGANDENERGYINFO_RC_2009.csv',encoding = "ISO-8859-1")
nger_2010 = pd.read_csv('C:/Users/conno/OneDrive/University Study/Honours Thesis/cnolan-thesis/data/NGER_GHGANDENERGYINFO_RC_2010.csv',encoding = "ISO-8859-1")
nger_2011 = pd.read_csv('C:/Users/conno/OneDrive/University Study/Honours Thesis/cnolan-thesis/data/NGER_GHGANDENERGYINFO_RC_2011.csv',encoding = "ISO-8859-1")
nger_2012 = pd.read_csv('C:/Users/conno/OneDrive/University Study/Honours Thesis/cnolan-thesis/data/NGER_GHGANDENERGYINFO_RC_2012.csv',encoding = "ISO-8859-1")
nger_2013 = pd.read_csv('C:/Users/conno/OneDrive/University Study/Honours Thesis/cnolan-thesis/data/NGER_GHGANDENERGYINFO_RC_2013.csv',encoding = "ISO-8859-1")
nger_2014 = pd.read_csv('C:/Users/conno/OneDrive/University Study/Honours Thesis/cnolan-thesis/data/NGER_GHGANDENERGYINFO_RC_2014.csv',encoding = "ISO-8859-1")
nger_2015 = pd.read_csv('C:/Users/conno/OneDrive/University Study/Honours Thesis/cnolan-thesis/data/NGER_GHGANDENERGYINFO_RC_2015.csv',encoding = "ISO-8859-1")
nger_2016 = pd.read_csv('C:/Users/conno/OneDrive/University Study/Honours Thesis/cnolan-thesis/data/NGER_GHGANDENERGYINFO_RC_2016.csv',encoding = "ISO-8859-1")
nger_2017 = pd.read_csv('C:/Users/conno/OneDrive/University Study/Honours Thesis/cnolan-thesis/data/NGER_GHGANDENERGYINFO_RC_2017.csv',encoding = "ISO-8859-1")
nger_2018 = pd.read_csv('C:/Users/conno/OneDrive/University Study/Honours Thesis/cnolan-thesis/data/NGER_GHGANDENERGYINFO_RC_2018.csv',encoding = "ISO-8859-1")
nger_2019 = pd.read_csv('C:/Users/conno/OneDrive/University Study/Honours Thesis/cnolan-thesis/data/NGER_GHGANDENERGYINFO_RC_2019.csv',encoding = "ISO-8859-1")
nger_2020 = pd.read_csv('C:/Users/conno/OneDrive/University Study/Honours Thesis/cnolan-thesis/data/NGER_GHGANDENERGYINFO_RC_2020.csv',encoding = "ISO-8859-1")
nger_2021 = pd.read_csv('C:/Users/conno/OneDrive/University Study/Honours Thesis/cnolan-thesis/data/NGER_GHGANDENERGYINFO_RC_2021.csv',encoding = "ISO-8859-1")

"COLLATE DATA"
"Keep only Firm Name, Scope 1 Emissions, Scope 2 Emissions, and Energy Consumption Columns"
nger_2012 = nger_2012.drop(nger_2012.columns[[3]],axis=1)
nger_2013 = nger_2013.drop(nger_2013.columns[[4]],axis=1)
nger_2014 = nger_2014.drop(nger_2014.columns[[1,5]],axis=1)
nger_2015 = nger_2015.drop(nger_2015.columns[[1,5]],axis=1)
nger_2016 = nger_2016.drop(nger_2016.columns[[1,5]],axis=1)
nger_2017 = nger_2017.drop(nger_2017.columns[[1,5]],axis=1)
nger_2018 = nger_2018.drop(nger_2018.columns[[1,5]],axis=1)
nger_2019 = nger_2019.drop(nger_2019.columns[[1,5]],axis=1)
nger_2020 = nger_2020.drop(nger_2020.columns[[1,5]],axis=1)
nger_2021 = nger_2021.drop(nger_2021.columns[[1,5]],axis=1)


"Standarize Headings"

nger_list = [nger_2009,nger_2010,nger_2011,nger_2012,nger_2013,nger_2014,nger_2015,nger_2016,nger_2017,nger_2018,nger_2019,nger_2020,nger_2021]

def standard_names(dataset):
    
    dataset.columns = ['firm_name', 'scope1', 'scope2','energy_consumption']

for i in nger_list:
    standard_names(i)


"Add Year To Datasets"
#add in year
def add_year(dataset,year):
    dataset.insert(0, 'year', year)
#Registered Corporation Datasets
add_year(nger_2009,2009)
add_year(nger_2010,2010)
add_year(nger_2011,2011)
add_year(nger_2012,2012)
add_year(nger_2013,2013)
add_year(nger_2014,2014)
add_year(nger_2015,2015)
add_year(nger_2016,2016)
add_year(nger_2017,2017)
add_year(nger_2018,2018)
add_year(nger_2019,2019)
add_year(nger_2020,2020)
add_year(nger_2021,2021)



"Combined Datasets"
nger_data = pd.DataFrame(columns=['year', 'corporation', 'scope1', 'scope2', 'energy_consumption','total_emissions'])
nger_list = [nger_2009,nger_2010,nger_2011,nger_2012,nger_2013,nger_2014,nger_2015,nger_2016,nger_2017,nger_2018,nger_2019,nger_2020,nger_2021]
nger_data = pd.concat(nger_list)
print(list(nger_data))


"CLEAN UP NGER DATA"

"Clean up nger_data"

#remove comma's from emissions values 
nger_data['scope1'] = nger_data['scope1'].replace(",", "", regex=True)
nger_data['scope2'] = nger_data['scope2'].replace(",", "", regex=True)
#nger_data['total_emissions'] = nger_data['total_emissions'].replace(",", "", regex=True)
nger_data['energy_consumption'] = nger_data['energy_consumption'].replace(",", "", regex=True)

#remove spaces's from emissions values 
nger_data['scope1'] = nger_data['scope1'].replace(" ", "", regex=True)
nger_data['scope2'] = nger_data['scope2'].replace(" ", "", regex=True)
#nger_data['total_emissions'] = nger_data['total_emissions'].replace(" ", "", regex=True)
nger_data['energy_consumption'] = nger_data['energy_consumption'].replace(" ", "", regex=True)

#remove alphanumeric charaters from emissions values
nger_data['scope1'] = nger_data['scope1'].str.replace('[a-z]', '', regex=True, flags=re.IGNORECASE)
nger_data['scope2'] = nger_data['scope2'].str.replace('[a-z]', '',regex=True, flags=re.IGNORECASE)
#ger_data['total_emissions'] = nger_data['total_emissions'].str.replace('[a-z]', '',regex=True, flags=re.IGNORECASE)
nger_data['energy_consumption'] = nger_data['energy_consumption'].str.replace('[a-z]', '',regex=True, flags=re.IGNORECASE)

#replace blanks with nan
nger_data = nger_data.replace(r'^\s*$', np.nan, regex=True)

#drop rows with missing scope1 & 2 data
nger_data = nger_data.dropna(axis=0, how= 'all', subset=['scope1', 'scope2'])

#convert emissions values to float
nger_data['scope1'] = nger_data['scope1'].astype(float)
nger_data['scope2'] = nger_data['scope2'].astype(float)
#nger_data['total_emissions'] = nger_data['total_emissions'].astype(float)
nger_data['energy_consumption'] = nger_data['energy_consumption'].astype(float)

#convert year column to date time format
#nger_data['year'] =  pd.to_datetime(nger_data['year'], format='%Y').dt.to_period("Y")
nger_data['year'] = nger_data['year'].astype(str)

"Construct Total Emissions"

'''
nger_list = [nger_2009,nger_2010,nger_2011,nger_2012,nger_2013,nger_2014,nger_2015,nger_2016,nger_2017,nger_2018,nger_2019,nger_2020,nger_2021]

def convert_emissisons_float(dataset):
    dataset['scope1'] = dataset['scope1'].astype(float)
    dataset['scope2'] = dataset['scope2'].astype(float)
    dataset['energy_consumption'] = dataset['energy_consumption'].astype(float)

for i in nger_list:
    convert_emissisons_float(i)
    
def calculate_total_emissions(dataset):
    dataset['total_emissions'] = dataset['scope1'] + dataset['scope2']
    


for i in nger_list:
    calculate_total_emissions(i)
'''
nger_data['total_emissions'] = nger_data['scope1'] + nger_data['scope2']

"FORMAT NGER COMPANY NAMES FOR MATCHING"
nger_data['firm_name']=nger_data['firm_name'].str.lower()
nger_data['firm_name']=nger_data['firm_name'].str.replace('pty ltd','',regex=True)
nger_data['firm_name']=nger_data['firm_name'].str.replace('limited group','',regex=True)
nger_data['firm_name']=nger_data['firm_name'].str.replace('limited','',regex=True)
nger_data['firm_name']=nger_data['firm_name'].str.replace('group','',regex=True)
nger_data['firm_name']=nger_data['firm_name'].str.replace('ltd','',regex=True)
nger_data['firm_name']=nger_data['firm_name'].str.replace('holdings','',regex=True)
nger_data['firm_name']=nger_data['firm_name'].str.replace('holding','',regex=True)
nger_data['firm_name']=nger_data['firm_name'].str.replace('pty','',regex=True)
nger_data['firm_name']=nger_data['firm_name'].str.replace('proprietary','',regex=True)
nger_data['firm_name']=nger_data['firm_name'].str.replace('corporation','',regex=True)
nger_data['firm_name']=nger_data['firm_name'].str.rstrip('.')
nger_data['firm_name']=nger_data['firm_name'].str.strip()
nger_data = nger_data.rename(columns={'firm_name':'nger_name'})

nger_data = nger_data.reset_index(drop=True)


"EXTRACT LIST OF NGER FIRMS"
"Extract unique nger firms"
nger_firms_list = []
nger_firms_list = nger_data['nger_name'].unique().tolist()


nger_data = nger_data.reset_index(drop=True)


"SAVE NGER DATA"

"Save to csv file"
output_filename = 'nger_data.csv'
outputname = output_path + output_filename
nger_data.to_csv(outputname, mode='w')
print ('Exported: '+outputname)

print('Number of Observations:')
print (len(nger_data))

#%%

'''
MORNINGSTAR DATA
'''

"IMPORT DATA"

#Morningstar Firm Data
ms_capex = pd.read_csv ('C:/Users/conno/OneDrive/University Study/Honours Thesis/cnolan-thesis/data/capex.csv', encoding='latin1')
ms_eoy_price = pd.read_csv ('C:/Users/conno/OneDrive/University Study/Honours Thesis/cnolan-thesis/data/eoy_price.csv', encoding='latin1')
ms_eps = pd.read_csv ('C:/Users/conno/OneDrive/University Study/Honours Thesis/cnolan-thesis/data/eps.csv', encoding='latin1')
ms_ltdebt = pd.read_csv ('C:/Users/conno/OneDrive/University Study/Honours Thesis/cnolan-thesis/data/longtermdebt.csv', encoding='latin1')
ms_marketcap = pd.read_csv ('C:/Users/conno/OneDrive/University Study/Honours Thesis/cnolan-thesis/data/marketcap.csv', encoding='latin1')
ms_ppe = pd.read_csv ('C:/Users/conno/OneDrive/University Study/Honours Thesis/cnolan-thesis/data/ppe.csv', encoding='latin1')
ms_revenue = pd.read_csv ('C:/Users/conno/OneDrive/University Study/Honours Thesis/cnolan-thesis/data/revenue.csv', encoding='latin1')
ms_roe = pd.read_csv ('C:/Users/conno/OneDrive/University Study/Honours Thesis/cnolan-thesis/data/roe.csv', encoding='latin1')
ms_stdebt = pd.read_csv ('C:/Users/conno/OneDrive/University Study/Honours Thesis/cnolan-thesis/data/shorttermdebt.csv', encoding='latin1')
ms_assets = pd.read_csv ('C:/Users/conno/OneDrive/University Study/Honours Thesis/cnolan-thesis/data/totalassets.csv', encoding='latin1')
ms_liabilities = pd.read_csv ('C:/Users/conno/OneDrive/University Study/Honours Thesis/cnolan-thesis/data/totalliabilities.csv', encoding='latin1')



"Melt Data to Time Series Format"
ms_capex = pd.melt(ms_capex, id_vars = ['ASX Code', 'Company Name', 'Item'], value_vars= ['2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022'], var_name = 'year', value_name='capex',col_level=None)
ms_eoy_price = pd.melt(ms_eoy_price, id_vars = ['ASX Code', 'Company Name', 'Item'], value_vars= ['2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022'], var_name = 'year', value_name='eoy_price',col_level=None)
ms_eps = pd.melt(ms_eps, id_vars = ['ASX Code', 'Company Name', 'Item'], value_vars= ['2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022'], var_name = 'year', value_name='eps',col_level=None)
ms_ltdebt = pd.melt(ms_ltdebt, id_vars = ['ASX Code', 'Company Name', 'Item'], value_vars= ['2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022'], var_name = 'year', value_name='ltdebt',col_level=None)
ms_marketcap = pd.melt(ms_marketcap, id_vars = ['ASX Code', 'Company Name', 'Item'], value_vars= ['2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022'], var_name = 'year', value_name='marketcap',col_level=None)
ms_ppe = pd.melt(ms_ppe, id_vars = ['ASX Code', 'Company Name', 'Item'], value_vars= ['2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022'], var_name = 'year', value_name='ppe',col_level=None)
ms_revenue = pd.melt(ms_revenue, id_vars = ['ASX Code', 'Company Name', 'Item'], value_vars= ['2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022'], var_name = 'year', value_name='revenue',col_level=None)
ms_roe = pd.melt(ms_roe, id_vars = ['ASX Code', 'Company Name', 'Item'], value_vars= ['2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022'], var_name = 'year', value_name='roe',col_level=None)
ms_stdebt = pd.melt(ms_stdebt, id_vars = ['ASX Code', 'Company Name', 'Item'], value_vars= ['2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022'], var_name = 'year', value_name='stdebt',col_level=None)
ms_assets = pd.melt(ms_assets, id_vars = ['ASX Code', 'Company Name', 'Item'], value_vars= ['2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022'], var_name = 'year', value_name='assets',col_level=None)
ms_liabilities = pd.melt(ms_liabilities, id_vars = ['ASX Code', 'Company Name', 'Item'], value_vars= ['2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022'], var_name = 'year', value_name='liabilities',col_level=None)

"Merge Data Sets"

#make capex the main dataset to merge on
ms_data = ms_capex
#merge eoy_price
ms_data = pd.merge(ms_data[['ASX Code', 'Company Name','year', 'capex']], ms_eoy_price[['ASX Code', 'year','eoy_price']], on = ['ASX Code', 'year'], how = 'inner')
#merge eps
ms_data = pd.merge(ms_data[['ASX Code', 'Company Name','year', 'capex','eoy_price']], ms_eps[['ASX Code', 'year','eps']], on = ['ASX Code', 'year'], how = 'inner')
#merge ltdebt
ms_data = pd.merge(ms_data[['ASX Code', 'Company Name','year', 'capex','eoy_price','eps']], ms_ltdebt[['ASX Code', 'year','ltdebt']], on = ['ASX Code', 'year'], how = 'inner')
#merge marketcap
ms_data = pd.merge(ms_data[['ASX Code', 'Company Name','year', 'capex','eoy_price','eps','ltdebt']], ms_marketcap[['ASX Code', 'year','marketcap']], on = ['ASX Code', 'year'], how = 'inner')
#merge ppe
ms_data = pd.merge(ms_data[['ASX Code', 'Company Name','year', 'capex','eoy_price','eps','ltdebt','marketcap']],  ms_ppe[['ASX Code', 'year','ppe']], on = ['ASX Code', 'year'], how = 'inner')
#merge revenue
ms_data = pd.merge(ms_data[['ASX Code', 'Company Name','year', 'capex','eoy_price','eps','ltdebt','marketcap','ppe']], ms_revenue[['ASX Code', 'year','revenue']], on = ['ASX Code', 'year'], how = 'inner')
#merge roe
ms_data = pd.merge(ms_data[['ASX Code', 'Company Name','year', 'capex','eoy_price','eps','ltdebt','marketcap','ppe','revenue']], ms_roe[['ASX Code', 'year','roe']], on = ['ASX Code', 'year'], how = 'inner')
#merge stdebt
ms_data = pd.merge(ms_data[['ASX Code', 'Company Name','year', 'capex','eoy_price','eps','ltdebt','marketcap','ppe','revenue','roe']], ms_stdebt[['ASX Code', 'year','stdebt']], on = ['ASX Code', 'year'], how = 'inner')
#merge assets
ms_data = pd.merge(ms_data[['ASX Code', 'Company Name','year', 'capex','eoy_price','eps','ltdebt','marketcap','ppe','revenue','roe','stdebt']], ms_assets[['ASX Code', 'year','assets']],on = ['ASX Code', 'year'], how = 'inner')
#merge liabilities
ms_data = pd.merge(ms_data[['ASX Code', 'Company Name','year', 'capex','eoy_price','eps','ltdebt','marketcap','ppe','revenue','roe','stdebt','assets']], ms_liabilities[['ASX Code', 'year','liabilities']], on = ['ASX Code', 'year'], how = 'inner')


"Clean up ['capex']"
#remove comma's from capex column
ms_data["capex"] = ms_data["capex"].replace(",", "", regex=True)
#replace blanks with nan
ms_data["capex"] = ms_data["capex"].replace(r'^\s*$', np.nan, regex=True)
#replace '--'' with nan
ms_data["capex"] = ms_data["capex"].replace('--', np.nan, regex=True)
#convert capex values to float
ms_data['capex'] = ms_data['capex'].astype(float)

"Clean up ['eoy_price']"
#remove comma's from eoy_price values 
ms_data["eoy_price"] = ms_data["eoy_price"].replace(",", "", regex=True)
#replace blanks with nan
ms_data["eoy_price"] = ms_data["eoy_price"].replace(r'^\s*$', np.nan, regex=True)
#replace '--'' with nan
ms_data["eoy_price"] = ms_data["eoy_price"].replace('--', np.nan, regex=True)
#convert eoy_price values to float
ms_data['eoy_price'] =ms_data['eoy_price'].astype(float)
#replace negative numbers with nan
ms_data.loc[ms_data['eoy_price'] < 0, 'eoy_price'] = np.nan
#replace 0 with nan
ms_data['eoy_price'] = ms_data['eoy_price'].replace(0, np.nan)


"Clean up ['eps']"
#remove comma's from revenue values 
ms_data["eps"] = ms_data["eps"].replace(",", "", regex=True)
#replace blanks with nan
ms_data["eps"] = ms_data["eps"].replace(r'^\s*$', np.nan, regex=True)
#replace '--'' with nan
ms_data["eps"] = ms_data["eps"].replace('--', np.nan, regex=True)
#convert eps values to float
ms_data['eps'] = ms_data["eps"].astype(float)

"Clean up ['ltdebt']"
#remove comma's from ltdebt  
ms_data["ltdebt"] = ms_data["ltdebt"].replace(",", "", regex=True)
#replace blanks with nan
ms_data["ltdebt"] = ms_data["ltdebt"].replace(r'^\s*$', np.nan, regex=True)
#replace '--'' with nan
ms_data["ltdebt"] = ms_data["ltdebt"].replace('--', np.nan, regex=True)
#convert ltdebt values to float
ms_data['ltdebt'] = ms_data['ltdebt'].astype(float)
#replace 0 with nan
ms_data['ltdebt'] = ms_data['ltdebt'].replace(0, np.nan)
#replace negative numbers with nan
ms_data.loc[ms_data['ltdebt'] < 0, 'ltdebt'] = np.nan

"Clean up ['marketcap']"
#replace blanks with nan
ms_data['marketcap'] = ms_data['marketcap'].replace(r'^\s*$', np.nan, regex=True)
#convert marketcap values to float
ms_data['marketcap'] = ms_data['marketcap'].astype(float)
#replace negative numbers with nan
ms_data.loc[ms_data['marketcap'] < 0, 'marketcap'] = np.nan
#replace 0 with nan
ms_data['marketcap'] = ms_data['marketcap'].replace(0, np.nan)

"Clean up ['ppe']"

#remove comma's from ppe value 
ms_data["ppe"] = ms_data["ppe"].replace(",", "", regex=True)
#replace blanks with nan
ms_data["ppe"] = ms_data["ppe"].replace(r'^\s*$', np.nan, regex=True)
#replace '--'' with nan
ms_data["ppe"] = ms_data["ppe"].replace('--', np.nan, regex=True)
#convert ppe values to float
ms_data['ppe'] = ms_data["ppe"].astype(float)
#replace negative numbers with nan
ms_data.loc[ms_data['ppe'] < 0, 'ppe'] = np.nan

"Clean up ['revenue']"
#remove comma's from revenue values 
ms_data["revenue"] = ms_data["revenue"].replace(",", "", regex=True)
#replace blanks with nan
ms_data["revenue"] = ms_data["revenue"].replace(r'^\s*$', np.nan, regex=True)
#replace '--'' with nan
ms_data["revenue"] = ms_data["revenue"].replace('--', np.nan, regex=True)
#convert revenue values to float
ms_data['revenue'] = ms_data["revenue"].astype(float)
#replace negative numbers with nan
ms_data.loc[ms_data['revenue'] < 0, 'revenue'] = np.nan
#replace 0 with nan
ms_data['revenue'] = ms_data['revenue'].replace(0, np.nan)

"Clean up ['roe']"
#remove comma's from roe 
ms_data["roe"] = ms_data["roe"].replace(",", "", regex=True)
#replace blanks with nan
ms_data["roe"] = ms_data["roe"].replace(r'^\s*$', np.nan, regex=True)
#replace '--'' with nan
ms_data["roe"] = ms_data["roe"].replace('--', np.nan, regex=True)
#convert percentage string to float for roe 
ms_data['roe'] = (pd.to_numeric(ms_data['roe'].str[:-1]).div(100).mask(ms_data['roe']=='%',0))

"Clean up ['stdebt']"
#remove comma's from stdebt  
ms_data["stdebt"] = ms_data["stdebt"].replace(",", "", regex=True)
#replace blanks with nan
ms_data["stdebt"] = ms_data["stdebt"].replace(r'^\s*$', np.nan, regex=True)
#replace '--'' with nan
ms_data["stdebt"] = ms_data["stdebt"].replace('--', np.nan, regex=True)
#convert stdebt values to float
ms_data['stdebt'] = ms_data["stdebt"].astype(float)
#replace negative numbers with nan
ms_data.loc[ms_data['stdebt'] < 0, 'stdebt'] = np.nan
#replace 0 with nan
ms_data['stdebt'] = ms_data['stdebt'].replace(0, np.nan)

"Clean up ['assets']"
#remove comma's from total asset value 
ms_data["assets"] = ms_data["assets"].replace(",", "", regex=True)
#replace blanks with nan
ms_data["assets"] = ms_data["assets"].replace(r'^\s*$', np.nan, regex=True)
#replace '--'' with nan
ms_data["assets"] = ms_data["assets"].replace('--', np.nan, regex=True)
#convert marketcap values to float
ms_data["assets"] = ms_data["assets"].astype(float)
#replace negative numbers with nan
ms_data.loc[ms_data['assets'] < 0, 'assets'] = np.nan
#replace 0 with nan
ms_data['assets'] = ms_data['assets'].replace(0, np.nan)

"Clean up ['liabilities']"
#remove comma's from total asset value 
ms_data["liabilities"] = ms_data["liabilities"].replace(",", "", regex=True)
#replace blanks with nan
ms_data["liabilities"] = ms_data["liabilities"].replace(r'^\s*$', np.nan, regex=True)
#replace '--'' with nan
ms_data["liabilities"] = ms_data["liabilities"].replace('--', np.nan, regex=True)
#convert marketcap values to float
ms_data['liabilities'] = ms_data["liabilities"].astype(float)
#replace negative numbers with nan
ms_data.loc[ms_data['liabilities'] < 0, 'liabilities'] = np.nan
"Convert year column to date time format"
ms_data['year'] =  pd.to_datetime(ms_data['year'], format='%Y').dt.to_period("Y")

"FORMAT MORNINGSTAR COMPANY NAMES FOR MATCHING"
ms_data['Company Name']=ms_data['Company Name'].str.lower()
ms_data['Company Name']=ms_data['Company Name'].str.replace('pty ltd','',regex=True)
ms_data['Company Name']=ms_data['Company Name'].str.replace('limited group','',regex=True)
ms_data['Company Name']=ms_data['Company Name'].str.replace('limited','',regex=True)
ms_data['Company Name']=ms_data['Company Name'].str.replace('group','',regex=True)
ms_data['Company Name']=ms_data['Company Name'].str.replace('ltd.','',regex=True)
ms_data['Company Name']=ms_data['Company Name'].str.replace('ltd','',regex=True)
ms_data['Company Name']=ms_data['Company Name'].str.replace('holdings','',regex=True)
ms_data['Company Name']=ms_data['Company Name'].str.replace('holding','',regex=True)
ms_data['Company Name']=ms_data['Company Name'].str.replace('pty.','',regex=True)
ms_data['Company Name']=ms_data['Company Name'].str.replace('proprietary','',regex=True)
ms_data['Company Name']=ms_data['Company Name'].str.replace('corporation','',regex=True)
ms_data['Company Name']=ms_data['Company Name'].str.rstrip('.')
ms_data['Company Name']=ms_data['Company Name'].str.strip()
ms_data = ms_data.rename(columns={'Company Name':'morningstar_name','ASX Code':'ticker'})

"Save collated file"
output_filename = 'ms_data.csv'
outputname = output_path + output_filename
ms_data.to_csv(outputname, mode='w', index=False)
print("Exported File: " + outputname)

print('Number of Observations:')
print (len(ms_data))

#%%

'''
FAMA FRENCH FACTORS
'''

"IMPORT DATA"
famafrench = pd.read_csv ('C:/Users/conno/OneDrive/University Study/Honours Thesis/cnolan-thesis/data/Asia_Pacific_ex_Japan_5_Factors.csv')
famafrench_wml = pd.read_csv ('C:/Users/conno/OneDrive/University Study/Honours Thesis/cnolan-thesis/data/Asia_Pacific_ex_Japan_MOM_Factor.csv')
exchange_rate = pd.read_csv ('C:/Users/conno/OneDrive/University Study/Honours Thesis/cnolan-thesis/data/usdaud_exchange_rate.csv')


"MERGE AND FORMAT"
famafrench = pd.merge(famafrench,famafrench_wml[['yearmonth','wml']], how = 'left', on=['yearmonth'])
famafrench = famafrench.loc[(famafrench['yearmonth'] >= 200807) & (famafrench['yearmonth'] <= 202206)]
famafrench = famafrench[['yearmonth', 'year', 'month', 'smb', 'hml', 'rmw', 'cma', 'wml']]


"CONVERT FACTORS FROM USD TO AUD"

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

#%%
'''
"ASX500"
'''

"2008"
os.chdir('C:/Users/conno/OneDrive/University Study/Honours Thesis/cnolan-thesis/data/ASX500 MONTHLY/2008/')

may_2008 = pd.read_csv('200805.csv')
may_2008['yearmonth'] = 200805

june_2008 = pd.read_csv('AS30 as of Jun 30 20081.csv')
june_2008['yearmonth'] = 200806

july_2008 = pd.read_csv('AS30 as of Jul 31 20081.csv')
july_2008['yearmonth'] = 200807

august_2008 = pd.read_csv('AS30 as of Aug 29 20081.csv')
august_2008['yearmonth'] = 200808

september_2008 = pd.read_csv('AS30 as of Sep 30 20081.csv')
september_2008['yearmonth'] = 200809

october_2008 = pd.read_csv('AS30 as of Oct 31 20081.csv')
october_2008['yearmonth'] = 200810

november_2008 = pd.read_csv('AS30 as of Nov 28 20081.csv')
november_2008['yearmonth'] = 200811

december_2008 = pd.read_csv('200812.csv')
december_2008['yearmonth'] = 200812

asx500_2008 = pd.concat([may_2008, june_2008, july_2008, august_2008, september_2008, october_2008, november_2008, december_2008], axis=0).reset_index(drop=True)
#%%

"2009"
os.chdir('C:/Users/conno/OneDrive/University Study/Honours Thesis/cnolan-thesis/data/ASX500 MONTHLY/2009/')

jan_2009 = pd.read_csv('jan 2009.csv')
jan_2009['yearmonth'] = 200901

feb_2009 = pd.read_csv('feb 2009.csv')
feb_2009['yearmonth'] = 200902

mar_2009 = pd.read_csv('mar 2009.csv')
mar_2009['yearmonth'] = 200903

apr_2009 = pd.read_csv('apr 2009.csv')
apr_2009['yearmonth'] = 200904

may_2009 = pd.read_csv('may 2009.csv')
may_2009['yearmonth'] = 200905

jun_2009 = pd.read_csv('jun 2009.csv')
jun_2009['yearmonth'] = 200906

jul_2009 = pd.read_csv('jul 2009.csv')
jul_2009['yearmonth'] = 200907

aug_2009 = pd.read_csv('aug 2009.csv')
aug_2009['yearmonth'] = 200908

sep_2009 = pd.read_csv('sep 2009.csv')
sep_2009['yearmonth'] = 200909

oct_2009 = pd.read_csv('oct 2009.csv')
oct_2009['yearmonth'] = 200910

nov_2009 = pd.read_csv('nov 2009.csv')
nov_2009['yearmonth'] = 200911

dec_2009 = pd.read_csv('dec 2009.csv')
dec_2009['yearmonth'] = 200912

asx500_2009 = pd.concat([jan_2009, feb_2009, mar_2009, apr_2009, may_2009, jun_2009, jul_2009, aug_2009, sep_2009, oct_2009, nov_2009, dec_2009], axis=0).reset_index(drop=True)


#%%


"2010"
os.chdir('C:/Users/conno/OneDrive/University Study/Honours Thesis/cnolan-thesis/data/ASX500 MONTHLY/2010/')

jan_2010 = pd.read_csv('jan 2010.csv')
jan_2010['yearmonth'] = 201001

feb_2010 = pd.read_csv('feb 2010.csv')
feb_2010['yearmonth'] = 201002

mar_2010 = pd.read_csv('mar 2010.csv')
mar_2010['yearmonth'] = 201003

apr_2010 = pd.read_csv('apr 2010.csv')
apr_2010['yearmonth'] = 201004

may_2010 = pd.read_csv('may 2010.csv')
may_2010['yearmonth'] = 201005

jun_2010 = pd.read_csv('jun 2010.csv')
jun_2010['yearmonth'] = 201006

jul_2010 = pd.read_csv('jul 2010.csv')
jul_2010['yearmonth'] = 201007

aug_2010 = pd.read_csv('aug 2010.csv')
aug_2010['yearmonth'] = 201008

sep_2010 = pd.read_csv('sep 2010.csv')
sep_2010['yearmonth'] = 201009

oct_2010 = pd.read_csv('oct 2010.csv')
oct_2010['yearmonth'] = 201010

nov_2010 = pd.read_csv('nov 2010.csv')
nov_2010['yearmonth'] = 201011

dec_2010 = pd.read_csv('dec 2010.csv')
dec_2010['yearmonth'] = 201012

asx500_2010 = pd.concat([jan_2010, feb_2010, mar_2010, apr_2010, may_2010, jun_2010, jul_2010, aug_2010, sep_2010, oct_2010, nov_2010, dec_2010], axis=0).reset_index(drop=True)

#%%


"2011"
os.chdir('C:/Users/conno/OneDrive/University Study/Honours Thesis/cnolan-thesis/data/ASX500 MONTHLY/2011/')

jan_2011 = pd.read_csv('jan 2011.csv')
jan_2011['yearmonth'] = 201101

feb_2011 = pd.read_csv('feb 2011.csv')
feb_2011['yearmonth'] = 201102

mar_2011 = pd.read_csv('mar 2011.csv')
mar_2011['yearmonth'] = 201103

apr_2011 = pd.read_csv('apr 2011.csv')
apr_2011['yearmonth'] = 201104

may_2011 = pd.read_csv('may 2011.csv')
may_2011['yearmonth'] = 201105

jun_2011 = pd.read_csv('jun 2011.csv')
jun_2011['yearmonth'] = 201106

jul_2011 = pd.read_csv('jul 2011.csv')
jul_2011['yearmonth'] = 201107

aug_2011 = pd.read_csv('aug 2011.csv')
aug_2011['yearmonth'] = 201108

sep_2011 = pd.read_csv('sep 2011.csv')
sep_2011['yearmonth'] = 201109

oct_2011 = pd.read_csv('oct 2011.csv')
oct_2011['yearmonth'] = 201110

nov_2011 = pd.read_csv('nov 2011.csv')
nov_2011['yearmonth'] = 201111

dec_2011 = pd.read_csv('dec 2011.csv')
dec_2011['yearmonth'] = 201112

asx500_2011 = pd.concat([jan_2011, feb_2011, mar_2011, apr_2011, may_2011, jun_2011, jul_2011, aug_2011, sep_2011, oct_2011, nov_2011, dec_2011], axis=0).reset_index(drop=True)

#%%


"2012"
os.chdir('C:/Users/conno/OneDrive/University Study/Honours Thesis/cnolan-thesis/data/ASX500 MONTHLY/2012/')

jan_2012 = pd.read_csv('jan 2012.csv')
jan_2012['yearmonth'] = 201201

feb_2012 = pd.read_csv('feb 2012.csv')
feb_2012['yearmonth'] = 201202

mar_2012 = pd.read_csv('mar 2012.csv')
mar_2012['yearmonth'] = 201203

apr_2012 = pd.read_csv('apr 2012.csv')
apr_2012['yearmonth'] = 201204

may_2012 = pd.read_csv('may 2012.csv')
may_2012['yearmonth'] = 201205

jun_2012 = pd.read_csv('jun 2012.csv')
jun_2012['yearmonth'] = 201206

jul_2012 = pd.read_csv('jul 2012.csv')
jul_2012['yearmonth'] = 201207

aug_2012 = pd.read_csv('aug 2012.csv')
aug_2012['yearmonth'] = 201208

sep_2012 = pd.read_csv('sep 2012.csv')
sep_2012['yearmonth'] = 201209

oct_2012 = pd.read_csv('oct 2012.csv')
oct_2012['yearmonth'] = 201210

nov_2012 = pd.read_csv('nov 2012.csv')
nov_2012['yearmonth'] = 201211

dec_2012 = pd.read_csv('dec 2012.csv')
dec_2012['yearmonth'] = 201212

asx500_2012 = pd.concat([jan_2012, feb_2012, mar_2012, apr_2012, may_2012, jun_2012, jul_2012, aug_2012, sep_2012, oct_2012, nov_2012, dec_2012], axis=0).reset_index(drop=True)

#%%

"2013"
os.chdir('C:/Users/conno/OneDrive/University Study/Honours Thesis/cnolan-thesis/data/ASX500 MONTHLY/2013/')

jan_2013 = pd.read_csv('jan 2013.csv')
jan_2013['yearmonth'] = 201301

feb_2013 = pd.read_csv('feb 2013.csv')
feb_2013['yearmonth'] = 201302

mar_2013 = pd.read_csv('mar 2013.csv')
mar_2013['yearmonth'] = 201303

apr_2013 = pd.read_csv('apr 2013.csv')
apr_2013['yearmonth'] = 201304

may_2013 = pd.read_csv('may 2013.csv')
may_2013['yearmonth'] = 201305

jun_2013 = pd.read_csv('jun 2013.csv')
jun_2013['yearmonth'] = 201306

jul_2013 = pd.read_csv('jul 2013.csv')
jul_2013['yearmonth'] = 201307

aug_2013 = pd.read_csv('aug 2013.csv')
aug_2013['yearmonth'] = 201308

sep_2013 = pd.read_csv('sep 2013.csv')
sep_2013['yearmonth'] = 201309

oct_2013 = pd.read_csv('oct 2013.csv')
oct_2013['yearmonth'] = 201310

nov_2013 = pd.read_csv('nov 2013.csv')
nov_2013['yearmonth'] = 201311

dec_2013 = pd.read_csv('dec 2013.csv')
dec_2013['yearmonth'] = 201312

asx500_2013 = pd.concat([jan_2013, feb_2013, mar_2013, apr_2013, may_2013, jun_2013, jul_2013, aug_2013, sep_2013, oct_2013, nov_2013, dec_2013], axis=0).reset_index(drop=True)

#%%


"2014"
os.chdir('C:/Users/conno/OneDrive/University Study/Honours Thesis/cnolan-thesis/data/ASX500 MONTHLY/2014/')

jan_2014 = pd.read_csv('jan 2014.csv')
jan_2014['yearmonth'] = 201401

feb_2014 = pd.read_csv('feb 2014.csv')
feb_2014['yearmonth'] = 201402

mar_2014 = pd.read_csv('mar 2014.csv')
mar_2014['yearmonth'] = 201403

apr_2014 = pd.read_csv('apr 2014.csv')
apr_2014['yearmonth'] = 201404

may_2014 = pd.read_csv('may 2014.csv')
may_2014['yearmonth'] = 201405

jun_2014 = pd.read_csv('jun 2014.csv')
jun_2014['yearmonth'] = 201406

jul_2014 = pd.read_csv('jul 2014.csv')
jul_2014['yearmonth'] = 201407

aug_2014 = pd.read_csv('aug 2014.csv')
aug_2014['yearmonth'] = 201408

sep_2014 = pd.read_csv('sep 2014.csv')
sep_2014['yearmonth'] = 201409

oct_2014 = pd.read_csv('oct 2014.csv')
oct_2014['yearmonth'] = 201410

nov_2014 = pd.read_csv('nov 2014.csv')
nov_2014['yearmonth'] = 201411

dec_2014 = pd.read_csv('dec 2014.csv')
dec_2014['yearmonth'] = 201412

asx500_2014 = pd.concat([jan_2014, feb_2014, mar_2014, apr_2014, may_2014, jun_2014, jul_2014, aug_2014, sep_2014, oct_2014, nov_2014, dec_2014], axis=0).reset_index(drop=True)

#%%


"2015"
os.chdir('C:/Users/conno/OneDrive/University Study/Honours Thesis/cnolan-thesis/data/ASX500 MONTHLY/2015/')

jan_2015 = pd.read_csv('jan 2015.csv')
jan_2015['yearmonth'] = 201501

feb_2015 = pd.read_csv('feb 2015.csv')
feb_2015['yearmonth'] = 201502

mar_2015 = pd.read_csv('mar 2015.csv')
mar_2015['yearmonth'] = 201503

apr_2015 = pd.read_csv('apr 2015.csv')
apr_2015['yearmonth'] = 201504

may_2015 = pd.read_csv('may 2015.csv')
may_2015['yearmonth'] = 201505

jun_2015 = pd.read_csv('jun 2015.csv')
jun_2015['yearmonth'] = 201506

jul_2015 = pd.read_csv('jul 2015.csv')
jul_2015['yearmonth'] = 201507

aug_2015 = pd.read_csv('aug 2015.csv')
aug_2015['yearmonth'] = 201508

sep_2015 = pd.read_csv('sep 2015.csv')
sep_2015['yearmonth'] = 201509

oct_2015 = pd.read_csv('oct 2015.csv')
oct_2015['yearmonth'] = 201510

nov_2015 = pd.read_csv('nov 2015.csv')
nov_2015['yearmonth'] = 201511

dec_2015 = pd.read_csv('dec 2015.csv')
dec_2015['yearmonth'] = 201512

asx500_2015 = pd.concat([jan_2015, feb_2015, mar_2015, apr_2015, may_2015, jun_2015, jul_2015, aug_2015, sep_2015, oct_2015, nov_2015, dec_2015], axis=0).reset_index(drop=True)

#%%


"2016"
os.chdir('C:/Users/conno/OneDrive/University Study/Honours Thesis/cnolan-thesis/data/ASX500 MONTHLY/2016/')

jan_2016 = pd.read_csv('jan 2016.csv')
jan_2016['yearmonth'] = 201601

feb_2016 = pd.read_csv('feb 2016.csv')
feb_2016['yearmonth'] = 201602

mar_2016 = pd.read_csv('mar 2016.csv')
mar_2016['yearmonth'] = 201603

apr_2016 = pd.read_csv('apr 2016.csv')
apr_2016['yearmonth'] = 201604

may_2016 = pd.read_csv('may 2016.csv')
may_2016['yearmonth'] = 201605

jun_2016 = pd.read_csv('jun 2016.csv')
jun_2016['yearmonth'] = 201606

jul_2016 = pd.read_csv('jul 2016.csv')
jul_2016['yearmonth'] = 201607

aug_2016 = pd.read_csv('aug 2016.csv')
aug_2016['yearmonth'] = 201608

sep_2016 = pd.read_csv('sep 2016.csv')
sep_2016['yearmonth'] = 201609

oct_2016 = pd.read_csv('oct 2016.csv')
oct_2016['yearmonth'] = 201610

nov_2016 = pd.read_csv('nov 2016.csv')
nov_2016['yearmonth'] = 201611

dec_2016 = pd.read_csv('dec 2016.csv')
dec_2016['yearmonth'] = 201612

asx500_2016 = pd.concat([jan_2016, feb_2016, mar_2016, apr_2016, may_2016, jun_2016, jul_2016, aug_2016, sep_2016, oct_2016, nov_2016, dec_2016], axis=0).reset_index(drop=True)

#%%


"2017"
os.chdir('C:/Users/conno/OneDrive/University Study/Honours Thesis/cnolan-thesis/data/ASX500 MONTHLY/2017/')

jan_2017 = pd.read_csv('jan 2017.csv')
jan_2017['yearmonth'] = 201701

feb_2017 = pd.read_csv('feb 2017.csv')
feb_2017['yearmonth'] = 201702

mar_2017 = pd.read_csv('mar 2017.csv')
mar_2017['yearmonth'] = 201703

apr_2017 = pd.read_csv('apr 2017.csv')
apr_2017['yearmonth'] = 201704

may_2017 = pd.read_csv('may 2017.csv')
may_2017['yearmonth'] = 201705

jun_2017 = pd.read_csv('jun 2017.csv')
jun_2017['yearmonth'] = 201706

jul_2017 = pd.read_csv('jul 2017.csv')
jul_2017['yearmonth'] = 201707

aug_2017 = pd.read_csv('aug 2017.csv')
aug_2017['yearmonth'] = 201708

sep_2017 = pd.read_csv('sep 2017.csv')
sep_2017['yearmonth'] = 201709

oct_2017 = pd.read_csv('oct 2017.csv')
oct_2017['yearmonth'] = 201710

nov_2017 = pd.read_csv('nov 2017.csv')
nov_2017['yearmonth'] = 201711

dec_2017 = pd.read_csv('dec 2017.csv')
dec_2017['yearmonth'] = 201712

asx500_2017 = pd.concat([jan_2017, feb_2017, mar_2017, apr_2017, may_2017, jun_2017, jul_2017, aug_2017, sep_2017, oct_2017, nov_2017, dec_2017], axis=0).reset_index(drop=True)

#%%


"2018"
os.chdir('C:/Users/conno/OneDrive/University Study/Honours Thesis/cnolan-thesis/data/ASX500 MONTHLY/2018/')

jan_2018 = pd.read_csv('jan 2018.csv')
jan_2018['yearmonth'] = 201801

feb_2018 = pd.read_csv('feb 2018.csv')
feb_2018['yearmonth'] = 201802

mar_2018 = pd.read_csv('mar 2018.csv')
mar_2018['yearmonth'] = 201803

apr_2018 = pd.read_csv('apr 2018.csv')
apr_2018['yearmonth'] = 201804

may_2018 = pd.read_csv('may 2018.csv')
may_2018['yearmonth'] = 201805

jun_2018 = pd.read_csv('jun 2018.csv')
jun_2018['yearmonth'] = 201806

jul_2018 = pd.read_csv('jul 2018.csv')
jul_2018['yearmonth'] = 201807

aug_2018 = pd.read_csv('aug 2018.csv')
aug_2018['yearmonth'] = 201808

sep_2018 = pd.read_csv('sep 2018.csv')
sep_2018['yearmonth'] = 201809

oct_2018 = pd.read_csv('oct 2018.csv')
oct_2018['yearmonth'] = 201810

nov_2018 = pd.read_csv('nov 2018.csv')
nov_2018['yearmonth'] = 201811

dec_2018 = pd.read_csv('dec 2018.csv')
dec_2018['yearmonth'] = 201812

asx500_2018 = pd.concat([jan_2018, feb_2018, mar_2018, apr_2018, may_2018, jun_2018, jul_2018, aug_2018, sep_2018, oct_2018, nov_2018, dec_2018], axis=0).reset_index(drop=True)

#%%


"2019"
os.chdir('C:/Users/conno/OneDrive/University Study/Honours Thesis/cnolan-thesis/data/ASX500 MONTHLY/2019/')

jan_2019 = pd.read_csv('jan 2019.csv')
jan_2019['yearmonth'] = 201901

feb_2019 = pd.read_csv('feb 2019.csv')
feb_2019['yearmonth'] = 201902

mar_2019 = pd.read_csv('mar 2019.csv')
mar_2019['yearmonth'] = 201903

apr_2019 = pd.read_csv('apr 2019.csv')
apr_2019['yearmonth'] = 201904

may_2019 = pd.read_csv('may 2019.csv')
may_2019['yearmonth'] = 201905

jun_2019 = pd.read_csv('jun 2019.csv')
jun_2019['yearmonth'] = 201906

jul_2019 = pd.read_csv('jul 2019.csv')
jul_2019['yearmonth'] = 201907

aug_2019 = pd.read_csv('aug 2019.csv')
aug_2019['yearmonth'] = 201908

sep_2019 = pd.read_csv('sep 2019.csv')
sep_2019['yearmonth'] = 201909

oct_2019 = pd.read_csv('oct 2019.csv')
oct_2019['yearmonth'] = 201910

nov_2019 = pd.read_csv('nov 2019.csv')
nov_2019['yearmonth'] = 201911

dec_2019 = pd.read_csv('dec 2019.csv')
dec_2019['yearmonth'] = 201912

asx500_2019 = pd.concat([jan_2019, feb_2019, mar_2019, apr_2019, may_2019, jun_2019, jul_2019, aug_2019, sep_2019, oct_2019, nov_2019, dec_2019], axis=0).reset_index(drop=True)


#%%


"2020"
os.chdir('C:/Users/conno/OneDrive/University Study/Honours Thesis/cnolan-thesis/data/ASX500 MONTHLY/2020/')

jan_2020 = pd.read_csv('jan 2020.csv')
jan_2020['yearmonth'] = 202001

feb_2020 = pd.read_csv('feb 2020.csv')
feb_2020['yearmonth'] = 202002

mar_2020 = pd.read_csv('mar 2020.csv')
mar_2020['yearmonth'] = 202003

apr_2020 = pd.read_csv('apr 2020.csv')
apr_2020['yearmonth'] = 202004

may_2020 = pd.read_csv('may 2020.csv')
may_2020['yearmonth'] = 202005

jun_2020 = pd.read_csv('jun 2020.csv')
jun_2020['yearmonth'] = 202006

jul_2020 = pd.read_csv('jul 2020.csv')
jul_2020['yearmonth'] = 202007

aug_2020 = pd.read_csv('aug 2020.csv')
aug_2020['yearmonth'] = 202008

sep_2020 = pd.read_csv('sep 2020.csv')
sep_2020['yearmonth'] = 202009

oct_2020 = pd.read_csv('oct 2020.csv')
oct_2020['yearmonth'] = 202010

nov_2020 = pd.read_csv('nov 2020.csv')
nov_2020['yearmonth'] = 202011

dec_2020 = pd.read_csv('dec 2020.csv')
dec_2020['yearmonth'] = 202012

asx500_2020 = pd.concat([jan_2020, feb_2020, mar_2020, apr_2020, may_2020, jun_2020, jul_2020, aug_2020, sep_2020, oct_2020, nov_2020, dec_2020], axis=0).reset_index(drop=True)

#%%


"2021"
os.chdir('C:/Users/conno/OneDrive/University Study/Honours Thesis/cnolan-thesis/data/ASX500 MONTHLY/2021/')

jan_2021 = pd.read_csv('jan 2021.csv')
jan_2021['yearmonth'] = 202101

feb_2021 = pd.read_csv('feb 2021.csv')
feb_2021['yearmonth'] = 202102

mar_2021 = pd.read_csv('mar 2021.csv')
mar_2021['yearmonth'] = 202103

apr_2021 = pd.read_csv('apr 2021.csv')
apr_2021['yearmonth'] = 202104

may_2021 = pd.read_csv('may 2021.csv')
may_2021['yearmonth'] = 202105

jun_2021 = pd.read_csv('jun 2021.csv')
jun_2021['yearmonth'] = 202106

jul_2021 = pd.read_csv('jul 2021.csv')
jul_2021['yearmonth'] = 202107

aug_2021 = pd.read_csv('aug 2021.csv')
aug_2021['yearmonth'] = 202108

sep_2021 = pd.read_csv('sep 2021.csv')
sep_2021['yearmonth'] = 202109

oct_2021 = pd.read_csv('oct 2021.csv')
oct_2021['yearmonth'] = 202110

nov_2021 = pd.read_csv('nov 2021.csv')
nov_2021['yearmonth'] = 202111

dec_2021 = pd.read_csv('dec 2021.csv')
dec_2021['yearmonth'] = 202112

asx500_2021 = pd.concat([jan_2021, feb_2021, mar_2021, apr_2021, may_2021, jun_2021, jul_2021, aug_2021, sep_2021, oct_2021, nov_2021, dec_2021], axis=0).reset_index(drop=True)

#%%


"2022"
os.chdir('C:/Users/conno/OneDrive/University Study/Honours Thesis/cnolan-thesis/data/ASX500 MONTHLY/2022/')

jan_2022 = pd.read_csv('jan 2022.csv')
jan_2022['yearmonth'] = 202201

feb_2022 = pd.read_csv('feb 2022.csv')
feb_2022['yearmonth'] = 202202

mar_2022 = pd.read_csv('mar 2022.csv')
mar_2022['yearmonth'] = 202203

apr_2022 = pd.read_csv('apr 2022.csv')
apr_2022['yearmonth'] = 202204

may_2022 = pd.read_csv('may 2022.csv')
may_2022['yearmonth'] = 202205

jun_2022 = pd.read_csv('jun 2022.csv')
jun_2022['yearmonth'] = 202206

jul_2022 = pd.read_csv('jul 2022.csv')
jul_2022['yearmonth'] = 202207



asx500_2022 = pd.concat([jan_2022, feb_2022, mar_2022, apr_2022, may_2022, jun_2022, jul_2022], axis=0).reset_index(drop=True)

#%%

asx500 = pd.concat([asx500_2008, asx500_2009,asx500_2010,asx500_2011,asx500_2012,asx500_2013,asx500_2014,asx500_2015,asx500_2016,asx500_2017,asx500_2018,asx500_2019,asx500_2020,asx500_2021,asx500_2022], axis=0).reset_index(drop=True)

asx500['Price (I)\n'] = asx500['Price (I)\n'].astype(str)

asx500['Price (I)\n'] = asx500['Price (I)\n'].replace({'--':np.nan})

asx500['Price (I)\n'] = asx500['Price (I)\n'].astype(float)

asx500['prev month price'] = asx500.groupby(['Ticker'])['Price (I)\n'].shift(1).reset_index(drop=True)

asx500['monthly return'] = (asx500['Price (I)\n']/asx500['prev month price']) - 1

asx500_all_output = asx500

"Save asx500"
output_filename = 'asx500_all.csv'
outputname = output_path + output_filename
asx500_all_output.to_csv(outputname, mode='w', index=False)
print("Exported File: " + outputname)

#%%
os.chdir('C:/Users/conno/OneDrive/University Study/Honours Thesis/cnolan-thesis/data/')

matched_firms = pd.read_csv("matched_firms.csv", index_col=0)

sample_firms = pd.read_csv('sample_firm_tickers.csv')

stock_sample = pd.merge(matched_firms[['ticker','morningstar_name']],sample_firms, on=['ticker'], how='right')
stock_sample['nger'] = 1

#asx500 = pd.merge(asx500, stock_sample[['ticker','nger']], how='left', on=['ticker])

#%%

asx500_firms = asx500[['Ticker', 'Name']]
asx500_firms = asx500_firms.drop_duplicates(subset=['Name']).reset_index(drop=True)

"FORMAT NGER COMPANY NAMES FOR MATCHING"

asx500_firms['match_name'] = asx500_firms['Name']

asx500_firms['match_name']=asx500_firms['match_name'].str.lower()
asx500_firms['match_name']=asx500_firms['match_name'].str.replace('pty ltd','',regex=True)
asx500_firms['match_name']=asx500_firms['match_name'].str.replace('limited group','',regex=True)
asx500_firms['match_name']=asx500_firms['match_name'].str.replace('limited','',regex=True)
asx500_firms['match_name']=asx500_firms['match_name'].str.replace('group','',regex=True)
asx500_firms['match_name']=asx500_firms['match_name'].str.replace('ltd','',regex=True)
asx500_firms['match_name']=asx500_firms['match_name'].str.replace('holdings','',regex=True)
asx500_firms['match_name']=asx500_firms['match_name'].str.replace('holding','',regex=True)
asx500_firms['match_name']=asx500_firms['match_name'].str.replace('pty','',regex=True)
asx500_firms['match_name']=asx500_firms['match_name'].str.replace('proprietary','',regex=True)
asx500_firms['match_name']=asx500_firms['match_name'].str.replace('corporation','',regex=True)
asx500_firms['match_name']=asx500_firms['match_name'].str.rstrip('.')
asx500_firms['match_name']=asx500_firms['match_name'].str.strip()

asx500_firms_list = []
asx500_firms_list = asx500_firms['match_name'].unique().tolist()


stock_sample['morningstar_name']=stock_sample['morningstar_name'].str.lower()
stock_sample['morningstar_name']=stock_sample['morningstar_name'].str.replace('pty ltd','',regex=True)
stock_sample['morningstar_name']=stock_sample['morningstar_name'].str.replace('limited group','',regex=True)
stock_sample['morningstar_name']=stock_sample['morningstar_name'].str.replace('limited','',regex=True)
stock_sample['morningstar_name']=stock_sample['morningstar_name'].str.replace('group','',regex=True)
stock_sample['morningstar_name']=stock_sample['morningstar_name'].str.replace('ltd','',regex=True)
stock_sample['morningstar_name']=stock_sample['morningstar_name'].str.replace('holdings','',regex=True)
stock_sample['morningstar_name']=stock_sample['morningstar_name'].str.replace('holding','',regex=True)
stock_sample['morningstar_name']=stock_sample['morningstar_name'].str.replace('pty','',regex=True)
stock_sample['morningstar_name']=stock_sample['morningstar_name'].str.replace('proprietary','',regex=True)
stock_sample['morningstar_name']=stock_sample['morningstar_name'].str.replace('corporation','',regex=True)
stock_sample['morningstar_name']=stock_sample['morningstar_name'].str.rstrip('.')
stock_sample['morningstar_name']=stock_sample['morningstar_name'].str.strip()

stock_sample_firms_list = []
stock_sample_firms_list = stock_sample['morningstar_name'].unique().tolist()

#%%
print('starting fuzzy matching')

threshold = 95 #note: in preliminary analysis a threshold of 95 provided matching without mismatching 
names_response = []
for name in asx500_firms_list:
    resp_match =  process.extractOne(name,stock_sample_firms_list)
    if resp_match[1] > threshold:
         row = {'match_name':name,'morningstar_name':resp_match[0], 'match_score':resp_match[1]}
         names_response.append(row)
         
print('finish fuzzy matching')

#%%

fuzzy_matched_asx500 = pd.DataFrame(names_response)
fuzzy_matched_asx500['fuzzy_matched'] = 1
fuzzy_matched_asx500 = pd.merge(fuzzy_matched_asx500, asx500_firms[['Name', 'match_name']], how='left', on=['match_name'])

#%%
asx500 = asx500.rename(columns={'Ticker': 'ticker'})
asx500 = pd.merge(asx500, stock_sample[['ticker', 'nger']], how='left',on=['ticker'])


asx500 = pd.merge(asx500, fuzzy_matched_asx500[['Name','fuzzy_matched']], how='left', on=['Name'])

len_before = len(asx500)
asx500 = asx500[asx500.nger != 1]
len_after = len(asx500)
print('Dropped:' + str(len_before-len_after))

len_before = len(asx500)
asx500 = asx500[asx500.fuzzy_matched != 1]
len_after = len(asx500)
print('Dropped:' + str(len_before-len_after))

"Save asx500"
output_filename = 'asx500_filtered.csv'
outputname = output_path + output_filename
asx500.to_csv(outputname, mode='w', index=False)
print("Exported File: " + outputname)


#%%

"MONTHLY ASX500 RETURNS"

asx500_all = asx500_all_output

asx500_ret = asx500_all[['Ticker', 'Name', 'yearmonth', 'Market Cap\n','monthly return']]


asx500_ret = asx500_ret.rename(columns={'Market Cap\n': 'marketcap', 'monthly return':'ret'})

asx500_ret['ret'] = asx500_ret['ret'].replace({'--':np.nan})
asx500_ret['marketcap'] = asx500_ret['marketcap'].replace({'--':np.nan})

asx500_ret['ret'] = asx500_ret['ret'].astype(float)
asx500_ret['marketcap'] = asx500_ret['marketcap'].astype(float)


asx500_ret['weighted_returns'] =  asx500_ret['ret'] * (asx500_ret['marketcap'] / asx500_ret.groupby(['yearmonth'])['marketcap'].transform('sum'))
asx500_ret['asx500_ret'] = asx500_ret.groupby(['yearmonth'])['weighted_returns'].transform('sum')

asx500_ret = asx500_ret[['yearmonth','asx500_ret']]
asx500_ret = asx500_ret.drop_duplicates(subset=['yearmonth']).reset_index(drop=True)

asx500_ret = asx500_ret.loc[(asx500_ret['yearmonth'] >= 200807) & (asx500_ret['yearmonth'] <= 202206)]


"Save asx_returns"
output_filename = 'asx500_returns.csv'
outputname = output_path + output_filename
asx500_ret.to_csv(outputname, mode='w', index=False)
print("Exported File: " + outputname)


#%%
print('COLLATE DATA - DONE')

