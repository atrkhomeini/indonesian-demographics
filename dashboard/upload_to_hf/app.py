"""
Indonesia Demographics Market Intelligence Dashboard
Streamlit Application for Market Segmentation & Forecasting

Author: Data Science Team
Deployed: Hugging Face Spaces
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from data_loader import DataLoader
from visualizations import Visualizer

# Page configuration
st.set_page_config(
    page_title="Indonesia Demographics Intelligence",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem 0;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .segment-stars {
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
        color: white;
    }
    .segment-cashcows {
        background: linear-gradient(135deg, #90EE90 0%, #32CD32 100%);
        color: white;
    }
    .segment-developing {
        background: linear-gradient(135deg, #87CEEB 0%, #4682B4 100%);
        color: white;
    }
    .segment-saturated {
        background: linear-gradient(135deg, #FFB6C1 0%, #FF69B4 100%);
        color: white;
    }
</style>
""", unsafe_allow_html=True)


# Initialize session state
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False


@st.cache_data
def load_all_data():
    """Load all required data"""
    loader = DataLoader()
    return {
        'national_forecast': loader.load_national_forecast(),
        'regional_forecasts': loader.load_regional_forecasts(),
        'segmentation': loader.load_market_segmentation(),
        'segment_stats': loader.load_segment_statistics(),
        'expenditure_historical': loader.load_expenditure_historical(),
        'tfr_data': loader.load_tfr_data(),
    }


def main():
    """Main dashboard application"""
    
    # Header
    st.markdown('<h1 class="main-header">Indonesia Demographics Market Intelligence</h1>', 
                unsafe_allow_html=True)
    st.markdown("---")
    
    # Load data
    with st.spinner('Loading data...'):
        try:
            data = load_all_data()
            st.session_state.data_loaded = True
        except Exception as e:
            st.error(f"Error loading data: {e}")
            st.info("Please ensure data files are in the correct location.")
            return
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Select Analysis",
        ["Executive Summary", "Market Segmentation", "Forecasting", 
         "Regional Analysis", "Data Explorer"],
        key="navigation"
    )
    
    # Render selected page
    if page == "Executive Summary":
        show_executive_summary(data)
    elif page == "Market Segmentation":
        show_market_segmentation(data)
    elif page == "Forecasting":
        show_forecasting(data)
    elif page == "Regional Analysis":
        show_regional_analysis(data)
    elif page == "Data Explorer":
        show_data_explorer(data)
    
    # Footer
    st.sidebar.markdown("---")
    st.sidebar.info("""
    **About**
    
    Market intelligence platform analyzing Indonesian demographic trends 
    for business decision-making.
    
    **Data Sources:**
    - TFR: SP2020 Long Form
    - Expenditure: Susenas (2010-2025)
    
    **Tech Stack:**
    - Python, Pandas, Statsmodels
    - PostgreSQL, Streamlit
    - Plotly, Hugging Face
    """)


