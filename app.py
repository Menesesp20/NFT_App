import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.title('NFT Dashboard')

nft = pd.read_csv('data/nft_sales.csv')

nft.rename(columns = {'Sales':'Sales in USD','Txns':'Transactions'}, inplace = True)
nft['Sales in USD'] = nft['Sales in USD'].str.replace(',', '')
nft['Sales in USD'] = nft['Sales in USD'].str.replace('$', '')
nft['Buyers'] = nft['Buyers'].str.replace(',','')
nft['Transactions'] = nft['Transactions'].str.replace(',','')
nft['Owners'] = nft['Owners'].str.replace(',','')
nft=nft.dropna()

# CONVERTING STRING NUMERICALS TO INT
nft['Sales in USD'] = nft['Sales in USD'].astype('int64')
nft['Buyers'] = nft['Buyers'].astype('int64')
nft['Transactions'] = nft['Transactions'].astype('int64')
nft['Owners'] = nft['Owners'].astype('int32')

sorted_collections = nft.sort_values('Sales in USD', ascending=False)['Collections'].unique().tolist()

collection_choosed = st.sidebar.selectbox(
    "Select a NFT Collection",
    sorted_collections
)

compare_choice = st.sidebar.selectbox(
    "Compare with over 100M sales?",
    ('Yes', 'No')
)

if compare_choice == 'Yes':
    delta_DF = nft[nft['Sales in USD'] >= 100000000].reset_index(drop=True)
else:
    delta_DF = nft.copy()

collection = collection_choosed
collection_value = nft[nft.Collections == collection].reset_index(drop=True)

col1, col2, col3, col4 = st.columns(spec=[0.3, 0.233, 0.233, 0.233])

col1.subheader('Total Sales')
col1.metric(label='', value=collection_value['Sales in USD'].sum())

col2.subheader('Transactions')
col2.metric(label='', value=collection_value['Transactions'].sum())

col3.subheader('Owners')
col3.metric(label='', value=collection_value['Owners'].sum())

col4.subheader('Buyers')
col4.metric(label='', value=collection_value['Buyers'].sum())

st.header('Descriptive Analysis')

nft_Describe = nft.describe()

st.dataframe(nft_Describe)

# MODIFYING THE DATA SET, CREATE A COLUMN TO INDICATE THE NFT COLLECTION THAT SELL MORE THAN 100 MILLION
nft['100 million club'] = np.where(nft['Sales in USD'] >= 100000000, 'Yes', 'No')

st.header('All NFT Collections that sold more than 100 Million USD')

columns = nft.columns[:-1].tolist()

nft_100 = nft[nft['100 million club'] == 'Yes'][columns].reset_index(drop=True)

st.dataframe(nft_100)