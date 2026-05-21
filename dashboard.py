import streamlit as st
import psutil
import time
import pandas as pd

st.set_page_config(
    page_title="System Control Center Pro",
    layout="wide"
)

if "cpu_history" not in st.session_state:
    st.session_state.cpu_history = []
if "ram_history" not in st.session_state:
    st.session_state.ram_history = []
if "alerts" not in st.session_state:
    st.session_state.alerts = []

st.sidebar.title("Control Panel")

mode = st.sidebar.selectbox(
    "Performance Mode",
    ["Balanced", "Performance", "Silent"]
)

refresh = st.sidebar.slider("Refresh Rate (sec)", 1, 5, 1)

if mode == "Silent":
    refresh = max(refresh, 3)
    theme_color = "🟢"
elif mode == "Performance":
    refresh = 1
    theme_color = "🔴"
else:
    theme_color = "🔵"

cpu = psutil.cpu_percent(interval=0.5)
ram = psutil.virtual_memory().percent
disk = psutil.disk_usage('/').percent
uptime = time.time() - psutil.boot_time()

st.session_state.cpu_history.append(cpu)
st.session_state.ram_history.append(ram)

st.session_state.cpu_history = st.session_state.cpu_history[-60:]
st.session_state.ram_history = st.session_state.ram_history[-60:]

def add_alert(message):
    timestamp = time.strftime("%H:%M:%S")
    st.session_state.alerts.append(f"[{timestamp}] {message}")
    st.session_state.alerts = st.session_state.alerts[-10:]

if cpu > 85:
    add_alert("High CPU usage detected")
if ram > 85:
    add_alert("High memory usage detected")
if disk > 90:
    add_alert("Low disk space warning")

st.title(f"{theme_color} System Control Center Pro")
st.caption("Real-time system monitoring dashboard")

st.divider()

col1, col2, col3, col4 = st.columns(4)

col1.metric("CPU Usage", f"{cpu}%")
col2.metric("RAM Usage", f"{ram}%")
col3.metric("Disk Usage", f"{disk}%")
col4.metric("Uptime (hrs)", f"{uptime/3600:.1f}")

st.divider()

st.subheader("Performance Monitoring")

g1, g2 = st.columns(2)

with g1:
    st.line_chart(st.session_state.cpu_history, height=250)

with g2:
    st.line_chart(st.session_state.ram_history, height=250)

st.divider()

st.subheader("Top Processes")

processes = []
for p in psutil.process_iter(['name', 'cpu_percent']):
    try:
        processes.append(p.info)
    except:
        pass

df = pd.DataFrame(processes)
df = df.sort_values(by="cpu_percent", ascending=False).head(10)

st.dataframe(df, use_container_width=True)

st.divider()

st.subheader("System Information")

st.write("CPU Cores:", psutil.cpu_count(logical=True))
st.write("Physical Cores:", psutil.cpu_count(logical=False))
st.write("Memory Total (GB):", round(psutil.virtual_memory().total / (1024**3), 2))
st.write("OS:", psutil.os.name)

st.divider()

st.subheader("System Alerts")

if len(st.session_state.alerts) == 0:
    st.success("No alerts detected")
else:
    for alert in reversed(st.session_state.alerts):
        st.warning(alert)

st.sidebar.markdown("Live Status")
st.sidebar.write(f"CPU: {cpu}%")
st.sidebar.write(f"RAM: {ram}%")
st.sidebar.write(f"Disk: {disk}%")

st.sidebar.info(mode)

time.sleep(refresh)
st.rerun()