# Import libraries
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
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
season_alltime = df.groupby(by=["yr","season"]).agg({
    "cnt": "mean"
})
season_alltime = season_alltime.reset_index()
season_alltime.rename(columns={
    "yr": "yr",
    "cnt": "cnt"
}, inplace=True)
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
    else:
        labels = [group]
        fall_means = season_alltime[season_alltime["season"]=="Fall"][season_alltime["yr"]==group]["cnt"].tolist()
        spring_means = season_alltime[season_alltime["season"]=="Spring"][season_alltime["yr"]==group]["cnt"].tolist()
        summer_means = season_alltime[season_alltime["season"]=="Summer"][season_alltime["yr"]==group]["cnt"].tolist()
        winter_means = season_alltime[season_alltime["season"]=="Winter"][season_alltime["yr"]==group]["cnt"].tolist()
    x = np.arange(len(labels))
    width = 0.2
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(x - 1.5*width, fall_means, width, label='Fall')
    ax.bar(x - 0.5*width, spring_means, width, label='Spring')
    ax.bar(x + 0.5*width, summer_means, width, label='Summer')
    ax.bar(x + 1.5*width, winter_means, width, label='Winter')
    ax.set_ylabel('Rata-Rata Peminjaman Sepeda')
    ax.set_xlabel('Tahun')
    ax.set_title('Rata-Rata Peminjaman Sepeda Tiap Musim')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()
    st.pyplot(fig)

# Layouting Streamlit Interface
# ⤷ Header
st.title('Bike Sharing System :bike:')
st.header('System Dashboard')
st.markdown('Selamat datang di Bike Sharing System Dashboard. Silahkan pantau perkembangan sistem ini melalui _dashboard_ berikut.')
# ⤷ Monthly rented bikes section
st.subheader('Monthly Rented Bikes 📆')
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
st.subheader('Rented Bikes by Season 🍁')
r3c1, r3c2 = st.columns(2)
with r3c1:
    sub1_r3c1, sub2_r3c1 = st.columns(2)
    with sub1_r3c1:
        st.metric("Highest season", value="Fall")
    with sub2_r3c1:
        st.metric("Lowest season", value="Spring")
with r3c2:
    timerange2 = st.selectbox(
    key="season",
    label="Time range (year)",
    options=('All time', 2012, 2011)
    )
seasonrecap_by_range(timerange2)
if timerange2 == "All time":
    fall_means = season_alltime[season_alltime["season"]=="Fall"]["cnt"].sum()
    spring_means = season_alltime[season_alltime["season"]=="Spring"]["cnt"].sum()
    summer_means = season_alltime[season_alltime["season"]=="Summer"]["cnt"].sum()
    winter_means = season_alltime[season_alltime["season"]=="Winter"]["cnt"].sum()
else:
    fall_means = season_alltime[season_alltime["season"]=="Fall"][season_alltime["yr"]==timerange2]["cnt"].sum()
    spring_means = season_alltime[season_alltime["season"]=="Spring"][season_alltime["yr"]==timerange2]["cnt"].sum()
    summer_means = season_alltime[season_alltime["season"]=="Summer"][season_alltime["yr"]==timerange2]["cnt"].sum()
    winter_means = season_alltime[season_alltime["season"]=="Winter"][season_alltime["yr"]==timerange2]["cnt"].sum()
r4c1, r4c2, r4c3, r4c4 = st.columns(4)
with r4c1:
    st.metric("Fall", value=round(fall_means,2))
with r4c2:
    st.metric("Summer", value=round(summer_means,2))
with r4c3:
    st.metric("Winter", value=round(winter_means,2)) 
with r4c4:
    st.metric("Spring", value=round(spring_means,2))   
# ⤷ Footer
st.caption("by Izzananda Adimas Faza / M312D4KY3106")
