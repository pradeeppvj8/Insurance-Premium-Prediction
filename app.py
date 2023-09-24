import streamlit as st
import numpy as np
import pandas as pd
import pickle

model = pickle.load(open("model.pkl", "rb"))
transformer = pickle.load(open("transformer.pkl", "rb"))
encoder = pickle.load(open("label_encoder.pkl", "rb"))

# Title
st.title("Insurance Premium Prediction")

# Age
age = st.text_input(label="Age", value=18)

# Gender dropdown
gender = st.selectbox( label="Gender", options= ('Male','Female'))

# BMI
bmi = st.text_input(label="BMI", value=20, max_chars=20)

if bmi != "":
    bmi = float(bmi)

# Children
children = st.selectbox(label="Number Of Children", options=(0,1,2,3,4,5,6))
children = int(children)

# Smoker
smoker = st.selectbox(label="Smoker ?", options=("Yes", "No"))

# Region
region = st.selectbox(label="Region", options=("southwest","northwest","southeast","northeast"))

l = {}
l["age"] = age
l["sex"] = gender
l["bmi"] = bmi
l["children"] = children
l["smoker"] = smoker 
l["region"] = region

df = pd.DataFrame(l, index= [0])
df["region"] = encoder.transform(df["region"])
df["smoker"] = df["smoker"].map({"Yes" : 1 , "No" : 0})
df["sex"] =  df["sex"].map({"Male" : 1 , "Female" : 0})

df = transformer.transform(df)
prediction = model.predict(df)

if st.button("Submit"):
    prediction_str = str(round(prediction[0],2))
    st.header(f"{prediction_str} INR")