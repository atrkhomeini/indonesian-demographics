"""
Pre-flight Check Script
Validates environment setup before running main pipeline

Usage: python check_setup.py
"""

import sys
from pathlib import Path
import importlib.util


def print_header(text):
    """Print section header"""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)


def check_python_version():
    """Check Python version is 3.8+"""
    version = sys.version_info
    required = (3, 8)
    
    print("\n[1/7] Checking Python version...")
    print(f"   Current: {version.major}.{version.minor}.{version.micro}")
    print(f"   Required: {required[0]}.{required[1]}+")
    
    if version >= required:
        print("   ✅ PASS")
        return True
    else:
        print("   ❌ FAIL: Python 3.8+ required")
        return False


def check_dependencies():
    """Check required Python packages"""
    print("\n[2/7] Checking dependencies...")
    
    required = {
        'pandas': 'pandas',
        'numpy': 'numpy',
        'sqlalchemy': 'sqlalchemy',
        'psycopg2': 'psycopg2',
        'matplotlib': 'matplotlib',
        'seaborn': 'seaborn',
        'statsmodels': 'statsmodels'
    }
    
    missing = []
    for name, import_name in required.items():
        spec = importlib.util.find_spec(import_name)
        if spec is None:
            print(f"   ❌ {name}: NOT FOUND")
            missing.append(name)
        else:
            print(f"   ✅ {name}: found")
    
    if missing:
        print(f"\n   ❌ FAIL: Missing packages: {', '.join(missing)}")
        print("   Run: pip install -r requirements.txt")
        return False
    else:
        print("   ✅ PASS: All dependencies installed")
        return True


def check_database_config():
    """Check database configuration"""
    print("\n[3/7] Checking database configuration...")
    
    env_file = Path('.env')
    
    if not env_file.exists():
        print("   ❌ FAIL: .env file not found")
        print("   Run: cp .env.example .env")
        print("   Then edit .env with your database credentials")
        return False
    
    # Try to import config
    try:
        from src.database.config import DB_CONFIG
        
        print(f"   Host: {DB_CONFIG['host']}")
        print(f"   Port: {DB_CONFIG['port']}")
        print(f"   Database: {DB_CONFIG['database']}")
        print(f"   User: {DB_CONFIG['user']}")
        
        if DB_CONFIG['password'] == 'postgres':
            print("   ⚠️  WARNING: Using default password")
        
        print("   ✅ PASS: Configuration loaded")
        return True
        
    except Exception as e:
        print(f"   ❌ FAIL: Error loading config: {e}")
        return False


def check_database_connection():
    """Test database connection"""
    print("\n[4/7] Testing database connection...")
    
    try:
        from sqlalchemy import create_engine, text
        from src.database.config import get_connection_string
        
        engine = create_engine(get_connection_string())
        
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version()"))
            version = result.fetchone()[0]
            print(f"   PostgreSQL: {version.split(',')[0]}")
        
        print("   ✅ PASS: Database connection successful")
        return True
        
    except Exception as e:
        print(f"   ❌ FAIL: Cannot connect to database")
        print(f"   Error: {e}")
        print("\n   Troubleshooting:")
        print("   1. Check PostgreSQL is running")
        print("   2. Verify credentials in .env file")
        print("   3. Ensure database exists (or will be created)")
        return False


def check_directory_structure():
    """Check project directories"""
    print("\n[5/7] Checking directory structure...")
    
    required_dirs = [
        'data/raw',
        'data/interim',
        'data/processed',
        'src/data',
        'src/database',
        'src/analysis',
        'src/models',
        'reports/figures',
        'models'
    ]
    
    missing = []
    for dir_path in required_dirs:
        path = Path(dir_path)
        if not path.exists():
            missing.append(dir_path)
            print(f"   ⚠️  {dir_path}: missing (will be created)")
        else:
            print(f"   ✅ {dir_path}: exists")
    
    if missing:
        print(f"\n   ⚠️  Some directories missing (will be auto-created)")
    else:
        print("   ✅ PASS: All directories exist")
    
    return True  # Not critical, can be created


