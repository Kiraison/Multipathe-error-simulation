"""
Statistical analysis for GNSS measurements
"""

import math
from typing import List, Dict

class StatisticalAnalysis:
    """Statistical analysis tools for GNSS data"""
    
    def __init__(self):
        self.measurements = []
    
    def add_measurement(self, measurement: Dict):
        self.measurements.append(measurement)
    
    def get_statistics(self) -> Dict:
        if not self.measurements:
            return {'count': 0, 'mean': 0, 'std': 0, 'min': 0, 'max': 0}
        
        errors = [m.get('total_error', 0) for m in self.measurements]
        n = len(errors)
        mean = sum(errors) / n
        variance = sum((e - mean) ** 2 for e in errors) / n
        std = math.sqrt(variance)
        
        return {
            'count': n,
            'mean': round(mean, 2),
            'std': round(std, 2),
            'min': round(min(errors), 2),
            'max': round(max(errors), 2)
        }