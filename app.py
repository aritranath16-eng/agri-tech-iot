import streamlit as st
import pandas as pd
from supabase import create_client
import time

# 1. Connect to Database (Paste your URL and Key here again!)
SUPABASE_URL = "https://qtnmomvlratulfbwklyj.supabase.co"
SUPABASE_KEY = "sb_publishable_jubeneginJg1j6r0ZnHNYQ_O0B4MuCA"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

st.set_page_config(page_title="Agri-Tech Dashboard", layout="wide")
st.title("🌱 Real-Time Agri-Tech IoT Dashboard")

# 2. Add Interactive Sidebar for Alert Thresholds
st.sidebar.header("⚙️ Alert Thresholds")
st.sidebar.write("Adjust the sliders to set danger zones.")
temp_limit = st.sidebar.slider("Max Temperature (°C)", 20.0, 35.0, 30.0)
hum_limit = st.sidebar.slider("Max Humidity (%)", 50.0, 90.0, 80.0)
co2_limit = st.sidebar.slider("Max CO2 (ppm)", 500.0, 1000.0, 800.0)

# 3. Function to grab the latest data
def fetch_data():
    response = supabase.table('sensor_data').select('*').order('created_at', desc=True).limit(50).execute()
    if len(response.data) > 0:
        df = pd.DataFrame(response.data)
        df = df.sort_values('created_at') 
        return df
    return None

df = fetch_data()

if df is not None:
    latest = df.iloc[-1]
    
    # 4. ALERT LOGIC: Check if latest data crosses our slider limits
    alerts = []
    if latest['temperature'] > temp_limit:
        alerts.append(f"🌡️ High Temperature Alert: {latest['temperature']} °C")
    if latest['humidity'] > hum_limit:
        alerts.append(f"💧 High Humidity Alert: {latest['humidity']} %")
    if latest['co2'] > co2_limit:
        alerts.append(f"💨 High CO2 Alert: {latest['co2']} ppm")
        
    # Display alerts if any exist
    if alerts:
        for alert in alerts:
            st.error(f"**🚨 {alert}**")
    else:
        st.success("✅ All environmental systems are normal.")

    st.divider()

    # 5. Display Current Metrics
    col1, col2, col3 = st.columns(3)
    
    # We can use delta to show how much it changed from the previous reading
    previous = df.iloc[-2] if len(df) > 1 else latest
    
    col1.metric("Current Temperature", f"{latest['temperature']} °C", f"{round(latest['temperature'] - previous['temperature'], 2)} °C")
    col2.metric("Current Humidity", f"{latest['humidity']} %", f"{round(latest['humidity'] - previous['humidity'], 2)} %")
    col3.metric("Current CO2", f"{latest['co2']} ppm", f"{round(latest['co2'] - previous['co2'], 2)} ppm")
    
    st.divider()
    
    # 6. Display Graphs
    st.subheader("Historical Trends (Last 50 Readings)")
    graph_col1, graph_col2, graph_col3 = st.columns(3)
    
    with graph_col1:
        st.write("Temperature (°C)")
        st.line_chart(df, y='temperature', x='created_at', height=250, color="#ff4b4b")
        
    with graph_col2:
        st.write("Humidity (%)")
        st.line_chart(df, y='humidity', x='created_at', height=250, color="#0068c9")
        
    with graph_col3:
        st.write("CO2 (ppm)")
        st.line_chart(df, y='co2', x='created_at', height=250, color="#29b09d")

# 7. Modern Streamlit Auto-Refresh
time.sleep(3)
st.rerun()