import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def shorten_categories(categories,cutoff):
    categorical_map = {}
    for i in range(len(categories)):
        if categories.values[i] >= cutoff:
            categorical_map[categories.index[i]] = categories.index[i]
        else:
            categorical_map[categories.index[i]] = 'other'
        
    return categorical_map

def clean_education(x):
    if 'Bachelor’s degree' in x:
        return "Bachelor's degree"
    if 'Master’s degree' in x:
        return "Master's degree"
    if 'Professional degree' in x or 'other doctoral' in x:
        return "Post grad"
    return 'Less than a Bachelors'

def clean_experience(x):
    if x == "More than 50 years":
        return 50
    if x == "Less than 1 year":
        return 0.5
    return float(x)

@st.cache_data
def load_data():
    df = pd.read_csv("data/survey_results_public.csv")
    df = df[["Country","EdLevel","YearsCodePro","Employment","ConvertedCompYearly","Age"]]
    df = df.rename({"ConvertedCompYearly":"Salary"},axis=1)
    df = df[df['Salary'].notnull()]
    df = df.dropna()
    df = df[df['Employment'] == "Employed, full-time"]
    df.drop("Employment",axis=1)
    country_map = shorten_categories(df['Country'].value_counts(),400)
    df['Country'] = df['Country'].map(country_map)
    df = df[df['Salary']< df.Salary.quantile(0.98)]
    df = df[df['Salary']>= df.Salary.quantile(0.05)]
    df = df[df['Country'] != 'Other']
    df['YearsCodePro'] = df['YearsCodePro'].apply(clean_experience)
    df['EdLevel'] = df['EdLevel'].apply(clean_education)
    return df

df = load_data()

def show_explore_page():
    st.title("Explore Software Developer Salaries")

    st.write("""
        ### Stack Overflow Developer Salary 2023
""")
    
    data = df['Country'].value_counts()

    fig1, ax1 = plt.subplots()
    ax1.pie(data,labels=data.index,autopct="%1.1f",shadow=True,startangle=90)
    ax1.axis("equal")

    st.write("""### :red[Number of Data from different Countries]""")

    st.pyplot(fig1)

    st.write("""
        ### :red[Mean salary (in $) based on country]
             
""")
    
    data = df.groupby(["Country"])['Salary'].mean().sort_values(ascending=True)
    st.bar_chart(data)

    st.write("""
        ### :red[Mean salary (in $) based on Experience]
             
""")
    
    data = df.groupby(["YearsCodePro"])['Salary'].mean().sort_values(ascending=True)
    st.line_chart(data,color="#ffaa00")
