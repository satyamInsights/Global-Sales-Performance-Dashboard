import streamlit as st
import pandas as pd
import plotly.express as px

# Page Config
st.set_page_config(
    page_title="Sales Analysis Dashboard",
    page_icon="📊",
    layout="wide"
)

# Title
st.title("📊 Sales Analysis Dashboard")
st.markdown("Interactive Dashboard using Streamlit")

# Load Data
@st.cache_data
def load_data():
    df = pd.read_csv("Sales.csv")
    return df

df = load_data()

# Sidebar
st.sidebar.header("Filters")

country = st.sidebar.multiselect(
    "Select Country",
    options=df["Country"].unique(),
    default=df["Country"].unique()
)

gender = st.sidebar.multiselect(
    "Select Gender",
    options=df["Customer_Gender"].unique(),
    default=df["Customer_Gender"].unique()
)

year = st.sidebar.multiselect(
    "Select Year",
    options=sorted(df["Year"].unique()),
    default=sorted(df["Year"].unique())
)

# Filter Data
filtered_df = df[
    (df["Country"].isin(country))
    & (df["Customer_Gender"].isin(gender))
    & (df["Year"].isin(year))
]

# KPI Section
total_revenue = filtered_df["Revenue"].sum()
total_profit = filtered_df["Profit"].sum()
total_cost = filtered_df["Cost"].sum()
total_orders = filtered_df["Order_Quantity"].sum()

st.subheader("📌 Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Revenue", f"${total_revenue:,.0f}")
col2.metric("Total Profit", f"${total_profit:,.0f}")
col3.metric("Total Cost", f"${total_cost:,.0f}")
col4.metric("Total Orders", f"{total_orders:,}")

# Dataset Preview
st.subheader("📋 Dataset Preview")
st.dataframe(filtered_df.head())

# Revenue by Product Category
st.subheader("💰 Revenue by Product Category")

cat_rev = (
    filtered_df.groupby("Product_Category")["Revenue"]
    .sum()
    .reset_index()
)

fig1 = px.bar(
    cat_rev,
    x="Product_Category",
    y="Revenue",
    title="Revenue by Product Category"
)

st.plotly_chart(fig1, use_container_width=True)

# Profit by Country
st.subheader("🌍 Profit by Country")

country_profit = (
    filtered_df.groupby("Country")["Profit"]
    .sum()
    .reset_index()
)

fig2 = px.pie(
    country_profit,
    names="Country",
    values="Profit",
    title="Profit Distribution by Country"
)

st.plotly_chart(fig2, use_container_width=True)

# Revenue by Year
st.subheader("📈 Revenue Trend by Year")

year_rev = (
    filtered_df.groupby("Year")["Revenue"]
    .sum()
    .reset_index()
)

fig3 = px.line(
    year_rev,
    x="Year",
    y="Revenue",
    markers=True,
    title="Revenue Trend"
)

st.plotly_chart(fig3, use_container_width=True)

# Gender Analysis
st.subheader("👨‍🦱 Customer Gender Analysis")

gender_rev = (
    filtered_df.groupby("Customer_Gender")["Revenue"]
    .sum()
    .reset_index()
)

fig4 = px.bar(
    gender_rev,
    x="Customer_Gender",
    y="Revenue",
    color="Customer_Gender",
    title="Revenue by Gender"
)

st.plotly_chart(fig4, use_container_width=True)

# Age Group Analysis
st.subheader("🎯 Revenue by Age Group")

age_rev = (
    filtered_df.groupby("Age_Group")["Revenue"]
    .sum()
    .reset_index()
)

fig5 = px.bar(
    age_rev,
    x="Age_Group",
    y="Revenue",
    color="Age_Group",
    title="Revenue by Age Group"
)

st.plotly_chart(fig5, use_container_width=True)

# Top Products
st.subheader("🏆 Top 10 Products by Revenue")

top_products = (
    filtered_df.groupby("Product")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig6 = px.bar(
    top_products,
    x="Product",
    y="Revenue",
    title="Top 10 Products"
)

st.plotly_chart(fig6, use_container_width=True)

# Summary Statistics
st.subheader("📊 Summary Statistics")
st.dataframe(filtered_df.describe())

# Download Filtered Data
st.subheader("⬇ Download Filtered Data")

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download CSV",
    data=csv,
    file_name="filtered_sales_data.csv",
    mime="text/csv"
)