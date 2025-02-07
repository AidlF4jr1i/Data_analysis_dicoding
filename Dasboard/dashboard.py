import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import numpy as np
# Load dataset
hour_df = pd.read_csv('analysis.csv')

# Set the page title
st.set_page_config(page_title='Bike Sharing Dashboard', page_icon=':bike:')

# Set the sidebar image
st.sidebar.image("https://3.bp.blogspot.com/_UaJWUMI3LDg/TOS0kZnRCCI/AAAAAAAAAB4/nodyhhiM1PY/s1600/CIMG0443.JPG", 
                 caption='Bike Sharing Dataset')

# Add title to the app
st.title('Bike Sharing Dashboard')

# Add subtitle
st.subheader('Insights and Visualizations')

# Explore the effect of weather on bike rentals
st.header('Effect of Weather on Bike Rentals')
fig1, ax1 = plt.subplots(figsize=(10,6))

# Temperature
hour_df.groupby('temp_y')['cnt_y'].mean().plot(ax=ax1, label='Temperature', color='blue')

# Humidity
hour_df.groupby('hum_y')['cnt_y'].mean().plot(ax=ax1, label='Humidity', color='green')

# Windspeed
hour_df.groupby('windspeed_y')['cnt_y'].mean().plot(ax=ax1, label='Windspeed', color='red')

ax1.set_title('Effect of Weather on Total Bike Rentals')
ax1.set_xlabel('Weather Parameter')
ax1.set_ylabel('Average Bike Rentals')
ax1.legend()
st.pyplot(fig1)

# Explore the difference in bike rentals between weekdays and weekends/holidays
st.header('Difference in Bike Rentals between Weekdays and Weekends/Holidays')
fig2, ax2 = plt.subplots(figsize=(10,6))
weekday_counts = hour_df.groupby(['weekday_y'])['cnt_y'].mean()
colors = ['grey' if day != 'Saturday' else 'red' for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']]
ax2.pie(weekday_counts, labels=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], colors=colors, autopct='%1.1f%%')
ax2.set_title('Comparison of Total Bike Rentals')
st.pyplot(fig2)

# Explore the comparison of bike rental behavior between registered and casual users
st.header('Comparison of Bike Rental Behavior between Registered and Casual Users')

# Monthly comparison
fig3, ax3 = plt.subplots(figsize=(10,6))
month_registered_counts = hour_df.groupby(['mnth_x'])['registered_y'].sum()
month_casual_counts = hour_df.groupby(['mnth_x'])['casual_y'].sum()

df_month = pd.DataFrame({'Registered': month_registered_counts, 'Casual': month_casual_counts})
df_month.plot(kind='bar', color=['blue', 'orange'], ax=ax3)
ax3.set_title('Comparison of Bike Rental Behavior (Monthly)')
ax3.set_xlabel('Month')
ax3.set_ylabel('Total Number of Bike Rentals')
ax3.legend()
st.pyplot(fig3)

# Clustering result visualization
st.header('Clustering Result Visualization')

# Scatter plot
fig5, ax5 = plt.subplots(figsize=(10,6))
colors = ['red', 'green', 'blue']
for i in range(3):
    df_cluster = hour_df[hour_df['cluster'] == i]
    ax5.scatter(df_cluster['hr'], df_cluster['cnt_y'], label=f'Cluster {i+1}', color=colors[i])
ax5.set_title('Clustering Result')
ax5.set_xlabel('Hour')
ax5.set_ylabel('Number of Bike Rentals')
ax5.legend()
st.pyplot(fig5)

# Add correlation calculation to the sidebar
numeric_columns = hour_df.select_dtypes(include=[np.number]).columns
correlation = hour_df[numeric_columns].corr()
st.sidebar.header('Correlation Calculation')
st.sidebar.write(correlation)

# Calculate the total number of 'Casual' and 'Registered' users
total_casual = hour_df['casual_y'].sum()
total_registered = hour_df['registered_y'].sum()
total_users = total_casual + total_registered

# Calculate the percentage of 'Casual' and 'Registered' users
percentage_casual = (total_casual / total_users) * 100
percentage_registered = (total_registered / total_users) * 100

# Add user counts to the sidebar
st.sidebar.header('User Counts')
st.sidebar.write(f"Casual Users: {total_casual} ({percentage_casual:.2f}%)")
st.sidebar.write(f"Registered Users: {total_registered} ({percentage_registered:.2f}%)")

# Add dataset information to the sidebar
st.sidebar.header('Dataset Information')
st.sidebar.write('The dataset contains 33 columns, including data on instant, dteday, season, yr, mnth, hr, holiday, weekday, workingday, weathersit, temp_x and temp_y (temperature), atemp_x and atemp_y (feeling temperature), hum_x and hum_y (humidity), windspeed_x and windspeed_y (wind speed), casual_x and casual_y (number of casual users), registered_x and registered_y (number of registered users), cnt_x and cnt_y (total count of bike rentals) for two different years (_x for one year and _y for another year). The dataset also includes a \'cluster\' column.')
