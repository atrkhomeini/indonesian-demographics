"""
Dashboard Source Package
Contains data loading and visualization utilities
"""

__version__ = "1.0.0"
__author__ = "Data Science Team"

from .data_loader import DataLoader
from .visualizations import Visualizer

__all__ = ['DataLoader', 'Visualizer']