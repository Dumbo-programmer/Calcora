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
import sympy as sp

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


def _validate_verbosity(verbosity: str) -> str | None:
    if verbosity not in ('concise', 'detailed', 'teacher'):
        return f"Invalid verbosity '{verbosity}'. Valid options: concise, detailed, teacher"
    return None


def _parse_multivariable_expression(expression: str, variables: list[str]):
    if not expression or not expression.strip():
        raise ValueError("Missing required field 'expression'")
    if not variables:
        raise ValueError("Missing required field 'variables' (example: ['x','y'])")

    symbols = [sp.Symbol(v.strip()) for v in variables if v and v.strip()]
    if not symbols:
        raise ValueError('Variables list cannot be empty')

    local_symbols = {str(sym): sym for sym in symbols}
    expr = sp.sympify(expression, locals=local_symbols)
    return expr, symbols


def _evaluation_subs(point: dict[str, float] | None, symbols: list[sp.Symbol]):
    if not point:
        return None
    subs = {}
    for sym in symbols:
        name = str(sym)
        if name not in point:
            raise ValueError(f"Point missing coordinate '{name}'")
        subs[sym] = point[name]
    return subs


def _parse_equation_or_expression(expression: str):
    if '=' in expression:
        left, right = expression.split('=', 1)
        left_expr = sp.sympify(left.strip())
        right_expr = sp.sympify(right.strip())
        return sp.Eq(left_expr, right_expr)
    return sp.sympify(expression)

@app.route('/')
def index():
    return send_from_directory(STATIC_FOLDER, 'index.html')


@app.route('/favicon.ico')
def favicon():
    icon_dir = os.path.join(os.path.dirname(__file__), 'media')
    icon_path = os.path.join(icon_dir, 'calcora-icon.ico')
    if os.path.exists(icon_path):
        return send_from_directory(icon_dir, 'calcora-icon.ico', mimetype='image/x-icon')
    return '', 204

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
        lower_limit = request.args.get('lower_limit', request.args.get('lower', None))
        upper_limit = request.args.get('upper_limit', request.args.get('upper', None))
        verbosity = request.args.get('verbosity', 'detailed')

        err = _validate_verbosity(verbosity)
        if err:
            return jsonify({'error': err}), 400
        
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
        data = request.get_json(silent=True) or {}
        
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
        err = _validate_verbosity(verbosity)
        if err:
            return jsonify({'error': err}), 400
        
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
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/multivariable/partial', methods=['POST', 'OPTIONS'])
def multivariable_partial():
    if request.method == 'OPTIONS':
        return '', 204
    try:
        req = request.get_json(silent=True) or {}
        verbosity = req.get('verbosity', 'detailed')
        err = _validate_verbosity(verbosity)
        if err:
            return jsonify({'error': err}), 400

        expr, symbols = _parse_multivariable_expression(req.get('expression', ''), req.get('variables', []))
        target = symbols[0]
        derivative = sp.diff(expr, target)
        subs = _evaluation_subs(req.get('point'), symbols)

        payload = {
            'operation': 'partial_derivative',
            'input': req.get('expression', ''),
            'variable': str(target),
            'variables': [str(s) for s in symbols],
            'output': str(derivative),
            'steps': [
                {
                    'rule': 'Partial differentiation',
                    'before': str(expr),
                    'after': str(derivative),
                    'explanation': f'Differentiate with respect to {target} while treating other variables as constants.'
                }
            ]
        }
        if subs:
            payload['evaluated_at_point'] = str(sp.N(derivative.subs(subs)))
            payload['point'] = req.get('point')
        return jsonify(payload), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/multivariable/gradient', methods=['POST', 'OPTIONS'])
