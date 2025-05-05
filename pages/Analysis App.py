import streamlit as st
import pandas as pd
import plotly.express as px
import pickle
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn as sns
import os

st.set_page_config(page_title="Plotting Demo")

st.title('Analytics')

# Load data
file_path = os.path.join(os.path.dirname(__file__), '..', 'datasets', 'data_viz1.csv')
new_df = pd.read_csv(file_path)

feature_text_path = os.path.join(os.path.dirname(__file__), '..', 'datasets', 'feature_text.pkl')
with open(feature_text_path, 'rb') as f:
    feature_text = pickle.load(f)


# Optional: Convert price from lakhs to crores if needed
new_df['price'] = new_df['price'] / 100

numeric_cols = ['price', 'price_per_sqft', 'built_up_area', 'latitude', 'longitude']
group_df = new_df.groupby('sector')[numeric_cols].mean()

# Sector-wise Geomap
st.header('Sector Price per Sqft Geomap')
fig = px.scatter_map(group_df,
                     lat="latitude",
                     lon="longitude",
                     color="price_per_sqft",
                     size='built_up_area',
                     color_continuous_scale=px.colors.cyclical.IceFire,
                     zoom=10,
                     width=1200,
                     height=700,
                     hover_name=group_df.index,
                     map_style="open-street-map")
st.plotly_chart(fig)

# WordCloud
st.header("Features Wordcloud")
wordcloud = WordCloud(width=800, height=800,
                      background_color='white',
                      stopwords=set(['s']),
                      min_font_size=10).generate(feature_text)
fig, ax = plt.subplots(figsize=(8, 8))
ax.imshow(wordcloud, interpolation='bilinear')
ax.axis("off")
plt.tight_layout(pad=0)
st.pyplot(fig)

# Area vs Price scatter
st.header("Area, Price, and Bedroom Distribution")
property_type = st.selectbox("Select Property Type", ['flat', 'house'])

if property_type == 'house':
    fig1 = px.scatter(new_df[new_df['property_type'] == 'house'],
                      x="built_up_area",
                      y="price",
                      color="bedRoom",
                      title="Price vs. Area vs. Number of Bedrooms for Houses")
else:
    fig1 = px.scatter(new_df[new_df['property_type'] == 'flat'],
                      x="built_up_area",
                      y="price",
                      color="bedRoom",
                      title="Price vs. Area vs. Number of Bedrooms for Flats")

fig1.update_layout(
    xaxis_title="Built-up Area (sq. ft.)",
    yaxis_title="Price (in Crore)",
    coloraxis_colorbar_title="Number of Bedrooms"
)
st.plotly_chart(fig1, use_container_width=True)

# Pie Chart
st.header('BHK Pie Chart')
sector_options = new_df['sector'].unique().tolist()
sector_options.insert(0, 'overall')
selected_sector = st.selectbox('Select Sector', sector_options)

if selected_sector == 'overall':
    bed_room_counts = new_df['bedRoom'].value_counts(normalize=True) * 100
else:
    bed_room_counts = new_df[new_df['sector'] == selected_sector]['bedRoom'].value_counts(normalize=True) * 100

bed_room_counts = bed_room_counts.reset_index()
bed_room_counts.columns = ['bedRoom', 'percentage']

# Combine categories <= 2%
bed_room_counts['bedRoom'] = bed_room_counts.apply(
    lambda row: 'Others' if row['percentage'] <= 2 else row['bedRoom'], axis=1)
others_percentage = bed_room_counts[bed_room_counts['bedRoom'] == 'Others']['percentage'].sum()
bed_room_counts = bed_room_counts[bed_room_counts['bedRoom'] != 'Others']
others_df = pd.DataFrame({'bedRoom': ['Others'], 'percentage': [others_percentage]})
bed_room_counts = pd.concat([bed_room_counts, others_df], ignore_index=True)

fig2 = px.pie(bed_room_counts, names='bedRoom', values='percentage', title="Pie Chart: Number of Bedrooms")
st.plotly_chart(fig2, use_container_width=True)

# BHK Box Plot
st.header('Side by Side BHK Price Comparison')
fig3 = px.box(
    new_df[new_df['bedRoom'] <= 4],
    x='bedRoom',
    y='price',
    title='BHK Price Range',
    labels={'bedRoom': 'Number of Bedrooms (BHK)', 'price': 'Price (in Crore)'}
)
st.plotly_chart(fig3, use_container_width=True)

# Filter negative prices before plotting
new_df = new_df[new_df['price'] > 0]

# Distribution Plot
st.header('Side by Side Price Distribution by Property Type')
st.markdown("📊 **Price** is in crores. The **y-axis** shows probability density (1 per crore).")

fig4 = plt.figure(figsize=(10, 4))
sns.histplot(data=new_df[new_df['property_type'] == 'house'], x='price', kde=True, label='House', stat='density', color='skyblue')
sns.histplot(data=new_df[new_df['property_type'] == 'flat'], x='price', kde=True, label='Flat', stat='density', color='salmon')

plt.xlabel('Price (Cr)')
plt.ylabel('Density (1/Cr)')
plt.title('Price Distribution: House vs Flat')
plt.legend(title='Property Type')
plt.grid(True)

st.pyplot(fig4)
