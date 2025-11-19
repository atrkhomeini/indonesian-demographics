# config.py
"""
Database Configuration
Centralized configuration for PostgreSQL connection
"""

import os

# Database connection parameters
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'indonesia_demographics',
    'user': 'postgres',
    'password': 'Time12:30' 
}

# SQLAlchemy connection string
def get_connection_string():
    """Generate SQLAlchemy connection string"""
    return (
        f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}"
        f"@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
    )

# Psycopg2 connection string
def get_psycopg2_config():
    """Get config dict for psycopg2"""
    return DB_CONFIG

# File paths
BASE_DIR = '../data'
DATA_PATH = BASE_DIR /'raw' 
OUTPUT_PATH = '../data/processed'