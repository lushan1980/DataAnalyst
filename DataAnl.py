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



from pandas.io.json import json_normalize
#---------------------------------#
# Page layout
## Page expands to full width
st.set_page_config(page_title='Lumendi Data Analysis App',
    layout='wide')

#---------------------------------#
st.write("""
# Lumendi Data Analysis App
In this implementation, you can choose a Excel data table from your computer can analyze it.
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
def plot():
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.write("""
    ### Surgery Time by Group
    """)
    sns.boxplot(x="Randomization", y="SurgeryTime", palette="husl", data=df)
    st.pyplot()

    st.write("""
    ### Surgery Time by Month
    """)
    l = sns.pointplot(x="MonthProc", y="SurgeryTime", hue="Randomization", err_style="bars", ci=95, data=df, dodge=0.4, join=True)
    plt.setp(l.get_xticklabels(), rotation=45)
    st.pyplot()


#---------------------------------#
# Main panel

# Displays the dataset
st.subheader('Dataset')

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write(df)
    plot()

else:
    st.info('Awaiting for CSV file to be uploaded.')
    if st.button('Press to use Example Dataset'):


        url = 'http://logecal.us/VAS/Data'        
        
        driver = webdriver.Chrome("/Users/SLu/Downloads/chromedriver_win32/chromedriver")
        driver.get(url)

        # this is just to ensure that the page is loaded 
        time.sleep(1)  
        
        # Now we have the page, let BeautifulSoup do the rest!
        soup = bs(driver.page_source)
        

        data = []
        table = soup.find('table')
 
        table_body = table.find('tbody')

        rows = table_body.find_all('tr')
        for row in rows:            
            cols = row.find_all('td') or row.find_all('th')
            cols = [ele.text.strip() for ele in cols]
            data.append([ele for ele in cols if ele]) # Get rid of empty values

        jsonList = json.dumps(data)
        json = pd.read_json(jsonList)

        json.columns = json.iloc[0]
        json = json[1:]
        
        df = pd.DataFrame(json)

        df["SurgeryTime"] = df["SurgeryTime"].astype(str).astype(int)
        st.write(df)

        plot()

    


