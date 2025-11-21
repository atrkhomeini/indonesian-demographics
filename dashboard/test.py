#!/usr/bin/env python3
"""
Dashboard Test Script
Validates dashboard functionality before deployment
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    """Test all required imports"""
    print("\n" + "="*60)
    print("TESTING IMPORTS")
    print("="*60)
    
    required_modules = [
        ('streamlit', 'Streamlit'),
        ('pandas', 'Pandas'),
        ('numpy', 'NumPy'),
        ('plotly', 'Plotly'),
    ]
    
    failed = []
    
    for module, name in required_modules:
        try:
            __import__(module)
            print(f"   ✓ {name}")
        except ImportError as e:
            print(f"   ❌ {name}: {e}")
            failed.append(name)
    
    if failed:
        print(f"\n   ❌ Missing modules: {', '.join(failed)}")
        print("   Run: pip install -r requirements.txt")
        return False
    else:
        print("\n   ✅ All imports successful")
        return True


def test_modules():
    """Test custom modules"""
    print("\n" + "="*60)
    print("TESTING CUSTOM MODULES")
    print("="*60)
    
    try:
        from src.data_loader import DataLoader
        print("   ✓ DataLoader imported")
    except Exception as e:
        print(f"   ❌ DataLoader import failed: {e}")
        return False
    
    try:
        from src.visualizations import Visualizer
        print("   ✓ Visualizer imported")
    except Exception as e:
        print(f"   ❌ Visualizer import failed: {e}")
        return False
    
    print("\n   ✅ All custom modules loaded")
    return True


def test_data_loading():
    """Test data loading"""
    print("\n" + "="*60)
    print("TESTING DATA LOADING")
    print("="*60)
    
    try:
        from src.data_loader import DataLoader
        loader = DataLoader()
        
        # Test each data loading method
        datasets = {
            'National Forecast': loader.load_national_forecast(),
            'Market Segmentation': loader.load_market_segmentation(),
            'Segment Statistics': loader.load_segment_statistics(),
        }
        
        for name, df in datasets.items():
            if df is not None and len(df) > 0:
                print(f"   ✓ {name}: {len(df)} rows")
            else:
                print(f"   ⚠️  {name}: Empty or None (will use sample data)")
        
        print("\n   ✅ Data loading successful")
        return True
        
    except Exception as e:
        print(f"   ❌ Data loading failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_visualizations():
    """Test visualization creation"""
    print("\n" + "="*60)
    print("TESTING VISUALIZATIONS")
    print("="*60)
    
    try:
        from src.visualizations import Visualizer
        from src.data_loader import DataLoader
        import pandas as pd
        
        viz = Visualizer()
        loader = DataLoader()
        
        # Test with sample data
        sample_segment = pd.DataFrame({
            'segment': ['Stars', 'Cash Cows', 'Developing', 'Saturated'],
            'count': [10, 15, 20, 5]
        })
        
        # Try creating a simple visualization
        fig = viz.create_segment_pie(sample_segment)
        
        if fig:
            print("   ✓ Segment pie chart created")
        
        # Test quadrant plot
        segmentation = loader.load_market_segmentation()
        if segmentation is not None:
            fig = viz.create_quadrant_plot(segmentation)
            print("   ✓ Quadrant plot created")
        
        print("\n   ✅ Visualizations working")
        return True
        
    except Exception as e:
        print(f"   ❌ Visualization test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_configuration():
    """Test configuration files"""
    print("\n" + "="*60)
    print("TESTING CONFIGURATION")
    print("="*60)
    
    required_files = {
        'app.py': 'Main application',
        'requirements.txt': 'Dependencies',
        'src/data_loader.py': 'Data loader',
        'src/visualizations.py': 'Visualizations',
        '.streamlit/config.toml': 'Streamlit config'
    }
    
    dashboard_root = Path(__file__).parent
    missing = []
    
    for file_path, description in required_files.items():
        full_path = dashboard_root / file_path
        if full_path.exists():
            print(f"   ✓ {description}: {file_path}")
        else:
            print(f"   ❌ {description}: {file_path} - NOT FOUND")
            missing.append(file_path)
    
    if missing:
        print(f"\n   ❌ Missing files: {len(missing)}")
        return False
    else:
        print("\n   ✅ All configuration files present")
        return True


def test_data_structure():
    """Test data directory structure"""
    print("\n" + "="*60)
    print("TESTING DATA STRUCTURE")
    print("="*60)
    
    dashboard_root = Path(__file__).parent
    
    # Check directories
    dirs = [
        'data/processed',
        'data/interim'
    ]
    
    for dir_path in dirs:
        full_path = dashboard_root / dir_path
        if full_path.exists():
            csv_count = len(list(full_path.glob('*.csv')))
            print(f"   ✓ {dir_path}: {csv_count} CSV files")
        else:
            print(f"   ⚠️  {dir_path}: Directory not found (will be created)")
    
    print("\n   ✅ Data structure check complete")
    return True


def run_all_tests():
    """Run all tests"""
    print("="*60)
    print("DASHBOARD PRE-DEPLOYMENT TESTS")
    print("="*60)
    
    tests = [
        ("Imports", test_imports),
        ("Custom Modules", test_modules),
        ("Configuration", test_configuration),
        ("Data Structure", test_data_structure),
        ("Data Loading", test_data_loading),
        ("Visualizations", test_visualizations),
    ]
    
    results = []
    
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ {name} test crashed: {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"   {name:20s} {status}")
    
    total = len(results)
    passed = sum(1 for _, p in results if p)
    
    print(f"\n   Total: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n" + "="*60)
        print("✅ ALL TESTS PASSED - READY FOR DEPLOYMENT")
        print("="*60)
        print("\nNext steps:")
        print("1. Test locally: streamlit run app.py")
        print("2. Deploy to Hugging Face (see DEPLOYMENT.md)")
        return 0
    else:
        print("\n" + "="*60)
        print("❌ SOME TESTS FAILED")
        print("="*60)
        print("\nFix the issues above before deploying")
        return 1


if __name__ == '__main__':
    exit_code = run_all_tests()
    sys.exit(exit_code)