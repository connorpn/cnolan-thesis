
import pandas as pd
import numpy as np
import os
import requests
import io
import re

#%%
working_directory = 'C:/cnolan-thesis/' #set location using back slashes

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

#%%

"Import Files"
#NGER Greenhouse Gas and Energy Information by Corporation
nger_2009 = pd.read_csv('https://raw.githubusercontent.com/connorpn/cnolan-thesis/main/data/NGER_GHGANDENERGYINFO_RC_2009.csv',encoding = "ISO-8859-1")
nger_2010 = pd.read_csv('https://raw.githubusercontent.com/connorpn/cnolan-thesis/main/data/NGER_GHGANDENERGYINFO_RC_2010.csv',encoding = "ISO-8859-1")
nger_2011 = pd.read_csv('https://raw.githubusercontent.com/connorpn/cnolan-thesis/main/data/NGER_GHGANDENERGYINFO_RC_2011.csv',encoding = "ISO-8859-1")
nger_2012 = pd.read_csv('https://raw.githubusercontent.com/connorpn/cnolan-thesis/main/data/NGER_GHGANDENERGYINFO_RC_2012.csv',encoding = "ISO-8859-1")
nger_2013 = pd.read_csv('https://raw.githubusercontent.com/connorpn/cnolan-thesis/main/data/NGER_GHGANDENERGYINFO_RC_2013.csv',encoding = "ISO-8859-1")
nger_2014 = pd.read_csv('https://raw.githubusercontent.com/connorpn/cnolan-thesis/main/data/NGER_GHGANDENERGYINFO_RC_2014.csv',encoding = "ISO-8859-1")
nger_2015 = pd.read_csv('https://raw.githubusercontent.com/connorpn/cnolan-thesis/main/data/NGER_GHGANDENERGYINFO_RC_2015.csv',encoding = "ISO-8859-1")
nger_2016 = pd.read_csv('https://raw.githubusercontent.com/connorpn/cnolan-thesis/main/data/NGER_GHGANDENERGYINFO_RC_2016.csv',encoding = "ISO-8859-1")
nger_2017 = pd.read_csv('https://raw.githubusercontent.com/connorpn/cnolan-thesis/main/data/NGER_GHGANDENERGYINFO_RC_2017.csv',encoding = "ISO-8859-1")
nger_2018 = pd.read_csv('https://raw.githubusercontent.com/connorpn/cnolan-thesis/main/data/NGER_GHGANDENERGYINFO_RC_2018.csv',encoding = "ISO-8859-1")
nger_2019 = pd.read_csv('https://raw.githubusercontent.com/connorpn/cnolan-thesis/main/data/NGER_GHGANDENERGYINFO_RC_2019.csv',encoding = "ISO-8859-1")
nger_2020 = pd.read_csv('https://raw.githubusercontent.com/connorpn/cnolan-thesis/main/data/NGER_GHGANDENERGYINFO_RC_2020.csv',encoding = "ISO-8859-1")
nger_2021 = pd.read_csv('https://raw.githubusercontent.com/connorpn/cnolan-thesis/main/data/NGER_GHGANDENERGYINFO_RC_2021.csv',encoding = "ISO-8859-1")

#Morningstar Firm Data
ms_capex = pd.read_csv ('https://raw.githubusercontent.com/connorpn/cnolan-thesis/main/data/capex.csv', encoding='latin1')
ms_eoy_price = pd.read_csv ('https://raw.githubusercontent.com/connorpn/cnolan-thesis/main/data/eoy_price.csv', encoding='latin1')
ms_eps = pd.read_csv ('https://raw.githubusercontent.com/connorpn/cnolan-thesis/main/data/eps.csv', encoding='latin1')
ms_ltdebt = pd.read_csv ('https://raw.githubusercontent.com/connorpn/cnolan-thesis/main/data/longtermdebt.csv', encoding='latin1')
ms_marketcap = pd.read_csv ('https://raw.githubusercontent.com/connorpn/cnolan-thesis/main/data/marketcap.csv', encoding='latin1')
ms_ppe = pd.read_csv ('https://raw.githubusercontent.com/connorpn/cnolan-thesis/main/data/ppe.csv', encoding='latin1')
ms_revenue = pd.read_csv ('https://raw.githubusercontent.com/connorpn/cnolan-thesis/main/data/revenue.csv', encoding='latin1')
ms_roe = pd.read_csv ('https://raw.githubusercontent.com/connorpn/cnolan-thesis/main/data/roe.csv', encoding='latin1')
ms_stdebt = pd.read_csv ('https://raw.githubusercontent.com/connorpn/cnolan-thesis/main/data/shorttermdebt.csv', encoding='latin1')
ms_assets = pd.read_csv ('https://raw.githubusercontent.com/connorpn/cnolan-thesis/main/data/totalassets.csv', encoding='latin1')
ms_liabilities = pd.read_csv ('https://raw.githubusercontent.com/connorpn/cnolan-thesis/main/data/totalliabilities.csv', encoding='latin1')

