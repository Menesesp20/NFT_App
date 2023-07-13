import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
st.set_option('deprecation.showPyplotGlobalUse', False)


st.title('Visualization Insights')

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

maximum_sale = nft['Sales in USD'].max()
collection = nft[nft['Sales in USD'] == maximum_sale ]['Collections'][0]

col1, col2 = st.columns(spec=[0.5, 0.5])

col1.metric(label='NFT Collection with more sales', value=collection)

col2.metric(label=f'Total sales of {collection}', value=maximum_sale)

print(f'The NFT Collection having maxiumum sales is {collection}')
print(f'Total sales of {collection} are {maximum_sale:,} USD')

# MODIFYING THE DATA SET, CREATE A COLUMN TO INDICATE THE NFT COLLECTION THAT SELL MORE THAN 100 MILLION
nft['100 million club'] = np.where(nft['Sales in USD'] >= 100000000, 'Yes', 'No')

count = nft.groupby(['100 million club']).count()['Collections']

def distribuiton_Collections_100M():
    labels = ["Not in 100 million club", "100 million club"]
    plt.style.use('fivethirtyeight')
    plt.figure(figsize=(10, 8))
    plt.pie(count,labels=labels,autopct='%.2f %%',textprops={'fontsize': 14})
    plt.title("Distribution of Collections",fontdict={'fontsize': 19})
    plt.legend(fontsize=10)

figPieChart = distribuiton_Collections_100M()

st.pyplot(figPieChart)

def Corelation():
    most_transaction  = nft['Transactions'].max()
    most_data = nft[nft['Transactions'] == most_transaction]
    collection_of_most = most_data['Collections'].iloc[0]
    sales_of_most = most_data['Sales in USD'].iloc[0]

    lower_transact = nft.iloc[1][3]
    collection_of_lower = nft.iloc[1][0]
    sales_of_lower = nft.iloc[1][1]

    #LET'S VISUALIZE THIS USING GRAPHS
    collections = [collection_of_most,collection_of_lower]
    sales = [sales_of_most,sales_of_lower]
    transactions = [most_transaction,lower_transact]

    plt.style.use('fivethirtyeight')
    fig,ax1 = plt.subplots(figsize=(10, 8))
    ax2=ax1.twinx()
    p = ax1.bar(collections,sales)
    ax2.plot(collections,transactions,'r-')
    ax1.bar_label(p)
    plt.title('Correlation between Sales and Transactions')
    ax1.set_xlabel('NFT Collection')
    ax1.set_ylabel('Sales in $', color='g')
    ax2.set_ylabel('Transactions', color='r')

figCorelation = Corelation()

st.pyplot(figCorelation)