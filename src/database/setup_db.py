"""
PostgreSQL database setup
Creates database and tables
"""

import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import sys

from .config import DB_CONFIG


def create_database():
    """Create the database if it doesn't exist"""
    print("\n🗄️  Setting up database...")
    
    try:
        # Connect to PostgreSQL server
        conn = psycopg2.connect(
            host=DB_CONFIG['host'],
            port=DB_CONFIG['port'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            database='postgres'
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Check if database exists
        cursor.execute(
            "SELECT 1 FROM pg_database WHERE datname = %s",
            (DB_CONFIG['database'],)
        )
        
        if not cursor.fetchone():
            cursor.execute(
                sql.SQL("CREATE DATABASE {}").format(
                    sql.Identifier(DB_CONFIG['database'])
                )
            )
            print(f"   ✓ Database '{DB_CONFIG['database']}' created")
        else:
            print(f"   ℹ️  Database '{DB_CONFIG['database']}' exists")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False


def create_tables():
    """Create all tables with proper schema"""
    print("\n📊 Creating tables...")
    
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Regions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS regions (
                region_id SERIAL PRIMARY KEY,
                region_name VARCHAR(100) UNIQUE NOT NULL,
                region_type VARCHAR(20),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # TFR table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tfr (
                id SERIAL PRIMARY KEY,
                region_name VARCHAR(100) NOT NULL,
                year INTEGER NOT NULL,
                tfr NUMERIC(5, 2),
                data_source VARCHAR(50),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(region_name, year)
            )
        """)
        
        # ASFR table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS asfr (
                id SERIAL PRIMARY KEY,
                region_name VARCHAR(100) NOT NULL,
                year INTEGER NOT NULL,
                age_15_19 NUMERIC(6, 2),
                age_20_24 NUMERIC(6, 2),
                age_25_29 NUMERIC(6, 2),
                age_30_34 NUMERIC(6, 2),
                age_35_39 NUMERIC(6, 2),
                age_40_44 NUMERIC(6, 2),
                age_45_49 NUMERIC(6, 2),
                data_source VARCHAR(50),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(region_name, year)
            )
        """)
        
        # Expenditure table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS expenditure (
                id SERIAL PRIMARY KEY,
                region_name VARCHAR(100) NOT NULL,
                year INTEGER NOT NULL,
                expenditure INTEGER,
                data_source VARCHAR(50),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(region_name, year)
            )
        """)
        
        # Market analysis table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS market_analysis (
                id SERIAL PRIMARY KEY,
                region_name VARCHAR(100) NOT NULL,
                year INTEGER NOT NULL,
                tfr NUMERIC(5, 2),
                expenditure INTEGER,
                quadrant VARCHAR(20),
                market_score NUMERIC(5, 4),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(region_name, year)
            )
        """)
        
        # Create indexes
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_tfr_region_year ON tfr(region_name, year)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_exp_region_year ON expenditure(region_name, year)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_market_quadrant ON market_analysis(quadrant)")
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print("   ✓ All tables created")
        return True
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False


def setup():
    """Complete database setup"""
    print("="*60)
    print("DATABASE SETUP")
    print("="*60)
    
    if not create_database():
        return False
    
    if not create_tables():
        return False
    
    print("\n" + "="*60)
    print("✅ DATABASE SETUP COMPLETE")
    print("="*60)
    
    return True


if __name__ == '__main__':
    success = setup()
    sys.exit(0 if success else 1)