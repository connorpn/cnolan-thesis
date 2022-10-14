# -*- coding: utf-8 -*-
"""
Created on Fri Oct 14 18:18:41 2022

@author: Connor
"""
import pandas as pd
import os
import requests
import io

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
nger_data_list = [nger_2009,nger_2010,nger_2011,nger_2012,nger_2013,nger_2014,nger_2015,nger_2016,nger_2017,nger_2018,nger_2019,nger_2020,nger_2021]
nger_data = pd.concat(nger_data_list)
nger_data = nger_data.dropna(how='all',subset=['firm_name', 'scope1', 'scope2', 'energy_consumption', 'total_emissions'])

print('Number of Observations:')
print (len(nger_data))

#with pd.option_context('display.max_rows', None, 'display.max_columns', None):
   # display(nger_data)