"""
Indonesia Demographics Market Intelligence Dashboard
Professional market analysis platform with dark mode support

Author: Data Science Team
Last Updated: November 2024
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / 'src'))

from data_loader import DataLoader
from visualizations import Visualizer

# Page config
st.set_page_config(
    page_title="Indonesia Demographics Intelligence",
    page_icon="🇮🇩",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state for dark mode
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False

def toggle_dark_mode():
    """Toggle dark mode state"""
    st.session_state.dark_mode = not st.session_state.dark_mode

# Get current theme
dark_mode = st.session_state.dark_mode

# Dynamic CSS based on theme
if dark_mode:
    bg_color = "#0f172a"
    bg_secondary = "#1e293b"
    text_color = "#e2e8f0"
    text_secondary = "#94a3b8"
    card_bg = "#1e293b"
    card_bg_gradient = "linear-gradient(135deg, #1e293b 0%, #0f172a 100%)"
    border_color = "#334155"
    hover_bg = "#334155"
else:
    bg_color = "#fafafa"
    bg_secondary = "#ffffff"
    text_color = "#111827"
    text_secondary = "#6b7280"
    card_bg = "#ffffff"
    card_bg_gradient = "linear-gradient(135deg, #ffffff 0%, #fafafa 100%)"
    border_color = "#e5e7eb"
    hover_bg = "#f9fafb"

# Professional Custom CSS
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');
    
    * {{
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }}
    
    .main {{
        background-color: {bg_color};
        color: {text_color};
    }}
    
    .main-header {{
        font-size: 2.75rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.25rem;
        letter-spacing: -0.03em;
        line-height: 1.2;
    }}
    
    .sub-header {{
        color: {text_secondary};
        font-size: 1.15rem;
        font-weight: 400;
        margin-bottom: 2rem;
        letter-spacing: 0.01em;
    }}
    
    .status-badge {{
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.5rem 1rem;
        background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
        border-radius: 8px;
        border: 1px solid #6ee7b7;
        font-size: 0.875rem;
        font-weight: 600;
        color: #065f46;
    }}
    
    .status-dot {{
        width: 8px;
        height: 8px;
        background: #10b981;
        border-radius: 50%;
        animation: pulse 2s ease-in-out infinite;
    }}
    
    @keyframes pulse {{
        0%, 100% {{ opacity: 1; }}
        50% {{ opacity: 0.5; }}
    }}
    
    .metric-card {{
        background: {card_bg_gradient};
        padding: 1.75rem;
        border-radius: 16px;
        border: 1px solid {border_color};
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        height: 100%;
    }}
    
    .metric-card:hover {{
        transform: translateY(-4px);
        box-shadow: 0 12px 24px rgba(0, 0, 0, 0.08);
    }}
    
    .metric-value {{
        font-size: 2.75rem;
        font-weight: 700;
        color: {text_color};
        font-family: 'JetBrains Mono', monospace;
        letter-spacing: -0.02em;
        line-height: 1;
        margin-bottom: 0.5rem;
    }}
    
    .metric-label {{
        font-size: 0.8125rem;
        color: {text_secondary};
        text-transform: uppercase;
        letter-spacing: 0.1em;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }}
    
    .metric-delta {{
        font-size: 0.875rem;
        font-weight: 500;
    }}
    
    .delta-positive {{ color: #059669; }}
    .delta-negative {{ color: #dc2626; }}
    .delta-neutral {{ color: {text_secondary}; }}
    
    .segment-card {{
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1rem;
        border-left: 4px solid;
        background: {card_bg};
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.06);
        transition: all 0.3s ease;
    }}
    
    .segment-card:hover {{
        transform: translateX(8px);
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
    }}
    
    .segment-emoji {{
        font-size: 2rem;
        margin-bottom: 0.5rem;
        display: block;
    }}
    
    .segment-title {{
        font-size: 1.25rem;
        font-weight: 600;
        margin-bottom: 0.75rem;
        color: {text_color};
    }}
    
    .segment-stat {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.9375rem;
        color: {text_color};
        margin: 0.5rem 0;
        display: flex;
        justify-content: space-between;
    }}
    
    .section-header {{
        font-size: 1.5rem;
        font-weight: 600;
        color: {text_color};
        margin: 2rem 0 1rem 0;
    }}
    
    .section-subheader {{
        font-size: 0.9375rem;
        color: {text_secondary};
        margin-bottom: 1.5rem;
    }}
    
    .divider {{
        height: 1px;
        background: linear-gradient(90deg, transparent 0%, {border_color} 50%, transparent 100%);
        margin: 2.5rem 0;
        border: none;
    }}
    
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
        padding-top: 2rem;
    }}
    
    [data-testid="stSidebar"] * {{
        color: #e2e8f0 !important;
    }}
    
    .stSelectbox [data-baseweb="select"] {{
        background-color: {card_bg};
        color: {text_color};
    }}
    
    .stTextInput input {{
        background-color: {card_bg};
        color: {text_color};
        border-color: {border_color};
    }}
    
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
</style>
""", unsafe_allow_html=True)


