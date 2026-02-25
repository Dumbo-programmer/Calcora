"""
Simple Flask API server for Calcora - can be deployed to Render/Railway/PythonAnywhere
"""
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from calcora.bootstrap import default_engine
from calcora.renderers.json_renderer import JsonRenderer
import json
import os
import sys

# Determine static folder location (dev vs PyInstaller bundle)
if getattr(sys, 'frozen', False):
    # Running as PyInstaller bundle - use bundled web folder
    STATIC_FOLDER = os.path.join(sys._MEIPASS, 'web')
else:
    # Running as script - use src/calcora/web for actual app
    # For production deployment (Netlify): use 'site' directory
    STATIC_FOLDER = os.environ.get('CALCORA_STATIC_FOLDER', 'src/calcora/web')

app = Flask(__name__, static_folder=STATIC_FOLDER, static_url_path='/static')
CORS(app)

@app.route('/')
def index():
    return send_from_directory(STATIC_FOLDER, 'index.html')

# GET endpoint for differentiate (used by src/calcora/web/app.js)
@app.route('/differentiate', methods=['GET', 'OPTIONS'])
def differentiate_get():
    if request.method == 'OPTIONS':
        return '', 204
    
    try:
        expr = request.args.get('expr')
        variable = request.args.get('variable', 'x')
        order = int(request.args.get('order', 1))
        verbosity = request.args.get('verbosity', 'detailed')
        
        if not expr:
            return jsonify({'error': 'Missing required parameter: expr'}), 400
        
        engine = default_engine(load_entry_points=True)
        result = engine.run(
            operation='differentiate',
            expression=expr,
            variable=variable,
            order=order
        )
        
        renderer = engine.registry.get_renderer(format='json') or JsonRenderer()
        rendered = renderer.render(result=result, format='json', verbosity=verbosity)
        response_data = json.loads(rendered) if isinstance(rendered, str) else rendered
        
        return jsonify(response_data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# GET endpoint for integrate (used by src/calcora/web/app.js)
@app.route('/integrate', methods=['GET', 'OPTIONS'])
def integrate_get():
    if request.method == 'OPTIONS':
        return '', 204
    
    try:
        from calcora.integration_engine import IntegrationEngine
        
        expr = request.args.get('expr')
        variable = request.args.get('variable', 'x')
        lower_limit = request.args.get('lower', None)
        upper_limit = request.args.get('upper', None)
        verbosity = request.args.get('verbosity', 'detailed')
        
        if not expr:
            return jsonify({'error': 'Missing required parameter: expr'}), 400
        
        # Convert limits to float if provided
        if lower_limit is not None and lower_limit != '':
            lower_limit = float(lower_limit)
        else:
            lower_limit = None
            
        if upper_limit is not None and upper_limit != '':
            upper_limit = float(upper_limit)
        else:
            upper_limit = None
        
        int_engine = IntegrationEngine()
        result = int_engine.integrate(
            expression=expr,
            variable=variable,
            lower_limit=lower_limit,
            upper_limit=upper_limit,
            verbosity=verbosity,
            generate_graph=True
        )
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# POST endpoints for matrix operations (used by src/calcora/web/app.js)
@app.route('/matrix/<operation>', methods=['POST', 'OPTIONS'])
def matrix_operation(operation):
    if request.method == 'OPTIONS':
        return '', 204
    
    try:
        data = request.get_json()
        
        # For multiply: app.js sends matrix_a and matrix_b
        # For other ops: app.js sends matrix
        if operation == 'multiply':
            matrix = data.get('matrix_a') or data.get('matrix')
            matrix_b = data.get('matrix_b')
            if not matrix or not matrix_b:
                return jsonify({'error': 'matrix_multiply requires matrix_a and matrix_b'}), 400
        else:
            matrix = data.get('matrix')
            if not matrix:
                return jsonify({'error': 'Missing required field: matrix'}), 400
        
        verbosity = data.get('verbosity', 'detailed')
        
        engine = default_engine(load_entry_points=True)
        
        # Map URL operation to engine operation
        op_map = {
            'multiply': 'matrix_multiply',
            'determinant': 'matrix_determinant',
            'inverse': 'matrix_inverse',
            'rref': 'matrix_rref',
            'eigenvalues': 'matrix_eigenvalues',
            'lu': 'matrix_lu'
        }
        
        engine_op = op_map.get(operation)
        if not engine_op:
            return jsonify({'error': f'Unsupported matrix operation: {operation}'}), 400
        
        kwargs = {'operation': engine_op, 'expression': matrix}
        
        if operation == 'multiply':
            kwargs['matrix_b'] = matrix_b
        
        result = engine.run(**kwargs)
        
        renderer = engine.registry.get_renderer(format='json') or JsonRenderer()
        rendered = renderer.render(result=result, format='json', verbosity=verbosity)
        response_data = json.loads(rendered) if isinstance(rendered, str) else rendered
        
        return jsonify(response_data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/<path:path>')
def serve_static(path):
    # Don't serve API routes as static files
    if path.startswith('api/') or path.startswith('.netlify/') or path.startswith('differentiate') or path.startswith('integrate') or path.startswith('matrix/'):
        return '', 404
    return send_from_directory(STATIC_FOLDER, path)

@app.route('/.netlify/functions/calcora_engine', methods=['POST', 'OPTIONS'])
@app.route('/api/compute', methods=['POST', 'OPTIONS'])
def compute():
    if request.method == 'OPTIONS':
        return '', 204
    
    try:
        data = request.get_json()
        operation = data.get('operation', 'differentiate')
        expression = data.get('expression')
        
        if not expression:
            return jsonify({'error': 'Missing required field: expression'}), 400
        
        verbosity = data.get('verbosity', 'detailed')
        engine = default_engine(load_entry_points=True)
        
        if operation == 'differentiate':
            variable = data.get('variable', 'x')
            order = int(data.get('order', 1))
            result = engine.run(
                operation='differentiate',
                expression=expression,
                variable=variable,
                order=order
            )
        elif operation == 'integrate':
            # New integration endpoint
            from calcora.integration_engine import IntegrationEngine
            
            variable = data.get('variable', 'x')
            lower_limit = data.get('lower_limit')
            upper_limit = data.get('upper_limit')
            
            # Convert string limits to float if provided
            if lower_limit is not None:
                try:
                    lower_limit = float(lower_limit)
                except ValueError:
                    return jsonify({'error': f'Invalid lower limit: {lower_limit}'}), 400
            
            if upper_limit is not None:
                try:
                    upper_limit = float(upper_limit)
                except ValueError:
                    return jsonify({'error': f'Invalid upper limit: {upper_limit}'}), 400
            
            int_engine = IntegrationEngine()
            result = int_engine.integrate(
                expression=expression,
                variable=variable,
                lower_limit=lower_limit,
                upper_limit=upper_limit,
                verbosity=verbosity,
                generate_graph=True
            )
            
            return jsonify(result), 200
            
        elif operation in ('matrix_multiply', 'matrix_determinant', 'matrix_inverse',
                          'matrix_rref', 'matrix_eigenvalues', 'matrix_lu'):
            kwargs = {'operation': operation, 'expression': expression}
            if operation == 'matrix_multiply':
                matrix_b = data.get('matrix_b')
                if not matrix_b:
                    return jsonify({'error': 'matrix_multiply requires matrix_b'}), 400
                kwargs['matrix_b'] = matrix_b
            result = engine.run(**kwargs)
        else:
            return jsonify({'error': f'Unsupported operation: {operation}'}), 400
        
        renderer = engine.registry.get_renderer(format='json') or JsonRenderer()
        rendered = renderer.render(result=result, format='json', verbosity=verbosity)
        
        # Parse the JSON string to ensure proper format
        response_data = json.loads(rendered) if isinstance(rendered, str) else rendered
        
        return jsonify(response_data), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/shutdown', methods=['POST', 'OPTIONS'])
def shutdown():
    """
    Gracefully shutdown the server (desktop mode only).
    
    This endpoint is only functional when running via calcora_desktop.py
    and should only be accessible from localhost.
    """
    if request.method == 'OPTIONS':
        return '', 204
    
    # Security: Only allow shutdown from localhost
    if request.remote_addr not in ('127.0.0.1', 'localhost', '::1'):
        return jsonify({'error': 'Shutdown only allowed from localhost'}), 403
    
    # Attempt graceful shutdown
    try:
        # Method 1: Try werkzeug's shutdown function (if available)
        shutdown_func = request.environ.get('werkzeug.server.shutdown')
        if shutdown_func:
            shutdown_func()
            return jsonify({'message': 'Server shutting down...'}), 200
        
        # Method 2: For newer Werkzeug versions, use os._exit as last resort
        # This is intentionally delayed to allow the response to be sent
        import signal
        import os
        import threading
        
        def delayed_shutdown():
            import time
            time.sleep(0.5)  # Allow response to be sent
            os.kill(os.getpid(), signal.SIGTERM)
        
        threading.Thread(target=delayed_shutdown, daemon=True).start()
        return jsonify({'message': 'Server shutting down...'}), 200
        
    except Exception as e:
        return jsonify({'error': f'Shutdown failed: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
