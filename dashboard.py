import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from datetime import datetime

# Load dataset
data = pd.read_csv('hour.csv')
data['dteday'] = pd.to_datetime(data['dteday'])

# Sidebar for user inputs
st.header("Pilih Rentang Tanggal")
start_date = st.date_input("Tanggal Mulai", value=data['dteday'].min())
end_date = st.date_input("Tanggal Akhir", value=data['dteday'].max())

# Ensure start_date is not greater than end_date
if start_date > end_date:
    st.error("Tanggal mulai tidak boleh lebih besar dari tanggal akhir.")
else:
    # Filter data berdasarkan rentang tanggal
    filtered_data = data[(data['dteday'] >= pd.to_datetime(start_date)) & (data['dteday'] <= pd.to_datetime(end_date))]

    # Display header
    st.title('Analisis Data Bike Sharing')
    st.write('## Overview of Bike Sharing Dataset')

    # Show dataset
    if st.checkbox('Tampilkan data mentah'):
        st.subheader('Data Mentah')
        st.write(filtered_data)

    # Data wrangling
    filtered_data.loc[:, 'day_of_week'] = filtered_data['dteday'].dt.day_name()

    # Analysis Questions
    st.write('## Pertanyaan Bisnis')
    st.write('1. Bagaimana pengaruh cuaca dan musim terhadap penggunaan sepeda?')
    st.write('2. Apa perbedaan penggunaan sepeda antara hari kerja dan akhir pekan?')

    # Grouping data for analysis
    seasonal_usage = filtered_data.groupby('season')['cnt'].mean()
    workingday_usage = filtered_data.groupby('workingday')['cnt'].mean()

    # Visualization for weather effects
    st.write('### Rata-rata Penggunaan Sepeda Berdasarkan Kondisi Cuaca')
    weather_effect = filtered_data.groupby('weathersit')['cnt'].mean()
    fig, ax = plt.subplots()
    sns.barplot(x=weather_effect.index, y=weather_effect.values, ax=ax)
    ax.set_xlabel('Kondisi Cuaca')
    ax.set_ylabel('Rata-rata Penggunaan')
    ax.set_title('Pengaruh Cuaca Terhadap Penggunaan Sepeda')
    st.pyplot(fig)

    # Visualization for seasonal usage
    st.write('### Rata-rata Penggunaan Sepeda Berdasarkan Musim')
    fig2, ax2 = plt.subplots()
    sns.barplot(x=seasonal_usage.index, y=seasonal_usage.values, ax=ax2)
    ax2.set_xlabel('Musim')
    ax2.set_ylabel('Rata-rata Penggunaan')
    ax2.set_title('Penggunaan Sepeda Berdasarkan Musim')
    st.pyplot(fig2)

    # Visualization for working day vs weekend
    st.write('### Rata-rata Penggunaan Sepeda: Hari Kerja vs. Akhir Pekan')
    fig3, ax3 = plt.subplots()
    sns.barplot(x=['Akhir Pekan', 'Hari Kerja'], y=workingday_usage.values, ax=ax3)
    ax3.set_ylabel('Rata-rata Penggunaan')
    ax3.set_title('Penggunaan Sepeda pada Hari Kerja vs. Akhir Pekan')
    st.pyplot(fig3)

    # RFM Analysis
    st.write('## Analisis RFM')
    rfm_filtered_data = filtered_data.groupby('dteday').agg({'cnt': 'sum'}).reset_index()
    max_date = rfm_filtered_data['dteday'].max()
    rfm_filtered_data['Recency'] = (max_date - rfm_filtered_data['dteday']).dt.days
    rfm_filtered_data['Frequency'] = rfm_filtered_data['cnt']
    rfm_filtered_data['Monetary'] = rfm_filtered_data['cnt']

    # RFM Distribution
    fig4, axs = plt.subplots(3, 1, figsize=(10, 15))
    sns.histplot(rfm_filtered_data['Recency'], kde=True, ax=axs[0])
    axs[0].set_title('Distribusi Recency')
    sns.histplot(rfm_filtered_data['Frequency'], kde=True, ax=axs[1])
    axs[1].set_title('Distribusi Frequency')
    sns.histplot(rfm_filtered_data['Monetary'], kde=True, ax=axs[2])
    axs[2].set_title('Distribusi Monetary')
    st.pyplot(fig4)

    # Time of Day Analysis
    st.write('### Penggunaan Sepeda Berdasarkan Waktu Dalam Sehari')
    filtered_data['time_of_day'] = filtered_data['hr'].apply(lambda hour: 'Pagi' if 5 <= hour < 11 else 'Siang' if 11 <= hour < 17 else 'Sore' if 17 <= hour < 21 else 'Malam')
    time_of_day_filtered_data = filtered_data.groupby('time_of_day')['cnt'].sum().reset_index()
    fig5, ax5 = plt.subplots()
    sns.barplot(data=time_of_day_filtered_data, x='time_of_day', y='cnt', ax=ax5, palette='viridis')
    ax5.set_title('Penggunaan Sepeda Berdasarkan Waktu Dalam Sehari')
    st.pyplot(fig5)

    # Conclusion Section
    st.write('## Kesimpulan')
    st.write('### Insight dari analisis:')
    st.write('- Kondisi cuaca sangat mempengaruhi penggunaan sepeda.')
    st.write('- Terdapat perbedaan yang mencolok dalam penggunaan sepeda antara hari kerja dan akhir pekan.')