def show_executive_summary(data):
    """Executive Summary Dashboard"""
    
    st.header("📊 Executive Summary")
    st.markdown("Key insights and metrics at a glance")
    
    # Key Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    
    segmentation = data['segmentation']
    segment_stats = data['segment_stats']
    national_forecast = data['national_forecast']
    
    with col1:
        total_regions = len(segmentation)
        st.metric("Total Regions", f"{total_regions:,}")
    
    with col2:
        stars_count = len(segmentation[segmentation['segment'] == 'Stars'])
        st.metric("⭐ Stars Markets", stars_count, 
                 delta=f"{stars_count/total_regions*100:.1f}%")
    
    with col3:
        latest_exp = national_forecast[national_forecast['type'] == 'historical']['expenditure'].iloc[-1]
        st.metric("Current Avg Expenditure", f"Rp {latest_exp:,.0f}k")
    
    with col4:
        forecast_2030 = national_forecast[national_forecast['year'] == 2030]['expenditure'].iloc[0]
        growth = ((forecast_2030 / latest_exp) - 1) * 100
        st.metric("2030 Projection", f"Rp {forecast_2030:,.0f}k", 
                 delta=f"{growth:.1f}%")
    
    st.markdown("---")
    
    # Market Segmentation Overview
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Market Segmentation Distribution")
        
        viz = Visualizer()
        fig = viz.create_segment_pie(segmentation)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Segment Statistics")
        
        # Format segment stats
        display_stats = segment_stats.copy()
        display_stats = display_stats.rename(columns={
            'segment': 'Segment',
            'count': 'Regions',
            'tfr_mean': 'Avg TFR',
            'expenditure_mean': 'Avg Expenditure'
        })
        display_stats = display_stats[['Segment', 'Regions', 'Avg TFR', 'Avg Expenditure']]
        display_stats['Avg Expenditure'] = display_stats['Avg Expenditure'].apply(lambda x: f"Rp {x:,.0f}k")
        display_stats['Avg TFR'] = display_stats['Avg TFR'].apply(lambda x: f"{x:.2f}")
        
        st.dataframe(display_stats, hide_index=True, use_container_width=True)
    
    st.markdown("---")
    
    # National Forecast Preview
    st.subheader("National Expenditure Forecast (2010-2030)")
    
    viz = Visualizer()
    fig = viz.create_forecast_chart(national_forecast)
    st.plotly_chart(fig, use_container_width=True)
    
    # Insights
    st.markdown("---")
    st.subheader("🔍 Key Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Market Opportunities:**
        - ⭐ **Stars**: High growth + high value → Primary expansion targets
        - 🐮 **Cash Cows**: Mature markets → Premium product positioning
        - 🌱 **Developing**: High volume + emerging wealth → Mass market potential
        """)
    
    with col2:
        st.markdown(f"""
        **Forecast Highlights:**
        - Projected **{growth:.1f}% growth** in per capita expenditure by 2030
        - Current average: **Rp {latest_exp:,.0f}k** → **Rp {forecast_2030:,.0f}k**
        - Confidence interval provides strategic planning range
        """)


def show_market_segmentation(data):
    """Market Segmentation Analysis"""
    
    st.header("🎯 Market Segmentation Analysis")
    st.markdown("Quadrant-based segmentation using TFR and Per Capita Expenditure")
    
    segmentation = data['segmentation']
    segment_stats = data['segment_stats']
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        selected_segment = st.selectbox(
            "Filter by Segment",
            ["All"] + sorted(segmentation['segment'].unique().tolist())
        )
    
    with col2:
        tfr_range = st.slider(
            "TFR Range",
            float(segmentation['tfr'].min()),
            float(segmentation['tfr'].max()),
            (float(segmentation['tfr'].min()), float(segmentation['tfr'].max()))
        )
    
    with col3:
        exp_range = st.slider(
            "Expenditure Range (Rp 000)",
            int(segmentation['expenditure'].min()),
            int(segmentation['expenditure'].max()),
            (int(segmentation['expenditure'].min()), int(segmentation['expenditure'].max()))
        )
    
    # Apply filters
    filtered = segmentation.copy()
    if selected_segment != "All":
        filtered = filtered[filtered['segment'] == selected_segment]
    filtered = filtered[
        (filtered['tfr'] >= tfr_range[0]) & 
        (filtered['tfr'] <= tfr_range[1]) &
        (filtered['expenditure'] >= exp_range[0]) &
        (filtered['expenditure'] <= exp_range[1])
    ]
    
    st.info(f"Showing {len(filtered)} of {len(segmentation)} regions")
    
    # Quadrant Plot
    st.subheader("Quadrant Analysis")
    
    viz = Visualizer()
    fig = viz.create_quadrant_plot(segmentation, highlight_regions=filtered['region_name'].tolist())
    st.plotly_chart(fig, use_container_width=True)
    
    # Segment Cards
    st.markdown("---")
    st.subheader("Segment Profiles")
    
    col1, col2, col3, col4 = st.columns(4)
    
    segments_info = {
        'Stars': {'emoji': '⭐', 'desc': 'High Growth + High Value'},
        'Cash Cows': {'emoji': '🐮', 'desc': 'Mature + High Value'},
        'Developing': {'emoji': '🌱', 'desc': 'Emerging + High Volume'},
        'Saturated': {'emoji': '⚠️', 'desc': 'Low Growth + Low Value'}
    }
    
    for col, segment in zip([col1, col2, col3, col4], segments_info.keys()):
        with col:
            count = len(segmentation[segmentation['segment'] == segment])
            stats = segment_stats[segment_stats['segment'] == segment].iloc[0]
            
            st.markdown(f"""
            <div class="metric-card segment-{segment.lower().replace(' ', '')}">
                <h3>{segments_info[segment]['emoji']} {segment}</h3>
                <p><b>{count}</b> regions</p>
                <p>Avg TFR: <b>{stats['tfr_mean']:.2f}</b></p>
                <p>Avg Exp: <b>Rp {stats['expenditure_mean']:,.0f}k</b></p>
                <p style="font-size: 0.9rem; margin-top: 0.5rem;">{segments_info[segment]['desc']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Regional List
    st.markdown("---")
    st.subheader("Region Details")
    
    display_df = filtered.copy()
    display_df = display_df.sort_values('expenditure', ascending=False)
    display_df['tfr'] = display_df['tfr'].apply(lambda x: f"{x:.2f}")
    display_df['expenditure'] = display_df['expenditure'].apply(lambda x: f"Rp {x:,.0f}k")
    
    st.dataframe(
        display_df[['region_name', 'segment', 'tfr', 'expenditure']],
        hide_index=True,
        use_container_width=True,
        height=400
    )


def show_forecasting(data):
    """Time Series Forecasting Analysis"""
    
    st.header("📈 Time Series Forecasting")
    st.markdown("ARIMA-based expenditure projections (2010-2030)")
    
    national_forecast = data['national_forecast']
    regional_forecasts = data['regional_forecasts']
    
    # Tabs
    tab1, tab2, tab3 = st.tabs(["National Forecast", "Regional Forecasts", "Model Details"])
    
    with tab1:
        st.subheader("National Per Capita Expenditure")
        
        viz = Visualizer()
        fig = viz.create_forecast_chart(national_forecast)
        st.plotly_chart(fig, use_container_width=True)
        
        # Metrics
        col1, col2, col3 = st.columns(3)
        
        historical = national_forecast[national_forecast['type'] == 'historical']
        forecast = national_forecast[national_forecast['type'] == 'forecast']
        
        with col1:
            last_hist = historical['expenditure'].iloc[-1]
            st.metric("Last Historical (2025)", f"Rp {last_hist:,.0f}k")
        
        with col2:
            forecast_2030 = forecast[forecast['year'] == 2030]['expenditure'].iloc[0]
            st.metric("Forecast 2030", f"Rp {forecast_2030:,.0f}k")
        
        with col3:
            growth = ((forecast_2030 / last_hist) - 1) * 100
            st.metric("5-Year Growth", f"{growth:.2f}%")
        
        # Forecast Table
        st.markdown("---")
        st.subheader("Forecast Values")
        
        forecast_display = forecast[['year', 'expenditure', 'lower_ci', 'upper_ci']].copy()
        forecast_display.columns = ['Year', 'Forecast', '95% CI Lower', '95% CI Upper']
        forecast_display['Forecast'] = forecast_display['Forecast'].apply(lambda x: f"Rp {x:,.0f}k")
        forecast_display['95% CI Lower'] = forecast_display['95% CI Lower'].apply(lambda x: f"Rp {x:,.0f}k")
        forecast_display['95% CI Upper'] = forecast_display['95% CI Upper'].apply(lambda x: f"Rp {x:,.0f}k")
        
        st.dataframe(forecast_display, hide_index=True, use_container_width=True)
    
    with tab2:
        st.subheader("Regional Forecasts (Top 10 Regions)")
        
        if regional_forecasts is not None:
            # Region selector
            regions = sorted(regional_forecasts['region_name'].unique())
            selected_regions = st.multiselect(
                "Select regions to compare",
                regions,
                default=regions[:5]
            )
            
            if selected_regions:
                viz = Visualizer()
                fig = viz.create_regional_forecast_chart(
                    data['expenditure_historical'],
                    regional_forecasts,
                    selected_regions
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # Regional forecast table
                st.markdown("---")
                region_2030 = regional_forecasts[
                    (regional_forecasts['year'] == 2030) &
                    (regional_forecasts['region_name'].isin(selected_regions))
                ].sort_values('forecast', ascending=False)
                
                display_rf = region_2030[['region_name', 'forecast', 'lower_ci', 'upper_ci']].copy()
                display_rf.columns = ['Region', '2030 Forecast', 'Lower CI', 'Upper CI']
                display_rf['2030 Forecast'] = display_rf['2030 Forecast'].apply(lambda x: f"Rp {x:,.0f}k")
                display_rf['Lower CI'] = display_rf['Lower CI'].apply(lambda x: f"Rp {x:,.0f}k")
                display_rf['Upper CI'] = display_rf['Upper CI'].apply(lambda x: f"Rp {x:,.0f}k")
                
                st.dataframe(display_rf, hide_index=True, use_container_width=True)
        else:
            st.info("Regional forecast data not available")
    
    with tab3:
        st.subheader("Model Information")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **Model Specification**
            
            - **Algorithm**: ARIMA (Auto-Regressive Integrated Moving Average)
            - **Parameter Selection**: Grid search via AIC minimization
            - **Confidence Level**: 95%
            - **Historical Period**: 2010-2025
            - **Forecast Horizon**: 5 years (2026-2030)
            """)
        
        with col2:
            st.markdown("""
            **Model Performance**
            
            - **RMSE**: Root Mean Square Error
            - **MAE**: Mean Absolute Error
            - **MAPE**: Mean Absolute Percentage Error
            
            *Detailed metrics available in model metadata files*
            """)
        
        st.markdown("---")
        st.info("""
        **Interpretation Guide:**
        
        - **Forecast Line**: Expected trajectory based on historical patterns
        - **Confidence Interval**: 95% probability that actual values will fall within this range
        - **Wider CI**: Greater uncertainty (common in longer-term forecasts)
        """)


def show_regional_analysis(data):
    """Regional Deep-Dive Analysis"""
    
    st.header("🗺️ Regional Analysis")
    st.markdown("Detailed profiles for individual regions")
    
    segmentation = data['segmentation']
    expenditure_hist = data['expenditure_historical']
    tfr_data = data['tfr_data']
    
    # Region selector
    regions = sorted(segmentation['region_name'].unique())
    selected_region = st.selectbox("Select Region", regions)
    
    if selected_region:
        region_data = segmentation[segmentation['region_name'] == selected_region].iloc[0]
        
        # Region Profile Card
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    color: white; padding: 2rem; border-radius: 1rem; margin-bottom: 2rem;">
            <h2>{selected_region}</h2>
            <div style="display: flex; gap: 3rem; margin-top: 1rem;">
                <div>
                    <p style="font-size: 0.9rem; opacity: 0.9;">Market Segment</p>
                    <h3 style="margin: 0;">{region_data['segment']}</h3>
                </div>
                <div>
                    <p style="font-size: 0.9rem; opacity: 0.9;">Total Fertility Rate</p>
                    <h3 style="margin: 0;">{region_data['tfr']:.2f}</h3>
                </div>
                <div>
                    <p style="font-size: 0.9rem; opacity: 0.9;">Per Capita Expenditure</p>
                    <h3 style="margin: 0;">Rp {region_data['expenditure']:,.0f}k</h3>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Historical Trends
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Expenditure Trend (2010-2025)")
            
            region_exp = expenditure_hist[expenditure_hist['region_name'] == selected_region]
            if len(region_exp) > 0:
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=region_exp['year'],
                    y=region_exp['expenditure'],
                    mode='lines+markers',
                    name=selected_region,
                    line=dict(color='#1f77b4', width=3),
                    marker=dict(size=8)
                ))
                
                fig.update_layout(
                    xaxis_title="Year",
                    yaxis_title="Expenditure (Rp 000)",
                    hovermode='x unified',
                    height=400
                )
                
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Historical expenditure data not available")
        
        with col2:
            st.subheader("Regional Comparison")
            
            # Compare with segment peers
            segment_peers = segmentation[segmentation['segment'] == region_data['segment']]
            segment_avg_tfr = segment_peers['tfr'].mean()
            segment_avg_exp = segment_peers['expenditure'].mean()
            
            comparison_df = pd.DataFrame({
                'Metric': ['TFR', 'Expenditure'],
                'This Region': [region_data['tfr'], region_data['expenditure']],
                'Segment Average': [segment_avg_tfr, segment_avg_exp]
            })
            
            fig = go.Figure()
            fig.add_trace(go.Bar(
                name='This Region',
                x=comparison_df['Metric'],
                y=comparison_df['This Region'],
                marker_color='#1f77b4'
            ))
            fig.add_trace(go.Bar(
                name='Segment Average',
                x=comparison_df['Metric'],
                y=comparison_df['Segment Average'],
                marker_color='#ff7f0e'
            ))
            
            fig.update_layout(
                barmode='group',
                height=400,
                yaxis_title="Value"
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Market Insights
        st.markdown("---")
        st.subheader("📊 Market Insights")
        
        # Generate insights based on segment
        insights = generate_regional_insights(region_data, segment_avg_tfr, segment_avg_exp)
        
        for insight in insights:
            st.markdown(f"- {insight}")


def show_data_explorer(data):
    """Data Explorer & Download"""
    
    st.header("📁 Data Explorer")
    st.markdown("Explore and download raw data")
    
    # Dataset selector
    dataset = st.selectbox(
        "Select Dataset",
        ["Market Segmentation", "National Forecast", "Regional Forecasts", 
         "Expenditure Historical", "TFR Data"]
    )
    
    # Load and display selected dataset
    if dataset == "Market Segmentation":
        df = data['segmentation']
    elif dataset == "National Forecast":
        df = data['national_forecast']
    elif dataset == "Regional Forecasts":
        df = data['regional_forecasts']
    elif dataset == "Expenditure Historical":
        df = data['expenditure_historical']
    elif dataset == "TFR Data":
        df = data['tfr_data']
    
    if df is not None:
        st.dataframe(df, use_container_width=True, height=500)
        
        # Statistics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Rows", f"{len(df):,}")
        
        with col2:
            st.metric("Columns", len(df.columns))
        
        with col3:
            memory_mb = df.memory_usage(deep=True).sum() / 1024 / 1024
            st.metric("Memory Usage", f"{memory_mb:.2f} MB")
        
        # Download button
        st.markdown("---")
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="⬇️ Download CSV",
            data=csv,
            file_name=f"{dataset.lower().replace(' ', '_')}.csv",
            mime="text/csv"
        )
    else:
        st.warning("Dataset not available")


def generate_regional_insights(region_data, segment_avg_tfr, segment_avg_exp):
    """Generate insights for a region"""
    
    insights = []
    segment = region_data['segment']
    
    # TFR insight
    if region_data['tfr'] > segment_avg_tfr:
        insights.append(f"**Higher fertility** than {segment} average ({region_data['tfr']:.2f} vs {segment_avg_tfr:.2f}) → Stronger population growth potential")
    else:
        insights.append(f"**Lower fertility** than {segment} average ({region_data['tfr']:.2f} vs {segment_avg_tfr:.2f}) → Aging population trend")
    
    # Expenditure insight
    if region_data['expenditure'] > segment_avg_exp:
        insights.append(f"**Above-average purchasing power** (Rp {region_data['expenditure']:,.0f}k vs Rp {segment_avg_exp:,.0f}k) → Premium product opportunity")
    else:
        insights.append(f"**Below-average purchasing power** (Rp {region_data['expenditure']:,.0f}k vs Rp {segment_avg_exp:,.0f}k) → Mass market focus")
    
    # Segment-specific strategy
    if segment == "Stars":
        insights.append("**Strategic Priority**: Primary expansion target with strong growth and high value")
    elif segment == "Cash Cows":
        insights.append("**Strategic Priority**: Focus on premium products and services in mature market")
    elif segment == "Developing":
        insights.append("**Strategic Priority**: Build brand early in emerging high-volume market")
    elif segment == "Saturated":
        insights.append("**Strategic Priority**: Consider operational efficiency and niche strategies")
    
    return insights


if __name__ == "__main__":
    main()