def multivariable_gradient():
    if request.method == 'OPTIONS':
        return '', 204
    try:
        req = request.get_json(silent=True) or {}
        verbosity = req.get('verbosity', 'detailed')
        err = _validate_verbosity(verbosity)
        if err:
            return jsonify({'error': err}), 400

        expr, symbols = _parse_multivariable_expression(req.get('expression', ''), req.get('variables', []))
        grad = [sp.diff(expr, s) for s in symbols]
        subs = _evaluation_subs(req.get('point'), symbols)

        payload = {
            'operation': 'gradient',
            'input': req.get('expression', ''),
            'variables': [str(s) for s in symbols],
            'output': json.dumps([str(g) for g in grad]),
            'gradient': [str(g) for g in grad],
            'steps': [
                {
                    'rule': 'Gradient operator',
                    'before': str(expr),
                    'after': '[' + ', '.join(str(g) for g in grad) + ']',
                    'explanation': 'Compute all first-order partial derivatives to form the gradient vector.'
                }
            ]
        }
        if subs:
            payload['gradient_at_point'] = [str(sp.N(g.subs(subs))) for g in grad]
            payload['point'] = req.get('point')
        return jsonify(payload), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/multivariable/directional', methods=['POST', 'OPTIONS'])
def multivariable_directional():
    if request.method == 'OPTIONS':
        return '', 204
    try:
        req = request.get_json(silent=True) or {}
        verbosity = req.get('verbosity', 'detailed')
        err = _validate_verbosity(verbosity)
        if err:
            return jsonify({'error': err}), 400

        expr, symbols = _parse_multivariable_expression(req.get('expression', ''), req.get('variables', []))
        point = req.get('point')
        direction = req.get('direction')
        if not point:
            return jsonify({'error': "Directional derivative requires 'point' with values for all variables"}), 400
        if not direction:
            return jsonify({'error': "Directional derivative requires 'direction' vector"}), 400
        if len(direction) != len(symbols):
            return jsonify({'error': 'Direction vector length must match number of variables'}), 400

        subs = _evaluation_subs(point, symbols)
        grad = [sp.diff(expr, s) for s in symbols]
        grad_at_point = [sp.N(g.subs(subs)) for g in grad]

        direction_vec = sp.Matrix(direction)
        norm = sp.sqrt(sum(c ** 2 for c in direction_vec))
        if norm == 0:
            return jsonify({'error': 'Direction vector cannot be zero'}), 400
        unit_direction = direction_vec / norm
        directional_value = sp.N(sp.Matrix(grad_at_point).dot(unit_direction))

        payload = {
            'operation': 'directional_derivative',
            'input': req.get('expression', ''),
            'variables': [str(s) for s in symbols],
            'point': point,
            'direction': direction,
            'output': str(directional_value),
            'gradient_at_point': [str(v) for v in grad_at_point],
            'unit_direction': [str(sp.N(v)) for v in unit_direction],
            'steps': [
                {
                    'rule': 'Directional derivative',
                    'before': 'grad(f) dot u',
                    'after': str(directional_value),
                    'explanation': 'Evaluate gradient at the point and dot it with the normalized direction vector.'
                }
            ]
        }
        return jsonify(payload), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/multivariable/jacobian', methods=['POST', 'OPTIONS'])
def multivariable_jacobian():
    if request.method == 'OPTIONS':
        return '', 204
    try:
        req = request.get_json(silent=True) or {}
        verbosity = req.get('verbosity', 'detailed')
        err = _validate_verbosity(verbosity)
        if err:
            return jsonify({'error': err}), 400

        expressions = req.get('expressions')
        variables = req.get('variables')
        point = req.get('point')
        if not expressions or not isinstance(expressions, list):
            return jsonify({'error': "Missing required field 'expressions' as a list"}), 400
        if not variables or not isinstance(variables, list):
            return jsonify({'error': "Missing required field 'variables' as a list"}), 400

        symbols = [sp.Symbol(v.strip()) for v in variables if v and v.strip()]
        local_symbols = {str(sym): sym for sym in symbols}
        funcs = [sp.sympify(e, locals=local_symbols) for e in expressions]
        jac = sp.Matrix(funcs).jacobian(symbols)

        payload = {
            'operation': 'jacobian',
            'inputs': expressions,
            'variables': [str(s) for s in symbols],
            'output': json.dumps([[str(cell) for cell in row] for row in jac.tolist()]),
            'jacobian': [[str(cell) for cell in row] for row in jac.tolist()],
            'steps': [
                {
                    'rule': 'Jacobian matrix',
                    'before': 'Vector function',
                    'after': 'Matrix of first-order partial derivatives',
                    'explanation': 'Differentiate each component function with respect to each variable.'
                }
            ]
        }

        if point:
            subs = {}
            for sym in symbols:
                name = str(sym)
                if name not in point:
                    return jsonify({'error': f"Point missing coordinate '{name}'"}), 400
                subs[sym] = point[name]
            jac_num = jac.subs(subs)
            payload['point'] = point
            payload['jacobian_at_point'] = [[str(sp.N(cell)) for cell in row] for row in jac_num.tolist()]

        return jsonify(payload), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/symbolic/compute', methods=['POST', 'OPTIONS'])
