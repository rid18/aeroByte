import streamlit as st
import numpy as np
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta

# --- PAGE CONFIG ---
st.set_page_config(layout="wide", page_title="aeroByte AI Pro Max")

# --- CSS STYLING ---
st.markdown("""
    <style>
    header {visibility: hidden;}
    .stApp { background-color: #f4f7f6; }
    .block-container { padding-top: 4rem !important; max-width: 95% !important; }
    
    .main-title { 
        font-size: 52px; font-weight: 800; color: #0f172a; 
        text-align: center; margin-bottom: 5px;
    }
    
    .status-dot { color: #22c55e; animation: blinker 1.5s linear infinite; }
    @keyframes blinker { 50% { opacity: 0; } }

    [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: white;
        border-radius: 15px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02);
        padding: 20px;
    }
    
    .proto-label {
        background: #6366f1; color: white; padding: 5px 15px; 
        border-radius: 10px; font-size: 12px; font-weight: bold;
        display: inline-block; margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- DATA & SESSION STATE ---
if 'STATION_DATA' not in st.session_state:
    st.session_state.STATION_DATA = {"Anand Vihar": 361, "ITO": 245, "RK Puram": 185, "Dwarka": 210}

if 'MAP_LOCS' not in st.session_state:
    st.session_state.MAP_LOCS = {
        "Anand Vihar": {"lat": 28.6465, "lon": 77.3167},
        "ITO": {"lat": 28.6285, "lon": 77.2330},
        "RK Puram": {"lat": 28.5660, "lon": 77.1767},
        "Dwarka": {"lat": 28.5823, "lon": 77.0500}
    }

if 'reports' not in st.session_state: 
    st.session_state.reports = []

# --- SIDEBAR: MANUAL STATION REGISTRATION ---
with st.sidebar:
    st.header("📍 Control Panel")
    selected_station = st.selectbox("Active Station", list(st.session_state.STATION_DATA.keys()))
    aqi_val = st.slider("Global Sensor Input", 0, 500, st.session_state.STATION_DATA[selected_station])
    
    st.divider()
    st.subheader("➕ Register New Station")
    with st.form("station_form"):
        n_name = st.text_input("New Station Name")
        n_lat = st.number_input("Latitude", value=28.6139, format="%.4f")
        n_lon = st.number_input("Longitude", value=77.2090, format="%.4f")
        n_aqi = st.number_input("Initial AQI", 0, 500, 100)
        submitted = st.form_submit_button("Add Station")
        if submitted and n_name:
            st.session_state.STATION_DATA[n_name] = n_aqi
            st.session_state.MAP_LOCS[n_name] = {"lat": n_lat, "lon": n_lon}
            st.success(f"Registered {n_name}!")
            st.rerun()

    st.divider()
    st.subheader("👤 Citizen Profile")
    u_age = st.number_input("User Age", 1, 100, 25)
    u_resp = st.checkbox("Respiratory Issues?")

# --- HEADER ---
st.markdown(f"<div class='main-title'>🌍 aeroByte AI: {selected_station}</div>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 18px;'><span class='status-dot'>●</span> Live IoT Multi-Sensor Stream Active</p>", unsafe_allow_html=True)

# --- 1. EMERGENCY ZONE ---
if aqi_val > 300:
    st.markdown(f"""
        <div style="background-color:#1e1e2e; padding:30px; border-radius:15px; border: 3px solid #ff4b4b; color:white; margin-bottom:25px;">
            <h1 style='text-align:center; color:#ff4b4b; margin:0;'>☣️ AI CONTAINMENT ZONE ACTIVE</h1>
            <div style='display: flex; justify-content: space-around; text-align: center; margin-top:20px;'>
                <div><h3>🚿 Smog Guns</h3><b>DEPLOYED</b></div>
                <div><h3>🏗️ Construction</h3><b>HARD-BAN</b></div>
                <div><h3>🏭 Industrial</h3><b>SHUTDOWN</b></div>
            </div>
        </div>
    """, unsafe_allow_html=True)

# --- 2. TRAFFIC & EMISSION STRATEGY ---
st.subheader("🛠️ Sector-wise AI Interventions")
t_col, h_col = st.columns(2)
with t_col:
    t_status = "DIVERTED" if aqi_val > 250 else "OPTIMIZED"
    st.markdown(f"""<div style="background-color:#0f172a; padding:25px; border-radius:15px; color:white; border: 1px solid #334155;">
        <h2 style='margin:0;'>🚦 Traffic Strategy</h2><p style='font-size:22px; margin:0;'>Status: <b>{t_status}</b></p></div>""", unsafe_allow_html=True)
with h_col:
    i_status = "RESTRICTED" if aqi_val > 250 else "MONITORED"
    st.markdown(f"""<div style="background-color:#0f172a; padding:25px; border-radius:15px; color:white; border: 1px solid #334155;">
        <h2 style='margin:0;'>🏭 Emission Control</h2><p style='font-size:22px; margin:0;'>Status: <b>{i_status}</b></p></div>""", unsafe_allow_html=True)

# --- 3. HEALTH & 24-HOUR FORECAST ---
st.divider()
col_f1, col_f2 = st.columns([1, 1.4])
with col_f1:
    st.subheader("🏥 Health Risk AI")
    h_color = "#ef4444" if aqi_val > 200 else "#f59e0b" if aqi_val > 100 else "#10b981"
    st.markdown(f"""
        <div style="border-top: 10px solid {h_color}; padding:35px; background:white; border-radius:15px; box-shadow: 0 10px 15px rgba(0,0,0,0.1);">
            <h4 style='color:#64748b; margin:0;'>Current AQI Level</h4>
            <h1 style='margin:0; font-size:85px; color:#1e293b;'>{aqi_val}</h1>
            <h2 style='color:{h_color}; margin:0;'>{'Severe Risk' if aqi_val > 200 else 'Moderate'}</h2>
        </div>""", unsafe_allow_html=True)
with col_f2:
    st.subheader("📊 24-Hour Predictive Forecast")
    vals = [int(aqi_val + np.random.randint(-50, 50)) for _ in range(24)]
    fig = go.Figure(go.Bar(x=[f"{i}:00" for i in range(24)], y=vals, marker_color='#ef4444' if aqi_val > 200 else '#6366f1'))
    fig.update_layout(height=350, margin=dict(l=0, r=0, t=10, b=0), template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)

# --- 4. LIVE MAP ---
st.divider()
st.subheader(f"🗺️ Live Station View: {selected_station}")
coords = st.session_state.MAP_LOCS.get(selected_station, {"lat": 28.6139, "lon": 77.2090})
st.map(pd.DataFrame([coords]), zoom=12, use_container_width=True)

# --- 5. PROTOTYPE FEATURES & NOVELTY ---
st.divider()
st.markdown("<span class='proto-label'>PROTOTYPE V2.0</span>", unsafe_allow_html=True)
ex1, ex2, ex3 = st.columns(3)
with ex1:
    with st.container(border=True): 
        st.markdown("### 🤖 Health Assistant")
        if aqi_val > 150:
            if u_resp or u_age > 60:
                st.error("🚨 STAY INDOORS")
            else:
                st.warning("⚠️ Wear N95 Mask")
        else:
            st.success("✅ Safe for Profile")
with ex2:
    with st.container(border=True):
        st.markdown("### 💰 Economic Impact")
        loss = (aqi_val * 1.42)
        st.markdown(f"<h1 style='color:#ef4444; margin:0;'>₹ {loss:.1f}Cr</h1>", unsafe_allow_html=True)
        st.caption("Daily Productivity Loss")
with ex3:
    with st.container(border=True):
        st.markdown("### 🌳 Oxygen Impact")
        # Novelty: Eco-credits points system
        credits = int((500 - aqi_val) * 0.8)
        st.markdown(f"<h1 style='color:#10b981; margin:0;'>{credits} pts</h1>", unsafe_allow_html=True)
        st.caption("AI-Generated Eco-Credits")

# --- 6. ANALYTICS ROW ---
st.divider()
st.subheader("🔍 Deep AI Forecasting & Source Analysis")
graph_col1, graph_col2 = st.columns(2)

with graph_col1:
    st.markdown("### 📅 72-Hour AI Predictive Forecast")
    future_times = [(datetime.now() + timedelta(hours=i*6)).strftime("%d %b, %H:%M") for i in range(13)]
    future_vals = [int(aqi_val + np.random.randint(-70, 70)) for _ in range(13)]
    fig_72 = go.Figure(go.Scatter(x=future_times, y=future_vals, fill='tozeroy', mode='lines+markers', line=dict(color='#6366f1', width=3)))
    fig_72.update_layout(height=400, template="plotly_white", margin=dict(l=0, r=0, t=10, b=0))
    st.plotly_chart(fig_72, use_container_width=True)

with graph_col2:
    st.markdown("### 🛰️ AI Deep Source Analysis")
    tabs = st.tabs(["Pollution Source", "Satellite Heatmap"])
    with tabs[0]:
        fig_p = go.Figure(data=[go.Pie(labels=['Vehicles', 'Industry', 'Dust', 'Waste'], values=[30, 35, 20, 15], hole=.4)])
        fig_p.update_layout(height=350, margin=dict(l=0, r=0, t=0, b=0))
        st.plotly_chart(fig_p, use_container_width=True)
    with tabs[1]:
        fig_h = go.Figure(data=go.Heatmap(z=np.random.rand(10, 15), colorscale='Reds'))
        fig_h.update_layout(height=350, margin=dict(l=0, r=0, t=0, b=0))
        st.plotly_chart(fig_h, use_container_width=True)

# --- 7. COMMUNITY FEED (BOTTOM) ---
st.divider()
st.subheader("📢 Community Violation Feed")
v_form, v_feed = st.columns([1, 1.2])

with v_form:
    with st.container(border=True):
        v_type = st.selectbox("Violation Type", ["Industrial Smoke", "Garbage Burning", "Dust Source"])
        v_loc = st.text_input("Location Landmark")
        if st.button("Submit Report"):
            if v_loc:
                st.session_state.reports.append({"type": v_type, "loc": v_loc, "time": datetime.now().strftime("%H:%M")})
                st.toast("AI: Report Logged Successfully!")

with v_feed:
    if st.session_state.reports:
        for r in reversed(st.session_state.reports[-3:]):
            st.info(f"📍 {r['type']} at {r['loc']} | {r['time']}")
    else:
        st.write("No active reports in this zone.")

st.divider()
if st.button("🎁 Claim My aeroPoints"):
    st.balloons()