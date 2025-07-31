import streamlit as st
import random
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(
    page_title="Battery Management System",
    page_icon="🔋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dashboard theme
st.markdown("""
<style>
    /* Import Poppins font */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    /* Main styling */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #334155 100%);
        font-family: 'Poppins', sans-serif;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #1e293b 0%, #334155 100%);
    }
    
    /* Main container */
    .main .block-container {
        padding: 1rem 2rem;
        max-width: none;
    }
    
    /* Dashboard header */
    .dashboard-header {
        background: linear-gradient(135deg, #3b82f6, #8b5cf6);
        padding: 1.5rem 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    
    .dashboard-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.1'%3E%3Ccircle cx='7' cy='7' r='1'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
    }
    
    .dashboard-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: white;
        margin: 0;
        position: relative;
        z-index: 1;
    }
    
    .dashboard-subtitle {
        color: rgba(255,255,255,0.8);
        font-size: 1.1rem;
        margin: 0.5rem 0 0 0;
        position: relative;
        z-index: 1;
    }
    
    /* Status cards */
    .status-card {
        background: rgba(255,255,255,0.1);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255,255,255,0.2);
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .status-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.3);
    }
    
    .status-value {
        font-size: 2rem;
        font-weight: 700;
        color: #10b981;
        margin-bottom: 0.5rem;
    }
    
    .status-label {
        color: #94a3b8;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Cell grid */
    .cell-grid-container {
        background: rgba(255,255,255,0.05);
        border-radius: 20px;
        padding: 2rem;
        margin-bottom: 2rem;
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    .cell-item {
        background: linear-gradient(135deg, rgba(59,130,246,0.1), rgba(139,92,246,0.1));
        border: 1px solid rgba(255,255,255,0.15);
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 1rem;
        position: relative;
        overflow: hidden;
    }
    
    .cell-item::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #10b981, #06d6a0);
    }
    
    .cell-number {
        font-size: 0.8rem;
        color: #64748b;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    /* Results panel */
    .results-panel {
        background: rgba(255,255,255,0.05);
        border-radius: 20px;
        padding: 2rem;
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    .result-row {
        background: rgba(255,255,255,0.08);
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        border-left: 4px solid #3b82f6;
        transition: all 0.3s ease;
    }
    
    .result-row:hover {
        background: rgba(255,255,255,0.12);
        transform: translateX(5px);
    }
    
    .cell-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #e2e8f0;
        margin-bottom: 1rem;
    }
    
    /* Custom button */
    .custom-button {
        background: linear-gradient(135deg, #10b981, #06d6a0);
        color: white;
        border: none;
        padding: 1rem 2rem;
        border-radius: 50px;
        font-weight: 600;
        font-size: 1rem;
        cursor: pointer;
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
        width: 100%;
        margin: 1rem 0;
    }
    
    .custom-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 30px rgba(16,185,129,0.4);
    }
    
    /* Alert styles */
    .alert-success {
        background: rgba(16,185,129,0.2);
        border: 1px solid rgba(16,185,129,0.5);
        border-radius: 12px;
        padding: 1rem;
        color: #10b981;
        margin: 1rem 0;
    }
    
    .alert-warning {
        background: rgba(245,158,11,0.2);
        border: 1px solid rgba(245,158,11,0.5);
        border-radius: 12px;
        padding: 1rem;
        color: #f59e0b;
        margin: 1rem 0;
    }
    
    .alert-danger {
        background: rgba(239,68,68,0.2);
        border: 1px solid rgba(239,68,68,0.5);
        border-radius: 12px;
        padding: 1rem;
        color: #ef4444;
        margin: 1rem 0;
    }
    
    /* Hide streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
    
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'monitoring_active' not in st.session_state:
    st.session_state.monitoring_active = False
if 'analysis_data' not in st.session_state:
    st.session_state.analysis_data = None

# Sidebar configuration
with st.sidebar:
    st.markdown("### ⚙️ System Configuration")
    
    monitoring_mode = st.toggle("🔴 Live Monitoring", value=st.session_state.monitoring_active)
    st.session_state.monitoring_active = monitoring_mode
    
    st.markdown("### 📊 Display Options")
    show_charts = st.checkbox("Show Performance Charts", value=True)
    show_alerts = st.checkbox("Show System Alerts", value=True)
    auto_refresh = st.checkbox("Auto Refresh (5s)", value=False)
    
    st.markdown("### 🔧 Advanced Settings")
    temp_threshold = st.slider("Temperature Alert (°C)", 30, 50, 35)
    voltage_tolerance = st.slider("Voltage Tolerance (%)", 1, 10, 5)
    
    if auto_refresh:
        st.rerun()

# Dashboard Header
st.markdown("""
<div class="dashboard-header">
    <h1 class="dashboard-title">🔋 Battery Management System</h1>
    <p class="dashboard-subtitle">Real-time battery cell monitoring and analysis platform</p>
</div>
""", unsafe_allow_html=True)

# System status overview
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="status-card">
        <div class="status-value">8</div>
        <div class="status-label">Total Cells</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    active_cells = sum(1 for i in range(8) if st.session_state.get(f'current_{i}', 0) > 0)
    st.markdown(f"""
    <div class="status-card">
        <div class="status-value">{active_cells}</div>
        <div class="status-label">Active Cells</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    status = "ONLINE" if monitoring_mode else "STANDBY"
    color = "#10b981" if monitoring_mode else "#f59e0b"
    st.markdown(f"""
    <div class="status-card">
        <div class="status-value" style="color: {color};">{status}</div>
        <div class="status-label">System Status</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    current_time = datetime.now().strftime("%H:%M:%S")
    st.markdown(f"""
    <div class="status-card">
        <div class="status-value" style="font-size: 1.2rem;">{current_time}</div>
        <div class="status-label">Last Update</div>
    </div>
    """, unsafe_allow_html=True)

# Main content area
left_col, right_col = st.columns([1, 1.5])

# Left column - Input Configuration
with left_col:
    st.markdown("""
    <div class="cell-grid-container">
        <h3 style="color: #e2e8f0; margin-bottom: 1.5rem;">🔧 Cell Configuration</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Cell configuration in a different layout
    CELL_TYPES = ["LFP", "MNC", "NCA", "LTO"]
    CELL_SPECS = {
        "LFP": {"nominal_voltage": 3.2, "max_voltage": 3.6, "min_voltage": 2.5, "color": "#10b981"},
        "MNC": {"nominal_voltage": 3.7, "max_voltage": 4.2, "min_voltage": 3.0, "color": "#3b82f6"},
        "NCA": {"nominal_voltage": 3.6, "max_voltage": 4.1, "min_voltage": 3.0, "color": "#8b5cf6"},
        "LTO": {"nominal_voltage": 2.4, "max_voltage": 2.8, "min_voltage": 1.5, "color": "#f59e0b"}
    }
    
    cell_configs = {}
    
    for i in range(8):
        with st.container():
            st.markdown(f"""
            <div class="cell-item">
                <div class="cell-number">CELL MODULE {i+1:02d}</div>
            </div>
            """, unsafe_allow_html=True)
            
            col_a, col_b = st.columns(2)
            with col_a:
                cell_type = st.selectbox(
                    "Type",
                    CELL_TYPES,
                    key=f"cell_type_{i}",
                    label_visibility="collapsed"
                )
            
            with col_b:
                current = st.number_input(
                    "Current (A)",
                    min_value=0.0,
                    max_value=10.0,
                    value=0.0,
                    step=0.1,
                    key=f"current_{i}",
                    label_visibility="collapsed"
                )
            
            cell_configs[f"cell_{i+1}"] = {
                "type": cell_type,
                "current": current
            }
    
    # Analysis button with custom styling
    if st.button("🚀 START ANALYSIS", use_container_width=True):
        if any(config["current"] > 0 for config in cell_configs.values()):
            # Generate analysis data
            analysis_results = {}
            for cell_id, config in cell_configs.items():
                if config["current"] > 0:
                    specs = CELL_SPECS[config["type"]]
                    voltage = round(specs["nominal_voltage"] + random.uniform(-0.3, 0.3), 2)
                    temperature = random.randint(20, 45)
                    capacity = round(voltage * config["current"], 2)
                    efficiency = round(random.uniform(85, 98), 1)
                    health = "Excellent" if temperature < 30 else "Good" if temperature < 35 else "Warning"
                    
                    analysis_results[cell_id] = {
                        "type": config["type"],
                        "voltage": voltage,
                        "current": config["current"],
                        "temperature": temperature,
                        "capacity": capacity,
                        "efficiency": efficiency,
                        "health": health,
                        "max_voltage": specs["max_voltage"],
                        "min_voltage": specs["min_voltage"],
                        "color": specs["color"]
                    }
            
            st.session_state.analysis_data = analysis_results
            st.success("✅ Analysis completed successfully!")
        else:
            st.error("❌ Please configure at least one cell with current > 0")

# Right column - Results and Charts
with right_col:
    if st.session_state.analysis_data:
        st.markdown("""
        <div class="results-panel">
            <h3 style="color: #e2e8f0; margin-bottom: 1.5rem;">📈 Analysis Results</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Results in table format
        results_data = []
        alerts = []
        
        for cell_id, data in st.session_state.analysis_data.items():
            st.markdown(f"""
            <div class="result-row" style="border-left-color: {data['color']};">
                <div class="cell-title">{cell_id.replace('_', ' ').title()} - {data['type']}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Metrics in columns
            met_col1, met_col2, met_col3, met_col4 = st.columns(4)
            with met_col1:
                st.metric("Voltage", f"{data['voltage']}V", f"{data['voltage'] - CELL_SPECS[data['type']]['nominal_voltage']:+.1f}V")
            with met_col2:
                st.metric("Current", f"{data['current']}A")
            with met_col3:
                temp_delta = data['temperature'] - 25
                st.metric("Temperature", f"{data['temperature']}°C", f"{temp_delta:+d}°C")
            with met_col4:
                st.metric("Efficiency", f"{data['efficiency']}%")
            
            # Check for alerts
            if data['temperature'] > temp_threshold:
                alerts.append(f"🌡️ {cell_id.title()}: High temperature ({data['temperature']}°C)")
            
            results_data.append({
                'Cell': cell_id.replace('_', ' ').title(),
                'Type': data['type'],
                'Voltage': data['voltage'],
                'Current': data['current'],
                'Temperature': data['temperature'],
                'Efficiency': data['efficiency'],
                'Health': data['health']
            })
        
        # Charts section
        if show_charts and results_data:
            st.markdown("### 📊 Performance Visualization")
            
            # Create performance charts
            df = pd.DataFrame(results_data)
            
            chart_col1, chart_col2 = st.columns(2)
            
            with chart_col1:
                # Temperature chart
                fig_temp = px.bar(
                    df, 
                    x='Cell', 
                    y='Temperature',
                    color='Type',
                    title="Cell Temperature Distribution",
                    color_discrete_map={
                        'LFP': '#10b981',
                        'MNC': '#3b82f6', 
                        'NCA': '#8b5cf6',
                        'LTO': '#f59e0b'
                    }
                )
                fig_temp.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='white'
                )
                st.plotly_chart(fig_temp, use_container_width=True)
            
            with chart_col2:
                # Efficiency gauge
                avg_efficiency = df['Efficiency'].mean()
                fig_gauge = go.Figure(go.Indicator(
                    mode = "gauge+number+delta",
                    value = avg_efficiency,
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    title = {'text': "System Efficiency"},
                    delta = {'reference': 90},
                    gauge = {
                        'axis': {'range': [0, 100]},
                        'bar': {'color': "#10b981"},
                        'steps': [
                            {'range': [0, 50], 'color': "rgba(239,68,68,0.3)"},
                            {'range': [50, 80], 'color': "rgba(245,158,11,0.3)"},
                            {'range': [80, 100], 'color': "rgba(16,185,129,0.3)"}
                        ],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': 95
                        }
                    }
                ))
                fig_gauge.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='white',
                    height=300
                )
                st.plotly_chart(fig_gauge, use_container_width=True)
        
        # Alerts section
        if show_alerts and alerts:
            st.markdown("### 🚨 System Alerts")
            for alert in alerts:
                st.markdown(f'<div class="alert-warning">{alert}</div>', unsafe_allow_html=True)
        elif show_alerts:
            st.markdown('<div class="alert-success">✅ All systems operating within normal parameters</div>', unsafe_allow_html=True)
    
    else:
        st.info("👆 Configure cells and run analysis to see results here")

# Footer with system info
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("**System Version:** v2.1.0")
with col2:
    st.markdown("**Last Calibration:** 2025-01-15")
with col3:
    st.markdown("**Uptime:** 24h 15m 30s")