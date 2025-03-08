import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import numpy as np

# Load dataset
file_path = "analysis.csv"
hour_df = pd.read_csv(file_path)

# Konversi kolom tanggal ke format datetime
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

# Mapping untuk musim & kondisi cuaca
season_mapping = {1: "Musim Semi", 2: "Musim Panas", 3: "Musim Gugur", 4: "Musim Dingin"}
weather_mapping = {1: "Cerah", 2: "Berawan", 3: "Hujan Ringan", 4: "Hujan Lebat"}

# 🎨 Atur Tampilan Dashboard
st.set_page_config(page_title='🚴 Bike Sharing Dashboard', page_icon='🚲')

# 🖼️ Tambahkan Gambar di Sidebar
st.sidebar.image("https://3.bp.blogspot.com/_UaJWUMI3LDg/TOS0kZnRCCI/AAAAAAAAAB4/nodyhhiM1PY/s1600/CIMG0443.JPG", 
                 caption='Nikmati perjalanan sepeda Anda!')

# 🎛️ Sidebar untuk Filter Data
st.sidebar.header("🎚️ Sesuaikan Tampilan Data")

# 📆 Filter Tanggal
date_range = st.sidebar.date_input("📅 Pilih Rentang Tanggal", 
                                   [hour_df['dteday'].min(), hour_df['dteday'].max()],
                                   min_value=hour_df['dteday'].min(),
                                   max_value=hour_df['dteday'].max())

# 🌤️ Filter Musim
season_options = [season_mapping[s] for s in hour_df['season_y'].unique()]
selected_season = st.sidebar.multiselect("🍂 Pilih Musim", season_options, default=season_options)
selected_season_num = [k for k, v in season_mapping.items() if v in selected_season]

# ☁️ Filter Cuaca
weather_options = [weather_mapping[w] for w in hour_df['weathersit_y'].unique()]
selected_weather = st.sidebar.multiselect("⛅ Pilih Kondisi Cuaca", weather_options, default=weather_options)
selected_weather_num = [k for k, v in weather_mapping.items() if v in selected_weather]

# 🏢 Filter Hari Kerja vs Akhir Pekan
day_type = st.sidebar.radio("📅 Pilih Jenis Hari", ["Semua", "Hari Kerja", "Akhir Pekan/Hari Libur"])

# 🔍 Terapkan Filter
filtered_df = hour_df[
    (hour_df['dteday'] >= pd.to_datetime(date_range[0])) &
    (hour_df['dteday'] <= pd.to_datetime(date_range[1])) &
    (hour_df['season_y'].isin(selected_season_num)) &
    (hour_df['weathersit_y'].isin(selected_weather_num))
]

if day_type == "Hari Kerja":
    filtered_df = filtered_df[filtered_df["workingday_y"] == 1]
elif day_type == "Akhir Pekan/Hari Libur":
    filtered_df = filtered_df[filtered_df["workingday_y"] == 0]

# 📊 Judul Dashboard
st.title('🚲 Bike Sharing Dashboard')
st.subheader('🔍 Eksplorasi Data dan Wawasan Menarik!')

# 📅 Tren Penyewaan Sepeda Seiring Waktu (Diperbaiki)
st.header("📅 Bagaimana Tren Penyewaan Sepeda dari Waktu ke Waktu?")

# Konversi tanggal ke format datetime jika belum dilakukan
filtered_df['dteday'] = pd.to_datetime(filtered_df['dteday'])  

# Hanya gunakan kolom numerik dalam agregasi mingguan
weekly_trend = filtered_df.resample('W', on='dteday')[filtered_df.select_dtypes(include=[np.number]).columns].mean()

# Plot
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(weekly_trend.index, weekly_trend['cnt_y'], color='blue', linestyle='-', linewidth=2, label="Tren Mingguan")
ax.set_title("📊 Pola Penyewaan Sepeda Seiring Waktu")
ax.set_xlabel("📅 Waktu (Tahun/Bulan)")
ax.set_ylabel("🚲 Jumlah Penyewaan Sepeda")
ax.legend()

