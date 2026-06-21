"""
GNSS PROFESSIONAL SUITE - Main Application
IGS Standards | ITU-R Compliant | RTK Ready
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from datetime import datetime
import math

from config import Config
from models.gnss_constellation import GNSSConstellation
from models.multipath_engine import MultipathEngine
from models.environment import EnvironmentModel
from algorithms.rtk_engine import RTKEngine
from algorithms.statistical import StatisticalAnalysis

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

# Initialize directories
Config.init_directories()

# Initialize engines
gnss = GNSSConstellation()
multipath = MultipathEngine()
env_model = EnvironmentModel()
rtk = RTKEngine()
stats = StatisticalAnalysis()

# ==============================================
# HELPER FUNCTIONS
# ==============================================

def calculate_building_error(building, x, y):
    dist = math.hypot(x - building['x'], y - building['y'])
    if dist < building['width']:
        return multipath.calculate_building_multipath(
            dist, building['height'], building['width'], 
            building.get('material', 'concrete')
        )
    return 0.0

def calculate_tree_error(tree, x, y):
    dist = math.hypot(x - tree['x'], y - tree['y'])
    if dist < tree['radius']:
        return multipath.vegetation_attenuation(
            tree['radius'] - dist, tree['density'], 
            tree.get('type', 'medium')
        )
    return 0.0

def calculate_water_error(water, x, y):
    dist = math.hypot(x - water['x'], y - water['y'])
    if dist < water['radius']:
        return multipath.water_reflection(
            dist, water['radius'], water.get('type', 'lake')
        )
    return 0.0

def calculate_total_error(x, y, env_name):
    env = env_model.get(env_name)
    
    # Calculate errors
    building_error = 0
    buildings_affected = 0
    for b in env['buildings']:
        err = calculate_building_error(b, x, y)
        if err > 0:
            building_error += err
            buildings_affected += 1
    
    tree_error = 0
    trees_affected = 0
    for t in env['trees']:
        err = calculate_tree_error(t, x, y)
        if err > 0:
            tree_error += err
            trees_affected += 1
    
    water_error = 0
    water_affected = 0
    for w in env['water']:
        err = calculate_water_error(w, x, y)
        if err > 0:
            water_error += err
            water_affected += 1
    
    # Get satellites and DOP
    visible_sats = gnss.get_visible_satellites(15)
    dop = gnss.calculate_dop(visible_sats)
    
    # Calculate total error
    total_multipath = building_error + tree_error + water_error + env['multipath_factor']
    base_error = env['base_error'] * (1 + buildings_affected * 0.1)
    dop_contribution = (dop['GDOP'] - 1) * 0.4
    total_error = base_error + total_multipath + dop_contribution
    total_error = max(0.5, min(15.0, total_error))
    
    # RTK solution
    rtk_solution = rtk.calculate_solution(len(visible_sats), total_multipath)
    
    # Signal data
    signal_data = []
    for sat in visible_sats[:8]:
        if sat['elevation'] > 45:
            quality = 'good'
        elif sat['elevation'] > 25:
            quality = 'moderate'
        else:
            quality = 'poor'
        
        snr = sat['signal_strength'] - (total_multipath * 2)
        snr = max(20, min(55, snr))
        
        signal_data.append({
            'name': sat['name'],
            'constellation': sat['constellation'],
            'snr': round(snr, 1),
            'elevation': sat['elevation'],
            'quality': quality
        })
    
    result = {
        'total_error': round(total_error, 2),
        'multipath_error': round(total_multipath, 2),
        'building_error': round(building_error, 2),
        'tree_error': round(tree_error, 2),
        'water_error': round(water_error, 2),
        'base_error': round(base_error, 2),
        'gdop': dop['GDOP'],
        'pdop': dop['PDOP'],
        'hdop': dop['HDOP'],
        'vdop': dop['VDOP'],
        'visible_satellites': len(visible_sats),
        'signal_quality': round(env['signal_quality'] * 100, 1),
        'signal_data': signal_data,
        'rtk': rtk_solution,
        'buildings_affected': buildings_affected,
        'trees_affected': trees_affected,
        'water_affected': water_affected,
        'environment': env['name'],
        'environment_color': env['color'],
        'timestamp': datetime.now().strftime('%H:%M:%S')
    }
    
    stats.add_measurement(result)
    return result

# ==============================================
# FLASK ROUTES
# ==============================================

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/calculate', methods=['POST'])
def calculate():
    data = request.json
    x = float(data.get('x', 0))
    y = float(data.get('y', 0))
    environment = data.get('environment', 'urban')
    result = calculate_total_error(x, y, environment)
    return jsonify(result)

@app.route('/api/stats', methods=['GET'])
def get_stats():
    return jsonify(stats.get_statistics())

# ==============================================
# MAIN
# ==============================================

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
    print("="*60)
    print("  GNSS PROFESSIONAL SUITE v1.0")
    print("  IGS Standards | ITU-R Compliant | RTK Ready")
    print("="*60)
    print("\n✅ Server starting...")
    print("🌐 Open your browser: http://127.0.0.1:5000")
    print("🛑 Press CTRL+C to stop\n")
    print("="*60)
    app.run(debug=True, host='127.0.0.1', port=5000)
