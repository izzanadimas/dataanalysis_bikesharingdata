# Import libraries
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

# Dataset
# ⤷ Main dataset
main_df = pd.read_csv("dashboard/main_data.csv")
# ⤷ Main dataset (copy)
df = main_df.copy()
df["dteday"] = pd.to_datetime(df["dteday"])
# ⤷ Helper table (temporary pivot table, etc.)
#   ⤷ All time monthly recap
monthly_alltime = df.resample(rule='M', on='dteday').agg({
    "casual": "sum",
    "yr": "mean",
    "registered": "sum",
    "cnt": "sum"
})
monthly_alltime.index = monthly_alltime.index.strftime('%Y-%m')
monthly_alltime = monthly_alltime.reset_index()
monthly_alltime.rename(columns={
    "casual": "casual",
    "yr": "yr",
    "registered": "registered",
    "total": "cnt"
}, inplace=True)
#   ⤷ 2011 monthly recap
monthly_2011 = monthly_alltime[monthly_alltime["yr"]==2011]
#   ⤷ 2012 monthly recap
monthly_2012 = monthly_alltime[monthly_alltime["yr"]==2012]
#   ⤷ All time season recap
season_alltime = df.groupby(by=["dteday","yr","season"]).agg({
    "temp": "mean",
    "cnt": "sum"
})
season_alltime = season_alltime.reset_index()
season_alltime.rename(columns={
    "casual": "casual",
    "yr": "yr",
    "registered": "registered",
    "temp": "temp",
    "total": "cnt"
}, inplace=True)
season_alltime = season_alltime.groupby(by=["yr","season"]).agg({
    "temp": "mean",
    "cnt": "mean"
})
season_alltime = season_alltime.reset_index()
#   ⤷ 2011 season recap
season_2011 = season_alltime[season_alltime["yr"]==2011]
#   ⤷ 2012 season recap
season_2012 = season_alltime[season_alltime["yr"]==2012]

# Functions/Tasks/Logic
# ⤷ Show line chart by time range
def recap_by_range(dataset): 
    with r1c1:
        total_orders = dataset["casual"].sum() + dataset["registered"].sum()
        st.metric("Total Rental Bike(s)", value=total_orders)
        r2c1, r2c2 = st.columns(2)
        with r2c1:
            total_orders = dataset["registered"].sum()
            st.metric("by Registered Customer", value=total_orders)
        with r2c2:
            total_orders = dataset["casual"].sum()
            st.metric("by Casual Customer", value=total_orders)
    fig, ax = plt.subplots(figsize=(28, 12))
    ax.plot(
        dataset["dteday"],
        dataset["casual"],
        marker='o', 
        linewidth=2,
        color="blue",
        label='Casual customer'
    )
    ax.plot(
        dataset["dteday"],
        dataset["registered"],
        marker='o', 
        linewidth=2,
        color="green",
        label='Registered customer'
    )
    ax.tick_params(axis='x', labelsize=15, labelrotation=45)
    ax.tick_params(axis='y', labelsize=20)
    ax.legend(loc="upper left",fontsize=26)
    ax.grid(True)
    st.pyplot(fig)
