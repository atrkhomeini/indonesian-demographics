"""
Master script to run complete Phase 4 analysis
Run: python run_analysis.py
"""
import sys
from pathlib import Path

# Import analysis modules
from config_loader import Config
from forecast_expenditure import (
    load_data,
    forecast_national_expenditure,
    forecast_regional_expenditure,
    save_results,
    print_summary
)
from forecast_visualizer import ForecastVisualizer
from quadrant_analysis import run_quadrant_analysis


def main():
    """Run complete Phase 4 analysis pipeline"""
    
    print("\n" + "="*80)
    print(" "*15 + "INDONESIA DEMOGRAPHICS - PHASE 4 ANALYSIS")
    print(" "*10 + "Time Series Forecasting & Market Segmentation")
    print("="*80)
    
    # Load configuration
    try:
        config = Config('src/models/config.yml')
        print(f"\n✓ Configuration loaded: {config.config_path}")
    except Exception as e:
        print(f"\n✗ Error loading configuration: {e}")
        print("  Make sure config.yml exists at: src/models/config.yml")
        return
    
    # Initialize visualizer
    output_config = config.outputs
    visualizer = ForecastVisualizer(
        output_dir='reports/figures',
        dpi=output_config.get('plot_dpi', 300)
    )
    print("✓ Visualizer initialized")
    
    # Load data
    try:
        expenditure_df, tfr_df, region_master = load_data()
        print("✓ Data loaded successfully")
    except Exception as e:
        print(f"\n✗ Error loading data: {e}")
        print("  Make sure data files exist in: data/interim/")
        return
    
    # ===== PART 1: TIME SERIES FORECASTING =====
    print("\n" + "="*80)
    print(" "*25 + "PART 1: TIME SERIES FORECASTING")
    print("="*80)
    
    try:
        # National expenditure forecast
        national_ts, national_forecast, forecaster, metrics = forecast_national_expenditure(
            expenditure_df, config, visualizer
        )
        
        # Regional expenditure forecast
        regional_forecasts = forecast_regional_expenditure(
            expenditure_df, config, visualizer, forecaster
        )
        
        # Save forecasting results
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
        
        print("\n✓ Time series forecasting completed successfully")
        
    except Exception as e:
        print(f"\n✗ Error in time series forecasting: {e}")
        import traceback
        traceback.print_exc()
    
    # ===== PART 2: QUADRANT ANALYSIS =====
    print("\n" + "="*80)
    print(" "*25 + "PART 2: MARKET SEGMENTATION")
    print("="*80)
    
    try:
        quadrant_config = config.quadrant
        segmented_df = run_quadrant_analysis(
            tfr_df,
            expenditure_df,
            quadrant_config
        )
        
        print("\n✓ Quadrant analysis completed successfully")
        
    except Exception as e:
        print(f"\n✗ Error in quadrant analysis: {e}")
        import traceback
        traceback.print_exc()
    
    # ===== FINAL SUMMARY =====
    print("\n" + "="*80)
    print(" "*30 + "ANALYSIS COMPLETE")
    print("="*80)
    
    print("\nGenerated Outputs:")
    print("\n📊 Time Series Forecasting:")
    print("  • data/processed/national_expenditure_forecast.csv")
    print("  • data/processed/regional_expenditure_forecasts.csv")
    print("  • models/expenditure_arima_model_info.csv")
    print("  • reports/figures/expenditure_historical_trend.png")
    print("  • reports/figures/expenditure_model_diagnostics.png")
    print("  • reports/figures/expenditure_forecast.png")
    print("  • reports/figures/regional_expenditure_forecasts.png")
    
    print("\n🎯 Market Segmentation:")
    print("  • data/processed/market_segmentation.csv")
    print("  • data/processed/segment_statistics.csv")
    print("  • reports/figures/quadrant_analysis.png")
    print("  • reports/figures/segment_distribution.png")
    
    print("\n" + "="*80)
    print("All analyses completed successfully!")
    print("="*80 + "\n")


if __name__ == '__main__':
    main()
