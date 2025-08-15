import streamlit as st 
import pyodbc
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt



# connection to collect the data
conn = pyodbc.connect("DRIVER={MySQL ODBC 9.3 Unicode Driver};"
    "SERVER=midproject-midproject.h.aivencloud.com;"
    "PORT=17017;"
    "DATABASE=stroke_project;"
    "UID=avnadmin;"
    "PWD=AVNS_4cb10TGYTOTF7KRj5r3;"
    "OPTION=3;",
    autocommit=True)

# quering data
command = """           
SELECT * FROM stroke_data;                      
"""
df = pd.read_sql(command, conn) 

# page structure
st.markdown("<h1 style='text-align: center;'>Stroke data insights</h1>", unsafe_allow_html=True)
tab1, tab2 = st.tabs(['general insights', 'bi-variate plots'])


# correcting the dtype 
df['bmi'] = df['bmi'].astype(float)

# data extracted feature ...
# age categories
def categorical_age(arg):
    if arg <= 1:
        return 'new born'
    elif arg > 1 and arg <= 18:
        return 'young'
    elif arg > 19 and arg <= 59 :
        return 'adult'
    else:
        return 'old'

df['age_group'] = df['age'].apply(categorical_age)
# bmi categories
def categorical_bmi(arg):
    if arg < 18.5:
        return 'under weight'
    elif arg >= 18.5 and arg <= 24.9:
        return 'normal weight'
    elif arg >= 25 and arg < 27.5:
        return 'over weight'
    elif arg >= 27.5:
        return 'obese'
    else:
        return np.nan

df['bmi_group'] = df['bmi'].apply(categorical_bmi)  
# hypertension & heart disease  
def cardiovascular_check(arg):
    if arg['hypertension'] and arg['heart_disease']:
        return 1
    else:
        return 0

df['cardio_risk'] = df.apply(cardiovascular_check, axis=1)  

with tab1:
    st.subheader('Distribution of each feature:')
    st.write("<h5 style='text-align: center;'>Distribution of categorical feature</h5>",unsafe_allow_html=True)

    # cols creation
    col1, col2= st.columns(2)

    cat_col = df.select_dtypes(include='O').columns
    for col in cat_col:
        with col1:
            if df[col].nunique() < 4:
                dff = df.groupby(col)[['age']].count().reset_index()
                fig, axes = plt.subplots(figsize=(8, 6))
                axes.pie(x=dff['age'], labels=dff[col], autopct="%.2f%%")
                plt.title(f'distribution of {col}')
                st.pyplot(fig)
            else:
                with col2:
                    fig, axes = plt.subplots(figsize=(10,10))
                    sns.countplot(df, x=df[col], ax=axes)
                    plt.title(f"Countplot of {col}")
                    st.pyplot(fig)


    st.markdown('---')
    st.write("<h5 style='text-align: center;'>Distribution of numerical feature</h5>",unsafe_allow_html=True)

    # cols creation
    col1, col2= st.columns(2)

    num_cols = df.select_dtypes(include='number').columns
    for col in num_cols[1:]:
        if df[col].nunique() != 2:
            with col1:
                fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(8,6))
                sns.histplot(df, x=df[col], kde=True, ax=axes[0])
                sns.boxplot(df, x=df[col], ax=axes[1])
                fig.suptitle(f"Distribution of {col}", fontsize=14) 
                st.pyplot(fig)
        else:
            with col2:
                fig, axes = plt.subplots(figsize=(10,9))
                sns.histplot(df, x=df[col], bins= 2, ax=axes)
                plt.xticks([0, 1])
                plt.title(f"distribution of {col}")
                st.pyplot(fig)



with tab2:
    var_title = st.subheader('effect of categorical columns on the target \'stroke\' :')

    cate_option = st.selectbox(label='The effect of', options=['gender', 'age_group', 'Residence_type', 'work_type', 'bmi_group', 'ever_married', 'smoking_status'])

    # filtring on stroke cases
    stroke_df = df[df['stroke'] == 1]


    if st.button('apply effect', key='apply_effect_1'):
        var_title.write(f"<h5 style='text-align: center;'>effect of \'{cate_option}\' on the target \'stroke\' </h5>",unsafe_allow_html=True)
        fig, axes = plt.subplots(figsize=(8, 6))
        sns.countplot(stroke_df, x='stroke', hue=cate_option)
        plt.title(f'Distribution of stroke under the effect of {cate_option}')
        st.pyplot(fig)


    st.markdown('---')
    var_title = st.subheader('effect of numerical columns on the target \'stroke\' :')
    num_option = st.selectbox(label='The effect of', options=['age', 'bmi', 'avg_glucose_level', 'hypertension', 'heart_disease', 'cardio_risk'])



    if st.button('apply effect', key='apply_effect_2'):
        var_title.write(f"<h5 style='text-align: center;'>effect of \'{num_option}\' on the target \'stroke\' </h5>",unsafe_allow_html=True)
        if df[num_option].nunique() == 2:
            fig, axes = plt.subplots(figsize=(8, 6))
            sns.barplot(df, x='stroke', y=num_option)
            plt.title(f'Distribution of stroke under the effect of {num_option}')
            st.pyplot(fig)
        else:
            fig, axes = plt.subplots(figsize=(8, 6))
            sns.boxplot(df, x='stroke', y=num_option)
            plt.title(f'Distribution of stroke under the effect of {num_option}')
            st.pyplot(fig)
