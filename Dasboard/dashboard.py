import streamlit as st  # Import Streamlit duluan
st.set_page_config(page_title='🚴 Bike Sharing Dashboard', page_icon='🚲')  # Ini harus paling awal!

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# 📌 Caching untuk meningkatkan performa
@st.cache_data
def load_data(file_path):
    df = pd.read_csv(file_path)
    df['dteday'] = pd.to_datetime(df['dteday'])
    return df

# Load dataset
file_path = "analysis.csv"
df = load_data(file_path)

# Mapping untuk musim & kondisi cuaca
season_mapping = {1: "Musim Semi", 2: "Musim Panas", 3: "Musim Gugur", 4: "Musim Dingin"}
weather_mapping = {1: "Cerah", 2: "Berawan", 3: "Hujan Ringan", 4: "Hujan Lebat"}

# Sidebar dengan Filter
st.sidebar.image("https://3.bp.blogspot.com/_UaJWUMI3LDg/TOS0kZnRCCI/AAAAAAAAAB4/nodyhhiM1PY/s1600/CIMG0443.JPG", caption='Nikmati perjalanan sepeda Anda!')

st.sidebar.header("🎚️ Filter Data")
date_range = st.sidebar.date_input("📅 Pilih Rentang Tanggal", 
                                   [df['dteday'].min(), df['dteday'].max()],
                                   min_value=df['dteday'].min(),
                                   max_value=df['dteday'].max())

# Filter Musim
season_options = [season_mapping[s] for s in df['season_y'].unique()]
selected_season = st.sidebar.multiselect("🍂 Pilih Musim", season_options, default=season_options)
selected_season_num = [k for k, v in season_mapping.items() if v in selected_season]

# Filter Cuaca
weather_options = [weather_mapping[w] for w in df['weathersit_y'].unique()]
selected_weather = st.sidebar.multiselect("⛅ Pilih Kondisi Cuaca", weather_options, default=weather_options)
selected_weather_num = [k for k, v in weather_mapping.items() if v in selected_weather]

# Filter Hari Kerja vs Akhir Pekan
day_type = st.sidebar.radio("📅 Pilih Jenis Hari", ["Semua", "Hari Kerja", "Akhir Pekan/Hari Libur"])

# Terapkan Filter ke dataset dengan `.copy()` untuk menghindari `SettingWithCopyWarning`
filtered_df = df[
    (df['dteday'] >= pd.to_datetime(date_range[0])) & 
    (df['dteday'] <= pd.to_datetime(date_range[1])) & 
    (df['season_y'].isin(selected_season_num)) & 
    (df['weathersit_y'].isin(selected_weather_num))
].copy()

if day_type == "Hari Kerja":
    filtered_df = filtered_df[filtered_df["workingday_y"] == 1]
elif day_type == "Akhir Pekan/Hari Libur":
    filtered_df = filtered_df[filtered_df["workingday_y"] == 0]

# Tambahkan kolom Bulan dan Tahun
filtered_df['month'] = filtered_df['dteday'].dt.month
filtered_df['year'] = filtered_df['dteday'].dt.year

# 📊 Judul Dashboard
st.title('🚲 Bike Sharing Dashboard')
st.subheader('🔍 Eksplorasi Data dan Wawasan Menarik!')

# 📌 Fungsi untuk membuat Bar Chart
def plot_bar(data, x, y, hue=None, title="", xlabel="", ylabel="", palette="coolwarm"):
    fig, ax = plt.subplots(figsize=(10,6))
    sns.barplot(data=data, x=x, y=y, hue=hue, palette=palette, ax=ax)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    st.pyplot(fig)

