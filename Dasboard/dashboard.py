import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import numpy as np

# Load dataset
hour_df = pd.read_csv('analysis.csv')
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])  # Pastikan kolom tanggal dalam format datetime

# Set the page title
st.set_page_config(page_title='Bike Sharing Dashboard', page_icon=':bike:')

# Set the sidebar image
st.sidebar.image("https://3.bp.blogspot.com/_UaJWUMI3LDg/TOS0kZnRCCI/AAAAAAAAAB4/nodyhhiM1PY/s1600/CIMG0443.JPG", 
                 caption='Bike Sharing Dataset')

# Sidebar filters
st.sidebar.header("Filter Data")

# Filter berdasarkan rentang tanggal
date_range = st.sidebar.date_input("Pilih Rentang Tanggal", 
                                   [hour_df['dteday'].min(), hour_df['dteday'].max()],
                                   min_value=hour_df['dteday'].min(),
                                   max_value=hour_df['dteday'].max())

# Filter berdasarkan musim (season_y)
season_mapping = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
season_options = [season_mapping[s] for s in hour_df['season_y'].unique()]
selected_season = st.sidebar.selectbox("Pilih Musim", season_options)
selected_season_num = [k for k, v in season_mapping.items() if v == selected_season][0]

# Filter berdasarkan kondisi cuaca (weathersit_y)
weather_mapping = {1: "Clear", 2: "Cloudy", 3: "Light Rain", 4: "Heavy Rain"}
weather_options = [weather_mapping[w] for w in hour_df['weathersit_y'].unique()]
selected_weather = st.sidebar.multiselect("Pilih Kondisi Cuaca", weather_options, default=weather_options)
selected_weather_num = [k for k, v in weather_mapping.items() if v in selected_weather]

# Terapkan filter ke dataset
filtered_df = hour_df[(hour_df['dteday'] >= pd.to_datetime(date_range[0])) &
                      (hour_df['dteday'] <= pd.to_datetime(date_range[1])) &
                      (hour_df['season_y'] == selected_season_num) &
                      (hour_df['weathersit_y'].isin(selected_weather_num))]

# Add title to the app
st.title('Bike Sharing Dashboard')
st.subheader('Insights and Visualizations')

# Total Bike Rentals over Time
st.header('Total Bike Rentals over Time')
fig1, ax1 = plt.subplots(figsize=(12,6))
filtered_df.groupby('dteday')['cnt_y'].sum().plot(ax=ax1, color='blue', marker='o')
ax1.set_title('Total Bike Rentals Over Time')
ax1.set_xlabel('Date')
ax1.set_ylabel('Total Rentals')
st.pyplot(fig1)

# Bike Rentals by Hour
st.header('Bike Rentals by Hour of the Day')
fig2, ax2 = plt.subplots(figsize=(10,6))
filtered_df.groupby('hr')['cnt_y'].mean().plot(ax=ax2, color='green', marker='o')
ax2.set_title('Average Bike Rentals by Hour')
ax2.set_xlabel('Hour of the Day')
ax2.set_ylabel('Average Rentals')
st.pyplot(fig2)

# Comparison of Registered and Casual Users
st.header('Comparison of Registered vs Casual Users')
fig3, ax3 = plt.subplots(figsize=(10,6))
registered_counts = filtered_df.groupby(['mnth_y'])['registered_y'].sum()
casual_counts = filtered_df.groupby(['mnth_y'])['casual_y'].sum()

df_month = pd.DataFrame({'Registered': registered_counts, 'Casual': casual_counts})
df_month.plot(kind='bar', color=['blue', 'orange'], ax=ax3)
ax3.set_title('Comparison of Bike Rental Behavior (Monthly)')
ax3.set_xlabel('Month')
ax3.set_ylabel('Total Number of Bike Rentals')
ax3.legend()
st.pyplot(fig3)

# Clustering result visualization
st.header('Clustering Result Visualization')
fig4, ax4 = plt.subplots(figsize=(10,6))
colors = ['red', 'green', 'blue']
for i in range(3):
    df_cluster = filtered_df[filtered_df['cluster'] == i]
    ax4.scatter(df_cluster['hr'], df_cluster['cnt_y'], label=f'Cluster {i+1}', color=colors[i])
ax4.set_title('Clustering Result')
ax4.set_xlabel('Hour')
ax4.set_ylabel('Number of Bike Rentals')
ax4.legend()
st.pyplot(fig4)

# Add correlation calculation to the sidebar
numeric_columns = filtered_df.select_dtypes(include=[np.number]).columns
correlation = filtered_df[numeric_columns].corr()
st.sidebar.header('Correlation Calculation')
st.sidebar.write(correlation)

# Calculate user counts
total_casual = filtered_df['casual_y'].sum()
total_registered = filtered_df['registered_y'].sum()
total_users = total_casual + total_registered

percentage_casual = (total_casual / total_users) * 100 if total_users > 0 else 0
percentage_registered = (total_registered / total_users) * 100 if total_users > 0 else 0

# Display user counts
st.sidebar.header('User Counts')
st.sidebar.write(f"Casual Users: {total_casual} ({percentage_casual:.2f}%)")
st.sidebar.write(f"Registered Users: {total_registered} ({percentage_registered:.2f}%)")

# Add dataset information to the sidebar
st.sidebar.header('Dataset Information')
st.sidebar.write('This dataset contains bike rental data including season, weather, temperature, humidity, wind speed, and user type. The dataset is filtered based on user selections.')

