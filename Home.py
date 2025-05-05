import streamlit as st

# Set the page config
st.set_page_config(
    page_title="Gurgaon Real Estate Analytics App",
    page_icon="👋",
    layout="wide"
)

# Change background color (very light green)
st.markdown(
    """
    <style>
    .stApp {
        background-color: #d0f0c0;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Heading
st.markdown(
    "<h1 style='text-align: center; color: black;'>Welcome to Gurgaon Real Estate! 👋👋</h1>",
    unsafe_allow_html=True
)

# Full-width image
st.markdown(
    """
    <style>
    .banner-img {
        width: 100%;
        height: auto;
        display: block;
        margin-left: auto;
        margin-right: auto;
    }
    </style>
    <img class="banner-img" src="https://images.fineartamerica.com/images/artworkimages/mediumlarge/2/morning-in-mahattan-nyc-pawelgaul.jpg" alt="Gurgaon Skyline">
    """,
    unsafe_allow_html=True
)