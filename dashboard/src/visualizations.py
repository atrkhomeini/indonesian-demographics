"""
Visualization Module - Professional Charts with Dark Mode
Custom Plotly visualizations with theme support

Author: Data Science Team
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np


class Visualizer:
    """Professional visualization components with dark mode support"""
    
    def __init__(self, dark_mode=False):
        """
        Initialize with custom color scheme and styling
        
        Args:
            dark_mode (bool): Enable dark mode styling
        """
        self.dark_mode = dark_mode
        
        # Professional color palette
        self.colors = {
            'Stars': '#f59e0b',
            'Cash Cows': '#10b981',
            'Developing': '#3b82f6',
            'Saturated': '#64748b',
            'forecast': '#dc2626',
            'historical': '#0f172a' if not dark_mode else '#e2e8f0',
            'ci': 'rgba(220, 38, 38, 0.15)',
            'primary': '#667eea',
            'secondary': '#764ba2'
        }
        
        # Theme-specific colors
        if dark_mode:
            self.bg_color = '#0f172a'
            self.plot_bg = '#1e293b'
            self.text_color = '#e2e8f0'
            self.text_secondary = '#94a3b8'
            self.grid_color = '#334155'
            self.template = 'plotly_dark'
        else:
            self.bg_color = 'white'
            self.plot_bg = '#fafafa'
            self.text_color = '#374151'
            self.text_secondary = '#6b7280'
            self.grid_color = '#e5e7eb'
            self.template = 'plotly_white'
        
        # Professional chart layout
        self.layout_template = {
            'font': {
                'family': 'Inter, sans-serif',
                'size': 12,
                'color': self.text_color
            },
            'paper_bgcolor': self.bg_color,
            'plot_bgcolor': self.plot_bg,
            'margin': {'l': 60, 'r': 40, 't': 80, 'b': 60},
            'hovermode': 'closest',
            'hoverlabel': {
                'bgcolor': self.bg_color,
                'bordercolor': self.grid_color,
                'font': {'family': 'Inter, sans-serif', 'size': 13, 'color': self.text_color}
            },
            'xaxis': {
                'gridcolor': self.grid_color,
                'linecolor': self.grid_color,
                'zerolinecolor': self.grid_color,
                'title': {'font': {'size': 13, 'color': self.text_secondary}},
                'tickfont': {'size': 11, 'color': self.text_secondary}
            },
            'yaxis': {
                'gridcolor': self.grid_color,
                'linecolor': self.grid_color,
                'zerolinecolor': self.grid_color,
                'title': {'font': {'size': 13, 'color': self.text_secondary}},
                'tickfont': {'size': 11, 'color': self.text_secondary}
            }
        }
    
    def create_segment_pie(self, df):
        """
        Create market segment distribution pie chart
        
        Args:
            df: DataFrame with 'segment' column
            
        Returns:
            plotly.graph_objects.Figure
        """
        try:
            segment_counts = df['segment'].value_counts()
            
            # Sort in strategic order
            segment_order = ['Stars', 'Cash Cows', 'Developing', 'Saturated']
            segment_counts = segment_counts.reindex(
                [s for s in segment_order if s in segment_counts.index]
            )
            
            colors = [self.colors[seg] for seg in segment_counts.index]
            
            fig = go.Figure(data=[go.Pie(
                labels=segment_counts.index,
                values=segment_counts.values,
                marker=dict(
                    colors=colors,
                    line=dict(color=self.bg_color, width=3)
                ),
                textinfo='label+percent',
                textfont=dict(size=13, color='white'),
                hovertemplate='<b>%{label}</b><br>Regions: %{value}<br>Share: %{percent}<extra></extra>',
                hole=0.4
            )])
            
            # Center annotation
            fig.add_annotation(
                text=f"<b>{len(df)}</b><br><span style='font-size:11px'>regions</span>",
                x=0.5, y=0.5,
                font=dict(size=20, family='JetBrains Mono', color=self.text_color),
                showarrow=False
            )
            
            fig.update_layout(
                showlegend=True,
                legend=dict(
                    orientation='h',
                    yanchor='bottom',
                    y=-0.15,
                    xanchor='center',
                    x=0.5
                ),
                height=450,
                **self.layout_template
            )
            
            return fig
        
        except Exception as e:
            print(f"Error in create_segment_pie: {e}")
            return go.Figure().add_annotation(text=f"Error: {e}", showarrow=False)
    
    def create_quadrant_plot(self, df):
        """
        Create scatter plot with quadrant divisions
        
        Args:
            df: DataFrame with 'tfr', 'expenditure', 'segment', 'region'
            
        Returns:
            plotly.graph_objects.Figure
        """
        try:
            fig = go.Figure()
            
            # Calculate medians
            tfr_median = df['tfr'].median()
            exp_median = df['expenditure'].median()
            
            # Plot each segment
            for segment in df['segment'].unique():
                segment_data = df[df['segment'] == segment]
                
                fig.add_trace(go.Scatter(
                    x=segment_data['tfr'],
                    y=segment_data['expenditure'],
                    mode='markers',
                    name=segment,
                    marker=dict(
                        size=10,
                        color=self.colors[segment],
                        opacity=0.7,
                        line=dict(width=1, color=self.bg_color)
                    ),
                    text=segment_data['region'],
                    hovertemplate='<b>%{text}</b><br>TFR: %{x:.2f}<br>Expenditure: Rp %{y:,.0f}k<extra></extra>'
                ))
            
            # Quadrant lines
            fig.add_hline(y=exp_median, line_dash="dash", line_color=self.text_secondary, line_width=2, opacity=0.6)
            fig.add_vline(x=tfr_median, line_dash="dash", line_color=self.text_secondary, line_width=2, opacity=0.6)
            
            # Quadrant labels
            annotations = [
                dict(x=tfr_median * 1.3, y=exp_median * 1.15, text="Stars", showarrow=False,
                     font=dict(size=14, color=self.colors['Stars']), opacity=0.3),
                dict(x=tfr_median * 0.7, y=exp_median * 1.15, text="Cash Cows", showarrow=False,
                     font=dict(size=14, color=self.colors['Cash Cows']), opacity=0.3),
                dict(x=tfr_median * 1.3, y=exp_median * 0.85, text="Developing", showarrow=False,
                     font=dict(size=14, color=self.colors['Developing']), opacity=0.3),
                dict(x=tfr_median * 0.7, y=exp_median * 0.85, text="Saturated", showarrow=False,
                     font=dict(size=14, color=self.colors['Saturated']), opacity=0.3)
            ]
            
            fig.update_layout(
                xaxis_title="Total Fertility Rate",
                yaxis_title="Per Capita Expenditure (Rp 000s)",
                annotations=annotations,
                legend=dict(orientation='h', yanchor='bottom', y=-0.2, xanchor='center', x=0.5),
                height=600,
                **self.layout_template
            )
            
            return fig
        
        except Exception as e:
            print(f"Error in create_quadrant_plot: {e}")
            return go.Figure().add_annotation(text=f"Error: {e}", showarrow=False)
    
    def create_forecast_chart(self, df):
        """
        Create time series forecast chart
        
        Args:
            df: DataFrame with 'year', 'expenditure', 'type', 'lower_ci', 'upper_ci'
            
        Returns:
            plotly.graph_objects.Figure
        """
        try:
            fig = go.Figure()
            
            # Historical data
            hist_data = df[df['type'] == 'historical']
            
            fig.add_trace(go.Scatter(
                x=hist_data['year'],
                y=hist_data['expenditure'],
                mode='lines+markers',
                name='Historical',
                line=dict(color=self.colors['historical'], width=3),
                marker=dict(size=6),
                hovertemplate='<b>Year: %{x}</b><br>Expenditure: Rp %{y:,.0f}k<extra></extra>'
            ))
            
            # Forecast data
            forecast_data = df[df['type'] == 'forecast']
            
            if not forecast_data.empty:
                fig.add_trace(go.Scatter(
                    x=forecast_data['year'],
                    y=forecast_data['expenditure'],
                    mode='lines+markers',
                    name='Forecast',
                    line=dict(color=self.colors['forecast'], width=3, dash='dash'),
                    marker=dict(size=6),
                    hovertemplate='<b>Year: %{x}</b><br>Forecast: Rp %{y:,.0f}k<extra></extra>'
                ))
                
                # Confidence interval
                if 'lower_ci' in forecast_data.columns and 'upper_ci' in forecast_data.columns:
                    fig.add_trace(go.Scatter(
                        x=list(forecast_data['year']) + list(forecast_data['year'])[::-1],
                        y=list(forecast_data['upper_ci']) + list(forecast_data['lower_ci'])[::-1],
                        fill='toself',
                        fillcolor=self.colors['ci'],
                        line=dict(color='rgba(255,255,255,0)'),
                        name='95% Confidence',
                        hoverinfo='skip',
                        showlegend=True
                    ))
            
            fig.update_layout(
                xaxis_title="Year",
                yaxis_title="Per Capita Expenditure (Rp 000s)",
                legend=dict(orientation='h', yanchor='bottom', y=-0.25, xanchor='center', x=0.5),
                height=500,
                **self.layout_template
            )
            
            # Current year line
            fig.add_vline(x=2025, line_dash="dot", line_color=self.text_secondary, line_width=1, opacity=0.5)
            fig.add_annotation(x=2025, y=df['expenditure'].max(), text="Current",
                             showarrow=False, yshift=10, font=dict(size=10, color=self.text_secondary))
            
            return fig
        
        except Exception as e:
            print(f"Error in create_forecast_chart: {e}")
            return go.Figure().add_annotation(text=f"Error: {e}", showarrow=False)
    
    def create_regional_forecast_chart(self, df):
        """
        Create multi-region forecast comparison
        
        Args:
            df: DataFrame with 'region', 'year', 'expenditure'
            
        Returns:
            plotly.graph_objects.Figure
        """
        try:
            fig = go.Figure()
            
            region_colors = px.colors.qualitative.Set2
            
            for idx, region in enumerate(df['region'].unique()):
                region_data = df[df['region'] == region]
                
                fig.add_trace(go.Scatter(
                    x=region_data['year'],
                    y=region_data['expenditure'],
                    mode='lines+markers',
                    name=region,
                    line=dict(width=2.5),
                    marker=dict(size=5),
                    hovertemplate='<b>%{fullData.name}</b><br>Year: %{x}<br>Rp %{y:,.0f}k<extra></extra>'
                ))
            
            fig.update_layout(
                xaxis_title="Year",
                yaxis_title="Per Capita Expenditure (Rp 000s)",
                legend=dict(orientation='v', yanchor='top', y=1, xanchor='left', x=1.02),
                height=500,
                **self.layout_template
            )
            
            return fig
        
        except Exception as e:
            print(f"Error in create_regional_forecast_chart: {e}")
            return go.Figure().add_annotation(text=f"Error: {e}", showarrow=False)