# ⤷ Show clusstered bar chart by time range
def seasonrecap_by_range(group):
    if group == "All time":
        labels = season_alltime[season_alltime["season"]=="Fall"]["yr"].tolist()
        fall_means = season_alltime[season_alltime["season"]=="Fall"]["cnt"].tolist()
        spring_means = season_alltime[season_alltime["season"]=="Spring"]["cnt"].tolist()
        summer_means = season_alltime[season_alltime["season"]=="Summer"]["cnt"].tolist()
        winter_means = season_alltime[season_alltime["season"]=="Winter"]["cnt"].tolist()
        fall_temp = season_alltime[season_alltime["season"]=="Fall"]["temp"].tolist()
        spring_temp = season_alltime[season_alltime["season"]=="Spring"]["temp"].tolist()
        summer_temp = season_alltime[season_alltime["season"]=="Summer"]["temp"].tolist()
        winter_temp = season_alltime[season_alltime["season"]=="Winter"]["temp"].tolist()
    else:
        labels = [group]
        fall_means = season_alltime[season_alltime["season"]=="Fall"][season_alltime["yr"]==group]["cnt"].tolist()
        spring_means = season_alltime[season_alltime["season"]=="Spring"][season_alltime["yr"]==group]["cnt"].tolist()
        summer_means = season_alltime[season_alltime["season"]=="Summer"][season_alltime["yr"]==group]["cnt"].tolist()
        winter_means = season_alltime[season_alltime["season"]=="Winter"][season_alltime["yr"]==group]["cnt"].tolist()
        fall_temp = season_alltime[season_alltime["season"]=="Fall"][season_alltime["yr"]==group]["temp"].tolist()
        spring_temp = season_alltime[season_alltime["season"]=="Spring"][season_alltime["yr"]==group]["temp"].tolist()
        summer_temp = season_alltime[season_alltime["season"]=="Summer"][season_alltime["yr"]==group]["temp"].tolist()
        winter_temp = season_alltime[season_alltime["season"]=="Winter"][season_alltime["yr"]==group]["temp"].tolist()
        
    x = np.arange(len(labels))
    width = 0.2
    fig, (ax1, ax2) = plt.subplots(1,2,figsize=(10, 6))
    ax1.bar(x - 1.5*width, fall_means, width, label='Fall')
    ax1.bar(x - 0.5*width, spring_means, width, label='Spring')
    ax1.bar(x + 0.5*width, summer_means, width, label='Summer')
    ax1.bar(x + 1.5*width, winter_means, width, label='Winter')
    ax1.set_ylabel('Rata-Rata Peminjaman Sepeda')
    ax1.set_xlabel('Tahun')
    ax1.set_title('Rata-Rata Peminjaman Sepeda Tiap Musim')
    ax1.set_xticks(x)
    ax1.set_xticklabels(labels)
    ax1.legend(fontsize=8)
    ax2.bar(x - 1.5*width, fall_temp, width, label='Fall')
    ax2.bar(x - 0.5*width, spring_temp, width, label='Spring')
    ax2.bar(x + 0.5*width, summer_temp, width, label='Summer')
    ax2.bar(x + 1.5*width, winter_temp, width, label='Winter')
    ax2.set_ylabel('Rata-Rata Suhu')
    ax2.set_xlabel('Tahun')
    ax2.set_title('Rata-Rata Suhu Tiap Musim (Normalized)')
    ax2.set_xticks(x)
    ax2.set_xticklabels(labels)
    ax2.legend(fontsize=8)
    st.pyplot(fig)

# Layouting Streamlit Interface
# ⤷ Header
st.title('Bike Sharing System :bike:')
st.header('System Dashboard')
st.markdown('Selamat datang di Bike Sharing System Dashboard. Silahkan pantau perkembangan sistem ini melalui _dashboard_ berikut.')
# ⤷ Monthly rented bikes section
st.subheader('Monthly Total Rented Bikes 📆')
r1c1, r1c2 = st.columns(2)
with r1c2:
    timerange = st.selectbox(
    label="Time range (year)",
    options=('All time', 2012, 2011)
    )
if timerange == "All time":
    recap_by_range(monthly_alltime)
elif timerange == 2012:
    recap_by_range(monthly_2012)
elif timerange == 2011:
    recap_by_range(monthly_2011)
# ⤷ Rented bikes by season section
st.subheader('Average Rented Bikes per Day by Season 🍁')
r3c1, r3c2 = st.columns(2)
with r3c1:
    sub1_r3c1, sub2_r3c1 = st.columns(2)
    with sub1_r3c1:
        st.metric("Highest at", value="Fall")
    with sub2_r3c1:
        st.metric("Lowest at", value="Spring")
with r3c2:
    timerange2 = st.selectbox(
    key="season",
    label="Time range (year)",
    options=('All time', 2012, 2011)
    )
