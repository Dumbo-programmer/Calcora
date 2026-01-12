// Preprocess LaTeX for proper typesetting
function preprocessLatex(text) {
  if (!text) return text;
  
  // Replace ** with ^ for powers (must come before * replacement)
  let result = text.replace(/\*\*/g, '^');
  
  // Replace * with \cdot for multiplication
  result = result.replace(/\*/g, '\\cdot ');
  
  return result;
}

async function callAPI(expr, variable = 'x', order = 1) {
  const url = new URL(`/differentiate`, window.location.origin);
  url.searchParams.set('expr', expr);
  url.searchParams.set('variable', variable);
  url.searchParams.set('order', order);
  url.searchParams.set('format', 'json');
  url.searchParams.set('verbosity', 'detailed');

  const startTime = performance.now();
  const res = await fetch(url, { headers: { 'Accept': 'application/json' } });
  const endTime = performance.now();
  
  if (!res.ok) {
    const text = await res.text();
    let error;
    try {
      const json = JSON.parse(text);
      error = json.error || text;
    } catch {
      error = text || `HTTP ${res.status}`;
    }
    throw new Error(error);
  }
  
  const data = await res.json();
  return { data, timing: (endTime - startTime).toFixed(1) };
}

async function callMatrixAPI(operation, matrixA, matrixB = null) {
  const url = new URL(`/matrix/${operation.replace('matrix_', '')}`, window.location.origin);
  
  const body = {
    matrix: matrixA,
    format: 'json',
    verbosity: 'detailed'
  };
  
  if (matrixB && operation === 'matrix_multiply') {
    body.matrix_b = matrixB;
    body.matrix_a = matrixA;
    delete body.matrix;
  }

  const startTime = performance.now();
  const res = await fetch(url, { 
    method: 'POST',
    headers: { 
      'Content-Type': 'application/json',
      'Accept': 'application/json' 
    },
    body: JSON.stringify(body)
  });
  const endTime = performance.now();
  
  if (!res.ok) {
    const text = await res.text();
    let error;
    try {
      const json = JSON.parse(text);
      error = json.error || text;
    } catch {
      error = text || `HTTP ${res.status}`;
    }
    throw new Error(error);
  }
  
  const data = await res.json();
  return { data, timing: (endTime - startTime).toFixed(1) };
}

function pickExplanation(node, verbosity) {
  if (verbosity === 'concise') return '';
  const ex = (node.metadata && node.metadata.explanations) || null;
  if (!ex) return node.explanation || '';
  if (verbosity === 'teacher') return ex.teacher || node.explanation || '';
  return ex.detailed || node.explanation || '';
}

function formatMatrix(matrixStr) {
  try {
    const matrix = JSON.parse(matrixStr);
    if (!Array.isArray(matrix) || !Array.isArray(matrix[0])) {
      return matrixStr;
    }
    
    let html = '<table style="margin: 0 auto; border-collapse: collapse; font-family: \'JetBrains Mono\', monospace;">';
    html += '<tbody>';
    matrix.forEach((row, i) => {
      html += '<tr>';
      // Left bracket
      if (i === 0) {
        html += `<td rowspan="${matrix.length}" style="font-size: 3em; padding: 0 0.25rem; vertical-align: middle; line-height: 0.7;">⎡</td>`;
      }
      // Matrix values
      row.forEach((cell) => {
        html += `<td style="padding: 0.5rem 1rem; text-align: center; min-width: 60px; font-size: 1.2em;">${cell}</td>`;
      });
      // Right bracket
      if (i === 0) {
        html += `<td rowspan="${matrix.length}" style="font-size: 3em; padding: 0 0.25rem; vertical-align: middle; line-height: 0.7;">⎤</td>`;
      }
      html += '</tr>';
    });
    html += '</tbody></table>';
    return html;
  } catch {
    return matrixStr;
  }
}

function isMatrixString(str) {
  return str.trim().startsWith('[[') && str.trim().endsWith(']]');
}

function isEigenvalueOutput(str) {
  try {
    const data = JSON.parse(str);
    return data.eigenvalues && data.eigenvectors;
  } catch {
    return false;
  }
}

