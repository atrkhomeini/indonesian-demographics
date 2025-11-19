"""
ARIMA Time Series Forecasting Module
"""
import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller
import itertools
from typing import Tuple, Dict, List
import warnings

warnings.filterwarnings('ignore')


class ARIMAForecaster:
    """ARIMA model for time series forecasting"""
    
    def __init__(self, config: Dict):
        """
        Initialize ARIMA forecaster
        
        Args:
            config: ARIMA configuration dictionary
        """
        self.max_p = config.get('max_p', 3)
        self.max_d = config.get('max_d', 2)
        self.max_q = config.get('max_q', 3)
        self.ic = config.get('information_criterion', 'aic')
        
        self.best_model = None
        self.best_order = None
        self.best_ic = None
    
    def test_stationarity(self, timeseries: np.ndarray) -> Tuple[bool, Dict]:
        """
        Test stationarity using Augmented Dickey-Fuller test
        
        Args:
            timeseries: Time series data
            
        Returns:
            Tuple of (is_stationary, test_results)
        """
        result = adfuller(timeseries, autolag='AIC')
        
        is_stationary = result[1] <= 0.05
        
        test_results = {
            'adf_statistic': result[0],
            'p_value': result[1],
            'critical_values': result[4],
            'is_stationary': is_stationary
        }
        
        return is_stationary, test_results
    
    def grid_search(self, timeseries: np.ndarray, verbose: bool = True) -> pd.DataFrame:
        """
        Grid search for optimal ARIMA parameters
        
        Args:
            timeseries: Time series data
            verbose: Print progress
            
        Returns:
            DataFrame with search results
        """
        results = []
        best_ic = np.inf
        
        p_range = range(0, self.max_p + 1)
        d_range = range(0, self.max_d + 1)
        q_range = range(0, self.max_q + 1)
        
        total_combinations = (self.max_p + 1) * (self.max_d + 1) * (self.max_q + 1)
        
        if verbose:
            print(f"Testing {total_combinations} ARIMA parameter combinations...")
        
        for idx, (p, d, q) in enumerate(itertools.product(p_range, d_range, q_range)):
            try:
                model = ARIMA(timeseries, order=(p, d, q))
                fitted_model = model.fit()
                
                ic_value = fitted_model.aic if self.ic == 'aic' else fitted_model.bic
                
                results.append({
                    'p': p,
                    'd': d,
                    'q': q,
                    'order': f"({p},{d},{q})",
                    'AIC': fitted_model.aic,
                    'BIC': fitted_model.bic,
                    'IC': ic_value
                })
                
                if ic_value < best_ic:
                    best_ic = ic_value
                    self.best_order = (p, d, q)
                    self.best_model = fitted_model
                    self.best_ic = ic_value
                
            except Exception as e:
                continue
        
        results_df = pd.DataFrame(results).sort_values('IC')
        
        if verbose and self.best_order:
            print(f"\nBest model: ARIMA{self.best_order}")
            print(f"Best {self.ic.upper()}: {self.best_ic:.2f}")
        
        return results_df
    
    def fit(self, timeseries: np.ndarray, order: Tuple[int, int, int] = None):
        """
        Fit ARIMA model with specified or best order
        
        Args:
            timeseries: Time series data
            order: ARIMA order (p, d, q). If None, use best from grid search
        """
        if order is None:
            if self.best_order is None:
                self.grid_search(timeseries, verbose=False)
            order = self.best_order
        
        model = ARIMA(timeseries, order=order)
        self.best_model = model.fit()
        self.best_order = order
        
        return self.best_model
    
    def forecast(self, steps: int) -> Tuple[np.ndarray, pd.DataFrame]:
        """
        Generate forecast
        
        Args:
            steps: Number of steps to forecast
            
        Returns:
            Tuple of (forecast_mean, confidence_intervals)
        """
        if self.best_model is None:
            raise ValueError("Model not fitted. Call fit() first.")
        
        forecast_result = self.best_model.get_forecast(steps=steps)
        forecast_mean = forecast_result.predicted_mean
        forecast_ci = forecast_result.conf_int()
        
        # Convert to DataFrame if it's a numpy array
        if isinstance(forecast_ci, np.ndarray):
            forecast_ci = pd.DataFrame(
                forecast_ci,
                columns=['lower', 'upper']
            )
        
        return forecast_mean, forecast_ci
    
    def get_metrics(self, actual: np.ndarray, fitted: np.ndarray = None) -> Dict:
        """
        Calculate performance metrics
        
        Args:
            actual: Actual values
            fitted: Fitted values. If None, use model's fitted values
            
        Returns:
            Dictionary of metrics
        """
        if fitted is None:
            fitted = self.best_model.fittedvalues
        
        mse = np.mean((actual - fitted) ** 2)
        rmse = np.sqrt(mse)
        mae = np.mean(np.abs(actual - fitted))
        mape = np.mean(np.abs((actual - fitted) / actual)) * 100
        
        return {
            'MSE': mse,
            'RMSE': rmse,
            'MAE': mae,
            'MAPE': mape
        }
    
    def get_model_summary(self) -> Dict:
        """Get model summary information"""
        if self.best_model is None:
            return {}
        
        return {
            'order': self.best_order,
            'aic': self.best_model.aic,
            'bic': self.best_model.bic,
            'p': self.best_order[0],
            'd': self.best_order[1],
            'q': self.best_order[2]
        }


