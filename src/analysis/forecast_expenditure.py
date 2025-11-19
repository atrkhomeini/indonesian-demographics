"""
Main script for time series forecasting
Run: python forecast_expenditure.py
"""
import pandas as pd
import numpy as np
from pathlib import Path
import sys

# Import local modules
from .config_loader import Config
from .arima_forecaster import ARIMAForecaster, prepare_time_series, forecast_region
from .forecast_visualizer import ForecastVisualizer


def load_data(data_dir: str = 'data/interim'):
    """Load clean datasets"""
    data_dir = Path(data_dir)
    
    print("Loading datasets...")
    expenditure_df = pd.read_csv(data_dir / 'expenditure_clean.csv')
    tfr_df = pd.read_csv(data_dir / 'tfr_clean.csv')
    region_master = pd.read_csv(data_dir / 'region_master.csv')
    
    print(f"✓ Expenditure: {expenditure_df.shape}")
    print(f"✓ TFR: {tfr_df.shape}")
    print(f"✓ Regions: {region_master.shape}")
    
    return expenditure_df, tfr_df, region_master


def forecast_national_expenditure(expenditure_df: pd.DataFrame,
                                  config: Config,
                                  visualizer: ForecastVisualizer):
    """
    Forecast national average expenditure
    
    Args:
        expenditure_df: Expenditure dataframe
        config: Configuration object
        visualizer: Visualizer object
        
    Returns:
        Tuple of (historical_df, forecast_df, forecaster, metrics)
    """
    print("\n" + "="*80)
    print("NATIONAL EXPENDITURE FORECASTING")
    print("="*80)
    
    # Prepare national time series
    national_ts = prepare_time_series(
        expenditure_df,
        value_col='expenditure',
        time_col='year',
        agg_func='mean'
    )
    
    print(f"\nHistorical period: {national_ts['year'].min()} - {national_ts['year'].max()}")
    print(f"Data points: {len(national_ts)}")
    
    # Visualize historical trend
    visualizer.plot_time_series(
        national_ts,
        time_col='year',
        value_col='expenditure',
        title='National Average Per Capita Expenditure Trend',
        ylabel='Per Capita Expenditure (Rp 000)',
        save_name='expenditure_historical_trend'
    )
    
    # Initialize forecaster
    forecaster = ARIMAForecaster(config.arima)
    
    # Test stationarity
    is_stationary, test_results = forecaster.test_stationarity(
        national_ts['expenditure'].values
    )
    
    print(f"\nStationarity Test (ADF):")
    print(f"  ADF Statistic: {test_results['adf_statistic']:.6f}")
    print(f"  p-value: {test_results['p_value']:.6f}")
    print(f"  Result: {'STATIONARY' if is_stationary else 'NON-STATIONARY'}")
    
    # Grid search for best parameters
    print(f"\nSearching for optimal ARIMA parameters...")
    results_df = forecaster.grid_search(national_ts['expenditure'].values)
    
    print(f"\nTop 5 models:")
    print(results_df.head().to_string(index=False))
    
    # Get model summary
    model_summary = forecaster.get_model_summary()
    print(f"\nSelected Model: ARIMA{model_summary['order']}")
    print(f"AIC: {model_summary['aic']:.2f}")
    print(f"BIC: {model_summary['bic']:.2f}")
    
    # Calculate metrics
    metrics = forecaster.get_metrics(national_ts['expenditure'].values)
    print(f"\nModel Performance:")
    print(f"  RMSE: Rp {metrics['RMSE']:,.2f}")
    print(f"  MAE:  Rp {metrics['MAE']:,.2f}")
    print(f"  MAPE: {metrics['MAPE']:.2f}%")
    
    # Plot diagnostics
    visualizer.plot_model_diagnostics(
        forecaster.best_model,
        save_name='expenditure_model_diagnostics'
    )
    
    # Generate forecast
    forecast_steps = config.get('forecasting.forecast_horizon_years', 5)
    forecast_mean, forecast_ci = forecaster.forecast(forecast_steps)
    
    last_year = national_ts['year'].max()
    forecast_years = np.arange(last_year + 1, last_year + forecast_steps + 1)
    
    # Handle confidence interval columns (may be named or indexed)
    if isinstance(forecast_ci, pd.DataFrame):
        lower_ci = forecast_ci.iloc[:, 0].values
        upper_ci = forecast_ci.iloc[:, 1].values
    else:
        lower_ci = forecast_ci[:, 0]
        upper_ci = forecast_ci[:, 1]
    
    forecast_df = pd.DataFrame({
        'year': forecast_years,
        'forecast': forecast_mean.values if hasattr(forecast_mean, 'values') else forecast_mean,
        'lower_ci': lower_ci,
        'upper_ci': upper_ci
    })
    
    print(f"\nForecast ({forecast_years[0]} - {forecast_years[-1]}):")
    print(forecast_df.to_string(index=False))
    
    # Visualize forecast
    visualizer.plot_forecast(
        national_ts,
        forecast_df,
        time_col='year',
        value_col='expenditure',
        forecast_col='forecast',
        title='Per Capita Expenditure Forecast',
        ylabel='Per Capita Expenditure (Rp 000)',
        model_name=f"ARIMA{model_summary['order']}",
        save_name='expenditure_forecast'
    )
    
    # Calculate growth rate
    forecast_last = forecast_mean[-1] if isinstance(forecast_mean, np.ndarray) else forecast_mean.iloc[-1]
    growth_rate = ((forecast_last / national_ts['expenditure'].iloc[-1]) - 1) * 100
    print(f"\nProjected growth: {growth_rate:.2f}% over {forecast_steps} years")
    
    return national_ts, forecast_df, forecaster, metrics