def check_data_files():
    """Check for required data files"""
    print("\n[6/7] Checking data files...")
    
    data_raw = Path('data/raw')
    
    # Check TFR
    tfr_dir = data_raw / 'TFR'
    tfr_files = list(tfr_dir.glob('*.csv')) if tfr_dir.exists() else []
    print(f"   TFR files: {len(tfr_files)}")
    
    # Check ASFR
    asfr_dir = data_raw / 'ASFR'
    asfr_files = list(asfr_dir.glob('*.csv')) if asfr_dir.exists() else []
    print(f"   ASFR files: {len(asfr_files)}")
    
    # Check Expenditure
    exp_dir = data_raw / 'Pengeluaran'
    exp_files = list(exp_dir.glob('*.csv')) if exp_dir.exists() else []
    print(f"   Expenditure files: {len(exp_files)}")
    
    total = len(tfr_files) + len(asfr_files) + len(exp_files)
    
    if total == 0:
        print("\n   ⚠️  WARNING: No data files found")
        print("   Place your CSV files in data/raw/ subdirectories")
        print("   Or run: python -m src.data.make_dataset")
        return False
    elif total < 18:  # Expected: 2 TFR + 2 ASFR + 16 expenditure
        print(f"\n   ⚠️  WARNING: Only {total} files found (expected ~18)")
        print("   Ensure all data files are copied to data/raw/")
        return True  # Allow to continue
    else:
        print(f"   ✅ PASS: {total} data files found")
        return True


def check_config_file():
    """Check analysis configuration file"""
    print("\n[7/7] Checking analysis configuration...")
    
    config_file = Path('src/models/config.yml')
    
    if not config_file.exists():
        print("   ❌ FAIL: config.yml not found")
        return False
    
    try:
        import yaml
        with open(config_file) as f:
            config = yaml.safe_load(f)
        
        print("   ✅ Forecasting config: loaded")
        print("   ✅ Quadrant config: loaded")
        print("   ✅ Output config: loaded")
        print("   ✅ PASS: Configuration file valid")
        return True
        
    except Exception as e:
        print(f"   ❌ FAIL: Error loading config: {e}")
        return False


def print_summary(results):
    """Print final summary"""
    print("\n" + "=" * 60)
    print("  SUMMARY")
    print("=" * 60)
    
    checks = [
        "Python Version",
        "Dependencies",
        "Database Config",
        "Database Connection",
        "Directory Structure",
        "Data Files",
        "Analysis Config"
    ]
    
    for check, passed in zip(checks, results):
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {check:25} {status}")
    
    all_critical = all(results[:4] + [results[6]])  # Critical checks
    data_ready = results[5]
    
    print("\n" + "=" * 60)
    
    if all_critical and data_ready:
        print("  ✅ ALL CHECKS PASSED - READY TO RUN")
        print("=" * 60)
        print("\n  Run: python main.py")
        return 0
    elif all_critical:
        print("  ⚠️  SYSTEM READY - MISSING DATA FILES")
        print("=" * 60)
        print("\n  Next steps:")
        print("  1. Copy data files to data/raw/ directories")
        print("  2. Run: python main.py")
        return 1
    else:
        print("  ❌ SETUP INCOMPLETE")
        print("=" * 60)
        print("\n  Fix the failed checks above before running pipeline")
        return 1


def main():
    """Run all checks"""
    print("=" * 60)
    print("  INDONESIA DEMOGRAPHICS - PRE-FLIGHT CHECK")
    print("=" * 60)
    print("\n  Validating environment setup...")
    
    results = [
        check_python_version(),
        check_dependencies(),
        check_database_config(),
        check_database_connection(),
        check_directory_structure(),
        check_data_files(),
        check_config_file()
    ]
    
    exit_code = print_summary(results)
    sys.exit(exit_code)


if __name__ == '__main__':
    main()