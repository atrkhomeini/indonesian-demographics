"""
Data Loader Module
Handles loading and caching of data files
"""

import pandas as pd
from pathlib import Path
import streamlit as st


class DataLoader:
    """Load and cache dashboard data"""
    
    def __init__(self, data_dir=None):
        """
        Initialize DataLoader
        
        Args:
            data_dir: Path to data directory (auto-detected if None)
        """
        if data_dir is None:
            # Try multiple paths for flexibility
            possible_paths = [
                Path(__file__).parents[2] / 'data',  # From dashboard/src/
                Path('/home/claude/data'),  # Absolute path
                Path('data'),  # Relative to execution directory
            ]
            
            for path in possible_paths:
                if path.exists():
                    self.data_dir = path
                    break
            else:
                # If no data directory found, use first option and let it create
                self.data_dir = possible_paths[0]
        else:
            self.data_dir = Path(data_dir)
        
        self.processed_dir = self.data_dir / 'processed'
        self.interim_dir = self.data_dir / 'interim'
    
    def load_national_forecast(self):
        """Load national expenditure forecast"""
        try:
            df = pd.read_csv(self.processed_dir / 'national_expenditure_forecast.csv')
            return df
        except FileNotFoundError:
            st.warning("National forecast data not found")
            return self._generate_sample_national_forecast()
    
    def load_regional_forecasts(self):
        """Load regional expenditure forecasts"""
        try:
            df = pd.read_csv(self.processed_dir / 'regional_expenditure_forecasts.csv')
            return df
        except FileNotFoundError:
            st.warning("Regional forecast data not found")
            return None
    
    def load_market_segmentation(self):
        """Load market segmentation data"""
        try:
            df = pd.read_csv(self.processed_dir / 'market_segmentation.csv')
            return df
        except FileNotFoundError:
            st.warning("Market segmentation data not found")
            return self._generate_sample_segmentation()
    
    def load_segment_statistics(self):
        """Load segment statistics"""
        try:
            df = pd.read_csv(self.processed_dir / 'segment_statistics.csv')
            return df
        except FileNotFoundError:
            # Calculate from segmentation if not available
            segmentation = self.load_market_segmentation()
            return self._calculate_segment_stats(segmentation)
    
    def load_expenditure_historical(self):
        """Load historical expenditure data"""
        try:
            df = pd.read_csv(self.interim_dir / 'expenditure_clean.csv')
            return df
        except FileNotFoundError:
            st.warning("Historical expenditure data not found")
            return self._generate_sample_historical()
    
    def load_tfr_data(self):
        """Load TFR data"""
        try:
            df = pd.read_csv(self.interim_dir / 'tfr_clean.csv')
            return df
        except FileNotFoundError:
            st.warning("TFR data not found")
            return None
    
    def _calculate_segment_stats(self, segmentation):
        """Calculate segment statistics from segmentation data"""
        stats = segmentation.groupby('segment').agg({
            'region_name': 'count',
            'tfr': ['mean', 'median', 'std'],
            'expenditure': ['mean', 'median', 'std']
        }).round(2)
        
        stats.columns = ['_'.join(col).strip() for col in stats.columns.values]
        stats = stats.rename(columns={'region_name_count': 'count'})
        stats = stats.reset_index()
        
        return stats
    
    def _generate_sample_national_forecast(self):
        """Generate sample national forecast data for demo"""
        import numpy as np
        
        # Historical data (2010-2025)
        years_hist = list(range(2010, 2026))
        base_exp = 8000
        growth_rate = 1.05
        
        historical = pd.DataFrame({
            'year': years_hist,
            'expenditure': [base_exp * (growth_rate ** (i - 2010)) for i in years_hist],
            'type': 'historical',
            'lower_ci': np.nan,
            'upper_ci': np.nan
        })
        
        # Forecast data (2026-2030)
        years_fcst = list(range(2026, 2031))
        last_value = historical['expenditure'].iloc[-1]
        
        forecast = pd.DataFrame({
            'year': years_fcst,
            'expenditure': [last_value * (growth_rate ** (i - 2025)) for i in years_fcst],
            'type': 'forecast',
            'lower_ci': [last_value * (growth_rate ** (i - 2025)) * 0.9 for i in years_fcst],
            'upper_ci': [last_value * (growth_rate ** (i - 2025)) * 1.1 for i in years_fcst]
        })
        
        return pd.concat([historical, forecast], ignore_index=True)
    
    def _generate_sample_segmentation(self):
        """Generate sample segmentation data for demo"""
        import numpy as np
        
        np.random.seed(42)
        
        regions = [
            'JAKARTA', 'SURABAYA', 'BANDUNG', 'MEDAN', 'SEMARANG',
            'MAKASSAR', 'PALEMBANG', 'TANGERANG', 'DEPOK', 'BEKASI',
            'BOGOR', 'MALANG', 'YOGYAKARTA', 'SOLO', 'BALIKPAPAN'
        ]
        
        data = []
        for region in regions:
            tfr = np.random.uniform(1.5, 3.5)
            expenditure = np.random.uniform(8000, 18000)
            
            # Determine segment
            if tfr >= 2.3 and expenditure >= 12000:
                segment = 'Stars'
            elif tfr < 2.3 and expenditure >= 12000:
                segment = 'Cash Cows'
            elif tfr >= 2.3 and expenditure < 12000:
                segment = 'Developing'
            else:
                segment = 'Saturated'
            
            data.append({
                'region_name': region,
                'tfr': round(tfr, 2),
                'expenditure': int(expenditure),
                'segment': segment
            })
        
        return pd.DataFrame(data)
    
    def _generate_sample_historical(self):
        """Generate sample historical expenditure data"""
        import numpy as np
        
        regions = ['JAKARTA', 'SURABAYA', 'BANDUNG']
        years = list(range(2010, 2026))
        
        data = []
        for region in regions:
            base = np.random.uniform(8000, 15000)
            growth = np.random.uniform(1.03, 1.06)
            
            for year in years:
                exp = base * (growth ** (year - 2010))
                data.append({
                    'region_name': region,
                    'year': year,
                    'expenditure': int(exp)
                })
        
        return pd.DataFrame(data)


# Convenience function for quick data loading
def get_data():
    """Quick data loading function"""
    loader = DataLoader()
    return {
        'national_forecast': loader.load_national_forecast(),
        'regional_forecasts': loader.load_regional_forecasts(),
        'segmentation': loader.load_market_segmentation(),
        'segment_stats': loader.load_segment_statistics(),
        'expenditure_historical': loader.load_expenditure_historical(),
        'tfr_data': loader.load_tfr_data(),
    }