function isLUOutput(str) {
  try {
    const data = JSON.parse(str);
    return data.P && data.L && data.U;
  } catch {
    return false;
  }
}

function formatEigenvalues(outputStr) {
  try {
    const data = JSON.parse(outputStr);
    let html = '<div style="margin: 12px 0;">';
    
    // Display eigenvalues
    html += '<div style="font-weight: 600; margin-bottom: 8px;">Eigenvalues:</div>';
    html += '<ul style="margin: 4px 0 12px 20px;">';
    for (const ev of data.eigenvalues) {
      html += `<li>λ = ${ev.value} (multiplicity: ${ev.multiplicity})</li>`;
    }
    html += '</ul>';
    
    // Display eigenvectors
    html += '<div style="font-weight: 600; margin-bottom: 8px;">Eigenvectors:</div>';
    for (const [eigenval, vectors] of Object.entries(data.eigenvectors)) {
      html += `<div style="margin-left: 20px; margin-bottom: 8px;">For λ = ${eigenval}:</div>`;
      for (const vector of vectors) {
        html += '<div style="margin-left: 40px;">';
        html += formatMatrix(JSON.stringify(vector));
        html += '</div>';
      }
    }
    
    html += '</div>';
    return html;
  } catch {
    return outputStr;
  }
}

function formatLU(outputStr) {
  try {
    const data = JSON.parse(outputStr);
    let html = '<div style="margin: 12px 0;">';
    
    // Display P matrix
    html += '<div style="font-weight: 600; margin-bottom: 8px;">P (Permutation Matrix):</div>';
    html += '<div style="margin-left: 20px; margin-bottom: 12px;">';
    html += formatMatrix(JSON.stringify(data.P));
    html += '</div>';
    
    // Display L matrix
    html += '<div style="font-weight: 600; margin-bottom: 8px;">L (Lower Triangular):</div>';
    html += '<div style="margin-left: 20px; margin-bottom: 12px;">';
    html += formatMatrix(JSON.stringify(data.L));
    html += '</div>';
    
    // Display U matrix
    html += '<div style="font-weight: 600; margin-bottom: 8px;">U (Upper Triangular):</div>';
    html += '<div style="margin-left: 20px;">';
    html += formatMatrix(JSON.stringify(data.U));
    html += '</div>';
    
    html += '</div>';
    return html;
  } catch {
    return outputStr;
  }
}

function formatValue(value) {
  if (isEigenvalueOutput(value)) {
    return formatEigenvalues(value);
  }
  if (isLUOutput(value)) {
    return formatLU(value);
  }
  if (isMatrixString(value)) {
    return formatMatrix(value);
  }
  return value;
}

