"""
Visualization Module
Professional Plotly visualizations for dashboard
"""

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np


class Visualizer:
    """Create professional visualizations"""
    
    def __init__(self):
        """Initialize visualizer with custom theme"""
        self.colors = {
            'Stars': '#FFD700',
            'Cash Cows': '#90EE90',
            'Developing': '#87CEEB',
            'Saturated': '#FFB6C1',
            'forecast': '#FF6B6B',
            'historical': '#1f77b4',
            'ci': 'rgba(255, 107, 107, 0.2)'
        }
        
        self.template = 'plotly_white'
    
    def create_segment_pie(self, segmentation_df):
        """
        Create pie chart for segment distribution
        
        Args:
            segmentation_df: DataFrame with segment column
            
        Returns:
            Plotly figure
        """
        segment_counts = segmentation_df['segment'].value_counts()
        
        fig = go.Figure(data=[go.Pie(
            labels=segment_counts.index,
            values=segment_counts.values,
            hole=0.4,
            marker=dict(colors=[self.colors.get(s, '#cccccc') for s in segment_counts.index]),
            textinfo='label+percent',
            textfont_size=14,
            hovertemplate='<b>%{label}</b><br>Regions: %{value}<br>Percentage: %{percent}<extra></extra>'
        )])
        
        fig.update_layout(
            template=self.template,
            showlegend=True,
            height=400,
            margin=dict(l=20, r=20, t=40, b=20),
            annotations=[dict(
                text=f'Total<br>{segment_counts.sum()}',
                x=0.5, y=0.5,
                font_size=16,
                showarrow=False
            )]
        )
        
        return fig
    
    def create_quadrant_plot(self, segmentation_df, highlight_regions=None):
        """
        Create interactive quadrant plot
        
        Args:
            segmentation_df: DataFrame with tfr, expenditure, segment
            highlight_regions: List of regions to highlight
            
        Returns:
            Plotly figure
        """
        # Calculate thresholds
        tfr_threshold = segmentation_df['tfr'].median()
        exp_threshold = segmentation_df['expenditure'].median()
        
        # Create base plot
        fig = px.scatter(
            segmentation_df,
            x='tfr',
            y='expenditure',
            color='segment',
            hover_name='region_name',
            hover_data={'tfr': ':.2f', 'expenditure': ':,.0f', 'segment': True},
            color_discrete_map=self.colors,
            template=self.template,
            height=600
        )
        
        # Add threshold lines
        fig.add_hline(
            y=exp_threshold,
            line_dash="dash",
            line_color="red",
            line_width=2,
            annotation_text=f"Expenditure Threshold: Rp {exp_threshold:,.0f}k",
            annotation_position="top right"
        )
        
        fig.add_vline(
            x=tfr_threshold,
            line_dash="dash",
            line_color="blue",
            line_width=2,
            annotation_text=f"TFR Threshold: {tfr_threshold:.2f}",
            annotation_position="top right"
        )
        
        # Add quadrant labels
        x_range = segmentation_df['tfr'].max() - segmentation_df['tfr'].min()
        y_range = segmentation_df['expenditure'].max() - segmentation_df['expenditure'].min()
        
        quadrant_annotations = [
            dict(x=tfr_threshold + x_range * 0.15, y=exp_threshold + y_range * 0.4,
                 text="⭐ Stars", showarrow=False, font=dict(size=16, color='#FFD700')),
            dict(x=tfr_threshold - x_range * 0.15, y=exp_threshold + y_range * 0.4,
                 text="🐮 Cash Cows", showarrow=False, font=dict(size=16, color='#90EE90')),
            dict(x=tfr_threshold + x_range * 0.15, y=exp_threshold - y_range * 0.4,
                 text="🌱 Developing", showarrow=False, font=dict(size=16, color='#87CEEB')),
            dict(x=tfr_threshold - x_range * 0.15, y=exp_threshold - y_range * 0.4,
                 text="⚠️ Saturated", showarrow=False, font=dict(size=16, color='#FFB6C1'))
        ]
        
        # Highlight specific regions if provided
        if highlight_regions:
            highlight_df = segmentation_df[segmentation_df['region_name'].isin(highlight_regions)]
            
            fig.add_trace(go.Scatter(
                x=highlight_df['tfr'],
                y=highlight_df['expenditure'],
                mode='markers',
                marker=dict(
                    size=15,
                    color='rgba(255, 0, 0, 0)',
                    line=dict(color='red', width=3)
                ),
                name='Selected',
                hoverinfo='skip',
                showlegend=True
            ))
        
        fig.update_layout(
            annotations=quadrant_annotations,
            xaxis_title="Total Fertility Rate (TFR)",
            yaxis_title="Per Capita Expenditure (Rp 000)",
            hovermode='closest'
        )
        
        return fig
    
    def create_forecast_chart(self, national_forecast_df):
        """
        Create national forecast chart with confidence interval
        
        Args:
            national_forecast_df: DataFrame with year, expenditure, type, ci columns
            
        Returns:
            Plotly figure
        """
        historical = national_forecast_df[national_forecast_df['type'] == 'historical']
        forecast = national_forecast_df[national_forecast_df['type'] == 'forecast']
        
        fig = go.Figure()
        
        # Historical data
        fig.add_trace(go.Scatter(
            x=historical['year'],
            y=historical['expenditure'],
            mode='lines+markers',
            name='Historical',
            line=dict(color=self.colors['historical'], width=3),
            marker=dict(size=8),
            hovertemplate='<b>%{x}</b><br>Expenditure: Rp %{y:,.0f}k<extra></extra>'
        ))
        
        # Forecast data
        fig.add_trace(go.Scatter(
            x=forecast['year'],
            y=forecast['expenditure'],
            mode='lines+markers',
            name='Forecast',
            line=dict(color=self.colors['forecast'], width=3, dash='dash'),
            marker=dict(size=8),
            hovertemplate='<b>%{x}</b><br>Forecast: Rp %{y:,.0f}k<extra></extra>'
        ))
        
        # Confidence interval
        if 'lower_ci' in forecast.columns and 'upper_ci' in forecast.columns:
            fig.add_trace(go.Scatter(
                x=forecast['year'].tolist() + forecast['year'].tolist()[::-1],
                y=forecast['upper_ci'].tolist() + forecast['lower_ci'].tolist()[::-1],
                fill='toself',
                fillcolor=self.colors['ci'],
                line=dict(color='rgba(255,255,255,0)'),
                name='95% Confidence Interval',
                hoverinfo='skip',
                showlegend=True
            ))
        
        # Add vertical line at forecast start
        last_hist_year = historical['year'].max()
        fig.add_vline(
            x=last_hist_year,
            line_dash="dot",
            line_color="gray",
            line_width=1,
            annotation_text="Forecast Start",
            annotation_position="top"
        )
        
        fig.update_layout(
            template=self.template,
            xaxis_title="Year",
            yaxis_title="Per Capita Expenditure (Rp 000)",
            hovermode='x unified',
            height=500,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        return fig
    
    def create_regional_forecast_chart(self, historical_df, forecast_df, regions):
        """
        Create multi-region forecast chart
        
        Args:
            historical_df: Historical expenditure data
            forecast_df: Forecast data
            regions: List of regions to plot
            
        Returns:
            Plotly figure
        """
        fig = go.Figure()
        
        # Color palette
        colors = px.colors.qualitative.Set2
        
        for idx, region in enumerate(regions):
            color = colors[idx % len(colors)]
            
            # Historical
            hist_data = historical_df[historical_df['region_name'] == region]
            if len(hist_data) > 0:
                fig.add_trace(go.Scatter(
                    x=hist_data['year'],
                    y=hist_data['expenditure'],
                    mode='lines+markers',
                    name=f'{region} (Historical)',
                    line=dict(color=color, width=2),
                    marker=dict(size=6),
                    legendgroup=region,
                    hovertemplate=f'<b>{region}</b><br>%{{x}}: Rp %{{y:,.0f}}k<extra></extra>'
                ))
            
            # Forecast
            fcst_data = forecast_df[forecast_df['region_name'] == region]
            if len(fcst_data) > 0:
                fig.add_trace(go.Scatter(
                    x=fcst_data['year'],
                    y=fcst_data['forecast'],
                    mode='lines+markers',
                    name=f'{region} (Forecast)',
                    line=dict(color=color, width=2, dash='dash'),
                    marker=dict(size=6, symbol='square'),
                    legendgroup=region,
                    hovertemplate=f'<b>{region}</b><br>%{{x}}: Rp %{{y:,.0f}}k<extra></extra>'
                ))
        
        fig.update_layout(
            template=self.template,
            xaxis_title="Year",
            yaxis_title="Per Capita Expenditure (Rp 000)",
            hovermode='x unified',
            height=600,
            legend=dict(
                orientation="v",
                yanchor="top",
                y=1,
                xanchor="left",
                x=1.02
            )
        )
        
        return fig
    
    def create_segment_bars(self, segment_stats_df):
        """
        Create bar charts for segment comparison
        
        Args:
            segment_stats_df: Segment statistics dataframe
            
        Returns:
            Plotly figure
        """
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=("Average TFR by Segment", "Average Expenditure by Segment")
        )
        
        # TFR bars
        fig.add_trace(
            go.Bar(
                x=segment_stats_df['segment'],
                y=segment_stats_df['tfr_mean'],
                marker_color=[self.colors.get(s, '#cccccc') for s in segment_stats_df['segment']],
                name='TFR',
                text=segment_stats_df['tfr_mean'].round(2),
                textposition='outside',
                hovertemplate='<b>%{x}</b><br>Avg TFR: %{y:.2f}<extra></extra>'
            ),
            row=1, col=1
        )
        
        # Expenditure bars
        fig.add_trace(
            go.Bar(
                x=segment_stats_df['segment'],
                y=segment_stats_df['expenditure_mean'],
                marker_color=[self.colors.get(s, '#cccccc') for s in segment_stats_df['segment']],
                name='Expenditure',
                text=segment_stats_df['expenditure_mean'].round(0).astype(int),
                textposition='outside',
                hovertemplate='<b>%{x}</b><br>Avg Expenditure: Rp %{y:,.0f}k<extra></extra>'
            ),
            row=1, col=2
        )
        
        fig.update_xaxes(title_text="Segment", row=1, col=1)
        fig.update_xaxes(title_text="Segment", row=1, col=2)
        fig.update_yaxes(title_text="TFR", row=1, col=1)
        fig.update_yaxes(title_text="Expenditure (Rp 000)", row=1, col=2)
        
        fig.update_layout(
            template=self.template,
            showlegend=False,
            height=400
        )
        
        return fig
    
    def create_heatmap(self, data_df, x_col, y_col, value_col, title=""):
        """
        Create heatmap visualization
        
        Args:
            data_df: Data dataframe
            x_col: X-axis column
            y_col: Y-axis column
            value_col: Value to display
            title: Chart title
            
        Returns:
            Plotly figure
        """
        pivot = data_df.pivot_table(
            index=y_col,
            columns=x_col,
            values=value_col,
            aggfunc='mean'
        )
        
        fig = go.Figure(data=go.Heatmap(
            z=pivot.values,
            x=pivot.columns,
            y=pivot.index,
            colorscale='RdYlGn',
            text=pivot.values.round(0),
            texttemplate='%{text}',
            textfont={"size": 10},
            hovertemplate='<b>%{y}</b><br>%{x}: %{z:,.0f}<extra></extra>'
        ))
        
        fig.update_layout(
            template=self.template,
            title=title,
            xaxis_title=x_col.replace('_', ' ').title(),
            yaxis_title=y_col.replace('_', ' ').title(),
            height=500
        )
        
        return fig