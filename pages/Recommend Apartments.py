import streamlit as st
import pickle
import pandas as pd
import numpy as np

# Set page configuration
st.set_page_config(page_title="Recommend Apartments Based on Societies")

# Set background color to light blue using custom CSS
st.markdown("""
    <style>
        body {
            background-color: #ADD8E6;
            color: black;
        }
    </style>
""", unsafe_allow_html=True)

# Load the datasets
location_df = pickle.load(open('datasets/location_distance.pkl', 'rb'))
cosine_sim1 = pickle.load(open('datasets/cosine_sim1.pkl', 'rb'))
cosine_sim2 = pickle.load(open('datasets/cosine_sim2.pkl', 'rb'))
cosine_sim3 = pickle.load(open('datasets/cosine_sim3.pkl', 'rb'))


def recommend_properties_with_scores(property_name, top_n=5):
    cosine_sim_matrix = 0.5 * cosine_sim1 + 0.8 * cosine_sim2 + 1 * cosine_sim3

    # Get the similarity scores for the property using its name as the index
    sim_scores = list(enumerate(cosine_sim_matrix[location_df.index.get_loc(property_name)]))

    # Sort properties based on the similarity scores
    sorted_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the indices and scores of the top_n most similar properties
    top_indices = [i[0] for i in sorted_scores[1:top_n + 1]]
    top_scores = [i[1] for i in sorted_scores[1:top_n + 1]]

    # Retrieve the names of the top properties using the indices
    top_properties = location_df.index[top_indices].tolist()

    # Convert similarity scores to percentages and limit to 2 decimal places
    top_scores_percent = [round(score * 100, 2) for score in top_scores]

    # Create a dataframe with the results
    recommendations_df = pd.DataFrame({
        'Property Name': top_properties,
        'Your Ideal Match (%)': top_scores_percent
    })

    return recommendations_df


# Title and selection for location and radius
st.title('Select Location and Radius which will provide must popular society in that radius')

selected_location = st.selectbox('Location', sorted(location_df.columns.to_list()))

radius = st.number_input('Radius in Kms')

if st.button('Search'):
    result_ser = location_df[location_df[selected_location] < radius * 1000][selected_location].sort_values()

    for key, value in result_ser.items():
        st.text(f"{key} {round(value / 1000)} kms")

st.title('Recommend Societies Based on your Ideal Match')
selected_apartment = st.selectbox('Select an Apartment', sorted(location_df.index.to_list()))

if st.button('Recommend'):
    recommendation_df = recommend_properties_with_scores(selected_apartment)

    st.dataframe(recommendation_df)



