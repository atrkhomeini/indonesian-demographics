"""
Quadrant Analysis Module
Market segmentation based on TFR and Expenditure
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from typing import Tuple, Dict


class QuadrantAnalyzer:
    """Perform quadrant analysis for market segmentation"""
    
    def __init__(self, config: Dict):
        """
        Initialize quadrant analyzer
        
        Args:
            config: Quadrant configuration dictionary
        """
        self.tfr_threshold_method = config.get('tfr_threshold_method', 'median')
        self.exp_threshold_method = config.get('expenditure_threshold_method', 'median')
        self.tfr_threshold_fixed = config.get('tfr_threshold_fixed', 2.1)
        self.exp_threshold_fixed = config.get('expenditure_threshold_fixed', 10000)
        self.segments = config.get('segments', {})
    
    def calculate_thresholds(self,
                           df: pd.DataFrame,
                           tfr_col: str = 'tfr',
                           exp_col: str = 'expenditure') -> Tuple[float, float]:
        """
        Calculate thresholds for quadrant analysis
        
        Args:
            df: Dataframe with TFR and expenditure
            tfr_col: TFR column name
            exp_col: Expenditure column name
            
        Returns:
            Tuple of (tfr_threshold, expenditure_threshold)
        """
        # TFR threshold
        if self.tfr_threshold_method == 'median':
            tfr_threshold = df[tfr_col].median()
        elif self.tfr_threshold_method == 'mean':
            tfr_threshold = df[tfr_col].mean()
        else:
            tfr_threshold = self.tfr_threshold_fixed
        
        # Expenditure threshold
        if self.exp_threshold_method == 'median':
            exp_threshold = df[exp_col].median()
        elif self.exp_threshold_method == 'mean':
            exp_threshold = df[exp_col].mean()
        else:
            exp_threshold = self.exp_threshold_fixed
        
        return tfr_threshold, exp_threshold
    
    def assign_segments(self,
                       df: pd.DataFrame,
                       tfr_threshold: float,
                       exp_threshold: float,
                       tfr_col: str = 'tfr',
                       exp_col: str = 'expenditure') -> pd.DataFrame:
        """
        Assign quadrant segments to regions
        
        Args:
            df: Dataframe with TFR and expenditure
            tfr_threshold: TFR threshold value
            exp_threshold: Expenditure threshold value
            tfr_col: TFR column name
            exp_col: Expenditure column name
            
        Returns:
            Dataframe with segment column
        """
        df = df.copy()
        
        conditions = [
            (df[tfr_col] >= tfr_threshold) & (df[exp_col] >= exp_threshold),
            (df[tfr_col] >= tfr_threshold) & (df[exp_col] < exp_threshold),
            (df[tfr_col] < tfr_threshold) & (df[exp_col] >= exp_threshold),
            (df[tfr_col] < tfr_threshold) & (df[exp_col] < exp_threshold)
        ]
        
        choices = [
            self.segments.get('high_tfr_high_exp', 'Stars'),
            self.segments.get('high_tfr_low_exp', 'Developing'),
            self.segments.get('low_tfr_high_exp', 'Cash Cows'),
            self.segments.get('low_tfr_low_exp', 'Saturated')
        ]
        
        df['segment'] = np.select(conditions, choices, default='Unknown')
        
        return df
    
    def get_segment_statistics(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate statistics for each segment
        
        Args:
            df: Dataframe with segments
            
        Returns:
            Statistics dataframe
        """
        stats = df.groupby('segment').agg({
            'region_name': 'count',
            'tfr': ['mean', 'median', 'std'],
            'expenditure': ['mean', 'median', 'std']
        }).round(2)
        
        stats.columns = ['_'.join(col).strip() for col in stats.columns.values]
        stats = stats.rename(columns={'region_name_count': 'count'})
        stats = stats.reset_index()
        
        return stats
    
    def plot_quadrant(self,
                     df: pd.DataFrame,
                     tfr_threshold: float,
                     exp_threshold: float,
                     tfr_col: str = 'tfr',
                     exp_col: str = 'expenditure',
                     title: str = 'Market Segmentation - Quadrant Analysis',
                     save_path: str = None):
        """
        Create quadrant plot
        
        Args:
            df: Dataframe with segments
            tfr_threshold: TFR threshold
            exp_threshold: Expenditure threshold
            tfr_col: TFR column name
            exp_col: Expenditure column name
            title: Plot title
            save_path: Path to save figure
        """
        fig, ax = plt.subplots(figsize=(14, 10))
        
        # Define colors for segments
        segment_colors = {
            self.segments.get('high_tfr_high_exp', 'Stars'): '#FFD700',
            self.segments.get('high_tfr_low_exp', 'Developing'): '#87CEEB',
            self.segments.get('low_tfr_high_exp', 'Cash Cows'): '#90EE90',
            self.segments.get('low_tfr_low_exp', 'Saturated'): '#FFB6C1'
        }
        
        # Scatter plot by segment
        for segment in df['segment'].unique():
            segment_data = df[df['segment'] == segment]
            ax.scatter(segment_data[tfr_col],
                      segment_data[exp_col],
                      c=segment_colors.get(segment, 'gray'),
                      label=segment,
                      s=100,
                      alpha=0.6,
                      edgecolors='black',
                      linewidth=0.5)
        
        # Add threshold lines
        ax.axvline(x=tfr_threshold, color='red', linestyle='--',
                  linewidth=2, alpha=0.7, label=f'TFR Threshold = {tfr_threshold:.2f}')
        ax.axhline(y=exp_threshold, color='blue', linestyle='--',
                  linewidth=2, alpha=0.7, label=f'Exp Threshold = {exp_threshold:,.0f}')
        
        # Add quadrant labels
        y_max = df[exp_col].max()
        y_min = df[exp_col].min()
        x_max = df[tfr_col].max()
        x_min = df[tfr_col].min()
        
        quadrant_labels = [
            (tfr_threshold + (x_max - tfr_threshold) * 0.5,
             exp_threshold + (y_max - exp_threshold) * 0.9,
             self.segments.get('high_tfr_high_exp', 'Stars')),
            (tfr_threshold + (x_max - tfr_threshold) * 0.5,
             y_min + (exp_threshold - y_min) * 0.1,
             self.segments.get('high_tfr_low_exp', 'Developing')),
            (x_min + (tfr_threshold - x_min) * 0.5,
             exp_threshold + (y_max - exp_threshold) * 0.9,
             self.segments.get('low_tfr_high_exp', 'Cash Cows')),
            (x_min + (tfr_threshold - x_min) * 0.5,
             y_min + (exp_threshold - y_min) * 0.1,
             self.segments.get('low_tfr_low_exp', 'Saturated'))
        ]
        
        for x, y, label in quadrant_labels:
            ax.text(x, y, label,
                   fontsize=14, fontweight='bold',
                   ha='center', va='center',
                   bbox=dict(boxstyle='round,pad=0.5',
                           facecolor='white',
                           edgecolor='black',
                           alpha=0.7))
        
        ax.set_xlabel('Total Fertility Rate (TFR)', fontsize=13, fontweight='bold')
        ax.set_ylabel('Per Capita Expenditure (Rp 000)', fontsize=13, fontweight='bold')
        ax.set_title(title, fontsize=15, fontweight='bold', pad=20)
        ax.grid(True, alpha=0.3)
        ax.legend(fontsize=10, loc='best')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        plt.show()
    
    def plot_segment_distribution(self,
                                 df: pd.DataFrame,
                                 save_path: str = None):
        """
        Plot segment distribution
        
        Args:
            df: Dataframe with segments
            save_path: Path to save figure
        """
        fig, axes = plt.subplots(1, 2, figsize=(16, 6))
        
        # Count plot
        segment_counts = df['segment'].value_counts()
        axes[0].bar(segment_counts.index, segment_counts.values,
                   color=['#FFD700', '#90EE90', '#87CEEB', '#FFB6C1'])
        axes[0].set_xlabel('Segment', fontsize=12, fontweight='bold')
        axes[0].set_ylabel('Number of Regions', fontsize=12, fontweight='bold')
        axes[0].set_title('Region Count by Segment', fontsize=14, fontweight='bold')
        axes[0].grid(True, alpha=0.3, axis='y')
        
        for i, v in enumerate(segment_counts.values):
            axes[0].text(i, v + 0.5, str(v), ha='center', va='bottom',
                        fontweight='bold', fontsize=11)
        
        # Pie chart
        axes[1].pie(segment_counts.values,
                   labels=segment_counts.index,
                   autopct='%1.1f%%',
                   colors=['#FFD700', '#90EE90', '#87CEEB', '#FFB6C1'],
                   startangle=90)
        axes[1].set_title('Segment Distribution (%)', fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        plt.show()


def run_quadrant_analysis(tfr_df: pd.DataFrame,
                         expenditure_df: pd.DataFrame,
                         config: Dict,
                         output_dir: str = '../reports/figures'):
    """
    Run complete quadrant analysis
    
    Args:
        tfr_df: TFR dataframe
        expenditure_df: Expenditure dataframe
        config: Quadrant configuration
        output_dir: Directory to save outputs
        
    Returns:
        Segmented dataframe
    """
    print("\n" + "="*80)
    print("QUADRANT ANALYSIS - MARKET SEGMENTATION")
    print("="*80)
    
    # Merge TFR and expenditure data
    latest_tfr_year = tfr_df['year'].max()
    latest_exp_year = expenditure_df['year'].max()
    
    print(f"\nUsing TFR data from: {latest_tfr_year}")
    print(f"Using Expenditure data from: {latest_exp_year}")
    
    tfr_latest = tfr_df[tfr_df['year'] == latest_tfr_year][['region_name', 'tfr']]
    exp_latest = expenditure_df[expenditure_df['year'] == latest_exp_year][['region_name', 'expenditure']]
    
    merged_df = pd.merge(tfr_latest, exp_latest, on='region_name', how='inner')
    
    print(f"\nRegions in analysis: {len(merged_df)}")
    
    # Initialize analyzer
    analyzer = QuadrantAnalyzer(config)
    
    # Calculate thresholds
    tfr_threshold, exp_threshold = analyzer.calculate_thresholds(merged_df)
    
    print(f"\nThresholds:")
    print(f"  TFR: {tfr_threshold:.2f}")
    print(f"  Expenditure: Rp {exp_threshold:,.2f}")
    
    # Assign segments
    segmented_df = analyzer.assign_segments(merged_df, tfr_threshold, exp_threshold)
    
    # Get statistics
    stats = analyzer.get_segment_statistics(segmented_df)
    
    print(f"\nSegment Statistics:")
    print(stats.to_string(index=False))
    
    # Create output directory
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Plot quadrant
    analyzer.plot_quadrant(
        segmented_df,
        tfr_threshold,
        exp_threshold,
        save_path=output_dir / 'quadrant_analysis.png'
    )
    
    # Plot distribution
    analyzer.plot_segment_distribution(
        segmented_df,
        save_path=output_dir / 'segment_distribution.png'
    )
    
    # Save results
    segmented_df.to_csv('data/processed/market_segmentation.csv', index=False)
    stats.to_csv('data/processed/segment_statistics.csv', index=False)
    
    print(f"\n✓ Segmentation saved: data/processed/market_segmentation.csv")
    print(f"✓ Statistics saved: data/processed/segment_statistics.csv")
    
    return segmented_df