def forecast_regional_expenditure(expenditure_df: pd.DataFrame,
                                  config: Config,
                                  visualizer: ForecastVisualizer,
                                  national_forecaster: ARIMAForecaster):
    """
    Forecast expenditure for top regions
    
    Args:
        expenditure_df: Expenditure dataframe
        config: Configuration object
        visualizer: Visualizer object
        national_forecaster: Fitted national forecaster for parameter reference
        
    Returns:
        Regional forecasts dataframe
    """
    print("\n" + "="*80)
    print("REGIONAL EXPENDITURE FORECASTING")
    print("="*80)
    
    # Get top regions
    top_n = config.get('outputs.top_n_regions', 10)
    latest_year = expenditure_df['year'].max()
    top_regions = expenditure_df[expenditure_df['year'] == latest_year]\
                                .nlargest(top_n, 'expenditure')
    
    print(f"\nTop {top_n} regions by expenditure ({latest_year}):")
    print(top_regions[['region_name', 'expenditure']].to_string(index=False))
    
    # Forecast for each region
    forecast_steps = config.get('forecasting.forecast_horizon_years', 5)
    regional_forecasts = []
    
    print(f"\nForecasting {len(top_regions)} regions...")
    
    for idx, region in enumerate(top_regions['region_name'].values, 1):
        forecaster = ARIMAForecaster(config.arima)
        forecast_df = forecast_region(
            expenditure_df,
            region,
            'expenditure',
            forecaster,
            forecast_steps
        )
        
        if forecast_df is not None:
            regional_forecasts.append(forecast_df)
            print(f"  {idx}. {region} ✓")
        else:
            print(f"  {idx}. {region} ✗ (insufficient data)")
    
    if not regional_forecasts:
        print("No regional forecasts generated")
        return None
    
    regional_forecasts_df = pd.concat(regional_forecasts, ignore_index=True)
    
    # Visualize top 5 regional forecasts
    visualizer.plot_regional_forecasts(
        expenditure_df,
        regional_forecasts_df,
        regions=top_regions['region_name'].values[:5],
        time_col='year',
        value_col='expenditure',
        title='Regional Expenditure Forecasts - Top 5 Regions',
        ylabel='Per Capita Expenditure (Rp 000)',
        save_name='regional_expenditure_forecasts'
    )
    
    return regional_forecasts_df


def save_results(national_ts: pd.DataFrame,
                national_forecast: pd.DataFrame,
                regional_forecasts: pd.DataFrame,
                metrics: dict,
                model_summary: dict,
                config: Config):
    """Save all results to files"""
    
    output_dir = Path('data/processed')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    model_dir = Path('models')
    model_dir.mkdir(parents=True, exist_ok=True)
    
    print("\n" + "="*80)
    print("SAVING RESULTS")
    print("="*80)
    
    # Save national forecast
    national_full = pd.concat([
        national_ts.assign(type='historical', lower_ci=np.nan, upper_ci=np.nan),
        national_forecast.rename(columns={'forecast': 'expenditure'}).assign(type='forecast')
    ], ignore_index=True)
    
    national_full.to_csv(output_dir / 'national_expenditure_forecast.csv', index=False)
    print("✓ National forecast: data/processed/national_expenditure_forecast.csv")
    
    # Save regional forecasts
    if regional_forecasts is not None:
        regional_forecasts.to_csv(output_dir / 'regional_expenditure_forecasts.csv', index=False)
        print("✓ Regional forecasts: data/processed/regional_expenditure_forecasts.csv")
    
    # Save model info
    model_info = pd.DataFrame({
        'parameter': ['model_type', 'p', 'd', 'q', 'AIC', 'BIC', 'RMSE', 'MAE', 'MAPE'],
        'value': [
            'ARIMA',
            model_summary['p'],
            model_summary['d'],
            model_summary['q'],
            model_summary['aic'],
            model_summary['bic'],
            metrics['RMSE'],
            metrics['MAE'],
            metrics['MAPE']
        ]
    })
    
    model_info.to_csv(model_dir / 'expenditure_arima_model_info.csv', index=False)
    print("✓ Model info: models/expenditure_arima_model_info.csv")


