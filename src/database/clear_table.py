"""
Clear Market Analysis Table
Run this to delete all data from market_analysis table
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from sqlalchemy import create_engine, text
from src.database.config import get_connection_string

def clear_market_analysis():
    """Clear market_analysis table"""
    print("="*60)
    print("CLEARING MARKET ANALYSIS TABLE")
    print("="*60)
    
    engine = create_engine(get_connection_string())
    
    with engine.connect() as conn:
        # Check current count
        result = conn.execute(text("SELECT COUNT(*) FROM market_analysis"))
        count = result.fetchone()[0]
        print(f"\nCurrent records: {count}")
        
        # Delete all records
        print("\n🗑️  Deleting all records...")
        conn.execute(text("DELETE FROM market_analysis"))
        conn.commit()
        
        # Verify deletion
        result = conn.execute(text("SELECT COUNT(*) FROM market_analysis"))
        count = result.fetchone()[0]
        print(f"Records after deletion: {count}")
        
        if count == 0:
            print("\n✅ Table cleared successfully!")
        else:
            print("\n⚠️  Warning: Some records remain")
    
    print("\n" + "="*60)
    print("Now you can run: python -m src.database.load_data")
    print("="*60)

if __name__ == '__main__':
    clear_market_analysis()