def get_region_column(df):
    """
    Find the region column name in dataframe
    Handles various possible column names
    """
    possible_names = ['region', 'Region', 'nama_kabupaten_kota', 'wilayah', 'daerah', 'kabupaten_kota']
    
    for col in possible_names:
        if col in df.columns:
            return col
    
    # If no match, return first string column
    for col in df.columns:
        if df[col].dtype == 'object':
            return col
    
    return df.columns[0]  # Last resort


def standardize_dataframe(df):
    """
    Standardize column names for consistency
    """
    if df is None or df.empty:
        return df
    
    # Create a copy
    df = df.copy()
    
    # Find region column
    region_col = get_region_column(df)
    if region_col != 'region':
        df['region'] = df[region_col]
    
    return df


def show_executive_summary(data):
    """Executive Summary Dashboard"""
    
    st.markdown('<div class="section-header">📊 Market Overview</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subheader">Key metrics and insights into Indonesian demographic landscape</div>', unsafe_allow_html=True)
    
    segmentation = standardize_dataframe(data['segmentation'])
    segment_stats = data['segment_stats']
    national_forecast = data['national_forecast']
    
    if segmentation is None or segmentation.empty:
        st.warning("⚠️ Segmentation data not available")
        return
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    total_regions = len(segmentation)
    stars_count = len(segmentation[segmentation['segment'] == 'Stars']) if 'segment' in segmentation.columns else 0
    stars_pct = (stars_count / total_regions * 100) if total_regions > 0 else 0
    
    current_exp = national_forecast[national_forecast['type'] == 'historical']['expenditure'].iloc[-1] if not national_forecast.empty else 0
    future_exp = national_forecast[national_forecast['year'] == 2030]['expenditure'].iloc[0] if len(national_forecast[national_forecast['year'] == 2030]) > 0 else current_exp
    growth_pct = ((future_exp / current_exp) - 1) * 100 if current_exp > 0 else 0
    
    metrics = [
        {'col': col1, 'value': f"{total_regions:,}", 'label': 'Regions Analyzed', 'delta': 'Kabupaten & Kota', 'type': 'neutral'},
        {'col': col2, 'value': f"{stars_count}", 'label': 'High-Value Markets', 'delta': f"⭐ {stars_pct:.1f}% Stars", 'type': 'positive'},
        {'col': col3, 'value': f"Rp {current_exp:,.0f}k", 'label': 'Current Avg Spend', 'delta': 'Per capita 2025', 'type': 'neutral'},
        {'col': col4, 'value': f"Rp {future_exp:,.0f}k", 'label': '2030 Projection', 'delta': f"↗ +{growth_pct:.1f}%", 'type': 'positive'}
    ]
    
    for m in metrics:
        with m['col']:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">{m['label']}</div>
                <div class="metric-value">{m['value']}</div>
                <div class="metric-delta delta-{m['type']}">{m['delta']}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    
    # Charts
    col1, col2 = st.columns([1.3, 1])
    
    with col1:
        st.markdown('### 🎯 Market Distribution')
        try:
            viz = Visualizer(dark_mode=dark_mode)
            fig = viz.create_segment_pie(segmentation)
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"Chart error: {e}")
    
    with col2:
        st.markdown('### 📈 Segment Profiles')
        if segment_stats is not None and not segment_stats.empty:
            segment_config = {
                'Stars': {'emoji': '⭐', 'class': 'segment-stars'},
                'Cash Cows': {'emoji': '🎯', 'class': 'segment-cashcows'},
                'Developing': {'emoji': '📊', 'class': 'segment-developing'},
                'Saturated': {'emoji': '⚠️', 'class': 'segment-saturated'}
            }
            
            for idx, row in segment_stats.iterrows():
                config = segment_config.get(row['segment'], {'emoji': '•', 'class': 'segment-card'})
                st.markdown(f"""
                <div class="segment-card {config['class']}" style="border-left-color: #667eea;">
                    <span class="segment-emoji">{config['emoji']}</span>
                    <div class="segment-title">{row['segment']}</div>
                    <div class="segment-stat">
                        <span>Regions:</span><span><strong>{int(row['count'])}</strong></span>
                    </div>
                    <div class="segment-stat">
                        <span>Avg TFR:</span><span><strong>{row['tfr_mean']:.2f}</strong></span>
                    </div>
                    <div class="segment-stat">
                        <span>Avg Spend:</span><span><strong>Rp {row['expenditure_mean']:,.0f}k</strong></span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown('### 📈 National Expenditure Trajectory')
    
    try:
        viz = Visualizer(dark_mode=dark_mode)
        fig = viz.create_forecast_chart(national_forecast)
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Forecast chart error: {e}")


def show_market_segmentation(data):
    """Market Segmentation Analysis"""
    
    st.markdown('<div class="section-header">🎯 Market Segmentation</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subheader">Regional classification based on fertility rates and purchasing power</div>', unsafe_allow_html=True)
    
    segmentation = standardize_dataframe(data['segmentation'])
    
    if segmentation is None or segmentation.empty:
        st.warning("⚠️ Segmentation data not available")
        return
    
    # Filters
    st.markdown("### Filter & Explore")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        segments = ['All'] + sorted(segmentation['segment'].unique().tolist()) if 'segment' in segmentation.columns else ['All']
        selected_segment = st.selectbox("Market Segment", segments)
    
    with col2:
        if 'tfr' in segmentation.columns:
            tfr_range = st.slider(
                "TFR Range",
                float(segmentation['tfr'].min()),
                float(segmentation['tfr'].max()),
                (float(segmentation['tfr'].min()), float(segmentation['tfr'].max()))
            )
        else:
            tfr_range = (0, 10)
    
    with col3:
        if 'expenditure' in segmentation.columns:
            exp_range = st.slider(
                "Expenditure Range (Rp 000s)",
                float(segmentation['expenditure'].min()),
                float(segmentation['expenditure'].max()),
                (float(segmentation['expenditure'].min()), float(segmentation['expenditure'].max()))
            )
        else:
            exp_range = (0, 100000)
    
    # Apply filters
    filtered_data = segmentation.copy()
    if selected_segment != 'All' and 'segment' in filtered_data.columns:
        filtered_data = filtered_data[filtered_data['segment'] == selected_segment]
    
    if 'tfr' in filtered_data.columns and 'expenditure' in filtered_data.columns:
        filtered_data = filtered_data[
            (filtered_data['tfr'] >= tfr_range[0]) & 
            (filtered_data['tfr'] <= tfr_range[1]) &
            (filtered_data['expenditure'] >= exp_range[0]) & 
            (filtered_data['expenditure'] <= exp_range[1])
        ]
    
    st.info(f"📊 Showing **{len(filtered_data)}** of {len(segmentation)} regions")
    
    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown('### 📍 Regional Positioning')
    
    # Quadrant Plot
    try:
        viz = Visualizer(dark_mode=dark_mode)
        fig = viz.create_quadrant_plot(filtered_data)
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"⚠️ Chart error: {str(e)}")
        st.info("💡 Tip: Make sure your data has 'tfr', 'expenditure', 'segment', and 'region' columns")
    
    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown('### 📋 Region Details')
    
    search_term = st.text_input("🔍 Search regions", placeholder="Type region name...", label_visibility="visible")
    
    display_data = filtered_data.copy()
    if search_term and 'region' in display_data.columns:
        display_data = display_data[display_data['region'].str.contains(search_term, case=False, na=False)]
    
    required_cols = ['region', 'segment', 'tfr', 'expenditure']
    if all(col in display_data.columns for col in required_cols):
        display_df = display_data[required_cols].sort_values('expenditure', ascending=False)
        display_df.columns = ['Region', 'Segment', 'TFR', 'Expenditure (Rp 000)']
        st.dataframe(display_df, use_container_width=True, height=400)
        
        csv = display_df.to_csv(index=False)
        st.download_button("📥 Download Data", csv, "segmentation.csv", "text/csv")
    else:
        st.warning(f"⚠️ Required columns not found. Available: {', '.join(display_data.columns)}")


def show_forecasting(data):
    """Forecasting Analysis"""
    
    st.markdown('<div class="section-header">🔮 Expenditure Forecasting</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subheader">Where spending is headed through 2030</div>', unsafe_allow_html=True)
    
    national_forecast = data['national_forecast']
    
    if national_forecast is None or national_forecast.empty:
        st.warning("⚠️ Forecast data not available")
        return
    
    st.markdown("### National Trajectory")
    
    try:
        viz = Visualizer(dark_mode=dark_mode)
        fig = viz.create_forecast_chart(national_forecast)
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Chart error: {e}")
    
    with st.expander("📊 About the Model"):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            **Model:** ARIMA
            
            **Why ARIMA?**
            - Captures trends
            - Handles seasonality
            - Confidence intervals
            """)
        with col2:
            st.markdown("""
            **Coverage:**
            - Historical: 2010-2025
            - Forecast: 2026-2030
            - Confidence: 95%
            """)