function renderResult(payload, verbosity, timing) {
  const resultPanel = document.getElementById('resultPanel');
  const output = document.getElementById('output');
  const stepsEl = document.getElementById('steps');
  const stepCount = document.getElementById('stepCount');
  const timingEl = document.getElementById('timing');

  // Show result panel
  resultPanel.style.display = 'block';
  
  // Store both raw and formatted output
  let formattedOutput;
  const rawOutput = payload.output ?? '(no output)';
  
  // Check if it's a matrix
  const isMatrix = rawOutput && rawOutput.includes('[') && rawOutput.includes(']');
  
  if (isEigenvalueOutput(payload.output)) {
    formattedOutput = formatEigenvalues(payload.output);
  } else if (isLUOutput(payload.output)) {
    formattedOutput = formatLU(payload.output);
  } else if (isMatrix) {
    formattedOutput = formatMatrix(payload.output);
  } else {
    formattedOutput = rawOutput;
  }
  
  // Store for format toggle
  window.currentResultData = {
    raw: rawOutput,
    formatted: formattedOutput
  };
  
  // Reset to typeset format
  window.isTypesetFormat = true;
  const badge = document.getElementById('formatBadge');
  if (badge) {
    badge.innerHTML = '<i class="fas fa-font"></i> Typeset Format';
  }
  
  // Display formatted output
  output.className = 'output-value typeset';
  if (typeof formattedOutput === 'string' && formattedOutput === rawOutput) {
    output.textContent = formattedOutput;
  } else {
    output.innerHTML = formattedOutput;
  }
  
  // Display using KaTeX or formatted HTML via displayCurrentResult
  displayCurrentResult();
  
  // Set timing
  if (timing) {
    timingEl.textContent = `${timing}ms`;
  }

  // Show graph for differentiation
  if (payload.operation === 'differentiate') {
    showGraph(payload);
  }

  // Clear and render steps
  stepsEl.innerHTML = '';
  const nodes = (payload.graph && payload.graph.nodes) || [];
  
  if (!nodes.length) {
    stepCount.textContent = 'No steps';
    const li = document.createElement('li');
    li.textContent = '(no steps — already in simplest form)';
    li.style.borderColor = 'var(--muted)';
    stepsEl.appendChild(li);
    return;
  }

  stepCount.textContent = `${nodes.length} step${nodes.length !== 1 ? 's' : ''}`;

  for (const node of nodes) {
    const li = document.createElement('li');

    const rule = document.createElement('div');
    rule.className = 'rule';
    rule.textContent = node.rule;

    const io = document.createElement('div');
    io.className = 'io';
    
    // Format input and output with matrix support
    const inputFormatted = formatValue(node.input);
    const outputFormatted = formatValue(node.output);
    io.innerHTML = `${inputFormatted}  →  ${outputFormatted}`;

    const explainText = pickExplanation(node, verbosity);
    if (explainText) {
      const explain = document.createElement('div');
      explain.className = 'explain';
      explain.textContent = explainText;
      li.appendChild(rule);
      li.appendChild(io);
      li.appendChild(explain);
    } else {
      li.appendChild(rule);
      li.appendChild(io);
    }

    stepsEl.appendChild(li);
  }
}

function setStatus(text, type = 'normal') {
  const statusEl = document.getElementById('status');
  statusEl.textContent = text;
  statusEl.className = 'status';
  if (type === 'error') {
    statusEl.classList.add('error');
  } else if (type === 'success') {
    statusEl.classList.add('success');
  }
}

async function run() {
  const operationType = document.getElementById('operationType').value;
  const verbosity = document.getElementById('verbosity').value;
  const showJson = document.getElementById('showJson').checked;

  const jsonWrap = document.getElementById('jsonWrap');
  const jsonEl = document.getElementById('json');

  setStatus('Computing...', 'normal');
  const runBtn = document.getElementById('run');
  runBtn.disabled = true;

  try {
    let payload, timing;

    if (operationType === 'differentiate') {
      const expr = document.getElementById('expr').value.trim();
      const variable = document.getElementById('variable').value.trim() || 'x';
      const order = parseInt(document.getElementById('order').value, 10);

      if (!expr) {
        setStatus('Please enter an expression', 'error');
        runBtn.disabled = false;
        return;
      }

      const result = await callAPI(expr, variable, order);
      payload = result.data;
      timing = result.timing;

      // Check if the result is 0 (likely because variable not in expression)
      if (payload.output === '0') {
        const exprLower = expr.toLowerCase();
        const varLower = variable.toLowerCase();
        if (!exprLower.includes(varLower)) {
          setStatus(`⚠ Expression doesn't contain variable '${variable}' - derivative is 0`, 'error');
        }
      }
    } else {
      // Matrix operations
      const matrixA = document.getElementById('matrixA').value.trim();
      
      if (!matrixA) {
        setStatus('Please enter Matrix A', 'error');
        runBtn.disabled = false;
        return;
      }

      let matrixB = null;
      if (operationType === 'matrix_multiply') {
        matrixB = document.getElementById('matrixB').value.trim();
        if (!matrixB) {
          setStatus('Please enter Matrix B', 'error');
          runBtn.disabled = false;
          return;
        }
      }

      const result = await callMatrixAPI(operationType, matrixA, matrixB);
      payload = result.data;
      timing = result.timing;
    }
    
    renderResult(payload, verbosity, timing);

    if (showJson) {
      jsonWrap.classList.remove('hidden');
      jsonEl.textContent = JSON.stringify(payload, null, 2);
    } else {
      jsonWrap.classList.add('hidden');
      jsonEl.textContent = '';
    }

    setStatus('✓ Complete', 'success');
  } catch (e) {
    setStatus(`Error: ${e.message}`, 'error');
    document.getElementById('resultPanel').style.display = 'none';
  } finally {
    runBtn.disabled = false;
  }
}

