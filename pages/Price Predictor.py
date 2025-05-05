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

# Build the path for the pickle files, relative to the repo root
df_path = os.path.join(repo_root, 'datasets', 'df.pkl')
pipeline_rar_path = os.path.join(repo_root, 'datasets', 'pipeline.rar')
extracted_pipeline_path = os.path.join(repo_root, 'datasets', 'pipeline.pkl')

# Check if the files exist at the paths, if not, raise an error
if not os.path.exists(df_path):
    st.error(f"Error: 'df.pkl' not found at {df_path}")
    st.stop()

# Extract the pipeline.rar if the pipeline.pkl doesn't exist
if not os.path.exists(extracted_pipeline_path):
    if os.path.exists(pipeline_rar_path):
        try:
            # Extract the pipeline.rar file
            with rarfile.RarFile(pipeline_rar_path) as rar:
                rar.extractall(os.path.join(repo_root, 'datasets'))
            st.success("Pipeline extracted successfully.")
        except Exception as e:
            st.error(f"Error extracting the pipeline.rar: {e}")
            st.stop()
    else:
        st.error(f"Error: 'pipeline.rar' not found at {pipeline_rar_path}")
        st.stop()

# Load the data and pipeline
with open(df_path, 'rb') as file:
    df = pickle.load(file)

with open(extracted_pipeline_path, 'rb') as file:
    pipeline = pickle.load(file)

st.header('🏡 Enter Your Inputs')

# property_type
property_type = st.selectbox('Property Type', ['flat', 'house'])

# sector
sector = st.selectbox('Sector', sorted(df['sector'].unique().tolist()))

# Number of Bedrooms - slider
bedroom_min = int(df['bedRoom'].min())
bedroom_max = int(df['bedRoom'].max())
bedrooms = st.slider('Number of Bedrooms', min_value=bedroom_min, max_value=bedroom_max, value=2)

bathroom = float(st.selectbox('Number of Bathrooms', sorted(df['bathroom'].unique().tolist())))

balcony = st.selectbox('Balconies', sorted(df['balcony'].unique().tolist()))

property_age = st.selectbox('Property Age', sorted(df['agePossession'].unique().tolist()))

built_up_area = float(st.number_input('Built Up Area'))

# Servant Room - checkbox
servant_room = 1.0 if st.checkbox('Servant Room', value=False) else 0.0
store_room = float(st.selectbox('Store Room', [0.0, 1.0]))

furnishing_type = st.selectbox('Furnishing Type', sorted(df['furnishing_type'].unique().tolist()))
luxury_category = st.selectbox('Luxury Category', sorted(df['luxury_category'].unique().tolist()))
floor_category = st.selectbox('Floor Category', sorted(df['floor_category'].unique().tolist()))

if st.button('🏠 Predict'):

    # form a dataframe for prediction
    data = [[property_type, sector, bedrooms, bathroom, balcony, property_age, built_up_area, servant_room, store_room, furnishing_type, luxury_category, floor_category]]
    columns = ['property_type', 'sector', 'bedRoom', 'bathroom', 'balcony',
               'agePossession', 'built_up_area', 'servant room', 'store room',
               'furnishing_type', 'luxury_category', 'floor_category']

    # Convert to DataFrame
    one_df = pd.DataFrame(data, columns=columns)

    # Predict price
    base_price = np.expm1(pipeline.predict(one_df))[0]
    low = base_price - 0.22
    high = base_price + 0.22

    # Display predicted price
    st.text(f"The price of the flat is between {round(low, 2)} Cr and {round(high, 2)} Cr")
