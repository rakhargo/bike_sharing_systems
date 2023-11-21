import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

# create_daily_rents_df() digunakan untuk menyiapkan daily_orders_df
def create_daily_rents_df(df):
    daily_rents_df = df.resample(rule='D', on='dteday').agg({
        "instant_daily": "nunique",
        "cnt_hourly": "sum",
        "casual_hourly": "sum",
        "registered_hourly": "sum"
    })
    daily_rents_df = daily_rents_df.reset_index()
    daily_rents_df.rename(columns = {
        "instant_daily": "daily_count",
        "cnt_hourly": "rent_count",
        "casual_hourly": "casual_count",
        "registered_hourly": "registered_count"
    }, inplace=True)
    
    return daily_rents_df

# create_hour_rent_df() bertanggung jawab untuk menyiapkan hour_rent_df
def create_hour_rent_df(df):
    hour_rent_df = df.groupby("hr").cnt_hourly.sum().sort_values(ascending=False).reset_index()
    return hour_rent_df


all_df = pd.read_csv("all_data.csv")

all_df['dteday'] = pd.to_datetime(all_df['dteday'])
all_df.sort_values(by="dteday", inplace=True)
all_df.reset_index(inplace=True)
 
### Membuat komponen filter
min_date = all_df["dteday"].min()
max_date = all_df["dteday"].max()
 
with st.sidebar:
    st.image("https://www.anylogic.fr/upload/blog/c67/c671ba340460d0018a250d6c17fe8ad1.jpg")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = all_df[(all_df["dteday"] >= str(start_date)) & (all_df["dteday"] <= str(end_date))]

daily_rents_df = create_daily_rents_df(main_df)
hour_rent_df = create_hour_rent_df(main_df)

### Melengkapi Dashboard dengan Berbagai Visualisasi Data
st.header('Bike Sharing Systems Dashboard :sparkles:')

st.subheader('Daily Rents')
 
col1, col2, col3, col4 = st.columns(4)
 
with col1:
    total_daily = daily_rents_df.daily_count.sum()
    st.metric("Total days", value=total_daily)
 
with col2:
    total_rent_count = daily_rents_df.rent_count.sum()
    st.metric("Total rents", value=total_rent_count)

with col3:
    total_casual_count = daily_rents_df.casual_count.sum()
    st.metric("Total casual users", value=total_casual_count)

with col4:
    total_registered_count = daily_rents_df.registered_count.sum()
    st.metric("Total registered users", value=total_registered_count)


fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(daily_rents_df['dteday'], daily_rents_df['rent_count'], marker='o', linestyle='-', color='b')
ax.set_title('Distribusi total rent')
ax.set_xlabel('Tanggal')
ax.set_ylabel('Total rent')
st.pyplot(fig)

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(daily_rents_df['dteday'], daily_rents_df['casual_count'], marker='o', linestyle='-', color='b')
ax.set_title('Distribusi total casual users')
ax.set_xlabel('Tanggal')
ax.set_ylabel('Total casual users')
st.pyplot(fig)

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(daily_rents_df['dteday'], daily_rents_df['registered_count'], marker='o', linestyle='-', color='b')
ax.set_title('Distribusi total registered users')
ax.set_xlabel('Tanggal')
ax.set_ylabel('Total registered users')
st.pyplot(fig)


# #####
st.subheader("Best & Worst hour")
 
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))
  
sns.barplot(x="hr", y="cnt_hourly", data=hour_rent_df.head(), hue="hr", ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("hour", fontsize=30)
ax[0].set_title("Best hour for rent", loc="center", fontsize=50)
ax[0].tick_params(axis='y', labelsize=35)
ax[0].tick_params(axis='x', labelsize=30)
 
sns.barplot(x="hr", y="cnt_hourly", data=hour_rent_df.sort_values(by="cnt_hourly", ascending=True).head(), hue="hr", ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("hour", fontsize=30)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Worst hour for rent", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=35)
ax[1].tick_params(axis='x', labelsize=30)
 
st.pyplot(fig)

st.caption('Copyright (c) Dicoding 2023')