import streamlit as st
import pickle
import pandas as pd
import numpy as np
import os

st.set_page_config(page_title="Real Estate Price Predictor")

# Load the preprocessed dataset and prediction pipeline
df_path = os.path.join(os.path.dirname(__file__), 'df.pkl')
pipeline_path = os.path.join(os.path.dirname(__file__), 'pipeline.pkl')

# Check if files exist
if not os.path.exists(df_path):
    st.error(f"❌ Missing file: {df_path}")
    st.stop()
if not os.path.exists(pipeline_path):
    st.error(f"❌ Missing file: {pipeline_path}")
    st.stop()

# Load files
with open(df_path, 'rb') as file:
    df = pickle.load(file)

with open(pipeline_path, 'rb') as file:
    pipeline = pickle.load(file)

# Title
st.header('🏡 Real Estate Price Predictor')

# User Inputs
property_type = st.selectbox('Property Type', ['flat', 'house'])
sector = st.selectbox('Sector', sorted(df['sector'].unique()))
bedrooms = st.slider('Number of Bedrooms', int(df['bedRoom'].min()), int(df['bedRoom'].max()), 2)
bathroom = float(st.selectbox('Number of Bathrooms', sorted(df['bathroom'].unique())))
balcony = st.selectbox('Balconies', sorted(df['balcony'].unique()))
property_age = st.selectbox('Property Age', sorted(df['agePossession'].unique()))
built_up_area = float(st.number_input('Built Up Area (sq. ft.)'))

servant_room = 1.0 if st.checkbox('Servant Room', value=False) else 0.0
store_room = float(st.selectbox('Store Room', [0.0, 1.0]))
furnishing_type = st.selectbox('Furnishing Type', sorted(df['furnishing_type'].unique()))
luxury_category = st.selectbox('Luxury Category', sorted(df['luxury_category'].unique()))
floor_category = st.selectbox('Floor Category', sorted(df['floor_category'].unique()))

# Prediction
if st.button('🏠 Predict'):

    input_data = [[
        property_type, sector, bedrooms, bathroom, balcony, property_age,
        built_up_area, servant_room, store_room, furnishing_type,
        luxury_category, floor_category
    ]]

    columns = [
        'property_type', 'sector', 'bedRoom', 'bathroom', 'balcony',
        'agePossession', 'built_up_area', 'servant room', 'store room',
        'furnishing_type', 'luxury_category', 'floor_category'
    ]

    input_df = pd.DataFrame(input_data, columns=columns)

    # Predict and display result
    try:
        base_price = np.expm1(pipeline.predict(input_df))[0]
        low = base_price - 0.22
        high = base_price + 0.22

        st.success(f"💰 Estimated price: ₹ {round(low, 2)} Cr to ₹ {round(high, 2)} Cr")
    except Exception as e:
        st.error(f"Prediction failed: {e}")