def prepare_time_series(df: pd.DataFrame, 
                       value_col: str,
                       time_col: str = 'year',
                       group_col: str = None,
                       agg_func: str = 'mean') -> pd.DataFrame:
    """
    Prepare time series data for forecasting
    
    Args:
        df: Input dataframe
        value_col: Column containing values to forecast
        time_col: Column containing time information
        group_col: Optional grouping column
        agg_func: Aggregation function if grouping
        
    Returns:
        Prepared time series dataframe
    """
    if group_col:
        ts_df = df.groupby([time_col, group_col])[value_col].agg(agg_func).reset_index()
    else:
        ts_df = df.groupby(time_col)[value_col].agg(agg_func).reset_index()
    
    ts_df = ts_df.sort_values(time_col)
    return ts_df


def forecast_region(df: pd.DataFrame,
                   region_name: str,
                   value_col: str,
                   forecaster: ARIMAForecaster,
                   forecast_steps: int,
                   time_col: str = 'year') -> pd.DataFrame:
    """
    Forecast for a specific region
    
    Args:
        df: Input dataframe
        region_name: Region to forecast
        value_col: Column to forecast
        forecaster: ARIMAForecaster instance
        forecast_steps: Number of steps to forecast
        time_col: Time column name
        
    Returns:
        Forecast dataframe
    """
    region_data = df[df['region_name'] == region_name].sort_values(time_col)
    
    if len(region_data) < 5:
        return None
    
    try:
        # Fit model
        forecaster.fit(region_data[value_col].values)
        
        # Generate forecast
        forecast_mean, forecast_ci = forecaster.forecast(forecast_steps)
        
        # Create forecast dataframe
        last_year = region_data[time_col].max()
        forecast_years = np.arange(last_year + 1, last_year + forecast_steps + 1)
        
        # Handle confidence interval columns
        if isinstance(forecast_ci, pd.DataFrame):
            lower_ci = forecast_ci.iloc[:, 0].values
            upper_ci = forecast_ci.iloc[:, 1].values
        else:
            lower_ci = forecast_ci[:, 0]
            upper_ci = forecast_ci[:, 1]
        
        forecast_df = pd.DataFrame({
            'region_name': region_name,
            time_col: forecast_years,
            'forecast': forecast_mean.values if hasattr(forecast_mean, 'values') else forecast_mean,
            'lower_ci': lower_ci,
            'upper_ci': upper_ci
        })
        
        return forecast_df
        
    except Exception as e:
        print(f"Error forecasting {region_name}: {str(e)}")
        return None