// Event listeners
document.getElementById('run').addEventListener('click', run);

document.getElementById('operationType').addEventListener('change', () => {
  const operationType = document.getElementById('operationType').value;
  const calcInput = document.getElementById('calcInput');
  const matrixInput = document.getElementById('matrixInput');
  const variableLabel = document.getElementById('variableLabel');
  const orderLabel = document.getElementById('orderLabel');
  const matrixBLabel = document.getElementById('matrixBLabel');

  if (operationType === 'differentiate') {
    calcInput.style.display = 'block';
    matrixInput.style.display = 'none';
    variableLabel.style.display = 'block';
    orderLabel.style.display = 'block';
  } else {
    calcInput.style.display = 'none';
    matrixInput.style.display = 'block';
    variableLabel.style.display = 'none';
    orderLabel.style.display = 'none';

    // Show/hide Matrix B based on operation
    if (operationType === 'matrix_multiply') {
      matrixBLabel.style.display = 'block';
    } else {
      matrixBLabel.style.display = 'none';
    }
  }
});

document.getElementById('showJson').addEventListener('change', () => {
  const jsonWrap = document.getElementById('jsonWrap');
  const showJson = document.getElementById('showJson').checked;
  if (showJson && jsonWrap.querySelector('#json').textContent) {
    jsonWrap.classList.remove('hidden');
  } else {
    jsonWrap.classList.add('hidden');
  }
});

document.getElementById('verbosity').addEventListener('change', () => {
  const outputEl = document.getElementById('output');
  if (outputEl.textContent && outputEl.textContent !== '(no output)') {
    // Re-render with new verbosity if we have results
    run();
  }
});

// Example buttons
document.querySelectorAll('.example-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    const expr = btn.getAttribute('data-expr');
    const variable = btn.getAttribute('data-var') || 'x';
    document.getElementById('expr').value = expr;
    document.getElementById('variable').value = variable;
    document.getElementById('operationType').value = 'differentiate';
    // Trigger change event to show correct inputs
    document.getElementById('operationType').dispatchEvent(new Event('change'));
    run();
  });
});

document.querySelectorAll('.matrix-example-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    const op = btn.getAttribute('data-op');
    const matrixA = btn.getAttribute('data-a');
    const matrixB = btn.getAttribute('data-b');
    
    document.getElementById('operationType').value = op;
    document.getElementById('matrixA').value = matrixA;
    if (matrixB) {
      document.getElementById('matrixB').value = matrixB;
    }
    
    // Trigger change event to show correct inputs
    document.getElementById('operationType').dispatchEvent(new Event('change'));
    run();
  });
});

// Ctrl/Cmd+Enter to run
document.getElementById('expr').addEventListener('keydown', (e) => {
  if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
    e.preventDefault();
    run();
  }
});

[document.getElementById('matrixA'), document.getElementById('matrixB')].forEach(el => {
  el.addEventListener('keydown', (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
      e.preventDefault();
      run();
    }
  });
});

// Auto-run on load if there's a default expression
window.addEventListener('load', () => {
  const operationType = document.getElementById('operationType').value;
  
  if (operationType === 'differentiate') {
    const expr = document.getElementById('expr').value;
    if (expr && expr.trim()) {
      run();
    }
  }
});

// Graph rendering
let currentChart = null;

