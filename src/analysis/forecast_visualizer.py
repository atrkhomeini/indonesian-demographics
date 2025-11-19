"""
Visualization module for time series forecasting
"""
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Optional, List

plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette('husl')


class ForecastVisualizer:
    """Visualize forecasting results"""
    
    def __init__(self, output_dir: str = 'reports/figures', dpi: int = 300):
        """
        Initialize visualizer
        
        Args:
            output_dir: Directory to save figures
            dpi: DPI for saved figures
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.dpi = dpi
    
    def plot_time_series(self,
                        df: pd.DataFrame,
                        time_col: str,
                        value_col: str,
                        title: str,
                        ylabel: str,
                        save_name: Optional[str] = None):
        """
        Plot time series data
        
        Args:
            df: Dataframe with time series
            time_col: Time column name
            value_col: Value column name
            title: Plot title
            ylabel: Y-axis label
            save_name: Filename to save (without extension)
        """
        fig, ax = plt.subplots(figsize=(14, 6))
        
        ax.plot(df[time_col], df[value_col],
                marker='o', linewidth=2, markersize=8,
                color='darkblue', label='Observed')
        
        ax.set_xlabel('Year', fontsize=12, fontweight='bold')
        ax.set_ylabel(ylabel, fontsize=12, fontweight='bold')
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.legend(fontsize=10)
        
        plt.tight_layout()
        
        if save_name:
            plt.savefig(self.output_dir / f"{save_name}.png",
                       dpi=self.dpi, bbox_inches='tight')
        
        plt.show()
    
    def plot_forecast(self,
                     historical_df: pd.DataFrame,
                     forecast_df: pd.DataFrame,
                     time_col: str,
                     value_col: str,
                     forecast_col: str,
                     title: str,
                     ylabel: str,
                     model_name: str = 'ARIMA',
                     save_name: Optional[str] = None):
        """
        Plot historical data with forecast
        
        Args:
            historical_df: Historical data
            forecast_df: Forecast data with confidence intervals
            time_col: Time column name
            value_col: Value column in historical data
            forecast_col: Forecast column in forecast data
            title: Plot title
            ylabel: Y-axis label
            model_name: Model name for title
            save_name: Filename to save
        """
        fig, ax = plt.subplots(figsize=(16, 7))
        
        # Historical data
        ax.plot(historical_df[time_col], historical_df[value_col],
                marker='o', linewidth=2, markersize=8,
                color='darkblue', label='Historical')
        
        # Forecast
        ax.plot(forecast_df[time_col], forecast_df[forecast_col],
                marker='s', linewidth=2, markersize=8,
                color='darkred', linestyle='--', label='Forecast')
        
        # Confidence interval
        if 'lower_ci' in forecast_df.columns and 'upper_ci' in forecast_df.columns:
            ax.fill_between(forecast_df[time_col],
                           forecast_df['lower_ci'],
                           forecast_df['upper_ci'],
                           alpha=0.3, color='red',
                           label='95% Confidence Interval')
        
        # Separator line
        last_historical_year = historical_df[time_col].max()
        ax.axvline(x=last_historical_year, color='gray',
                  linestyle=':', linewidth=2, alpha=0.7)
        
        ax.set_xlabel('Year', fontsize=13, fontweight='bold')
        ax.set_ylabel(ylabel, fontsize=13, fontweight='bold')
        ax.set_title(f'{title} - {model_name}', fontsize=15, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.legend(fontsize=11, loc='upper left')
        
        plt.tight_layout()
        
        if save_name:
            plt.savefig(self.output_dir / f"{save_name}.png",
                       dpi=self.dpi, bbox_inches='tight')
        
        plt.show()
    
    def plot_regional_forecasts(self,
                               historical_df: pd.DataFrame,
                               forecast_df: pd.DataFrame,
                               regions: List[str],
                               time_col: str,
                               value_col: str,
                               title: str,
                               ylabel: str,
                               save_name: Optional[str] = None):
        """
        Plot multiple regional forecasts
        
        Args:
            historical_df: Historical data for all regions
            forecast_df: Forecast data for all regions
            regions: List of regions to plot
            time_col: Time column name
            value_col: Value column name
            title: Plot title
            ylabel: Y-axis label
            save_name: Filename to save
        """
        fig, ax = plt.subplots(figsize=(16, 8))
        
        colors = plt.cm.tab10(np.linspace(0, 1, len(regions)))
        
        for region, color in zip(regions, colors):
            # Historical
            hist = historical_df[historical_df['region_name'] == region]
            ax.plot(hist[time_col], hist[value_col],
                   marker='o', linewidth=2, color=color,
                   label=f'{region} (Historical)')
            
            # Forecast
            fcst = forecast_df[forecast_df['region_name'] == region]
            if not fcst.empty:
                ax.plot(fcst[time_col], fcst['forecast'],
                       marker='s', linewidth=2, linestyle='--',
                       color=color, alpha=0.7)
        
        ax.set_xlabel('Year', fontsize=13, fontweight='bold')
        ax.set_ylabel(ylabel, fontsize=13, fontweight='bold')
        ax.set_title(title, fontsize=15, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.legend(fontsize=9, loc='best', ncol=2)
        
        plt.tight_layout()
        
        if save_name:
            plt.savefig(self.output_dir / f"{save_name}.png",
                       dpi=self.dpi, bbox_inches='tight')
        
        plt.show()
    
    def plot_model_diagnostics(self,
                              model,
                              save_name: Optional[str] = None):
        """
        Plot ARIMA model diagnostics
        
        Args:
            model: Fitted ARIMA model
            save_name: Filename to save
        """
        fig = model.plot_diagnostics(figsize=(16, 12))
        plt.suptitle('ARIMA Model Diagnostics',
                    fontsize=16, fontweight='bold', y=1.00)
        plt.tight_layout()
        
        if save_name:
            plt.savefig(self.output_dir / f"{save_name}.png",
                       dpi=self.dpi, bbox_inches='tight')
        
        plt.show()
    
    def plot_metrics_comparison(self,
                               metrics_df: pd.DataFrame,
                               title: str = 'Model Performance Metrics',
                               save_name: Optional[str] = None):
        """
        Plot model performance metrics
        
        Args:
            metrics_df: Dataframe with metrics
            title: Plot title
            save_name: Filename to save
        """
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        axes = axes.flatten()
        
        metrics = ['RMSE', 'MAE', 'MAPE', 'AIC']
        
        for idx, metric in enumerate(metrics):
            if metric in metrics_df.columns:
                ax = axes[idx]
                
                if 'region_name' in metrics_df.columns:
                    data = metrics_df.nsmallest(10, metric)
                    ax.barh(data['region_name'], data[metric])
                    ax.set_xlabel(metric, fontweight='bold')
                    ax.set_ylabel('Region', fontweight='bold')
                else:
                    ax.bar(['Model'], [metrics_df[metric].iloc[0]])
                    ax.set_ylabel(metric, fontweight='bold')
                
                ax.set_title(f'{metric} Comparison', fontweight='bold')
                ax.grid(True, alpha=0.3)
        
        plt.suptitle(title, fontsize=16, fontweight='bold')
        plt.tight_layout()
        
        if save_name:
            plt.savefig(self.output_dir / f"{save_name}.png",
                       dpi=self.dpi, bbox_inches='tight')
        
        plt.show()
