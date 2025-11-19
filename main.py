"""
Indonesia Demographics Market Intelligence
Main Pipeline: Phase 3 (Data Engineering) + Phase 4 (Analysis)

Usage:
    python main.py                  # Run complete pipeline
    python main.py --skip-phase3    # Skip data engineering, run analysis only
    python main.py --skip-phase4    # Run data engineering only
"""

import sys
import argparse
from pathlib import Path
from datetime import datetime

# Add src to path
project_root = Path(__file__).resolve().parent
sys.path.insert(0, str(project_root))


def print_header(text, char="="):
    """Print formatted section header"""
    width = 80
    print("\n" + char * width)
    padding = (width - len(text) - 2) // 2
    print(char + " " * padding + text + " " * (width - len(text) - padding - 2) + char)
    print(char * width)


def print_phase_header(phase_num, phase_name):
    """Print phase header with emoji"""
    print("\n" + "=" * 80)
    print(f"{'🔧' if phase_num == 3 else '📊'} PHASE {phase_num}: {phase_name}")
    print("=" * 80)


def run_phase3():
    """
    Phase 3: Data Engineering Pipeline
    - Organize raw data
    - Clean datasets
    - Setup PostgreSQL database
    - Load data to database
    """
    print_phase_header(3, "DATA ENGINEERING")
    
    try:
        # Step 1: Organize raw data
        print("\n[Step 1/4] Organizing raw data...")
        from src.data.make_dataset import DatasetMaker
        maker = DatasetMaker()
        maker.prepare_all()
        print("✓ Raw data organized")
        
        # Step 2: Clean data
        print("\n[Step 2/4] Cleaning datasets...")
        from src.data.clean_data import DataCleaner
        cleaner = DataCleaner()
        cleaned_data = cleaner.clean_all()
        print("✓ Data cleaned")
        
        # Step 3: Setup database
        print("\n[Step 3/4] Setting up PostgreSQL database...")
        from src.database.setup_db import setup
        if not setup():
            raise Exception("Database setup failed")
        print("✓ Database ready")
        
        # Step 4: Load data
        print("\n[Step 4/4] Loading data to database...")
        from src.database.load_data import load_to_database
        if not load_to_database():
            raise Exception("Data loading failed")
        print("✓ Data loaded to PostgreSQL")
        
        print_header("✅ PHASE 3 COMPLETE", "=")
        return True
        
    except Exception as e:
        print(f"\n❌ Phase 3 failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def run_phase4():
    """
    Phase 4: Data Science & Analysis Pipeline
    - Time series forecasting (ARIMA)
    - Quadrant analysis (market segmentation)
    - Generate visualizations and reports
    """
    print_phase_header(4, "DATA SCIENCE & ANALYSIS")
    
    try:
        # Import analysis modules
        from src.analysis.config_loader import Config
        from src.analysis.forecast_visualizer import ForecastVisualizer
        from src.analysis.forecast_expenditure import (
            load_data,
            forecast_national_expenditure,
            forecast_regional_expenditure,
            save_results,
            print_summary
        )
        from src.analysis.quadrant_analysis import run_quadrant_analysis
        
        # Load configuration
        print("\n[Setup] Loading configuration...")
        config = Config('src/models/config.yml')
        print(f"✓ Config loaded from: {config.config_path}")
        
        # Initialize visualizer
        output_config = config.outputs
        visualizer = ForecastVisualizer(
            output_dir='reports/figures',
            dpi=output_config.get('plot_dpi', 300)
        )
        print("✓ Visualizer initialized")
        
        # Load data from interim
        print("\n[Setup] Loading processed data...")
        expenditure_df, tfr_df, region_master = load_data()
        print("✓ Data loaded successfully")
        
        # Part 1: Time Series Forecasting
        print("\n" + "-" * 80)
        print("PART 1: TIME SERIES FORECASTING")
        print("-" * 80)
        
        print("\n[1.1] Forecasting national expenditure...")
        national_ts, national_forecast, forecaster, metrics = forecast_national_expenditure(
            expenditure_df, config, visualizer
        )
        print("✓ National forecast complete")
        
        print("\n[1.2] Forecasting regional expenditure...")
        regional_forecasts = forecast_regional_expenditure(
            expenditure_df, config, visualizer, forecaster
        )
        print("✓ Regional forecasts complete")
        
        # Save forecasting results
        if output_config.get('save_forecasts', True):
            print("\n[1.3] Saving forecast results...")
            save_results(
                national_ts,
                national_forecast,
                regional_forecasts,
                metrics,
                forecaster.get_model_summary(),
                config
            )
            print("✓ Forecast results saved")
        
        # Print forecast summary
        print_summary(
            national_ts,
            national_forecast,
            metrics,
            forecaster.get_model_summary(),
            config
        )
        
        # Part 2: Quadrant Analysis
        print("\n" + "-" * 80)
        print("PART 2: MARKET SEGMENTATION (QUADRANT ANALYSIS)")
        print("-" * 80)
        
        quadrant_config = config.quadrant
        segmented_df = run_quadrant_analysis(
            tfr_df,
            expenditure_df,
            quadrant_config,
            output_dir='reports/figures'
        )
        print("✓ Quadrant analysis complete")
        
        print_header("✅ PHASE 4 COMPLETE", "=")
        return True
        
    except Exception as e:
        print(f"\n❌ Phase 4 failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def print_final_summary(phase3_success, phase4_success, start_time):
    """Print final pipeline summary"""
    end_time = datetime.now()
    duration = end_time - start_time
    
    print("\n" + "#" * 80)
    print("#" + " " * 78 + "#")
    print("#" + " " * 25 + "PIPELINE SUMMARY" + " " * 37 + "#")
    print("#" + " " * 78 + "#")
    print("#" * 80)
    
    print(f"\n{'Phase 3 (Data Engineering):':30} {'✅ PASS' if phase3_success else '❌ FAIL'}")
    print(f"{'Phase 4 (Data Science):':30} {'✅ PASS' if phase4_success else '❌ FAIL'}")
    print(f"\n{'Total Duration:':30} {duration}")
    print(f"{'Completed At:':30} {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    if phase3_success and phase4_success:
        print("\n" + "=" * 80)
        print("📁 GENERATED OUTPUTS:")
        print("=" * 80)
        
        print("\n🗄️  Database:")
        print("   • PostgreSQL: indonesia_demographics")
        print("   • Tables: regions, tfr, asfr, expenditure, market_analysis")
        
        print("\n📊 Forecasts:")
        print("   • data/processed/national_expenditure_forecast.csv")
        print("   • data/processed/regional_expenditure_forecasts.csv")
        print("   • models/expenditure_arima_model_info.csv")
        
        print("\n🎯 Market Segmentation:")
        print("   • data/processed/market_segmentation.csv")
        print("   • data/processed/segment_statistics.csv")
        
        print("\n📈 Visualizations:")
        print("   • reports/figures/expenditure_historical_trend.png")
        print("   • reports/figures/expenditure_model_diagnostics.png")
        print("   • reports/figures/expenditure_forecast.png")
        print("   • reports/figures/regional_expenditure_forecasts.png")
        print("   • reports/figures/quadrant_analysis.png")
        print("   • reports/figures/segment_distribution.png")
    
    print("\n" + "#" * 80)
    print("#" + " " * 78 + "#")
    
    if phase3_success and phase4_success:
        print("#" + " " * 20 + "🎉 ALL PIPELINES COMPLETED SUCCESSFULLY 🎉" + " " * 16 + "#")
    else:
        print("#" + " " * 25 + "⚠️  PIPELINE COMPLETED WITH ERRORS" + " " * 20 + "#")
    
    print("#" + " " * 78 + "#")
    print("#" * 80 + "\n")


def main():
    """Main execution function"""
    
    # Parse arguments
    parser = argparse.ArgumentParser(
        description='Indonesia Demographics Market Intelligence Pipeline'
    )
    parser.add_argument(
        '--skip-phase3',
        action='store_true',
        help='Skip Phase 3 (Data Engineering)'
    )
    parser.add_argument(
        '--skip-phase4',
        action='store_true',
        help='Skip Phase 4 (Data Science & Analysis)'
    )
    args = parser.parse_args()
    
    # Start timer
    start_time = datetime.now()
    
    # Print main header
    print_header("INDONESIA DEMOGRAPHICS - MARKET INTELLIGENCE", "=")
    print(f"\nStarted: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Project Root: {project_root}")
    
    # Initialize success flags
    phase3_success = True  # Default to True if skipped
    phase4_success = True  # Default to True if skipped
    
    # Run Phase 3
    if not args.skip_phase3:
        phase3_success = run_phase3()
        
        if not phase3_success:
            print("\n⚠️  Phase 3 failed. Stopping pipeline.")
            print("Fix the errors and run again, or use --skip-phase3 to skip data engineering.")
            sys.exit(1)
    else:
        print("\n⏭️  Skipping Phase 3 (Data Engineering)")
    
    # Run Phase 4
    if not args.skip_phase4:
        phase4_success = run_phase4()
        
        if not phase4_success:
            print("\n⚠️  Phase 4 failed.")
            sys.exit(1)
    else:
        print("\n⏭️  Skipping Phase 4 (Data Science & Analysis)")
    
    # Print final summary
    print_final_summary(phase3_success, phase4_success, start_time)
    
    # Exit with appropriate code
    sys.exit(0 if (phase3_success and phase4_success) else 1)


if __name__ == '__main__':
    main()