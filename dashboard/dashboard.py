import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Data Gathering
hour_data = pd.read_csv(r'./data/hour.csv')
day_data = pd.read_csv(r'./data/day.csv')

# Data Cleaning
hour_data['dteday'] = pd.to_datetime(hour_data['dteday'])
day_data['dteday'] = pd.to_datetime(day_data['dteday'])

# Menambahkan judul utama untuk dashboard
st.set_page_config(page_title="Bike Rental Dashboard", layout="wide")  # Set page title
st.title('Bike Rental Dashboard :bike:')
st.markdown("""
Welcome to the **Bike Rental Dashboard**! This dashboard allows you to explore the bike rental usage trends based on:
- Hourly rentals to observe peak hours.
- Comparison between weekdays and weekends.
Please use the sidebar to filter the date range for analysis.
""")

# Filtering Date Range
min_date = day_data['dteday'].min()
max_date = day_data['dteday'].max()

# Sidebar untuk filter rentang tanggal
with st.sidebar:
    st.subheader('Filter berdasarkan rentang tanggal')

    selected_dates = st.date_input(
        label='Time Span',
        min_value=min_date, max_value=max_date,
        value=[min_date, max_date]
    )

    if isinstance(selected_dates, tuple) and len(selected_dates) == 2:
        start_date, end_date = selected_dates
    else:
        start_date = selected_dates[0]
        end_date = selected_dates[0]

start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

# Filter data berdasarkan tanggal yang dipilih
inputHour_df = hour_data[(hour_data['dteday'] >= start_date) & (hour_data['dteday'] <= end_date)]
inputDay_df = day_data[(day_data['dteday'] >= start_date) & (day_data['dteday'] <= end_date)]

# Debugging - Cek jumlah baris dalam inputDay_df
st.write(f'Jumlah baris dalam inputDay_df: {inputDay_df.shape[0]}')
st.write(f'Minimum tanggal dalam day_data: {day_data["dteday"].min()}')
st.write(f'Maksimum tanggal dalam day_data: {day_data["dteday"].max()}')

### Pertanyaan 1: Bagaimana pengaruh waktu terhadap jumlah sewa sepeda? (by hour)

# Visualisasi jumlah sewa sepeda berdasarkan jam
st.subheader('Pengaruh Waktu terhadap Jumlah Sewa Sepeda (by Hour)')
st.text(f'Dari {start_date.date()} hingga {end_date.date()}')

# Menghitung total sewa sepeda per jam
hourly_rentals = inputHour_df.groupby('hr')['cnt'].sum().reset_index()

# Plot untuk distribusi jumlah sewa sepeda berdasarkan jam
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(hourly_rentals['hr'], hourly_rentals['cnt'], linestyle='-', color='blue')
ax.set_title('Total Bike Rentals by Hour', fontsize=16)
ax.set_xlabel('Hour of the Day', fontsize=14)
ax.set_ylabel('Total Rentals', fontsize=14)
ax.set_facecolor('lightgray')
plt.xticks(rotation=0)
st.pyplot(fig)

### Pertanyaan 2: Bagaimana pola penggunaan sepeda selama hari kerja dibandingkan akhir pekan? (by day)

# Menyesuaikan label hari kerja dan akhir pekan
workingday_labels = {0: 'Akhir Pekan', 1: 'Hari Kerja'}
inputDay_df['workingday'] = inputDay_df['workingday'].replace(workingday_labels)

# Visualisasi pola penggunaan sepeda di hari kerja vs akhir pekan
st.subheader('Pola Penggunaan Sepeda Selama Hari Kerja vs Akhir Pekan')
st.text(f'Dari {start_date.date()} hingga {end_date.date()}')

# Boxplot perbandingan penggunaan sepeda di hari kerja dan akhir pekan
fig, ax = plt.subplots(figsize=(10, 6))
sns.boxplot(data=inputDay_df, x='workingday', y='cnt', ax=ax)
ax.set_title('Bike Rentals: Hari Kerja vs Akhir Pekan', fontsize=16)
ax.set_xlabel('Kategori Hari', fontsize=14)
ax.set_ylabel('Jumlah Sewa Sepeda (Count)', fontsize=14)
ax.set_facecolor('lightblue')
st.pyplot(fig)

# Visualisasi rata-rata penggunaan sepeda berdasarkan hari dalam seminggu
st.subheader('Rata-rata Penggunaan Sepeda Berdasarkan Hari dalam Seminggu')
st.text(f'Dari {start_date.date()} hingga {end_date.date()}')

# Mengubah weekday menjadi nama hari
weekday_labels = {0: 'Senin', 1: 'Selasa', 2: 'Rabu', 3: 'Kamis', 4: 'Jumat', 5: 'Sabtu', 6: 'Minggu'}
inputDay_df['weekday'] = inputDay_df['weekday'].replace(weekday_labels)

# Barplot rata-rata penggunaan sepeda per hari
avg_rentals_by_weekday = inputDay_df.groupby('weekday')['cnt'].mean().reset_index()

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='weekday', y='cnt', data=avg_rentals_by_weekday, ax=ax, palette='Blues_d')
ax.set_title('Rata-rata Sewa Sepeda per Hari', fontsize=16)
ax.set_xlabel('Hari dalam Seminggu', fontsize=14)
ax.set_ylabel('Rata-rata Jumlah Sewa Sepeda (Count)', fontsize=14)
ax.set_facecolor('lightgray')
plt.xticks(rotation=45)
st.pyplot(fig)