st.pyplot(fig)

# ⏳ Pola Penyewaan Sepeda Berdasarkan Jam
st.header('⏰ Pola Penyewaan Sepeda Sepanjang Hari')
fig2, ax2 = plt.subplots(figsize=(10,6))
filtered_df.groupby('hr')['cnt_y'].mean().plot(ax=ax2, color='green', marker='o')
ax2.set_title('🕒 Rata-rata Penyewaan Sepeda Berdasarkan Jam')
ax2.set_xlabel('Jam')
ax2.set_ylabel('Jumlah Penyewaan')
st.pyplot(fig2)

# 👥 Perbandingan Pengguna Terdaftar vs Kasual
st.header('🚴‍♂️ Siapa yang Lebih Sering Menyewa?')
fig3, ax3 = plt.subplots(figsize=(10,6))
sns.lineplot(data=filtered_df, x='hr', y='casual_y', label='Pengguna Kasual', ax=ax3)
sns.lineplot(data=filtered_df, x='hr', y='registered_y', label='Pengguna Terdaftar', ax=ax3)
ax3.set_title('📊 Perbandingan Pengguna Terdaftar vs Kasual')
ax3.set_xlabel('Jam')
ax3.set_ylabel('Jumlah Penyewaan')
ax3.legend()
st.pyplot(fig3)

# 🌦️ Cuaca dan Penyewaan Sepeda (Disederhanakan)
st.header('🌦️ Cuaca dan Penyewaan Sepeda')

fig, ax = plt.subplots(figsize=(10,6))
sns.scatterplot(data=filtered_df.sample(1000),  # Mengurangi jumlah titik data untuk kejelasan
                x='temp_y', y='cnt_y', hue='weathersit_y', 
                palette='coolwarm', alpha=0.5, edgecolor=None, ax=ax)
sns.regplot(data=filtered_df, x='temp_y', y='cnt_y', scatter=False, ax=ax, color='black', ci=None)

ax.set_title('🌡️ Hubungan Suhu dan Jumlah Penyewaan')
ax.set_xlabel('Suhu (Normalisasi)')
ax.set_ylabel('Jumlah Penyewaan')

st.pyplot(fig)


# 📊 Korelasi Antar Variabel (Disederhanakan)
st.header('📊 Hubungan Antar Variabel')

# Pilih variabel yang paling relevan
relevant_columns = ['cnt_y', 'registered_y', 'casual_y', 'temp_y', 'hum_y', 'windspeed_y']
corr_matrix = filtered_df[relevant_columns].corr()

# Sembunyikan korelasi yang terlalu kecil agar lebih fokus
mask = np.abs(corr_matrix) < 0.5  
corr_matrix = corr_matrix.mask(mask)

fig, ax = plt.subplots(figsize=(8,5))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f", ax=ax, linewidths=0.5)

ax.set_title('🔗 Korelasi Antara Variabel Utama')

st.pyplot(fig)


# 📢 Insight Singkat di Sidebar
st.sidebar.subheader("📌 Fakta Menarik")
max_rentals = filtered_df['cnt_y'].max()
min_rentals = filtered_df['cnt_y'].min()
avg_rentals = filtered_df['cnt_y'].mean()
st.sidebar.write(f"📈 Penyewaan terbanyak dalam satu hari: {max_rentals}")
st.sidebar.write(f"📉 Penyewaan paling sedikit: {min_rentals}")
st.sidebar.write(f"📊 Rata-rata penyewaan sepeda: {avg_rentals:.2f}")

# 📚 Informasi Dataset
st.sidebar.header('📖 Tentang Data Ini')
st.sidebar.write('📂 Data ini berisi informasi penyewaan sepeda berdasarkan musim, cuaca, suhu, kelembaban, kecepatan angin, dan tipe pengguna.')
