"""
Database Diagnostic Script
Checks what columns actually exist in tables
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from sqlalchemy import create_engine, text
from src.database.config import get_connection_string

def check_database():
    """Check database structure"""
    print("="*60)
    print("DATABASE DIAGNOSTIC")
    print("="*60)
    
    engine = create_engine(get_connection_string())
    
    tables = ['regions', 'tfr', 'asfr', 'expenditure', 'market_analysis']
    
    with engine.connect() as conn:
        for table in tables:
            print(f"\n📊 Table: {table}")
            try:
                # Get column names
                result = conn.execute(text(f"""
                    SELECT column_name, data_type 
                    FROM information_schema.columns 
                    WHERE table_name = '{table}'
                    ORDER BY ordinal_position
                """))
                
                print("   Columns:")
                for row in result:
                    print(f"      - {row[0]} ({row[1]})")
                
                # Get row count
                result = conn.execute(text(f"SELECT COUNT(*) FROM {table}"))
                count = result.fetchone()[0]
                print(f"   Rows: {count}")
                
            except Exception as e:
                print(f"   ❌ Error: {e}")
    
    print("\n" + "="*60)

if __name__ == '__main__':
    check_database()