import streamlit as st
import pickle
import pandas as pd
import numpy as np
import os
import rarfile

st.set_page_config(page_title="Viz Demo")

# Get the root directory of the project
file_dir = os.path.dirname(os.path.abspath(__file__))  # Directory of current file
repo_root = os.path.abspath(os.path.join(file_dir, '..'))  # One level up from /pages

# Build the paths for the pickle files, relative to the repo root
df_path = os.path.join(repo_root, 'datasets', 'df.pkl')
pipeline_rar_path = os.path.join(repo_root, 'datasets', 'pipeline.rar')
extracted_pipeline_path = os.path.join(repo_root, 'datasets', 'pipeline.pkl')

# Check if df.pkl exists
if not os.path.exists(df_path):
    st.error(f"Error: 'df.pkl' not found at {df_path}")
    st.stop()

# Extract pipeline.rar if pipeline.pkl doesn't exist
if not os.path.exists(extracted_pipeline_path):
    if os.path.exists(pipeline_rar_path):
        try:
            with rarfile.RarFile(pipeline_rar_path) as rar:
                rar.extractall(os.path.join(repo_root, 'datasets'))
            st.success("✅ pipeline.pkl extracted successfully from pipeline.rar.")
        except Exception as e:
            st.error(f"❌ Error extracting pipeline.rar: {e}")
            st.stop()
    else:
        st.error(f"Error: 'pipeline.rar' not found at {pipeline_rar_path}")
        st.stop()

# Load data and model pipeline
with open(df_path, 'rb') as file:
    df = pickle.load(file)

with open(extracted_pipeline_path, 'rb') as file:
    pipeline = pickle.load(file)

st.header('🏡 Enter Your Inputs')

# User input fields
property_type = st.selectbox('Property Type', ['flat', 'house'])
sector = st.selectbox('Sector', sorted(df['sector'].unique()))
bedroom_min = int(df['bedRoom'].min())
bedroom_max = int(df['bedRoom'].max())
bedrooms = st.slider('Number of Bedrooms', min_value=bedroom_min, max_value=bedroom_max, value=2)
bathroom = float(st.selectbox('Number of Bathrooms', sorted(df['bathroom'].unique())))
balcony = st.selectbox('Balconies', sorted(df['balcony'].unique()))
property_age = st.selectbox('Property Age', sorted(df['agePossession'].unique()))
built_up_area = float(st.number_input('Built Up Area'))
servant_room = 1.0 if st.checkbox('Servant Room', value=False) else 0.0
store_room = float(st.selectbox('Store Room', [0.0, 1.0]))
furnishing_type = st.selectbox('Furnishing Type', sorted(df['furnishing_type'].unique()))
luxury_category = st.selectbox('Luxury Category', sorted(df['luxury_category'].unique()))
floor_category = st.selectbox('Floor Category', sorted(df['floor_category'].unique()))

if st.button('🏠 Predict'):
    input_data = [[
        property_type, sector, bedrooms, bathroom, balcony,
        property_age, built_up_area, servant_room, store_room,
        furnishing_type, luxury_category, floor_category
    ]]

    input_columns = [
        'property_type', 'sector', 'bedRoom', 'bathroom', 'balcony',
        'agePossession', 'built_up_area', 'servant room', 'store room',
        'furnishing_type', 'luxury_category', 'floor_category'
    ]

    input_df = pd.DataFrame(input_data, columns=input_columns)

    # Predict and display result
    predicted_price = np.expm1(pipeline.predict(input_df))[0]
    price_low = predicted_price - 0.22
    price_high = predicted_price + 0.22

    st.success(f"💰 Estimated price range: ₹{round(price_low, 2)} Cr to ₹{round(price_high, 2)} Cr")
