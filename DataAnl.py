import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from bs4 import BeautifulSoup as bs
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import json
import base64

#---------------------------------#
# Page layout
## Page expands to full width
st.set_page_config(page_title='Demo Data Analysis App')

#---------------------------------#
st.write("""
# Demo Data Analysis App
In this implementation, you can choose a Excel data table from your computer and analyze it.
""")

#---------------------------------#
# Sidebar - Collects user input features into dataframe
st.sidebar.header('Upload your CSV data')
uploaded_file = st.sidebar.file_uploader("Upload your input CSV file", type=["csv"])
st.sidebar.markdown("""
[Example CSV input file](http://logecal.us/VAS/Data)
""")


#---------------------------------#
# Plot Function
def boxplot(x, y, group):
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.write(y, 'by', x)
    # sns.boxplot(x="Randomization", y="SurgeryTime", palette="husl", data=df)
    ax = sns.boxplot(x=x, y=y, hue=group, palette="husl", data=df)
    plt.setp(ax.get_xticklabels(), rotation=30)
    st.pyplot()

def pointplot(x, y, group):
    st.write(y, 'by', x)
    ax = sns.pointplot(x=x, y=y, hue=group, err_style="bars", ci=95, data=df, dodge=0.4, join=True)
    plt.setp(ax.get_xticklabels(), rotation=30)
    st.pyplot()


#---------------------------------#
# Download Function
def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="SurgeryAnalysis.csv">Download CSV File</a>'
    return href

#---------------------------------#
# Main panel

# Displays the dataset
st.subheader('Dataset')

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write(df)
    cloumns_list = df.columns.tolist()
    
    st.markdown(filedownload(df), unsafe_allow_html=True)

    Plot_options = cloumns_list
    # selected_Plot_x = st.sidebar.multiselect('Plot_X', Plot_X, Plot_X)
    Plot_X = st.sidebar.selectbox('Plot_X', Plot_options)
    Plot_Y = st.sidebar.selectbox('Plot_Y', Plot_options)
    Group = st.sidebar.selectbox('Group', Plot_options)

    if st.button('Show Box Plot'):
        boxplot(Plot_X, Plot_Y, Group)
    if st.button('Show Error Bar Plot'):
        pointplot(Plot_X, Plot_Y, Group)

else:
    st.info('Awaiting for CSV file to be uploaded.')
    # if st.button('Press to use Example Dataset'):

    #     url = 'http://logecal.us/VAS/Data'        
        
    #     driver = webdriver.Chrome("/Users/SLu/Downloads/chromedriver_win32/chromedriver")
    #     driver.get(url)

    #     # this is just to ensure that the page is loaded 
    #     time.sleep(1)  
        
    #     # Now we have the page, let BeautifulSoup do the rest!
    #     soup = bs(driver.page_source)
        

    #     data = []
    #     table = soup.find('table')
 
    #     table_body = table.find('tbody')

    #     rows = table_body.find_all('tr')
    #     for row in rows:            
    #         cols = row.find_all('td') or row.find_all('th')
    #         cols = [ele.text.strip() for ele in cols]
    #         data.append([ele for ele in cols if ele]) # Get rid of empty values

    #     jsonList = json.dumps(data)
    #     json = pd.read_json(jsonList)

    #     json.columns = json.iloc[0]
    #     json = json[1:]
        
    #     df = pd.DataFrame(json)

    #     df["SurgeryTime"] = df["SurgeryTime"].astype(str).astype(int)
    #     st.write(df)

    #     plot()

    