def show_regional_analysis(data):
    """Regional Analysis"""
    
    st.markdown('<div class="section-header">🗺️ Regional Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subheader">Deep dive into individual markets</div>', unsafe_allow_html=True)
    
    segmentation = standardize_dataframe(data['segmentation'])
    
    if segmentation is None or segmentation.empty:
        st.warning("⚠️ Segmentation data not available")
        return
    
    if 'region' not in segmentation.columns:
        st.error("⚠️ Region column not found in data")
        return
    
    regions = sorted(segmentation['region'].unique())
    selected_region = st.selectbox("Select a region", regions, label_visibility="visible")
    
    if selected_region:
        region_data = segmentation[segmentation['region'] == selected_region].iloc[0]
        
        st.markdown('<hr class="divider">', unsafe_allow_html=True)
        
        segment_emoji = {'Stars': '⭐', 'Cash Cows': '🎯', 'Developing': '📊', 'Saturated': '⚠️'}
        emoji = segment_emoji.get(region_data.get('segment', ''), '•')
        
        st.markdown(f"""
        <div class="segment-card" style="border-left-color: #667eea;">
            <span class="segment-emoji">{emoji}</span>
            <div class="segment-title">{selected_region}</div>
            <p style="color: #6b7280;">{region_data.get('segment', 'Unknown')} segment</p>
            <div class="segment-stat">
                <span>TFR:</span><span><strong>{region_data.get('tfr', 0):.2f}</strong></span>
            </div>
            <div class="segment-stat">
                <span>Expenditure:</span><span><strong>Rp {region_data.get('expenditure', 0):,.0f}k</strong></span>
            </div>
        </div>
        """, unsafe_allow_html=True)


