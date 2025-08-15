import streamlit as st 
import pandas as pd

train_df = pd.read_csv('assets/train_result.csv')
test_df = pd.read_csv('assets/test_result.csv')

# page structure 
st.markdown("<h1 style='text-align: center;'>preprocessed tables results</h1>", unsafe_allow_html=True)
st.markdown("---")
st.subheader('train result')
st.dataframe(train_df)
st.subheader('test result')
st.dataframe(test_df)