function showGraph(payload) {
  const graphPanel = document.getElementById('graphPanel');
  const canvas = document.getElementById('graphCanvas');
  
  if (!graphPanel || !canvas) return;
  
  graphPanel.style.display = 'block';

  // Generate x values
  const xMin = -10;
  const xMax = 10;
  const points = 200;
  const xValues = [];
  const yOriginal = [];
  const yDerivative = [];

  for (let i = 0; i <= points; i++) {
    const x = xMin + (i / points) * (xMax - xMin);
    xValues.push(x);
    
    try {
      const originalValue = evaluateExpression(payload.input, x);
      const derivativeValue = evaluateExpression(payload.output, x);
      yOriginal.push(originalValue);
      yDerivative.push(derivativeValue);
    } catch (e) {
      yOriginal.push(null);
      yDerivative.push(null);
    }
  }

  if (currentChart) {
    currentChart.destroy();
  }

  const isDark = document.body.classList.contains('dark-theme');
  const ctx = canvas.getContext('2d');
  
  currentChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: xValues,
      datasets: [
        {
          label: `f(x) = ${payload.input}`,
          data: yOriginal,
          borderColor: '#6366f1',
          backgroundColor: 'rgba(99, 102, 241, 0.1)',
          borderWidth: 3,
          tension: 0.4,
          pointRadius: 0
        },
        {
          label: `f'(x) = ${payload.output}`,
          data: yDerivative,
          borderColor: '#10b981',
          backgroundColor: 'rgba(16, 185, 129, 0.1)',
          borderWidth: 3,
          tension: 0.4,
          pointRadius: 0
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: true,
          labels: {
            color: isDark ? '#e5e7eb' : '#0f172a',
            font: { size: 14, family: 'JetBrains Mono' }
          }
        },
        tooltip: {
          enabled: true,
          mode: 'index',
          intersect: false
        }
      },
      scales: {
        x: {
          type: 'linear',
          grid: { color: isDark ? '#334155' : '#e2e8f0' },
          ticks: { color: isDark ? '#cbd5e1' : '#64748b' }
        },
        y: {
          grid: { color: isDark ? '#334155' : '#e2e8f0' },
          ticks: { color: isDark ? '#cbd5e1' : '#64748b' }
        }
      }
    }
  });
}

function evaluateExpression(expr, x) {
  let evaluated = expr.replace(/x/g, `(${x})`);
  
  // Replace ** with Math.pow
  evaluated = evaluated.replace(/(\d+\.?\d*)\*\*(\d+\.?\d*)/g, 'Math.pow($1,$2)');
  evaluated = evaluated.replace(/\(([^)]+)\)\*\*(\d+\.?\d*)/g, 'Math.pow($1,$2)');
  
  // Replace trigonometric functions
  evaluated = evaluated.replace(/\bsin\b/g, 'Math.sin');
  evaluated = evaluated.replace(/\bcos\b/g, 'Math.cos');
  evaluated = evaluated.replace(/\btan\b/g, 'Math.tan');
  
  // Replace inverse trig functions
  evaluated = evaluated.replace(/\basin\b/g, 'Math.asin');
  evaluated = evaluated.replace(/\bacos\b/g, 'Math.acos');
  evaluated = evaluated.replace(/\batan\b/g, 'Math.atan');
  
  // Replace hyperbolic functions
  evaluated = evaluated.replace(/\bsinh\b/g, 'Math.sinh');
  evaluated = evaluated.replace(/\bcosh\b/g, 'Math.cosh');
  evaluated = evaluated.replace(/\btanh\b/g, 'Math.tanh');
  evaluated = evaluated.replace(/\basinh\b/g, 'Math.asinh');
  evaluated = evaluated.replace(/\bacosh\b/g, 'Math.acosh');
  evaluated = evaluated.replace(/\batanh\b/g, 'Math.atanh');
  
  // Replace other functions
  evaluated = evaluated.replace(/\bexp\b/g, 'Math.exp');
  evaluated = evaluated.replace(/\blog\b/g, 'Math.log');
  evaluated = evaluated.replace(/\bsqrt\b/g, 'Math.sqrt');
  evaluated = evaluated.replace(/\bAbs\b/g, 'Math.abs');
  evaluated = evaluated.replace(/\babs\b/g, 'Math.abs');
  
  // Replace constants
  evaluated = evaluated.replace(/\bpi\b/g, 'Math.PI');
  evaluated = evaluated.replace(/\be\b(?!\d)/g, 'Math.E');
  
  try {
    return eval(evaluated);
  } catch (e) {
    return null;
  }
}