# 📌 Fungsi untuk membuat Pie Chart
def plot_pie(data, labels, title):
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.pie(data, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.set_title(title)
    st.pyplot(fig)

# 1️⃣ Tren Penyewaan Sepeda per Bulan dan Tahun
st.header("📅 Tren Penyewaan Sepeda per Bulan dan Tahun")
plot_bar(filtered_df, 'month', 'cnt_y', hue='year', title="📊 Tren Penyewaan Sepeda per Bulan", xlabel="Bulan", ylabel="Jumlah Penyewaan Sepeda")

# 2️⃣ Pengaruh Musim terhadap Penyewaan
st.header("🍂 Pengaruh Musim terhadap Penyewaan Sepeda")
season_counts = filtered_df.groupby("season_y")["cnt_y"].sum()
season_labels = [season_mapping[s] for s in season_counts.index]
plot_pie(season_counts, season_labels, "🚴‍♂️ Jumlah Penyewaan Sepeda Berdasarkan Musim")

# 3️⃣ Perbandingan Penyewaan Hari Kerja vs Akhir Pekan
st.header("📅 Perbandingan Penyewaan pada Hari Kerja vs Akhir Pekan")
workday_counts = filtered_df.groupby("workingday_y")["cnt_y"].sum()
if not workday_counts.empty:
    labels = ["Hari Kerja" if idx == 1 else "Akhir Pekan/Hari Libur" for idx in workday_counts.index]
    plot_pie(workday_counts, labels, "📊 Persentase Penyewaan Sepeda Hari Kerja vs Akhir Pekan")

# 4️⃣ Perbandingan Pengguna Terdaftar vs Kasual
st.header("👥 Perbandingan Penyewaan: Terdaftar vs Kasual")

# Bulanan
month_registered_counts = filtered_df.groupby(['month'])['registered_y'].sum()
month_casual_counts = filtered_df.groupby(['month'])['casual_y'].sum()
df_month = pd.DataFrame({'month': month_registered_counts.index, 'Terdaftar': month_registered_counts.values, 'Kasual': month_casual_counts.values})
df_month_melted = df_month.melt(id_vars=['month'], value_vars=['Terdaftar', 'Kasual'], var_name='Tipe Pengguna', value_name='Jumlah')
plot_bar(df_month_melted, 'month', 'Jumlah', hue='Tipe Pengguna', title="📊 Perbandingan Pengguna Terdaftar vs Kasual (Bulanan)", xlabel="Bulan", ylabel="Jumlah Pengguna")

# Tahunan
year_registered_counts = filtered_df.groupby(['year'])['registered_y'].sum()
year_casual_counts = filtered_df.groupby(['year'])['casual_y'].sum()
df_year = pd.DataFrame({'year': year_registered_counts.index, 'Terdaftar': year_registered_counts.values, 'Kasual': year_casual_counts.values})
df_year_melted = df_year.melt(id_vars=['year'], value_vars=['Terdaftar', 'Kasual'], var_name='Tipe Pengguna', value_name='Jumlah')
plot_bar(df_year_melted, 'year', 'Jumlah', hue='Tipe Pengguna', title="📊 Perbandingan Pengguna Terdaftar vs Kasual (Tahunan)", xlabel="Tahun", ylabel="Jumlah Pengguna")

# 5️⃣ Pengaruh Cuaca terhadap Penyewaan
st.header("🌦️ Pengaruh Cuaca terhadap Penyewaan Sepeda")

fig, ax = plt.subplots(figsize=(10,6))

# Suhu vs Penyewaan
filtered_df.groupby('temp_y')['cnt_y'].sum().plot(ax=ax, label='Suhu')

# Kelembapan vs Penyewaan
filtered_df.groupby('hum_y')['cnt_y'].sum().plot(ax=ax, label='Kelembapan')

# Kecepatan Angin vs Penyewaan
filtered_df.groupby('windspeed_y')['cnt_y'].sum().plot(ax=ax, label='Kecepatan Angin')

ax.set_title('Pengaruh Suhu, Kelembapan, dan Kecepatan Angin terhadap Jumlah Total Sepeda yang Disewa')
ax.set_xlabel('Parameter Cuaca')
ax.set_ylabel('Jumlah Total Sepeda yang Disewa')
ax.legend()
st.pyplot(fig)


# 📢 Fakta Menarik (Dibuat lebih eye-catching)
st.sidebar.header("📊 Fakta Menarik tentang Penyewaan Sepeda")
if not filtered_df.empty:
    max_rentals = filtered_df['cnt_y'].max()
    min_rentals = filtered_df['cnt_y'].min()
    avg_rentals = filtered_df['cnt_y'].mean()

    st.sidebar.write("🔹 **Penyewaan Tertinggi dalam Sehari:**", max_rentals)
    st.sidebar.write("🔹 **Penyewaan Terendah dalam Sehari:**", min_rentals)
    st.sidebar.write("🔹 **Rata-rata Penyewaan Sepeda per Hari:**", f"{avg_rentals:.2f}")

else:
    st.sidebar.write("⚠️ Tidak ada data yang cocok dengan filter yang dipilih.")