def show_data_explorer(data):
    """Data Explorer"""
    
    st.markdown('<div class="section-header">📁 Data Explorer</div>', unsafe_allow_html=True)
    
    datasets = {k: v for k, v in data.items() if v is not None and not (isinstance(v, pd.DataFrame) and v.empty)}
    
    if not datasets:
        st.warning("⚠️ No data available")
        return
    
    dataset_name = st.selectbox("Choose dataset", list(datasets.keys()), label_visibility="visible")
    selected_data = datasets[dataset_name]
    
    if selected_data is not None and not selected_data.empty:
        col1, col2, col3 = st.columns(3)
        col1.metric("Rows", f"{len(selected_data):,}")
        col2.metric("Columns", len(selected_data.columns))
        col3.metric("Memory", f"{selected_data.memory_usage(deep=True).sum() / 1024:.1f} KB")
        
        st.markdown('<hr class="divider">', unsafe_allow_html=True)
        st.dataframe(selected_data, use_container_width=True, height=400)
        
        csv = selected_data.to_csv(index=False)
        st.download_button(f"📥 Download {dataset_name}", csv, f"{dataset_name.lower().replace(' ', '_')}.csv", "text/csv")


def main():
    """Main dashboard application"""
    
    # Header
    col1, col2 = st.columns([6, 1])
    
    with col1:
        st.markdown('<h1 class="main-header">Indonesia Demographics</h1>', unsafe_allow_html=True)
        st.markdown('<p class="sub-header">Regional Market Intelligence Platform</p>', unsafe_allow_html=True)
    
    with col2:
        theme_icon = "🌙" if not dark_mode else "☀️"
        if st.button(f"{theme_icon}", key="theme_toggle", help="Toggle dark mode"):
            toggle_dark_mode()
            st.rerun()
    
    # Status
    col1, col2, col3 = st.columns([2, 1.5, 1.5])
    with col1:
        st.markdown('<div class="status-badge"><span class="status-dot"></span><span>Live Data</span></div>', unsafe_allow_html=True)
    
    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    
    # Sidebar - FIXED: Added label and label_visibility
    st.sidebar.markdown("### Navigation")
    page = st.sidebar.radio(
        "Select Page",  # Added proper label
        ["📊 Executive Summary", "🎯 Market Segmentation", "🔮 Forecasting", 
         "🗺️ Regional Analysis", "📁 Data Explorer"],
        label_visibility="collapsed"  # Hide label visually but keep for accessibility
    )
    
    st.sidebar.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.sidebar.markdown("""
    ### About
    
    Analyzing 500+ Indonesian regions across 16 years.
    
    **Data:** BPS Indonesia  
    **Updated:** Nov 2024
    """)
    
    # Load data
    loader = DataLoader()
    
    try:
        data = {
            'segmentation': loader.load_market_segmentation(),
            'segment_stats': loader.load_segment_statistics(),
            'national_forecast': loader.load_national_forecast(),
            'regional_forecasts': loader.load_regional_forecasts(),
            'expenditure_historical': loader.load_expenditure_historical(),
            'tfr_data': loader.load_tfr_data()
        }
        
        # Route to pages
        if "Executive Summary" in page:
            show_executive_summary(data)
        elif "Market Segmentation" in page:
            show_market_segmentation(data)
        elif "Forecasting" in page:
            show_forecasting(data)
        elif "Regional Analysis" in page:
            show_regional_analysis(data)
        elif "Data Explorer" in page:
            show_data_explorer(data)
            
    except Exception as e:
        st.error(f"⚠️ Error loading data: {str(e)}")
        st.info("💡 Running with sample data mode")


if __name__ == "__main__":
    main()