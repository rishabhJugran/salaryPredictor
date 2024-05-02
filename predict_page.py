import streamlit as st
import pickle
import numpy as np

def load_model():
    with open('saved_steps.pkl','rb') as file:
        data = pickle.load(file)
    return data

data = load_model()

regressor = data['model']
le_country = data['le_country']
le_age = data['le_age']
le_education = data['le_education']

def show_predict_page():
    st.title("Software Developer Salary Prediction")

    st.write("""### We need some information to predict the salary""")

    countries = (
        'United States of America',
        'Germany',
        'United Kingdom of Great Britain and Northern Ireland',
        'Canada',
        'India',
        'France',
        'Netherlands',
        'Australia',
        'Brazil',
        'Spain',
        'Sweden',
        'Italy',
        'Poland',
        'Switzerland',
        'Denmark',
        'Norway',
        'Israel'
    )

    educations = (
        'Less than a Bachelors',
        'Bachelor\'s degree',
        'Master\'s degree',
        'Post grad'
    )

    ages = (
        '25-34 years old',
        '35-44 years old',
        '18-24 years old',
        '45-54 years old',
        '55-64 years old',
        '65 years or older'
    )

    country = st.selectbox("Country",countries)
    age = st.selectbox("Developer's Age",ages)
    education = st.selectbox("Education Level",educations)
    experience = st.slider("Years of Experience",0,50,3)

    check_salary = st.button("Estimate Salary")
    if check_salary:
        x1 = np.array([[country,education,experience,age]])
        x1[:,0] = le_country.transform(x1[:,0])
        x1[:,1] = le_education.transform(x1[:,1])
        x1[:,3] = le_age.transform(x1[:,3])
        x1 = x1.astype(float)

        salary = regressor.predict(x1)
        st.subheader(f"The estimated salary is :green[${salary[0]:.2f}]")
