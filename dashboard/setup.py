#!/usr/bin/env python3
"""
Dashboard Setup Script
Prepares data for dashboard deployment
"""

import shutil
from pathlib import Path
import sys


def setup_dashboard_data():
    """Copy required data files to dashboard directory"""
    
    print("="*60)
    print("DASHBOARD DATA SETUP")
    print("="*60)
    
    # Paths
    project_root = Path(__file__).parents[2]  # Go up from master/dashboard/
    dashboard_root = Path(__file__).parent
    
    source_processed = project_root / 'data' / 'processed'
    source_interim = project_root / 'data' / 'interim'
    
    dest_processed = dashboard_root / 'data' / 'processed'
    dest_interim = dashboard_root / 'data' / 'interim'
    
    # Create destination directories
    dest_processed.mkdir(parents=True, exist_ok=True)
    dest_interim.mkdir(parents=True, exist_ok=True)
    
    print("\n📁 Copying processed data...")
    
    # Copy processed data files
    processed_files = [
        'national_expenditure_forecast.csv',
        'regional_expenditure_forecasts.csv',
        'market_segmentation.csv',
        'segment_statistics.csv'
    ]
    
    for filename in processed_files:
        source = source_processed / filename
        dest = dest_processed / filename
        
        if source.exists():
            shutil.copy2(source, dest)
            print(f"   ✓ {filename}")
        else:
            print(f"   ⚠️  {filename} not found")
    
    print("\n📁 Copying interim data...")
    
    # Copy interim data files
    interim_files = [
        'expenditure_clean.csv',
        'tfr_clean.csv',
        'asfr_clean.csv',
        'region_master.csv'
    ]
    
    for filename in interim_files:
        source = source_interim / filename
        dest = dest_interim / filename
        
        if source.exists():
            shutil.copy2(source, dest)
            print(f"   ✓ {filename}")
        else:
            print(f"   ⚠️  {filename} not found (optional)")
    
    # Check data size
    total_size = sum(f.stat().st_size for f in dest_processed.glob('*'))
    total_size += sum(f.stat().st_size for f in dest_interim.glob('*'))
    total_size_mb = total_size / (1024 * 1024)
    
    print(f"\n📊 Data Statistics:")
    print(f"   Processed files: {len(list(dest_processed.glob('*.csv')))}")
    print(f"   Interim files: {len(list(dest_interim.glob('*.csv')))}")
    print(f"   Total size: {total_size_mb:.2f} MB")
    
    if total_size_mb > 50:
        print("\n   ⚠️  WARNING: Data size > 50MB may cause issues with Hugging Face Spaces")
        print("   Consider uploading to external storage (S3, GCS) and loading dynamically")
    
    print("\n" + "="*60)
    print("✅ DASHBOARD DATA SETUP COMPLETE")
    print("="*60)
    print("\nNext steps:")
    print("1. Test locally: streamlit run app.py")
    print("2. Deploy to Hugging Face Spaces")
    print("3. Or build Docker image: docker build -t dashboard .")


def verify_dashboard():
    """Verify dashboard can run"""
    print("\n🔍 Verifying dashboard setup...")
    
    dashboard_root = Path(__file__).parent
    
    # Check required files
    required_files = [
        'app.py',
        'requirements.txt',
        'src/data_loader.py',
        'src/visualizations.py',
        '.streamlit/config.toml'
    ]
    
    missing = []
    for file_path in required_files:
        if not (dashboard_root / file_path).exists():
            missing.append(file_path)
    
    if missing:
        print("   ❌ Missing files:")
        for file in missing:
            print(f"      - {file}")
        return False
    else:
        print("   ✓ All required files present")
    
    # Check data
    data_dir = dashboard_root / 'data' / 'processed'
    if not data_dir.exists() or len(list(data_dir.glob('*.csv'))) == 0:
        print("   ⚠️  No data files found - dashboard will use sample data")
    else:
        print(f"   ✓ Data files found: {len(list(data_dir.glob('*.csv')))}")
    
    print("\n   ✅ Dashboard ready to run!")
    return True


if __name__ == '__main__':
    try:
        setup_dashboard_data()
        verify_dashboard()
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Setup failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)