import streamlit as st
import psutil
import time

st.set_page_config(page_title="System Monitor", layout="wide")

st.title("🖥️ System Health Dashboard")

# Live metrics
cpu = psutil.cpu_percent(interval=1)
ram = psutil.virtual_memory().percent
disk = psutil.disk_usage('/').percent

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("CPU Usage", f"{cpu}%")

with col2:
    st.metric("RAM Usage", f"{ram}%")

with col3:
    st.metric("Disk Usage", f"{disk}%")

st.divider()

# Alerts
st.subheader("System Status")

if cpu > 80:
    st.error("High CPU Usage Detected")
elif cpu > 50:
    st.warning("Moderate CPU Load")
else:
    st.success("CPU Normal")

if ram > 85:
    st.error("High Memory Usage")
else:
    st.success("Memory Normal")

if disk > 90:
    st.error("Low Disk Space")
else:
    st.success("Disk Space OK")