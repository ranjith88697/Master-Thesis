{\rtf1\ansi\ansicpg1252\cocoartf2822
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import streamlit as st\
import pandas as pd\
import plotly.express as px\
\
st.set_page_config(page_title="Tariff Forecast Dashboard", layout="wide")\
\
st.title("\uc0\u55357 \u56522  Trade Tariff Forecasting Dashboard")\
st.write("Machine Learning + Economic Theory")\
\
# Load your results\
results_ml_df = pd.read_csv("results_ml.csv")\
results_rw_df = pd.read_csv("results_rw.csv")\
fi_df = pd.read_csv("feature_importance.csv")\
forecast_df = pd.read_csv("forecast_results.csv")\
\
# Sidebar\
st.sidebar.header("Select Country")\
country = st.sidebar.selectbox("Partner Country", ["CHN", "DEU", "IND", "JPN"])\
\
# Filter data\
ml_country = results_ml_df[results_ml_df["Partner"] == country]\
rw_country = results_rw_df[results_rw_df["Partner"] == country]\
fi_country = fi_df[fi_df["Partner"] == country]\
forecast_country = forecast_df[forecast_df["Partner"] == country]\
\
# Best model\
best_row = ml_country.loc[ml_country["MAE"].idxmin()]\
best_model = best_row["Model"]\
\
# Overview cards\
col1, col2, col3 = st.columns(3)\
col1.metric("Best Model", best_model)\
col2.metric("MAE", round(best_row["MAE"], 3))\
col3.metric("RMSE", round(best_row["RMSE"], 3))\
\
# Model comparison charts\
st.subheader("Model Performance Comparison")\
\
fig_mae = px.bar(ml_country, x="Model", y="MAE", title="MAE by Model")\
fig_rmse = px.bar(ml_country, x="Model", y="RMSE", title="RMSE by Model")\
\
col4, col5 = st.columns(2)\
col4.plotly_chart(fig_mae, use_container_width=True)\
col5.plotly_chart(fig_rmse, use_container_width=True)\
\
# Rolling window\
st.subheader("Rolling-Window Forecast Performance")\
fig_rw = px.line(rw_country, x="Year", y=["Actual", "Predicted"], title="Rolling Forecast")\
st.plotly_chart(fig_rw, use_container_width=True)\
\
# Feature importance\
st.subheader("Top 5 Features")\
top5 = fi_country.sort_values("Importance", ascending=False).head(5)\
fig_fi = px.bar(top5, x="Importance", y="Feature", orientation="h", title="Feature Importance")\
st.plotly_chart(fig_fi, use_container_width=True)\
\
# Forecast plot\
st.subheader("Actual vs Predicted Tariff")\
fig_fc = px.line(forecast_country, x="Year", y=["Actual", "Predicted"], title="Forecast Results")\
st.plotly_chart(fig_fc, use_container_width=True)\
}