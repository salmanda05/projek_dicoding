#Meng-import library
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set(style='dark')

#Membaca file csv
day_df = pd.read_csv('day.csv')
day_df.head()

# Menyiapkan casual_daily_rent_df
def create_casual_daily_rent_df(df):
    casual_daily_rent_df = df.groupby(by='dteday').agg({
        'casual': 'sum'
    }).reset_index()
    return casual_daily_rent_df

# Menyiapkan registered_daily_rent_df
def create_registered_daily_rent_df(df):
    registered_daily_rent_df = df.groupby(by='dteday').agg({
        'registered': 'sum'
    }).reset_index()
    return registered_daily_rent_df

# Menyiapkan count_rent_df
def create_daily_rent_df(df):
    daily_rent_df = df.groupby(by='dteday').agg({
        'cnt': 'sum'
    }).reset_index()
    return daily_rent_df

# Menyiapkan rent_by_season_df
def create_rent_by_season_df(df):
    rent_by_season_df = df.groupby(by='season').agg({
        'cnt': 'sum'
    }).reset_index()
    return rent_by_season_df

# Menyiapkan rent_by_weather_df
def create_rent_by_weather_df(df):
    rent_by_weather_df = df.groupby(by='weathersit').agg({
        'cnt': 'sum'
    }).reset_index()
    return rent_by_weather_df

# Menyiapkan rent_by_workingday_df
def create_rent_by_workingday_df(df):
    rent_by_workingday_df = df.groupby(by='workingday').agg({
        'casual': 'sum',
        'registered': 'sum'
    }).reset_index()
    return rent_by_workingday_df

# Mengurutkan DataFrame berdasarkan dteday & memastikan kolom tersebut bertipe datetime
datetime_columns = ["dteday"]
day_df.sort_values(by="dteday", inplace=True)
day_df.reset_index(inplace=True)
 
for column in datetime_columns:
    day_df[column] = pd.to_datetime(day_df[column])

# Membuat filter dengan widget date input
min_date = day_df['dteday'].min()
max_date = day_df['dteday'].max()
 
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image('bike4.png')
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = day_df[(day_df['dteday'] >= str(start_date)) & 
                (day_df['dteday'] <= str(end_date))]


# Memanggil helper function
casual_daily_rent_df = create_casual_daily_rent_df(main_df)
registered_daily_rent_df = create_registered_daily_rent_df(main_df)
daily_rent_df = create_daily_rent_df(main_df)
rent_by_season_df = create_rent_by_season_df(main_df)
rent_by_weather_df = create_rent_by_weather_df(main_df)
rent_by_workingday_df = create_rent_by_workingday_df(main_df)


# Menamnbahkan CSS untuk membuat header dan subheader rata tengah
st.markdown("""
    <style>
    .centered-header {
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<h1 class="centered-header">Bicycle Rental Dashboard 🚲</h1>', unsafe_allow_html=True)

st.subheader('Daily Rentals')

# Menampilkan informasi jumlah penyewa sepeda dalam bentuk metric() yang ditampilkan menggunakan layout columns()
col1, col2, col3 = st.columns(3)
 
with col1:
    total_casual = casual_daily_rent_df['casual'].sum()
    st.metric('Casual User', value=total_casual)

with col2:
    total_registered = registered_daily_rent_df['registered'].sum()
    st.metric('Registered User', value=total_registered)

with col3:
    total_users = daily_rent_df['cnt'].sum()
    st.metric('Total User', value=total_users)


# Membuat jumlah penyewaan berdasarkan musim
st.subheader('Number of Bike Renters by Season')
sns.set_style('white')
fig, ax = plt.subplots(figsize=(10, 5))  # Ukuran fig diubah agar sesuai


colors = ['#2f5756', '#fdba45', '#ac163b', '#4a6252']

sns.barplot(
    x='season',     
    y='cnt',
    data=rent_by_season_df.sort_values(by='season', ascending=True), # Pastikan urutan data sama
    palette=colors,
    ax=ax
)

ax.set_title('Number of Bike Renters by Season', loc='center', fontsize=15, pad=20)
ax.set_xlabel('Season', fontsize=11)
ax.set_ylabel('Number of Bike Renters', fontsize=11)
ax.tick_params(axis='x', labelsize=12)
ax.tick_params(axis='y', labelsize=12)
plt.ticklabel_format(style='plain', axis='y')

ax.legend(
    handles=[
        plt.Line2D([0], [0], color=colors[0], lw=4),
        plt.Line2D([0], [0], color=colors[1], lw=4),
        plt.Line2D([0], [0], color=colors[2], lw=4),
        plt.Line2D([0], [0], color=colors[3], lw=4)
    ],
    labels=['1: Springer', '2: Summer', '3: Fall', '4: Winter'],
    title='Season',
    loc='upper left',
    fontsize=8,
    title_fontsize=10
)

# Menampilkan plot di Streamlit
st.pyplot(fig)

# Membuat jumlah penyewaan berdasarkan cuaca
st.subheader('Number of Bike Renters by Weather')
sns.set_style('white')
fig, ax = plt.subplots(figsize=(10, 5))  # Ukuran fig diubah agar sesuai

colors = ['#ac163b', '#fdba45', '#4a6252']

sns.barplot(
    x='weathersit',     
    y='cnt',
    data=rent_by_weather_df.sort_values(by='weathersit', ascending=True), # Pastikan urutan data sama
    palette=colors,
    ax=ax
)

ax.set_title('Number of Bike Renters by Weather', loc='center', fontsize=15, pad=20)
ax.set_xlabel('Weather', fontsize=11)
ax.set_ylabel('Number of Bike Renters', fontsize=11)
ax.tick_params(axis='x', labelsize=12)
ax.tick_params(axis='y', labelsize=12)
plt.ticklabel_format(style='plain', axis='y')

ax.legend(
    handles=[
        plt.Line2D([0], [0], color=colors[0], lw=4),
        plt.Line2D([0], [0], color=colors[1], lw=4),
        plt.Line2D([0], [0], color=colors[2], lw=4),
    ],
    labels=[
        '1: Clear, Few clouds, Partly cloudy', 
        '2: Mist + Cloudy, Mist + Broken clouds, Mist + Few clouds, Mist', 
        '3: Light Snow, Light Rain + Thunderstorm + Scattered clouds, Light Rain + Scattered clouds'], 
    title='Weather',
    loc='upper right',
    fontsize=8,
    title_fontsize=10
)

# Menampilkan plot di Streamlit
st.pyplot(fig)

# Membuat jumlah penyewaan berdasarkan hari kerja
st.subheader('Comparison of Casual and Registered Users on Working Days')
sns.set_style('white')

working_day_melted = rent_by_workingday_df.melt(id_vars='workingday', value_vars=['casual', 'registered'], 
                                                 var_name='user_type', value_name='count')

colors = {'casual': '#fdba45', 'registered': '#ac163b'}


fig, ax = plt.subplots(figsize=(10, 5))


sns.barplot(
    x='workingday', 
    y='count', 
    hue='user_type',
    data=working_day_melted,  
    palette=colors,
    ax=ax
)


ax.set_title('Comparison of Casual and Registered Users on Working Days', pad=20, fontsize=15)
ax.set_xlabel('Working day (0 = Non Working Day, 1 = Working Day)', fontsize=11)
ax.set_ylabel('Number of Bike Renters', fontsize=11)
ax.ticklabel_format(style='plain', axis='y')

# Menampilkan plot di Streamlit
st.pyplot(fig)