def print_summary(national_ts: pd.DataFrame,
                 national_forecast: pd.DataFrame,
                 metrics: dict,
                 model_summary: dict,
                 config: Config):
    """Print analysis summary"""
    
    forecast_years = national_forecast['year'].values
    forecast_values = national_forecast['forecast'].values
    
    print("\n" + "#"*80)
    print("#" + " "*78 + "#")
    print("#" + " "*20 + "ARIMA FORECASTING ANALYSIS SUMMARY" + " "*24 + "#")
    print("#" + " "*78 + "#")
    print("#"*80)
    
    print(f"\n{'='*80}")
    print("DATA OVERVIEW")
    print(f"{'='*80}")
    print(f"Historical Period:           {national_ts['year'].min()} - {national_ts['year'].max()}")
    print(f"Number of Observations:      {len(national_ts)}")
    print(f"Forecast Horizon:            {len(forecast_years)} years ({forecast_years[0]}-{forecast_years[-1]})")
    
    print(f"\n{'='*80}")
    print("BEST MODEL SPECIFICATION")
    print(f"{'='*80}")
    print(f"Model:                       ARIMA{model_summary['order']}")
    print(f"  - p (AR order):            {model_summary['p']}")
    print(f"  - d (Differencing):        {model_summary['d']}")
    print(f"  - q (MA order):            {model_summary['q']}")
    print(f"AIC:                         {model_summary['aic']:.2f}")
    print(f"BIC:                         {model_summary['bic']:.2f}")
    
    print(f"\n{'='*80}")
    print("MODEL PERFORMANCE")
    print(f"{'='*80}")
    print(f"RMSE:                        Rp {metrics['RMSE']:,.2f}")
    print(f"MAE:                         Rp {metrics['MAE']:,.2f}")
    print(f"MAPE:                        {metrics['MAPE']:.2f}%")
    
    print(f"\n{'='*80}")
    print("FORECAST SUMMARY")
    print(f"{'='*80}")
    print(f"Last Historical Value:       Rp {national_ts['expenditure'].iloc[-1]:,.2f}")
    print(f"First Forecast ({forecast_years[0]}):      Rp {forecast_values[0]:,.2f}")
    print(f"Final Forecast ({forecast_years[-1]}):     Rp {forecast_values[-1]:,.2f}")
    
    growth = ((forecast_values[-1] / national_ts['expenditure'].iloc[-1]) - 1) * 100
    print(f"Projected Growth:            {growth:.2f}%")
    
    print(f"\n{'#'*80}")
    print("#" + " "*78 + "#")
    print("#" + " "*25 + "ANALYSIS COMPLETE" + " "*37 + "#")
    print("#" + " "*78 + "#")
    print("#"*80 + "\n")


def main():
    """Main execution function"""
    
    print("\n" + "="*80)
    print("INDONESIA DEMOGRAPHICS - TIME SERIES FORECASTING")
    print("ARIMA Model for Per Capita Expenditure")
    print("="*80)
    
    # Load configuration
    config = Config('src/models/config.yml')
    print(f"\n✓ Configuration loaded from: {config.config_path}")
    
    # Initialize visualizer
    output_config = config.outputs
    visualizer = ForecastVisualizer(
        output_dir='reports/figures',
        dpi=output_config.get('plot_dpi', 300)
    )
    
    # Load data
    expenditure_df, tfr_df, region_master = load_data()
    
    # Forecast national expenditure
    national_ts, national_forecast, forecaster, metrics = forecast_national_expenditure(
        expenditure_df, config, visualizer
    )
    
    # Forecast regional expenditure
    regional_forecasts = forecast_regional_expenditure(
        expenditure_df, config, visualizer, forecaster
    )
    
    # Save results
    if output_config.get('save_forecasts', True):
        save_results(
            national_ts,
            national_forecast,
            regional_forecasts,
            metrics,
            forecaster.get_model_summary(),
            config
        )
    
    # Print summary
    print_summary(
        national_ts,
        national_forecast,
        metrics,
        forecaster.get_model_summary(),
        config
    )


if __name__ == '__main__':
    main()