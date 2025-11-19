"""
Load data into PostgreSQL database
"""

import pandas as pd
from sqlalchemy import create_engine, text
import sys

from .config import get_connection_string, DATA_INTERIM


def load_to_database():
    """Load cleaned data into PostgreSQL"""
    print("="*60)
    print("LOADING DATA TO POSTGRESQL")
    print("="*60)
    
    # Connect to database
    engine = create_engine(get_connection_string())
    print("\n✓ Connected to database")
    
    # Load regions
    print("\n📊 Loading regions...")
    df = pd.read_csv(DATA_INTERIM / 'region_master.csv')
    df.to_sql('regions', engine, if_exists='replace', index=False, method='multi')
    print(f"   ✓ Loaded {len(df)} regions")
    print(f"   Columns: {list(df.columns)}")
    
    # Load TFR
    print("\n📊 Loading TFR data...")
    df = pd.read_csv(DATA_INTERIM / 'tfr_clean.csv')
    # Ensure column is named 'region_name' not 'region'
    if 'region' in df.columns:
        df = df.rename(columns={'region': 'region_name'})
    df.to_sql('tfr', engine, if_exists='replace', index=False, method='multi')
    print(f"   ✓ Loaded {len(df)} records")
    print(f"   Columns: {list(df.columns)}")
    
    # Load ASFR
    print("\n📊 Loading ASFR data...")
    df = pd.read_csv(DATA_INTERIM / 'asfr_clean.csv')
    # Ensure column is named 'region_name' not 'region'
    if 'region' in df.columns:
        df = df.rename(columns={'region': 'region_name'})
    # Rename age columns
    df = df.rename(columns={
        '15-19': 'age_15_19', '20-24': 'age_20_24', '25-29': 'age_25_29',
        '30-34': 'age_30_34', '35-39': 'age_35_39', '40-44': 'age_40_44',
        '45-49': 'age_45_49'
    })
    df.to_sql('asfr', engine, if_exists='replace', index=False, method='multi')
    print(f"   ✓ Loaded {len(df)} records")
    print(f"   Columns: {list(df.columns)}")
    
    # Load expenditure
    print("\n📊 Loading expenditure data...")
    df = pd.read_csv(DATA_INTERIM / 'expenditure_clean.csv')
    # Ensure column is named 'region_name' not 'region'
    if 'region' in df.columns:
        df = df.rename(columns={'region': 'region_name'})
    chunk_size = 1000
    for i in range(0, len(df), chunk_size):
        chunk = df.iloc[i:i+chunk_size]
        chunk.to_sql('expenditure', engine, if_exists='append' if i > 0 else 'replace', 
                     index=False, method='multi')
        print(f"   Progress: {min(i+chunk_size, len(df))}/{len(df)}", end='\r')
    print(f"\n   ✓ Loaded {len(df)} records")
    print(f"   Columns: {list(df.columns)}")
    
    # Create market analysis
    print("\n📊 Creating market analysis...")
    
    with engine.connect() as conn:
        # First, delete existing data
        conn.execute(text("DELETE FROM market_analysis"))
        conn.commit()
        
        # Then insert new data
        query = text("""
            INSERT INTO market_analysis (region_name, year, tfr, expenditure, quadrant, market_score)
            SELECT 
                t.region_name, t.year, t.tfr, e.expenditure,
                CASE
                    WHEN t.tfr >= (SELECT PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY tfr) FROM tfr WHERE year = 2020)
                         AND e.expenditure >= (SELECT PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY expenditure) FROM expenditure WHERE year = 2020)
                    THEN 'Stars'
                    WHEN t.tfr < (SELECT PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY tfr) FROM tfr WHERE year = 2020)
                         AND e.expenditure >= (SELECT PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY expenditure) FROM expenditure WHERE year = 2020)
                    THEN 'Cash Cows'
                    WHEN t.tfr >= (SELECT PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY tfr) FROM tfr WHERE year = 2020)
                         AND e.expenditure < (SELECT PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY expenditure) FROM expenditure WHERE year = 2020)
                    THEN 'Developing'
                    ELSE 'Saturated'
                END as quadrant,
                ((t.tfr / (SELECT MAX(tfr) FROM tfr WHERE year = 2020)) +
                 (e.expenditure::NUMERIC / (SELECT MAX(expenditure) FROM expenditure WHERE year = 2020))) / 2.0 as market_score
            FROM tfr t
            JOIN expenditure e ON t.region_name = e.region_name AND t.year = e.year
            WHERE t.year = 2020
        """)
        
        conn.execute(query)
        conn.commit()
        
        # Count results
        result = conn.execute(text("SELECT COUNT(*) FROM market_analysis"))
        count = result.fetchone()[0]
    
    print(f"   ✓ Created {count} market analysis records")
    
    # Verify
    print("\n🔍 Verifying data...")
    with engine.connect() as conn:
        for table in ['regions', 'tfr', 'asfr', 'expenditure', 'market_analysis']:
            result = conn.execute(text(f"SELECT COUNT(*) FROM {table}"))
            count = result.fetchone()[0]
            print(f"   {table:20s}: {count:6,} rows")
    
    print("\n" + "="*60)
    print("✅ DATA LOADING COMPLETE")
    print("="*60)
    
    return True


if __name__ == '__main__':
    success = load_to_database()
    sys.exit(0 if success else 1)