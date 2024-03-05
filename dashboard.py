import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
st.set_option('deprecation.showPyplotGlobalUse', False)

sns.set(style='dark')
data_df = pd.read_csv("https://raw.githubusercontent.com/stephanievivienne/bikedataset/main/day.csv")
data2_df = pd.read_csv("https://raw.githubusercontent.com/stephanievivienne/bikedataset/main/hour.csv")

#Data preprocessing
data_df.drop_duplicates(inplace=True)
data2_df.drop_duplicates(inplace=True)
data_df.fillna(method="ffill", inplace=True)
data2_df.fillna(method="ffill", inplace=True)

bike_df = data2_df.merge(data_df, on='dteday', how='inner', suffixes=('_hour', '_day'))

weather_labels = {
    1: 'Jernih',
    2: 'Kabut',
    3: 'Curah Hujan Ringan',
    4: 'Curah Hujan Lebat'
}
bike_df['weather_label'] = bike_df['weathersit_day'].map(weather_labels)

# Streamlit app
st.title('Dashboard Visualisasi Data Sepeda')

# Show missing values
st.subheader('Jumlah Data yang Hilang:')
st.write("Data DataFrame:")
st.write(data_df.isna().sum())

st.write("Data2 DataFrame:")
st.write(data2_df.isna().sum())

# Show duplicates
st.subheader('Jumlah Duplikasi:')
st.write("Data DataFrame:")
st.write(data_df.duplicated().sum())

st.write("Data2 DataFrame:")
st.write(data2_df.duplicated().sum())

# Descriptive statistics
st.subheader('Statistik Deskriptif:')
st.write("Data DataFrame:")
st.write(data_df.describe())

st.write("Data2 DataFrame:")
st.write(data2_df.describe())

# Visualizations
st.subheader('Visualisasi Data:')

# Line plot of rental count over time
st.write("Grafik Perubahan Jumlah Penyewaan Sepeda dari Waktu ke Waktu:")
st.line_chart(bike_df.set_index('dteday')['cnt_day'])


# Bar plot of average rental count by weather label
st.write("Rata - Rata Penyewaan Sepeda berdasarkan Kondisi Cuaca:")
st.bar_chart(bike_df.groupby('weather_label')['cnt_day'].mean())

# Bar plot of average rental count by hour
st.write("Rata - Rata Penyewaan Sepeda berdasarkan Jam:")
st.bar_chart(bike_df.groupby('hr')['cnt_hour'].mean())

# Box plot of rental count by holiday
st.write("Perbandingan Jumlah Penyewaan Sepeda pada Hari Libur dan Bukan Hari Libur:")
plt.figure(figsize=(8, 5))
sns.boxplot(x='holiday_day', y='cnt_day', data=bike_df)
plt.xlabel('Hari Libur')
plt.ylabel('Jumlah Penyewaan Sepeda')
plt.xticks([0, 1], ['Tidak Libur', 'Libur'])
st.pyplot()

# Histogram of temperature distribution
st.write("Distribusi Suhu pada Data:")
plt.hist(data_df['temp'], bins=20, edgecolor='black')
plt.xlabel('Suhu')
plt.ylabel('Frekuensi')
st.pyplot()