seasonrecap_by_range(timerange2)
if timerange2 == "All time":

    fall_means1 = (season_alltime[season_alltime["season"]=="Fall"][season_alltime["yr"]==2011]["cnt"].sum()+season_alltime[season_alltime["season"]=="Fall"][season_alltime["yr"]==2012]["cnt"].sum())/2
    spring_means1 = (season_alltime[season_alltime["season"]=="Spring"][season_alltime["yr"]==2011]["cnt"].sum()+season_alltime[season_alltime["season"]=="Spring"][season_alltime["yr"]==2012]["cnt"].sum())/2
    summer_means1 = (season_alltime[season_alltime["season"]=="Summer"][season_alltime["yr"]==2011]["cnt"].sum()+season_alltime[season_alltime["season"]=="Summer"][season_alltime["yr"]==2012]["cnt"].sum())/2
    winter_means1 = (season_alltime[season_alltime["season"]=="Winter"][season_alltime["yr"]==2011]["cnt"].sum()+season_alltime[season_alltime["season"]=="Winter"][season_alltime["yr"]==2012]["cnt"].sum())/2
    fall_temp1 = (season_alltime[season_alltime["season"]=="Fall"][season_alltime["yr"]==2011]["temp"].sum()+season_alltime[season_alltime["season"]=="Fall"][season_alltime["yr"]==2012]["temp"].sum())/2
    spring_temp1 = (season_alltime[season_alltime["season"]=="Spring"][season_alltime["yr"]==2011]["temp"].sum()+season_alltime[season_alltime["season"]=="Spring"][season_alltime["yr"]==2012]["temp"].sum())/2
    summer_temp1 = (season_alltime[season_alltime["season"]=="Summer"][season_alltime["yr"]==2011]["temp"].sum()+season_alltime[season_alltime["season"]=="Summer"][season_alltime["yr"]==2012]["temp"].sum())/2
    winter_temp1 = (season_alltime[season_alltime["season"]=="Winter"][season_alltime["yr"]==2011]["temp"].sum()+season_alltime[season_alltime["season"]=="Winter"][season_alltime["yr"]==2012]["temp"].sum())/2

    r4c1, r4c2 = st.columns(2)
    with r4c1:
        st.markdown("Avg. rented bikes per day (all time):")
        r4c1_1, r4c1_2 = st.columns(2)
        with r4c1_1:
            st.metric("Fall 🍁", value=round(fall_means1,2))
            st.metric("Winter ❄️", value=round(winter_means1,2)) 
        with r4c1_2:
            st.metric("Summer ☀️", value=round(summer_means1,2))
            st.metric("Spring 🌼", value=round(spring_means1,2))
    with r4c2:
        st.markdown(f"Avg. normalized temperature per day ({timerange2}):")
        r4c2_1, r4c2_2 = st.columns(2)
        with r4c2_1:
            st.metric("Fall 🍁", value=f"{round(fall_temp1,2)} °C")
            st.metric("Winter ❄️", value=f"{round(winter_temp1,2)} °C") 
        with r4c2_2:
            st.metric("Summer ☀️", value=f"{round(summer_temp1,2)} °C")
            st.metric("Spring 🌼", value=f"{round(spring_temp1,2)} °C")

else:
    fall_means = season_alltime[season_alltime["season"]=="Fall"][season_alltime["yr"]==timerange2]["cnt"].sum()
    spring_means = season_alltime[season_alltime["season"]=="Spring"][season_alltime["yr"]==timerange2]["cnt"].sum()
    summer_means = season_alltime[season_alltime["season"]=="Summer"][season_alltime["yr"]==timerange2]["cnt"].sum()
    winter_means = season_alltime[season_alltime["season"]=="Winter"][season_alltime["yr"]==timerange2]["cnt"].sum()
    fall_temp = season_alltime[season_alltime["season"]=="Fall"][season_alltime["yr"]==timerange2]["temp"].sum()
    spring_temp = season_alltime[season_alltime["season"]=="Spring"][season_alltime["yr"]==timerange2]["temp"].sum()
    summer_temp = season_alltime[season_alltime["season"]=="Summer"][season_alltime["yr"]==timerange2]["temp"].sum()
    winter_temp = season_alltime[season_alltime["season"]=="Winter"][season_alltime["yr"]==timerange2]["temp"].sum()
    r4c1, r4c2 = st.columns(2)
    with r4c1:
        st.markdown(f"Avg. rented bikes per day ({timerange2}):")
        r4c1_1, r4c1_2 = st.columns(2)
        with r4c1_1:
            st.metric("Fall 🍁", value=round(fall_means,2))
            st.metric("Winter ❄️", value=round(winter_means,2)) 
        with r4c1_2:
            st.metric("Summer ☀️", value=round(summer_means,2))
            st.metric("Spring 🌼", value=round(spring_means,2))
    with r4c2:
        st.markdown(f"Avg. normalized temperature per day ({timerange2}):")
        r4c2_1, r4c2_2 = st.columns(2)
        with r4c2_1:
            st.metric("Fall 🍁", value=f"{round(fall_temp,2)} °C")
            st.metric("Winter ❄️", value=f"{round(winter_temp,2)} °C") 
        with r4c2_2:
            st.metric("Summer ☀️", value=f"{round(summer_temp,2)} °C")
            st.metric("Spring 🌼", value=f"{round(spring_temp,2)} °C")
     
# ⤷ Footer
st.caption("by Izzananda Adimas Faza / M312D4KY3106")
