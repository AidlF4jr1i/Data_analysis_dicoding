import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import numpy as np

# Load dataset
file_path = "analysis.csv"
df = pd.read_csv(file_path)

# Konversi tanggal ke format datetime
df['dteday'] = pd.to_datetime(df['dteday'])

# Mapping untuk musim & kondisi cuaca
season_mapping = {1: "Musim Semi", 2: "Musim Panas", 3: "Musim Gugur", 4: "Musim Dingin"}
weather_mapping = {1: "Cerah", 2: "Berawan", 3: "Hujan Ringan", 4: "Hujan Lebat"}

# 🎨 Atur Tampilan Dashboard
st.set_page_config(page_title='🚴 Bike Sharing Dashboard', page_icon='🚲')

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

# Terapkan Filter ke dataset
filtered_df = df[
    (df['dteday'] >= pd.to_datetime(date_range[0])) &
    (df['dteday'] <= pd.to_datetime(date_range[1])) &
    (df['season_y'].isin(selected_season_num)) &
    (df['weathersit_y'].isin(selected_weather_num))
]

if day_type == "Hari Kerja":
    filtered_df = filtered_df[filtered_df["workingday_y"] == 1]
elif day_type == "Akhir Pekan/Hari Libur":
    filtered_df = filtered_df[filtered_df["workingday_y"] == 0]

# 📊 Judul Dashboard
st.title('🚲 Bike Sharing Dashboard')
st.subheader('🔍 Eksplorasi Data dan Wawasan Menarik!')

# 1️⃣ Tren Penyewaan Sepeda per Bulan dan Tahun
st.header("📅 Tren Penyewaan Sepeda per Bulan dan Tahun")
filtered_df['month'] = filtered_df['dteday'].dt.month
filtered_df['year'] = filtered_df['dteday'].dt.year

fig, ax = plt.subplots(figsize=(10,6))
sns.barplot(data=filtered_df, x='month', y='cnt_x', hue='year', palette='coolwarm', ax=ax)
ax.set_title("📊 Tren Penyewaan Sepeda per Bulan")
ax.set_xlabel("Bulan")
ax.set_ylabel("Jumlah Penyewaan Sepeda")
ax.legend(title="Tahun")
st.pyplot(fig)

# 2️⃣ Pengaruh Musim terhadap Penyewaan
st.header("🍂 Pengaruh Musim terhadap Penyewaan Sepeda")
season_counts = filtered_df.groupby("season_y")["cnt_x"].sum()
season_labels = [season_mapping[s] for s in season_counts.index]

fig, ax = plt.subplots(figsize=(8,6))
sns.barplot(x=season_labels, y=season_counts.values, palette="viridis", ax=ax)
ax.set_title("🚴‍♂️ Jumlah Penyewaan Sepeda Berdasarkan Musim")
ax.set_xlabel("Musim")
ax.set_ylabel("Total Penyewaan")
st.pyplot(fig)

# 3️⃣ Perbandingan Penyewaan Hari Kerja vs Akhir Pekan
st.header("📅 Perbandingan Penyewaan pada Hari Kerja vs Akhir Pekan")
workday_counts = filtered_df.groupby("workingday_y")["cnt_x"].sum()

# Pastikan jumlah label sesuai dengan data
if len(workday_counts) > 0:
    labels = ["Akhir Pekan/Hari Libur", "Hari Kerja"]
    colors = ["red", "blue"]

    # Jika hanya ada satu kategori, sesuaikan label dan warna
    if len(workday_counts) == 1:
        labels = ["Hari Kerja"] if workday_counts.index[0] == 1 else ["Akhir Pekan/Hari Libur"]
        colors = ["blue"] if workday_counts.index[0] == 1 else ["red"]

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(workday_counts, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90)
    ax.set_title("📊 Persentase Penyewaan Sepeda")
    st.pyplot(fig)
else:
    st.warning("⚠️ Tidak ada data yang sesuai dengan filter yang dipilih.")


# 4️⃣ Tren Penyewaan Sepeda Berdasarkan Segmen Waktu
st.header("⏰ Tren Penyewaan Sepeda Berdasarkan Segmen Waktu")
segment_counts = filtered_df.groupby("time_segment")["cnt_y"].sum()

fig, ax = plt.subplots(figsize=(6,6))
ax.pie(segment_counts, labels=segment_counts.index, autopct='%1.1f%%', colors=['grey', 'pink', 'red'])
ax.set_title("🚲 Penyewaan Sepeda Berdasarkan Segmen Waktu")
st.pyplot(fig)

# 5️⃣ Pengaruh Cuaca terhadap Penyewaan
st.header("🌦️ Pengaruh Cuaca terhadap Penyewaan Sepeda")
fig, ax = plt.subplots(figsize=(10,6))

found_data = False  # Variabel untuk cek apakah ada data untuk tiap kategori cuaca

for i in range(1, 5):
    subset = filtered_df[filtered_df['weathersit_y'] == i]
    if not subset.empty:
        found_data = True
        subset.groupby('hr')['cnt_y'].mean().plot(label=weather_mapping[i], ax=ax)

if found_data:
    ax.set_title("⏳ Penyewaan Sepeda Berdasarkan Kondisi Cuaca")
    ax.set_xlabel("Jam")
    ax.set_ylabel("Rata-rata Penyewaan")
    ax.legend()
    st.pyplot(fig)
else:
    st.warning("⚠️ Tidak ada data yang sesuai dengan filter yang dipilih.")


# 📢 Insight Singkat di Sidebar
st.sidebar.subheader("📌 Fakta Menarik")
if not filtered_df.empty:
    max_rentals = filtered_df['cnt_y'].max()
    min_rentals = filtered_df['cnt_y'].min()
    avg_rentals = filtered_df['cnt_y'].mean()
    st.sidebar.write(f"📈 Penyewaan terbanyak dalam satu hari: {max_rentals}")
    st.sidebar.write(f"📉 Penyewaan paling sedikit: {min_rentals}")
    st.sidebar.write(f"📊 Rata-rata penyewaan sepeda: {avg_rentals:.2f}")
else:
    st.sidebar.write("⚠️ Tidak ada data yang cocok dengan filter!")


# 📚 Informasi Dataset
st.sidebar.header('📖 Tentang Data Ini')
st.sidebar.write('📂 Data ini berisi informasi penyewaan sepeda berdasarkan musim, cuaca, suhu, kelembaban, kecepatan angin, dan tipe pengguna.')
