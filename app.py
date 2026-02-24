import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Weather Data Analytics Platform",
    page_icon="🌦️",
    layout="wide"
)

st.title("🌦️ Weather Data Analytics Platform")

# ---------------- API KEY ----------------
# IMPORTANT: Add API_KEY inside Streamlit Secrets when deploying
API_KEY = st.secrets["API_KEY"] if "API_KEY" in st.secrets else "YOUR_API_KEY"

# ---------------- CITY INPUT ----------------
city = st.text_input("Enter City Name", "Bhubaneswar")

if st.button("Get Weather Data"):

    if API_KEY == "YOUR_API_KEY":
        st.error("⚠ Please add your API key.")
    else:

        # -------- CURRENT WEATHER API --------
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()

            temp = data["main"]["temp"]
            feels_like = data["main"]["feels_like"]
            humidity = data["main"]["humidity"]
            weather_desc = data["weather"][0]["description"]

            st.subheader(f"Current Weather in {city}")

            col1, col2, col3 = st.columns(3)

            col1.metric("🌡 Temperature (°C)", temp)
            col2.metric("🤒 Feels Like (°C)", feels_like)
            col3.metric("💧 Humidity (%)", humidity)

            st.write(f"**Condition:** {weather_desc.title()}")

            # -------- 5 DAY FORECAST --------
            forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
            forecast_response = requests.get(forecast_url)

            if forecast_response.status_code == 200:
                forecast_data = forecast_response.json()

                dates = []
                temperatures = []

                for item in forecast_data["list"]:
                    dates.append(datetime.strptime(item["dt_txt"], "%Y-%m-%d %H:%M:%S"))
                    temperatures.append(item["main"]["temp"])

                df = pd.DataFrame({
                    "Date": dates,
                    "Temperature (°C)": temperatures
                })

                st.subheader("📈 Temperature Trend (5 Day Forecast)")

                fig = px.line(df, x="Date", y="Temperature (°C)", title="Temperature Trend")
                st.plotly_chart(fig, use_container_width=True)

        else:
            st.error("City not found. Please enter a valid city name.")
