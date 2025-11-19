"""
Script to organize raw data into proper folder structure
Copies data from uploads to data/raw/ folders
"""

import shutil
from pathlib import Path
import sys


class DatasetMaker:
    """Organize raw data files"""
    
    def __init__(self, source_path='/mnt/user-data/uploads', project_root=None):
        """
        Initialize DatasetMaker
        
        Parameters:
        -----------
        source_path : str
            Path to source data files
        project_root : str, optional
            Project root directory (auto-detected if None)
        """
        self.source_path = Path(source_path)
        
        if project_root is None:
            # Auto-detect project root (go up from src/data/)
            self.project_root = Path(__file__).resolve().parents[2]
        else:
            self.project_root = Path(project_root)
        
        self.raw_path = self.project_root / 'data' / 'raw'
        
    def create_directories(self):
        """Create directory structure if it doesn't exist"""
        print("📁 Creating directory structure...")
        
        (self.raw_path / 'TFR').mkdir(parents=True, exist_ok=True)
        (self.raw_path / 'ASFR').mkdir(parents=True, exist_ok=True)
        (self.raw_path / 'Pengeluaran').mkdir(parents=True, exist_ok=True)
        
        print("   ✓ Directories created")
    
    def copy_tfr_data(self):
        """Copy TFR data files"""
        print("\n📊 Copying TFR data...")
        
        tfr_files = [
            'tfr_kab_2020.csv',
            'tfr_provinsi_1971_2020.csv'
        ]
        
        for filename in tfr_files:
            source = self.source_path / filename
            dest = self.raw_path / 'TFR' / filename
            
            if source.exists():
                shutil.copy2(source, dest)
                print(f"   ✓ {filename}")
            else:
                print(f"   ⚠️  {filename} not found")
    
    def copy_asfr_data(self):
        """Copy ASFR data files"""
        print("\n📊 Copying ASFR data...")
        
        asfr_files = [
            'asfr_kab_2020.csv',
            'asfr_provinsi_1971_2020.csv'
        ]
        
        for filename in asfr_files:
            source = self.source_path / filename
            dest = self.raw_path / 'ASFR' / filename
            
            if source.exists():
                shutil.copy2(source, dest)
                print(f"   ✓ {filename}")
            else:
                print(f"   ⚠️  {filename} not found")
    
    def copy_expenditure_data(self):
        """Copy expenditure data files (2010-2025)"""
        print("\n📊 Copying expenditure data...")
        
        count = 0
        for year in range(2010, 2026):
            filename = f'{year}.csv'
            source = self.source_path / filename
            dest = self.raw_path / 'Pengeluaran' / filename
            
            if source.exists():
                shutil.copy2(source, dest)
                count += 1
        
        print(f"   ✓ {count} expenditure files copied")
    
    def verify_data(self):
        """Verify all data files are in place"""
        print("\n🔍 Verifying data...")
        
        tfr_count = len(list((self.raw_path / 'TFR').glob('*.csv')))
        asfr_count = len(list((self.raw_path / 'ASFR').glob('*.csv')))
        exp_count = len(list((self.raw_path / 'Pengeluaran').glob('*.csv')))
        
        print(f"   TFR files: {tfr_count}")
        print(f"   ASFR files: {asfr_count}")
        print(f"   Expenditure files: {exp_count}")
        print(f"   Total: {tfr_count + asfr_count + exp_count} files")
    
    def prepare_all(self):
        """Run complete data preparation"""
        print("="*60)
        print("PREPARING RAW DATA")
        print("="*60)
        
        self.create_directories()
        self.copy_tfr_data()
        self.copy_asfr_data()
        self.copy_expenditure_data()
        self.verify_data()
        
        print("\n" + "="*60)
        print("✅ RAW DATA PREPARATION COMPLETE")
        print("="*60)
        print(f"\n📁 Data location: {self.raw_path}")


def prepare_raw_data():
    """Convenience function to prepare raw data"""
    maker = DatasetMaker()
    maker.prepare_all()
    return maker.raw_path


if __name__ == '__main__':
    # Run data preparation
    maker = DatasetMaker()
    maker.prepare_all()
    
    sys.exit(0)