#Datastream Data (data is of nger-morningstar matched firms only)
ds_price_data = pd.read_csv('https://raw.githubusercontent.com/connorpn/cnolan-thesis/main/data/ds_matched_dailyprice.csv') #daily price data of matched nger firms
ds_beta = pd.read_csv('https://raw.githubusercontent.com/connorpn/cnolan-thesis/main/data/ds_beta.csv')
ds_marketcap = pd.read_csv('https://raw.githubusercontent.com/connorpn/cnolan-thesis/main/data/ds_marketcap.csv')

#%%
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


"Construct Total Emissions"

def calculate_total_emissions(dataset):
    dataset['total_emissions'] = dataset['scope1'] + dataset['scope2']
    

nger_list = [nger_2009,nger_2010,nger_2011,nger_2012,nger_2013,nger_2014,nger_2015,nger_2016,nger_2017,nger_2018,nger_2019,nger_2020,nger_2021]

for i in nger_list:
    calculate_total_emissions(i)


"Combined Datasets"
nger_data = pd.DataFrame(columns=['year', 'corporation', 'scope1', 'scope2', 'energy_consumption','total_emissions'])
nger_list = [nger_2009,nger_2010,nger_2011,nger_2012,nger_2013,nger_2014,nger_2015,nger_2016,nger_2017,nger_2018,nger_2019,nger_2020,nger_2021]
nger_data = pd.concat(nger_list)
print(list(nger_data))



"Clean up nger_data"

#remove comma's from emissions values 
nger_data['scope1'] = nger_data['scope1'].replace(",", "", regex=True)
nger_data['scope2'] = nger_data['scope2'].replace(",", "", regex=True)
nger_data['total_emissions'] = nger_data['total_emissions'].replace(",", "", regex=True)
nger_data['energy_consumption'] = nger_data['energy_consumption'].replace(",", "", regex=True)

#remove spaces's from emissions values 
nger_data['scope1'] = nger_data['scope1'].replace(" ", "", regex=True)
nger_data['scope2'] = nger_data['scope2'].replace(" ", "", regex=True)
nger_data['total_emissions'] = nger_data['total_emissions'].replace(" ", "", regex=True)
nger_data['energy_consumption'] = nger_data['energy_consumption'].replace(" ", "", regex=True)

#remove alphanumeric charaters from emissions values
nger_data['scope1'] = nger_data['scope1'].str.replace('[a-z]', '', regex=True, flags=re.IGNORECASE)
nger_data['scope2'] = nger_data['scope2'].str.replace('[a-z]', '',regex=True, flags=re.IGNORECASE)
nger_data['total_emissions'] = nger_data['total_emissions'].str.replace('[a-z]', '',regex=True, flags=re.IGNORECASE)
nger_data['energy_consumption'] = nger_data['energy_consumption'].str.replace('[a-z]', '',regex=True, flags=re.IGNORECASE)

#replace blanks with nan
nger_data = nger_data.replace(r'^\s*$', np.nan, regex=True)

#drop rows with missing scope1 & 2 data
nger_data = nger_data.dropna(axis=0, how= 'all', subset=['scope1', 'scope2'])

#convert emissions values to float
nger_data['scope1'] = nger_data['scope1'].astype(float)
nger_data['scope2'] = nger_data['scope2'].astype(float)
nger_data['total_emissions'] = nger_data['total_emissions'].astype(float)
nger_data['energy_consumption'] = nger_data['energy_consumption'].astype(float)

#convert year column to date time format
#nger_data['year'] =  pd.to_datetime(nger_data['year'], format='%Y').dt.to_period("Y")
nger_data['year'] = nger_data['year'].astype(str)

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

"Extract unique nger firms"
nger_firms_list = []
nger_firms_list = nger_data['nger_name'].unique().tolist()

"Save to csv file"
output_filename = 'nger_data.csv'
outputname = output_path + output_filename
nger_data.to_csv(outputname, mode='w')
print ('Exported: '+outputname)

'VIEW'
#%%
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
ms_data.to_csv(outputname, mode='w')
print("Exported File: " + outputname)

"VIEW"