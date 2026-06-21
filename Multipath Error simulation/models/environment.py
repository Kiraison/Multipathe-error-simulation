"""
Environment modeling for GNSS Professional Suite
"""

class EnvironmentModel:
    """Environment configurations for simulation"""
    
    def __init__(self):
        self.environments = {
            'rural': self._rural(),
            'suburban': self._suburban(),
            'urban': self._urban(),
            'coastal': self._coastal()
        }
    
    def _rural(self) -> dict:
        return {
            'name': '🌾 Rural',
            'buildings': [],
            'trees': [
                {'x': -25, 'y': -15, 'radius': 12, 'density': 0.3, 'type': 'sparse'},
                {'x': 20, 'y': 10, 'radius': 10, 'density': 0.25, 'type': 'sparse'}
            ],
            'water': [],
            'base_error': 0.51,
            'multipath_factor': 0.5,
            'signal_quality': 0.95,
            'color': '#4caf50'
        }
    
    def _suburban(self) -> dict:
        return {
            'name': '🏘️ Suburban',
            'buildings': [
                {'x': -40, 'y': -25, 'width': 28, 'height': 8, 'material': 'brick'},
                {'x': 35, 'y': -15, 'width': 24, 'height': 7, 'material': 'concrete'},
                {'x': -20, 'y': 30, 'width': 26, 'height': 6, 'material': 'wood'}
            ],
            'trees': [
                {'x': -55, 'y': 15, 'radius': 10, 'density': 0.45, 'type': 'medium'},
                {'x': 50, 'y': 20, 'radius': 9, 'density': 0.4, 'type': 'medium'}
            ],
            'water': [
                {'x': 0, 'y': -50, 'radius': 14, 'type': 'pond'}
            ],
            'base_error': 1.20,
            'multipath_factor': 1.5,
            'signal_quality': 0.85,
            'color': '#ff9800'
        }
    
    def _urban(self) -> dict:
        return {
            'name': '🏙️ Urban',
            'buildings': [
                {'x': -50, 'y': -30, 'width': 38, 'height': 30, 'material': 'glass'},
                {'x': 30, 'y': -20, 'width': 35, 'height': 28, 'material': 'concrete'},
                {'x': -20, 'y': 40, 'width': 48, 'height': 35, 'material': 'steel'},
                {'x': 0, 'y': -60, 'width': 30, 'height': 25, 'material': 'concrete'},
                {'x': 45, 'y': 30, 'width': 28, 'height': 22, 'material': 'brick'},
                {'x': -45, 'y': 20, 'width': 32, 'height': 20, 'material': 'glass'}
            ],
            'trees': [
                {'x': -65, 'y': -45, 'radius': 7, 'density': 0.25, 'type': 'sparse'},
                {'x': 60, 'y': -35, 'radius': 6, 'density': 0.2, 'type': 'sparse'}
            ],
            'water': [],
            'base_error': 2.50,
            'multipath_factor': 2.5,
            'signal_quality': 0.65,
            'color': '#f44336'
        }
    
    def _coastal(self) -> dict:
        return {
            'name': '🌊 Coastal',
            'buildings': [
                {'x': -45, 'y': -25, 'width': 30, 'height': 15, 'material': 'concrete'}
            ],
            'trees': [
                {'x': -30, 'y': -20, 'radius': 8, 'density': 0.3, 'type': 'sparse'}
            ],
            'water': [
                {'x': 20, 'y': 30, 'radius': 35, 'type': 'sea'},
                {'x': -10, 'y': -40, 'radius': 25, 'type': 'sea'}
            ],
            'base_error': 3.00,
            'multipath_factor': 3.0,
            'signal_quality': 0.55,
            'color': '#2196f3'
        }
    
    def get(self, env_name: str) -> dict:
        """Get environment by name"""
        return self.environments.get(env_name, self.environments['urban'])