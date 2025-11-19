"""
Data cleaning module
Standardizes and cleans demographic data
"""

import pandas as pd
import re
from pathlib import Path
import sys


class DataCleaner:
    """Clean and standardize demographic data"""
    
    def __init__(self, project_root=None):
        """
        Initialize DataCleaner
        
        Parameters:
        -----------
        project_root : str, optional
            Project root directory (auto-detected if None)
        """
        if project_root is None:
            self.project_root = Path(__file__).resolve().parents[2]
        else:
            self.project_root = Path(project_root)
        
        self.raw_path = self.project_root / 'data' / 'raw'
        self.interim_path = self.project_root / 'data' / 'interim'
        self.interim_path.mkdir(parents=True, exist_ok=True)
    
    @staticmethod
    def clean_region_name(name):
        """
        Standardize region names
        
        Parameters:
        -----------
        name : str
            Region name to clean
            
        Returns:
        --------
        str : Cleaned region name
        """
        if pd.isna(name):
            return None
        
        # Convert to string, strip whitespace
        name = str(name).strip()
        
        # Remove extra spaces
        name = re.sub(r'\s+', ' ', name)
        
        # Convert to uppercase for consistency
        name = name.upper()
        
        return name
    
    def clean_tfr_data(self):
        """Clean Total Fertility Rate data"""
        print("\n📊 Cleaning TFR data...")
        
        # Load raw data
        input_file = self.raw_path / 'TFR' / 'tfr_kab_2020.csv'
        df = pd.read_csv(input_file, skiprows=2)
        df.columns = ['region_name', 'tfr']  # Use region_name for consistency
        
        # Clean data
        df = df.dropna(subset=['region_name'])
        df['region_name'] = df['region_name'].apply(self.clean_region_name)
        df['tfr'] = pd.to_numeric(df['tfr'], errors='coerce')
        df = df.dropna(subset=['tfr'])
        
        # Add metadata
        df['year'] = 2020
        df['data_source'] = 'SP2020_LF'
        
        df = df.drop_duplicates(subset=['region_name', 'year'])
        
        # Validate range
        df = df[(df['tfr'] >= 0.5) & (df['tfr'] <= 10.0)]
        
        # Save to interim
        output_file = self.interim_path / 'tfr_clean.csv'
        df.to_csv(output_file, index=False)
        
        print(f"   ✓ Cleaned {len(df)} regions")
        print(f"   📁 Saved to: {output_file.name}")
        
        return df
    
    def clean_asfr_data(self):
        """Clean Age-Specific Fertility Rate data"""
        print("\n📊 Cleaning ASFR data...")
        
        # Load raw data
        input_file = self.raw_path / 'ASFR' / 'asfr_kab_2020.csv'
        df = pd.read_csv(input_file, skiprows=2)
        
        # Set column names
        age_groups = ['15-19', '20-24', '25-29', '30-34', '35-39', '40-44', '45-49']
        df.columns = ['region_name'] + age_groups  # Use region_name for consistency
        
        # Clean data
        df = df.dropna(subset=['region_name'])
        df['region_name'] = df['region_name'].apply(self.clean_region_name)
        
        # Convert ASFR values to numeric
        for col in age_groups:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Add metadata
        df['year'] = 2020
        df['data_source'] = 'SP2020_LF'
        
        # Save to interim
        output_file = self.interim_path / 'asfr_clean.csv'
        df.to_csv(output_file, index=False)
        
        print(f"   ✓ Cleaned {len(df)} regions")
        print(f"   📁 Saved to: {output_file.name}")
        
        return df
    
    def clean_expenditure_data(self):
        """Clean expenditure per capita data (2010-2025)"""
        print("\n📊 Cleaning expenditure data...")
        
        all_data = []
        
        for year in range(2010, 2026):
            input_file = self.raw_path / 'Pengeluaran' / f'{year}.csv'
            
            if not input_file.exists():
                print(f"   ⚠️  {year}.csv not found")
                continue
            
            try:
                df = pd.read_csv(input_file, skiprows=2)
                df.columns = ['region_name', 'expenditure']  # Use region_name for consistency
                
                # Clean data
                df = df.dropna(subset=['region_name'])
                df['region_name'] = df['region_name'].apply(self.clean_region_name)
                df['expenditure'] = pd.to_numeric(df['expenditure'], errors='coerce')
                df = df.dropna(subset=['expenditure'])
                
                # Add metadata
                df['year'] = year
                df['data_source'] = 'Susenas'
                df = df.drop_duplicates(subset=['region_name', 'year'])
                # Validate range
                df = df[(df['expenditure'] >= 1000) & (df['expenditure'] <= 50000)]
                
                all_data.append(df)
                print(f"   Year {year}: {len(df)} regions")
                
            except Exception as e:
                print(f"   ❌ Error processing {year}: {e}")
                continue
        
        # Combine all years
        combined = pd.concat(all_data, ignore_index=True)
        
        # Save to interim
        output_file = self.interim_path / 'expenditure_clean.csv'
        combined.to_csv(output_file, index=False)
        
        print(f"\n   ✓ Total: {len(combined)} records")
        print(f"   📁 Saved to: {output_file.name}")
        
        return combined
    
    def create_region_master(self, tfr_df, asfr_df, exp_df):
        """Create master region table"""
        print("\n📊 Creating region master table...")
        
        # Get unique regions
        all_regions = set()
        all_regions.update(tfr_df['region_name'].unique())
        all_regions.update(asfr_df['region_name'].unique())
        all_regions.update(exp_df['region_name'].unique())
        
        # Create master table
        region_master = pd.DataFrame({
            'region_id': range(1, len(all_regions) + 1),
            'region_name': sorted(all_regions)
        })
        
        # Classify region type
        def classify_region(name):
            if name.startswith('KOTA '):
                return 'Kota'
            elif name.startswith('KABUPATEN ') or name.startswith('KAB. '):
                return 'Kabupaten'
            else:
                return 'Unknown'
        
        region_master['region_type'] = region_master['region_name'].apply(classify_region)
        
        # Save to interim
        output_file = self.interim_path / 'region_master.csv'
        region_master.to_csv(output_file, index=False)
        
        print(f"   ✓ Total regions: {len(region_master)}")
        print(f"   📁 Saved to: {output_file.name}")
        
        return region_master
    
    def clean_all(self):
        """Run complete data cleaning pipeline"""
        print("="*60)
        print("DATA CLEANING PIPELINE")
        print("="*60)
        
        # Clean all datasets
        tfr_df = self.clean_tfr_data()
        asfr_df = self.clean_asfr_data()
        exp_df = self.clean_expenditure_data()
        region_master = self.create_region_master(tfr_df, asfr_df, exp_df)
        
        print("\n" + "="*60)
        print("✅ DATA CLEANING COMPLETE")
        print("="*60)
        print(f"\n📁 Clean data location: {self.interim_path}")
        
        return {
            'tfr': tfr_df,
            'asfr': asfr_df,
            'expenditure': exp_df,
            'regions': region_master
        }


if __name__ == '__main__':
    cleaner = DataCleaner()
    cleaned_data = cleaner.clean_all()
    
    sys.exit(0)