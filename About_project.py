import streamlit as st
import mysql.connector
import pandas as pd

# side-bar features
# st.sidebar.title('Pages')
# st.sidebar.radio(label='go to :', options=['About project', 'Data insights', 'preprocessed data-frame'])

# page body
st.markdown("<h1 style='text-align: center;'>Stroke Prediction Dataset</h1>", unsafe_allow_html=True)
st.image('assets/h_stroke.png', width=700)

st.markdown('### Predicting Stroke Risk: Turning Data into Life-Saving Insights')
st.text('Every 2 seconds, someone in the world has a stroke but what if we could predict it before it happens?')
st.text('This project uses real-world inspired data to identify the factors most linked to stroke like : age, hypertension, heart disease, smoking, glucose level, BMI')

st.markdown("---")
st.markdown('### Source:')
st.text('Data originally sourced from Kaggle, then uploaded to an online MySQL database (Aiven) and retrieved programmatically for analysis')

st.markdown("---")
st.markdown('### Overview:')
st.text('The dataset contains patient health information used to predict stroke incidence.')
st.text('It includes medical history and lifestyle factors.')

st.markdown("---")
st.markdown('### Size:')
st.text('Rows: 43400\nFeature: 12')
st.text('features are:\nid : Unique identifier\ngender : Male / Female / Other\nage : Age of the patient\nhypertension : 0 = No, 1 = Yes\nheart_disease : 0 = No, 1 = Yes\never_married : Yes / No\nwork_type : Type of employment\nResidence_type : Urban / Rural\navg_glucose_level : Average blood glucose level\nbmi : Body Mass Index\nsmoking_status : Smoking habits\nstroke(Target) : 0 = No stroke, 1 = Stroke')

st.markdown("---")
st.markdown('### A snip of the dataframe:')
#coonection to snip some data


conn = mysql.connector.connect(
    host="midproject-midproject.h.aivencloud.com",
    port=17017,
    user="avnadmin",
    password="AVNS_4cb10TGYTOTF7KRj5r3", 
    database="stroke_project"
)


# quering data    
command = """           
SELECT * FROM stroke_data
LIMIT 10;                      
"""

df = pd.read_sql(command, conn) 

# to streamlit
st.dataframe(df)

st.markdown("---")
st.markdown('### Note:')
st.text('The dataset is imbalanced so majority of patients did not have a stroke.')  
st.text('Missing BMI and smoking_status values were handled during preprocessing.')

