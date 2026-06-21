"""
Configuration settings for GNSS Professional Suite
"""

import os

class Config:
    """Main configuration class"""
    
    # Flask settings
    SECRET_KEY = 'gnss-professional-secret-key-2024'
    DEBUG = True
    
    # Database
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_DIR = os.path.join(BASE_DIR, 'data')
    DATABASE_PATH = os.path.join(DATA_DIR, 'gnss_database.db')
    
    # GNSS Constants (WGS84)
    WGS84_A = 6378137.0          # Semi-major axis (m)
    WGS84_F = 1/298.257223563    # Flattening
    SPEED_OF_LIGHT = 299792458.0 # m/s
    GPS_L1_FREQ = 1575.42e6      # Hz
    GPS_L2_FREQ = 1227.60e6      # Hz
    
    # Simulation bounds (meters)
    BOUNDS_MIN = -100
    BOUNDS_MAX = 100
    
    # Create directories if not exists
    @staticmethod
    def init_directories():
        os.makedirs(Config.DATA_DIR, exist_ok=True)
        os.makedirs(os.path.join(Config.BASE_DIR, 'reports'), exist_ok=True)

config = Config