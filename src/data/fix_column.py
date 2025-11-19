"""
Quick Fix Script - Fixes Column Name Issue
Run this to fix the 'region' vs 'region_name' column problem
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

import pandas as pd
from src.database.config import DATA_INTERIM

def fix_column_names():
    """Fix column names in interim data files"""
    print("="*60)
    print("FIXING COLUMN NAMES")
    print("="*60)
    
    # Fix TFR
    print("\n📊 Fixing TFR file...")
    df = pd.read_csv(DATA_INTERIM / 'tfr_clean.csv')
    if 'region' in df.columns:
        df = df.rename(columns={'region': 'region_name'})
        df.to_csv(DATA_INTERIM / 'tfr_clean.csv', index=False)
        print("   ✓ Fixed: region → region_name")
    else:
        print("   ✓ Already correct")
    
    # Fix ASFR
    print("\n📊 Fixing ASFR file...")
    df = pd.read_csv(DATA_INTERIM / 'asfr_clean.csv')
    if 'region' in df.columns:
        df = df.rename(columns={'region': 'region_name'})
        df.to_csv(DATA_INTERIM / 'asfr_clean.csv', index=False)
        print("   ✓ Fixed: region → region_name")
    else:
        print("   ✓ Already correct")
    
    # Fix Expenditure
    print("\n📊 Fixing expenditure file...")
    df = pd.read_csv(DATA_INTERIM / 'expenditure_clean.csv')
    if 'region' in df.columns:
        df = df.rename(columns={'region': 'region_name'})
        df.to_csv(DATA_INTERIM / 'expenditure_clean.csv', index=False)
        print("   ✓ Fixed: region → region_name")
    else:
        print("   ✓ Already correct")
    
    print("\n" + "="*60)
    print("✅ COLUMN NAMES FIXED")
    print("="*60)
    print("\nNow run: python -m src.database.load_data")

if __name__ == '__main__':
    fix_column_names()