def symbolic_compute():
    if request.method == 'OPTIONS':
        return '', 204
    try:
        req = request.get_json(silent=True) or {}
        verbosity = req.get('verbosity', 'detailed')
        err = _validate_verbosity(verbosity)
        if err:
            return jsonify({'error': err}), 400

        operation = (req.get('operation') or '').strip().lower()
        expression = (req.get('expression') or '').strip()
        variable = (req.get('variable') or 'x').strip()
        point = req.get('point')
        order = int(req.get('order', 5))

        if not operation:
            return jsonify({'error': "Missing required field 'operation'"}), 400
        if not expression:
            return jsonify({'error': "Missing required field 'expression'"}), 400

        x = sp.Symbol(variable)
        parsed = _parse_equation_or_expression(expression)

        if operation == 'algebra_simplify':
            output = sp.simplify(parsed)
            explanation = 'Applied symbolic simplification rules.'
        elif operation == 'algebra_expand':
            output = sp.expand(parsed)
            explanation = 'Expanded products and powers into polynomial form where possible.'
        elif operation == 'algebra_factor':
            output = sp.factor(parsed)
            explanation = 'Factored the expression into irreducible symbolic factors.'
        elif operation == 'algebra_solve':
            output = sp.solve(parsed, x)
            explanation = f'Solved for variable {x}.'
        elif operation == 'calculus_limit':
            if point is None:
                return jsonify({'error': "calculus_limit requires 'point'"}), 400
            output = sp.limit(parsed, x, point)
            explanation = f'Computed limit as {x} approaches {point}.'
        elif operation == 'calculus_taylor':
            series_point = 0 if point is None else point
            safe_order = max(1, min(order, 20))
            output = sp.series(parsed, x, series_point, safe_order + 1).removeO()
            explanation = f'Computed Taylor polynomial around {x}={series_point} up to degree {safe_order}.'
        elif operation == 'calculus_tangent_line':
            if point is None:
                return jsonify({'error': "calculus_tangent_line requires 'point'"}), 400
            f_point = sp.simplify(parsed.subs(x, point))
            slope = sp.simplify(sp.diff(parsed, x).subs(x, point))
            output = sp.expand(slope * (x - point) + f_point)
            explanation = f"Computed tangent line at {x}={point} using y = f(a) + f'(a)(x-a)."
        else:
            return jsonify({'error': f'Unknown symbolic operation: {operation}'}), 400

        payload = {
            'operation': operation,
            'input': expression,
            'variable': str(x),
            'output': str(output),
            'steps': [
                {
                    'rule': operation,
                    'before': expression,
                    'after': str(output),
                    'explanation': explanation,
                }
            ],
        }
        return jsonify(payload), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/<path:path>')
def serve_static(path):
    # Don't serve API routes as static files
    if (
        path.startswith('api/')
        or path.startswith('.netlify/')
        or path.startswith('differentiate')
        or path.startswith('integrate')
        or path.startswith('matrix/')
        or path.startswith('multivariable/')
        or path.startswith('symbolic/')
        or path.startswith('favicon.ico')
    ):
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
