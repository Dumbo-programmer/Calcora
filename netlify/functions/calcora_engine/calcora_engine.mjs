import { spawn } from 'child_process';

export default async (request, context) => {
  // Handle CORS preflight
  if (request.method === 'OPTIONS') {
    return new Response('', {
      status: 204,
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
      },
    });
  }

  // Only allow POST
  if (request.method !== 'POST') {
    return new Response(JSON.stringify({ error: 'Only POST is supported' }), {
      status: 405,
      headers: { 'Content-Type': 'application/json' },
    });
  }

  try {
    const body = await request.json();
    const { operation = 'differentiate', expression, variable = 'x', verbosity = 'detailed', matrix_b } = body;

    if (!expression) {
      return new Response(JSON.stringify({ error: 'Missing required field: expression' }), {
        status: 400,
        headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' },
      });
    }

    // Build Python command
    let cmd = ['python', '-m', 'calcora', operation, expression];
    
    if (operation === 'differentiate') {
      cmd.push('--variable', variable);
    }
    
    if (operation === 'matrix_multiply' && matrix_b) {
      cmd.push('--matrix-b', matrix_b);
    }
    
    cmd.push('--verbosity', verbosity, '--format', 'json');

    // Execute Python command
    const result = await new Promise((resolve, reject) => {
      const process = spawn(cmd[0], cmd.slice(1));
      let stdout = '';
      let stderr = '';

      process.stdout.on('data', (data) => {
        stdout += data.toString();
      });

      process.stderr.on('data', (data) => {
        stderr += data.toString();
      });

      process.on('close', (code) => {
        if (code !== 0) {
          reject(new Error(stderr || `Process exited with code ${code}`));
        } else {
          resolve(stdout);
        }
      });

      process.on('error', (err) => {
        reject(err);
      });
    });

    return new Response(result, {
      status: 200,
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
      },
    });

  } catch (error) {
    return new Response(JSON.stringify({ error: error.message }), {
      status: 500,
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
      },
    });
  }
};
