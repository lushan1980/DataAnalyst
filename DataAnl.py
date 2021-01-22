import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

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
# Main panel

# Displays the dataset
st.subheader('Dataset')

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write(df)
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.write("""
    ### Surgery Time by Group
    """)
    sns.boxplot(x="Randomization", y="SurgeryTime", palette="husl", data=df)
    st.pyplot()

    # g = sns.catplot(x="MonthProc", y="SurgeryTime", hue="Randomization", kind="bar", palette="husl", ci=95, data=df)
    # g.set_xticklabels(rotation=45)
    # st.pyplot()
    st.write("""
    ### Surgery Time by Month
    """)
    l = sns.pointplot(x="MonthProc", y="SurgeryTime", hue="Randomization", err_style="bars", ci=95, data=df, dodge=0.4, join=True)
    plt.setp(l.get_xticklabels(), rotation=45)
    st.pyplot()

else:
    st.info('Awaiting for CSV file to be uploaded.')
    if st.button('Press to use Example Dataset'):
        diabetes = load_diabetes()
        X = pd.DataFrame(diabetes.data, columns=diabetes.feature_names)
        Y = pd.Series(diabetes.target, name='response')
        df = pd.concat( [X,Y], axis=1 )

        st.markdown('The **Diabetes** dataset is used as the example.')
        st.write(df.head(5))


