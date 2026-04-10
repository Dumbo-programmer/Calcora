// Preprocess LaTeX for proper typesetting
function preprocessLatex(text) {
  if (!text) return text;

  function replaceFunctionCalls(input, functionName, formatter) {
    const token = `${functionName}(`;
    let result = '';
    let i = 0;

    while (i < input.length) {
      const start = input.indexOf(token, i);
      if (start === -1) {
        result += input.slice(i);
        break;
      }

      result += input.slice(i, start);
      let j = start + token.length;
      let depth = 1;

      while (j < input.length && depth > 0) {
        if (input[j] === '(') depth += 1;
        if (input[j] === ')') depth -= 1;
        j += 1;
      }

      if (depth !== 0) {
        result += input.slice(start);
        break;
      }

      const inner = input.slice(start + token.length, j - 1);
      result += formatter(inner);
      i = j;
    }

    return result;
  }

  let result = String(text).trim();
  result = result.replace(/\*\*/g, '^');
  result = result.replace(/\bpi\b/g, '\\pi');
  result = result.replace(/\boo\b/g, '\\infty');
  result = result.replace(/\basin\(/g, '\\arcsin(');
  result = result.replace(/\bacos\(/g, '\\arccos(');
  result = result.replace(/\batan\(/g, '\\arctan(');
  result = result.replace(/\bsin\(/g, '\\sin(');
  result = result.replace(/\bcos\(/g, '\\cos(');
  result = result.replace(/\btan\(/g, '\\tan(');
  result = result.replace(/\bsec\(/g, '\\sec(');
  result = result.replace(/\bcsc\(/g, '\\csc(');
  result = result.replace(/\bcot\(/g, '\\cot(');
  result = result.replace(/\bsinh\(/g, '\\sinh(');
  result = result.replace(/\bcosh\(/g, '\\cosh(');
  result = result.replace(/\btanh\(/g, '\\tanh(');
  result = result.replace(/\blog\(/g, '\\ln(');
  result = replaceFunctionCalls(result, 'sqrt', (inner) => `\\sqrt{${inner}}`);
  result = replaceFunctionCalls(result, 'exp', (inner) => `e^{${inner}}`);
  result = result.replace(/\*/g, ' \\cdot ');
  result = result.replace(/\s+/g, ' ').trim();
  return result;
}

const TOOL_CONTEXT = {
  differentiate: {
    title: 'Differentiation',
    theory: 'Derivative as an instantaneous rate of change; dy/dx is slope of the tangent line.',
    wiki: 'https://en.wikipedia.org/wiki/Derivative',
    chapter: 'Anton Calculus: Differentiation chapters',
    chapterLink: 'https://archive.org/details/calculus0000anto_z8c2',
    applications: [
      'Velocity from position data and acceleration from velocity.',
      'Optimization in economics: maximizing profit and minimizing cost.'
    ]
  },
  integrate: {
    title: 'Integration',
    theory: 'Integral as accumulation and signed area under a curve.',
    wiki: 'https://en.wikipedia.org/wiki/Integral',
    chapter: 'Anton Calculus: Integration chapters',
    chapterLink: 'https://archive.org/details/calculus0000anto_z8c2',
    applications: [
      'Work and energy accumulation in mechanics.',
      'Total flow, charge, or population accumulation over time.'
    ]
  },
  calculus_limit: {
    title: 'Limit',
    theory: 'Limit describes function behavior near a point and underpins continuity and derivatives.',
    wiki: 'https://en.wikipedia.org/wiki/Limit_(mathematics)',
    chapter: 'Anton Calculus: Limits and continuity (early chapters)',
    chapterLink: 'https://archive.org/details/calculus0000anto_z8c2',
    applications: [
      'Modeling asymptotic behavior in engineering systems.',
      'Continuity checks in physical models near critical points.'
    ]
  },
  calculus_taylor: {
    title: 'Taylor Polynomial',
    theory: 'Taylor expansion approximates nonlinear behavior locally using derivatives at a point.',
    wiki: 'https://en.wikipedia.org/wiki/Taylor_series',
    chapter: 'Anton Calculus: Series and polynomial approximations',
    chapterLink: 'https://archive.org/details/calculus0000anto_z8c2',
    applications: [
      'Approximation for fast scientific computation.',
      'Model linearization in control and robotics.'
    ]
  },
  calculus_tangent_line: {
    title: 'Tangent Line',
    theory: 'Tangent line is the local linear approximation using slope dy/dx at a point.',
    wiki: 'https://en.wikipedia.org/wiki/Tangent',
    chapter: 'Anton Calculus: Derivative as slope',
    chapterLink: 'https://archive.org/details/calculus0000anto_z8c2',
    applications: [
      'Linear approximation around operating points.',
      'Geometric interpretation of instantaneous rate.'
    ]
  },
  algebra_simplify: {
    title: 'Simplify',
    theory: 'Symbolic simplification rewrites expressions into equivalent compact forms.',
    wiki: 'https://en.wikipedia.org/wiki/Simplification_of_algebraic_expressions',
    chapter: 'Anton algebra prerequisites: symbolic manipulation',
    chapterLink: 'https://archive.org/details/calculus0000anto_z8c2',
    applications: [
      'Reducing symbolic complexity in derivations.',
      'Improving readability of analytical solutions.'
    ]
  },
  algebra_expand: {
    title: 'Expand',
    theory: 'Expansion distributes products and powers to explicit polynomial forms.',
    wiki: 'https://en.wikipedia.org/wiki/Polynomial',
    chapter: 'Anton algebra prerequisites: polynomial operations',
    chapterLink: 'https://archive.org/details/calculus0000anto_z8c2',
    applications: [
      'Preparing expressions for term-wise integration or differentiation.',
      'Canonical forms in computer algebra pipelines.'
    ]
  },
  algebra_factor: {
    title: 'Factor',
    theory: 'Factoring expresses expressions as multiplicative structure for roots and simplification.',
    wiki: 'https://en.wikipedia.org/wiki/Factorization',
    chapter: 'Anton algebra prerequisites: factoring techniques',
    chapterLink: 'https://archive.org/details/calculus0000anto_z8c2',
    applications: [
      'Root finding and intercept analysis.',
      'Partial fraction preparation.'
    ]
  },
  algebra_solve: {
    title: 'Solve Equation',
    theory: 'Solving equations finds variable values that satisfy symbolic constraints.',
    wiki: 'https://en.wikipedia.org/wiki/Equation_solving',
    chapter: 'Anton algebra prerequisites: equation solving',
    chapterLink: 'https://archive.org/details/calculus0000anto_z8c2',
    applications: [
      'Physical equilibrium and design constraints.',
      'Parameter recovery in inverse problems.'
    ]
  },
  multivariable_partial: {
    title: 'Partial Derivative',
    theory: 'Partial derivatives quantify change along one axis while holding the other variables fixed.',
    wiki: 'https://en.wikipedia.org/wiki/Partial_derivative',
    chapter: 'Anton Calculus: Multivariable derivatives',
    chapterLink: 'https://archive.org/details/calculus0000anto_z8c2',
    applications: [
      'Heat maps and concentration fields in physics and chemistry.',
      'Sensitivity analysis in machine learning loss functions.'
    ]
  },
  multivariable_gradient: {
    title: 'Gradient',
    theory: 'The gradient points in the direction of steepest increase with magnitude equal to maximal local rate of change.',
    wiki: 'https://en.wikipedia.org/wiki/Gradient',
    chapter: 'Anton Calculus: Gradient and tangent planes',
    chapterLink: 'https://archive.org/details/calculus0000anto_z8c2',
    applications: [
      'Optimization methods including gradient descent.',
      'Terrain steepness and direction analysis in GIS.'
    ]
  },
  multivariable_directional: {
    title: 'Directional Derivative',
    theory: 'Directional derivative projects gradient along a chosen direction vector.',
    wiki: 'https://en.wikipedia.org/wiki/Directional_derivative',
    chapter: 'Anton Calculus: Directional derivatives',
    chapterLink: 'https://archive.org/details/calculus0000anto_z8c2',
    applications: [
      'Wind-aligned temperature change in meteorology.',
      'Material stress evaluation along preferred axes.'
    ]
  },
  multivariable_jacobian: {
    title: 'Jacobian',
    theory: 'Jacobian matrix captures first-order local linearization of vector-valued maps.',
    wiki: 'https://en.wikipedia.org/wiki/Jacobian_matrix_and_determinant',
    chapter: 'Anton Calculus: Vector functions and Jacobians',
    chapterLink: 'https://archive.org/details/calculus0000anto_z8c2',
    applications: [
      'Nonlinear coordinate transforms and robotics kinematics.',
      'Multivariate Newton methods and system sensitivity.'
    ]
  },
  matrix_multiply: {
    title: 'Matrix Multiplication',
    theory: 'Composition of linear transformations.',
    wiki: 'https://en.wikipedia.org/wiki/Matrix_multiplication',
    chapter: 'Anton Linear Algebra: Matrix operations',
    chapterLink: 'https://archive.org/details/ElementryLinearAlgebraByHowardAnton10thEdition',
    applications: [
      'Computer graphics transformations.',
      'State transition modeling in control systems.'
    ]
  },
  matrix_determinant: {
    title: 'Matrix Determinant',
    theory: 'Determinant measures area/volume scaling and invertibility.',
    wiki: 'https://en.wikipedia.org/wiki/Determinant',
    chapter: 'Anton Linear Algebra: Determinants',
    chapterLink: 'https://archive.org/details/ElementryLinearAlgebraByHowardAnton10thEdition',
    applications: [
      'Testing singular systems in engineering models.',
      'Jacobian scaling in coordinate transforms.'
    ]
  },
  matrix_inverse: {
    title: 'Matrix Inverse',
    theory: 'Inverse matrix undoes a linear transform when determinant is non-zero.',
    wiki: 'https://en.wikipedia.org/wiki/Invertible_matrix',
    chapter: 'Anton Linear Algebra: Inverse matrices',
    chapterLink: 'https://archive.org/details/ElementryLinearAlgebraByHowardAnton10thEdition',
    applications: [
      'Solving linear systems Ax=b in modeling.',
      'Calibration and coordinate recovery problems.'
    ]
  },
  matrix_rref: {
    title: 'Row Reduction',
    theory: 'Gaussian elimination exposes rank and system consistency.',
    wiki: 'https://en.wikipedia.org/wiki/Row_echelon_form',
    chapter: 'Anton Linear Algebra: Gaussian elimination',
    chapterLink: 'https://archive.org/details/ElementryLinearAlgebraByHowardAnton10thEdition',
    applications: [
      'Constraint solving in optimization.',
      'Feasibility analysis for linear models.'
    ]
  },
  matrix_eigenvalues: {
    title: 'Eigenvalues and Eigenvectors',
    theory: 'Eigenvectors preserve direction under linear transformation; eigenvalues scale them.',
    wiki: 'https://en.wikipedia.org/wiki/Eigenvalues_and_eigenvectors',
    chapter: 'Anton Linear Algebra: Eigen theory',
    chapterLink: 'https://archive.org/details/ElementryLinearAlgebraByHowardAnton10thEdition',
    applications: [
      'Principal component analysis and data compression.',
      'Stability analysis in dynamic systems.'
    ]
  },
  matrix_lu: {
    title: 'LU Decomposition',
    theory: 'Factorization PA=LU accelerates repeated solves.',
    wiki: 'https://en.wikipedia.org/wiki/LU_decomposition',
    chapter: 'Anton Linear Algebra: Matrix factorization',
    chapterLink: 'https://archive.org/details/ElementryLinearAlgebraByHowardAnton10thEdition',
    applications: [
      'Efficient simulation pipelines with repeated right-hand sides.',
      'Numerical methods in finite element systems.'
    ]
  }
};

const STUDENT_MODE_BANK = {
  differentiate: [
    { title: 'Damped Oscillation Velocity', expression: 'exp(-0.2*t)*sin(3*t)', variable: 't', level: 'advanced', goal: 'modeling', context: 'Mechanical vibration envelope and phase sensitivity.' },
    { title: 'Marginal Revenue Curve', expression: '(120*x - x**2)/(x+4)', variable: 'x', level: 'core', goal: 'exam', context: 'Differentiate rational functions used in economics optimization.' },
    { title: 'Chain Rule Stress Test', expression: 'ln(1 + cos(x**2))', variable: 'x', level: 'challenge', goal: 'concept', context: 'Nested chain rule with logarithmic outer map.' }
  ],
  integrate: [
    { title: 'Total Charge from Current', expression: '8*exp(-0.5*t)*sin(2*t)', variable: 't', level: 'advanced', goal: 'modeling', context: 'Integrate current profile to recover accumulated charge.' },
    { title: 'Area Under Nonlinear Demand', expression: '40 - 0.5*x**2', variable: 'x', level: 'core', goal: 'exam', context: 'Definite integral of demand curve for welfare quantities.' },
    { title: 'By-Parts Pattern', expression: 'x*exp(2*x)', variable: 'x', level: 'challenge', goal: 'concept', context: 'Identifies repeated integration by parts structure.' }
  ],
  calculus_limit: [
    { title: 'Transfer Function DC Gain', expression: '(exp(h)-1)/h', variable: 'h', point: 0, level: 'advanced', goal: 'modeling', context: 'Small-signal limit used in system linearization.' },
    { title: 'Removable Singularity', expression: '(x**2-1)/(x-1)', variable: 'x', point: 1, level: 'core', goal: 'exam', context: 'Classic continuity repair via cancellation.' },
    { title: 'Exponential Benchmark', expression: '(1+1/n)**n', variable: 'n', point: 1000000, level: 'challenge', goal: 'concept', context: 'Numerical approximation toward e.' }
  ],
  calculus_taylor: [
    { title: 'Sensor Linearization', expression: 'ln(1+x)', variable: 'x', point: 0, order: 4, level: 'advanced', goal: 'modeling', context: 'Near-zero approximation for signal calibration.' },
    { title: 'Maclaurin Sine', expression: 'sin(x)', variable: 'x', point: 0, order: 7, level: 'core', goal: 'exam', context: 'Odd-order series structure and truncation.' },
    { title: 'Nonzero Expansion Point', expression: 'exp(x)', variable: 'x', point: 1, order: 5, level: 'challenge', goal: 'concept', context: 'Taylor shift around operating point x=1.' }
  ],
  calculus_tangent_line: [
    { title: 'Operating Point Approximation', expression: 'x**2 + 2*x + 3', variable: 'x', point: 1, level: 'core', goal: 'exam', context: 'Local linear surrogate used in controls.' },
    { title: 'Biological Growth Snapshot', expression: '12/(1+exp(-0.8*(t-4)))', variable: 't', point: 4, level: 'advanced', goal: 'modeling', context: 'Instantaneous growth rate from logistic profile.' },
    { title: 'Curvature Comparison', expression: 'ln(x)', variable: 'x', point: 2, level: 'challenge', goal: 'concept', context: 'Tangent error analysis near non-unit x.' }
  ],
  algebra_simplify: [
    { title: 'Control Algebra Reduction', expression: '(s**2 - 1)/(s - 1)', variable: 's', level: 'core', goal: 'concept', context: 'Reduce transfer expression before differentiation.' },
    { title: 'Trig Identity Collapse', expression: 'sin(x)**2 + cos(x)**2', variable: 'x', level: 'core', goal: 'exam', context: 'Identity simplification as a preprocessing step.' },
    { title: 'Symbolic Pipeline Cleanup', expression: '(a*b + a*c + a*d)', variable: 'a', level: 'advanced', goal: 'modeling', context: 'Factorable common-term extraction in model equations.' }
  ],
  algebra_expand: [
    { title: 'Polynomial Forecast Expansion', expression: '(x+2)**5', variable: 'x', level: 'advanced', goal: 'modeling', context: 'Expand growth models into basis terms.' },
    { title: 'Quadratic Product Drill', expression: '(x-2)*(x+3)', variable: 'x', level: 'core', goal: 'exam', context: 'Foundational expansion pattern.' },
    { title: 'Multivariate Expansion', expression: '(x+y+z)**3', variable: 'x', level: 'challenge', goal: 'concept', context: 'Combinatorics of multinomial coefficients.' }
  ],
  algebra_factor: [
    { title: 'Pole-Zero Preparation', expression: 'x**2 + 5*x + 6', variable: 'x', level: 'core', goal: 'exam', context: 'Factor to expose roots immediately.' },
    { title: 'Difference of Powers', expression: 'x**4 - 1', variable: 'x', level: 'advanced', goal: 'concept', context: 'Nested factorization strategy.' },
    { title: 'Characteristic Polynomial', expression: 'r**3 - 6*r**2 + 11*r - 6', variable: 'r', level: 'challenge', goal: 'modeling', context: 'ODE stability roots via factorization.' }
  ],
  algebra_solve: [
    { title: 'Break-even Equation', expression: '2*x + 3 = 11', variable: 'x', level: 'core', goal: 'exam', context: 'Single-variable linear solve.' },
    { title: 'Mode Frequency Roots', expression: 'w**2 - 9 = 0', variable: 'w', level: 'advanced', goal: 'modeling', context: 'Natural frequency extraction in vibration systems.' },
    { title: 'Nonlinear Solve', expression: 'x**3 - 8 = 0', variable: 'x', level: 'challenge', goal: 'concept', context: 'Multiple roots and multiplicity reasoning.' }
  ],
  multivariable_partial: [
    { title: 'Heat Flux Sensitivity', expression: 'x**2*y + y**3 + exp(x)', vars: 'x,y', level: 'advanced', goal: 'modeling', context: 'Directional sensitivity along coordinate axes.' },
    { title: 'Coupled Surface', expression: 'sin(x*y)+x**2', vars: 'x,y', level: 'core', goal: 'exam', context: 'Mixed product and chain in multivariable form.' }
  ],
  multivariable_gradient: [
    { title: 'Potential Field Gradient', expression: 'x**2 + y**2 + z**2', vars: 'x,y,z', point: 'x:1,y:1,z:2', level: 'core', goal: 'exam', context: 'Steepest-ascent vector and magnitude.' },
    { title: 'Loss Surface Direction', expression: 'x*y + y*z + z*x', vars: 'x,y,z', point: 'x:1,y:2,z:3', level: 'advanced', goal: 'modeling', context: 'Optimization geometry for multivariate objectives.' }
  ],
  multivariable_directional: [
    { title: 'Wind-Aligned Temperature Change', expression: 'x**2 + y**2', vars: 'x,y', point: 'x:1,y:2', direction: '3,4', level: 'core', goal: 'modeling', context: 'Derivative along motion direction vector.' },
    { title: 'Stress Direction Probe', expression: 'x*y + y**2', vars: 'x,y', point: 'x:1,y:2', direction: '1,0', level: 'advanced', goal: 'concept', context: 'Compares principal axis vs oblique directions.' }
  ],
  multivariable_jacobian: [
    { title: 'Coordinate Transform Map', functions: 'x*y, x**2+y**2', vars: 'x,y', point: 'x:1,y:2', level: 'advanced', goal: 'modeling', context: 'Local linearization for change-of-variables.' },
    { title: 'System Coupling Matrix', functions: 'x+y+z, x*y*z', vars: 'x,y,z', point: 'x:1,y:2,z:3', level: 'challenge', goal: 'concept', context: 'Sensitivity matrix of nonlinear coupled outputs.' }
  ],
  matrix_multiply: [
    { title: '2D Transform Composition', matrixA: '[[0,-1],[1,0]]', matrixB: '[[2,0],[0,1]]', level: 'core', goal: 'modeling', context: 'Rotate then scale a planar state.' },
    { title: 'State-Space Update', matrixA: '[[1,0.1],[0,1]]', matrixB: '[[1],[0.4]]', level: 'advanced', goal: 'exam', context: 'One-step discrete-time propagation.' }
  ],
  matrix_determinant: [
    { title: 'Area Scale Factor', matrixA: '[[3,1],[2,2]]', level: 'core', goal: 'concept', context: '2D transformation area multiplier.' },
    { title: 'Invertibility Check', matrixA: '[[2,1,0],[1,3,2],[0,2,1]]', level: 'advanced', goal: 'exam', context: 'Nonzero determinant confirms unique solve.' }
  ],
  matrix_inverse: [
    { title: 'Calibration Recovery', matrixA: '[[4,1],[2,3]]', level: 'core', goal: 'exam', context: 'Recover original vector from transformed measurement.' },
    { title: 'Symbolic System Inverse', matrixA: '[["a","b"],["c","d"]]', level: 'challenge', goal: 'concept', context: 'Inverse constraints in symbolic design matrices.' }
  ],
  matrix_rref: [
    { title: 'Linear Constraint Solving', matrixA: '[[1,1,1],[1,2,3],[2,3,5]]', level: 'core', goal: 'exam', context: 'Solve and classify linear system rank.' },
    { title: 'Underdetermined Structure', matrixA: '[[1,2,1],[2,4,0],[3,6,3]]', level: 'advanced', goal: 'concept', context: 'Detect free variables and consistency.' }
  ],
  matrix_eigenvalues: [
    { title: 'Vibration Modes', matrixA: '[[2,1],[1,2]]', level: 'core', goal: 'modeling', context: 'Principal mode extraction from symmetric matrix.' },
    { title: 'Stability Spectrum', matrixA: '[[4,0,0],[0,1,0],[0,0,-1]]', level: 'advanced', goal: 'concept', context: 'Positive/negative eigenvalues indicate dynamic behavior.' }
  ],
  matrix_lu: [
    { title: 'Fast Repeated Solves', matrixA: '[[2,1,1],[4,-6,0],[-2,7,2]]', level: 'core', goal: 'exam', context: 'LU reusable for many right-hand-side vectors.' },
    { title: 'Finite Element Block', matrixA: '[[1,2,0],[3,4,4],[5,6,3]]', level: 'advanced', goal: 'modeling', context: 'Factor sparse-ish system for simulation pipelines.' }
  ]
};

const CHAPTER_PROGRESSION = {
  anton_limits: {
    operation: 'calculus_limit',
    objectives: ['Evaluate algebraic limits', 'Handle indeterminate forms', 'Connect limits to continuity'],
    sample: { expr: '(x**2-1)/(x-1)', variable: 'x' },
    pageMap: [
      { section: 'Anton Ch2.1-2.3 Intro to limits', pages: 'pp. 65-95', tools: 'calculus_limit, algebra_simplify' },
      { section: 'Anton Ch2.4 Continuity', pages: 'pp. 95-112', tools: 'calculus_limit' },
      { section: 'Anton Ch2.5 Infinite limits', pages: 'pp. 112-124', tools: 'calculus_limit' }
    ],
    practice: [
      { op: 'calculus_limit', problem: '(x**2-1)/(x-1)', variable: 'x', point: 1, ref: 'Ch2 p.76 #18' },
      { op: 'calculus_limit', problem: 'sin(x)/x', variable: 'x', point: 0, ref: 'Ch2 p.82 #31' },
      { op: 'algebra_simplify', problem: '(x**2-1)/(x-1)', variable: 'x', ref: 'Ch2 p.73 prep' }
    ]
  },
  anton_diff: {
    operation: 'differentiate',
    objectives: ['Power and product rules', 'Chain rule mastery', 'Implicit and higher-order derivatives'],
    sample: { expr: 'sin(x**2)', variable: 'x' },
    pageMap: [
      { section: 'Anton Ch2.7 Derivative definition', pages: 'pp. 102-118', tools: 'differentiate, calculus_tangent_line' },
      { section: 'Anton Ch3.1-3.6 Differentiation rules', pages: 'pp. 121-186', tools: 'differentiate' },
      { section: 'Anton Ch3.7 Linear approximation', pages: 'pp. 186-197', tools: 'calculus_tangent_line' },
      { section: 'Anton Ch4 Applications of derivatives', pages: 'pp. 198-278', tools: 'differentiate, algebra_solve' }
    ],
    practice: [
      { op: 'differentiate', problem: 'x**5 - 3*x**2 + 2', variable: 'x', ref: 'Ch3 p.129 #12' },
      { op: 'differentiate', problem: 'sin(x**2)', variable: 'x', ref: 'Ch3 p.141 #34' },
      { op: 'calculus_tangent_line', problem: 'x**2 + 2*x + 3', variable: 'x', point: 1, ref: 'Ch3 p.193 #8' },
      { op: 'algebra_solve', problem: '2*x+3=11', variable: 'x', ref: 'Ch4 p.240 #17' }
    ]
  },
  anton_int: {
    operation: 'integrate',
    objectives: ['Substitution patterns', 'Integration by parts', 'Definite integrals with interpretation'],
    sample: { expr: 'x*cos(x)', variable: 'x' },
    pageMap: [
      { section: 'Anton Ch5 Antiderivatives', pages: 'pp. 279-301', tools: 'integrate' },
      { section: 'Anton Ch6 Definite integral', pages: 'pp. 330-377', tools: 'integrate' },
      { section: 'Anton Ch7 Integration techniques', pages: 'pp. 420-495', tools: 'integrate, algebra_factor' }
    ],
    practice: [
      { op: 'integrate', problem: 'x**2 + 2*x + 1', variable: 'x', ref: 'Ch5 p.289 #16' },
      { op: 'integrate', problem: 'x*sin(x)', variable: 'x', ref: 'Ch7 p.448 #27' },
      { op: 'integrate', problem: '1/(x**2+1)', variable: 'x', ref: 'Ch7 p.463 #41' },
      { op: 'algebra_factor', problem: 'x**2+5*x+6', variable: 'x', ref: 'Ch7 p.438 prep' }
    ]
  },
  anton_series: {
    operation: 'calculus_taylor',
    objectives: ['Build Taylor polynomials', 'Estimate remainder behavior', 'Use series for approximation'],
    sample: { expr: 'ln(1+x)', variable: 'x' },
    pageMap: [
      { section: 'Anton Ch11.1 Sequences', pages: 'pp. 690-704', tools: 'calculus_limit' },
      { section: 'Anton Ch11.2-11.5 Series tests', pages: 'pp. 704-742', tools: 'calculus_limit' },
      { section: 'Anton Ch11.8 Taylor/Maclaurin', pages: 'pp. 742-764', tools: 'calculus_taylor' }
    ],
    practice: [
      { op: 'calculus_taylor', problem: 'ln(1+x)', variable: 'x', point: 0, order: 5, ref: 'Ch11 p.719 #22' },
      { op: 'calculus_taylor', problem: 'sin(x)', variable: 'x', point: 0, order: 7, ref: 'Ch11 p.753 #46' },
      { op: 'calculus_limit', problem: '(1+1/x)**x', variable: 'x', point: 1000000, ref: 'Ch11 p.699 #8' }
    ]
  },
  anton_parametric: {
    operation: 'differentiate',
    objectives: ['Analyze parametric curves', 'Differentiate polar expressions by chain rules', 'Link geometry and slope'],
    sample: { expr: 'sin(x)*cos(x)', variable: 'x' },
    pageMap: [
      { section: 'Anton Ch10.1 Parametric curves', pages: 'pp. 640-662', tools: 'differentiate, calculus_tangent_line' },
      { section: 'Anton Ch10.2 Polar coordinates', pages: 'pp. 662-683', tools: 'differentiate' }
    ],
    practice: [
      { op: 'differentiate', problem: 'sin(x)*cos(x)', variable: 'x', ref: 'Ch10 p.651 #12' },
      { op: 'calculus_tangent_line', problem: 'exp(x)', variable: 'x', point: 0, ref: 'Ch10 p.659 #29' }
    ]
  },
  anton_multivar: {
    operation: 'multivariable_gradient',
    objectives: ['Compute partial derivatives', 'Build and interpret gradient', 'Directional derivative at a point'],
    sample: { multiExpr: 'x**2 + y**2', multiVariables: 'x,y', multiPoint: 'x:1,y:2' },
    pageMap: [
      { section: 'Anton Ch12 Vectors and geometry', pages: 'pp. 780-838', tools: 'multivariable_partial' },
      { section: 'Anton Ch13 Functions of several variables', pages: 'pp. 842-919', tools: 'multivariable_partial, multivariable_gradient' },
      { section: 'Anton Ch13.6 Directional derivative', pages: 'pp. 902-910', tools: 'multivariable_directional' },
      { section: 'Anton Ch14 Jacobians', pages: 'pp. 964-980', tools: 'multivariable_jacobian' }
    ],
    practice: [
      { op: 'multivariable_partial', problem: 'x**2*y + y**3', vars: 'x,y', ref: 'Ch13 p.858 #14' },
      { op: 'multivariable_gradient', problem: 'x**2 + y**2 + z**2', vars: 'x,y,z', point: 'x:1,y:1,z:2', ref: 'Ch13 p.886 #31' },
      { op: 'multivariable_directional', problem: 'x**2 + y**2', vars: 'x,y', point: 'x:1,y:2', direction: '3,4', ref: 'Ch13 p.905 #47' },
      { op: 'multivariable_jacobian', problem: 'x*y, x**2+y**2', vars: 'x,y', point: 'x:1,y:2', ref: 'Ch14 p.972 #11' }
    ]
  },
  anton_vectorcalc: {
    operation: 'multivariable_jacobian',
    objectives: ['Understand vector fields', 'Interpret divergence/curl prerequisites', 'Apply Jacobian mappings'],
    sample: { multiFunctions: 'x*y, x**2+y**2', multiVariables: 'x,y', multiPoint: 'x:1,y:2' },
    pageMap: [
      { section: 'Anton Ch15 Vector fields', pages: 'pp. 980-1042', tools: 'multivariable_gradient, multivariable_jacobian' },
      { section: 'Anton Ch16 Line/surface integrals', pages: 'pp. 1042-1120', tools: 'integrate, multivariable_directional' }
    ],
    practice: [
      { op: 'multivariable_jacobian', problem: 'x*y, x**2+y**2', vars: 'x,y', point: 'x:1,y:2', ref: 'Ch15 p.1008 #23' },
      { op: 'multivariable_directional', problem: 'x*y + y**2', vars: 'x,y', point: 'x:1,y:2', direction: '1,0', ref: 'Ch16 p.1076 #15' }
    ]
  },
  anton_linalg: {
    operation: 'matrix_rref',
    objectives: ['Determinants and invertibility', 'Row-reduction fluency', 'Eigenvalue interpretation'],
    sample: { matrixA: '[[1,2,3],[2,4,7],[1,1,1]]' },
    pageMap: [
      { section: 'Anton LA Ch1 Systems and matrices', pages: 'pp. 1-69', tools: 'matrix_rref, matrix_multiply' },
      { section: 'Anton LA Ch2 Determinants', pages: 'pp. 70-122', tools: 'matrix_determinant' },
      { section: 'Anton LA Ch3 Inverse and factorization', pages: 'pp. 123-186', tools: 'matrix_inverse, matrix_lu' }
    ],
    practice: [
      { op: 'matrix_rref', matrixA: '[[1,2,3],[2,4,7],[1,1,1]]', ref: 'LA Ch1 p.44 #28' },
      { op: 'matrix_determinant', matrixA: '[[2,1,-1],[1,0,2],[3,4,1]]', ref: 'LA Ch2 p.95 #13' },
      { op: 'matrix_inverse', matrixA: '[[4,1],[2,3]]', ref: 'LA Ch3 p.138 #20' }
    ]
  },
  anton_linalg_adv: {
    operation: 'matrix_eigenvalues',
    objectives: ['Eigen decomposition intuition', 'Diagonalization checks', 'LU/eigen computational comparisons'],
    sample: { matrixA: '[[2,1],[1,2]]' },
    pageMap: [
      { section: 'Anton LA Ch5 Eigenvalues/eigenvectors', pages: 'pp. 247-302', tools: 'matrix_eigenvalues' },
      { section: 'Anton LA Ch6 Orthogonality', pages: 'pp. 303-352', tools: 'matrix_multiply' },
      { section: 'Anton LA Ch7 Advanced factorization', pages: 'pp. 353-410', tools: 'matrix_lu, matrix_rref' }
    ],
    practice: [
      { op: 'matrix_eigenvalues', matrixA: '[[2,1],[1,2]]', ref: 'LA Ch5 p.266 #9' },
      { op: 'matrix_lu', matrixA: '[[2,1,1],[4,-6,0],[-2,7,2]]', ref: 'LA Ch7 p.374 #12' }
    ]
  },
  gill_ode: {
    operation: 'calculus_tangent_line',
    objectives: ['Slope-field intuition (bridge)', 'Modeling change rates', 'Interpreting direction fields'],
    sample: { expr: 'x**2 + 1', variable: 'x' },
    pageMap: [
      { section: 'Gill Ch1 First-order DE models', pages: 'pp. 1-48', tools: 'calculus_tangent_line, calculus_limit' },
      { section: 'Gill Ch2 Separable equations', pages: 'pp. 49-96', tools: 'integrate' },
      { section: 'Gill Ch3 Linear first-order equations', pages: 'pp. 97-146', tools: 'integrate, algebra_solve' },
      { section: 'Gill Ch4 Direction fields (bridge)', pages: 'pp. 147-176', tools: 'multivariable_directional' }
    ],
    practice: [
      { op: 'calculus_tangent_line', problem: 'x**2 + 1', variable: 'x', point: 1, ref: 'Gill Ch1 p.22 #6' },
      { op: 'integrate', problem: '1/(x+1)', variable: 'x', ref: 'Gill Ch2 p.68 #11' },
      { op: 'algebra_solve', problem: '2*x+3=11', variable: 'x', ref: 'Gill Ch3 p.121 #4' },
      { op: 'multivariable_directional', problem: 'x*y + y**2', vars: 'x,y', point: 'x:1,y:2', direction: '1,0', ref: 'Gill Ch4 p.160 #15' }
    ]
  },
  gill_linear_ode: {
    operation: 'integrate',
    objectives: ['Second-order linear equation structure', 'Characteristic equation bridge', 'Forcing and solution behavior'],
    sample: { expr: 'exp(x)', variable: 'x' },
    pageMap: [
      { section: 'Gill Ch5 Second-order linear ODE', pages: 'pp. 177-236', tools: 'algebra_solve, integrate' },
      { section: 'Gill Ch6 Nonhomogeneous ODE', pages: 'pp. 237-294', tools: 'integrate, calculus_taylor' }
    ],
    practice: [
      { op: 'algebra_solve', problem: 'r**2-3*r+2=0', variable: 'r', ref: 'Gill Ch5 p.196 #9' },
      { op: 'integrate', problem: 'exp(x)', variable: 'x', ref: 'Gill Ch6 p.251 #14' }
    ]
  }
};

const TOOL_TO_CHAPTER = {
  differentiate: 'anton_diff',
  integrate: 'anton_int',
  calculus_limit: 'anton_limits',
  calculus_taylor: 'anton_series',
  calculus_tangent_line: 'anton_diff',
  algebra_simplify: 'anton_limits',
  algebra_expand: 'anton_diff',
  algebra_factor: 'anton_int',
  algebra_solve: 'anton_diff',
  multivariable_partial: 'anton_multivar',
  multivariable_gradient: 'anton_multivar',
  multivariable_directional: 'anton_vectorcalc',
  multivariable_jacobian: 'anton_multivar',
  matrix_multiply: 'anton_linalg',
  matrix_determinant: 'anton_linalg',
  matrix_inverse: 'anton_linalg',
  matrix_rref: 'anton_linalg',
  matrix_eigenvalues: 'anton_linalg_adv',
  matrix_lu: 'anton_linalg_adv'
};

const TOOL_BOOK_CONNECTIONS = {
  differentiate: [
    { label: 'Anton Calculus Ch3.3 (pp. 132-145)', detail: 'Chain rule for composite sensor models and nested growth laws.' },
    { label: 'Anton Calculus Ch4.1 (pp. 198-214)', detail: 'Use first derivative tests to classify local extrema in optimization.' },
    { label: 'Gill Ch1 bridge', detail: 'Derivative slope interpretation is the entry point to first-order ODEs.' }
  ],
  integrate: [
    { label: 'Anton Calculus Ch6.2 (pp. 338-354)', detail: 'Definite integral as accumulated quantity and signed area.' },
    { label: 'Anton Calculus Ch7.2 (pp. 438-454)', detail: 'Integration by parts for products like polynomial-exponential terms.' },
    { label: 'Gill Ch2 bridge', detail: 'Antiderivative structure underpins separable ODE solution steps.' }
  ],
  calculus_limit: [
    { label: 'Anton Calculus Ch2.1-2.4 (pp. 65-112)', detail: 'Formal limit behavior, continuity, and removable discontinuities.' },
    { label: 'Anton Calculus Ch2.5 (pp. 112-124)', detail: 'Infinite limits and asymptotic behavior in physical models.' }
  ],
  calculus_taylor: [
    { label: 'Anton Calculus Ch11.8 (pp. 742-764)', detail: 'Taylor/Maclaurin expansions for local nonlinear approximation.' },
    { label: 'Gill Ch6 bridge', detail: 'Series-based approximations support nonhomogeneous forcing analysis.' }
  ],
  calculus_tangent_line: [
    { label: 'Anton Calculus Ch3.7 (pp. 186-197)', detail: 'Linear approximation around an operating point.' },
    { label: 'Anton Calculus Ch4.8', detail: 'Error interpretation when local linear model deviates from nonlinear system.' }
  ],
  algebra_simplify: [
    { label: 'Anton Algebra Prerequisite', detail: 'Simplify before differentiation/integration to reduce algebraic noise.' },
    { label: 'Anton Ch2 prep', detail: 'Cancellations reveal limit structure and remove removable singularities.' }
  ],
  algebra_expand: [
    { label: 'Anton Algebra Prerequisite', detail: 'Expanded forms expose term-by-term derivative and integral behavior.' },
    { label: 'Anton Ch3 prep', detail: 'Expansion helps identify dominant growth order in derivative tests.' }
  ],
  algebra_factor: [
    { label: 'Anton Ch7 prep', detail: 'Factoring supports partial fractions and rational integration workflows.' },
    { label: 'Gill Ch5 bridge', detail: 'Characteristic equations factor into modal roots for ODE solutions.' }
  ],
  algebra_solve: [
    { label: 'Anton Ch4 Applications', detail: 'Critical-point equations arise in optimization and curve analysis.' },
    { label: 'Gill Ch3/Ch5', detail: 'Linear and characteristic equations determine ODE solution families.' }
  ],
  multivariable_partial: [
    { label: 'Anton Ch13.2 (pp. 852-866)', detail: 'Partial derivatives with one variable held constant.' },
    { label: 'Anton Ch13.4', detail: 'Higher-order and mixed-partial consistency checks.' }
  ],
  multivariable_gradient: [
    { label: 'Anton Ch13.5 (pp. 886-902)', detail: 'Gradient direction and maximal increase rate.' },
    { label: 'Anton Ch13.7', detail: 'Connection between gradient and tangent planes.' }
  ],
  multivariable_directional: [
    { label: 'Anton Ch13.6 (pp. 902-910)', detail: 'Directional derivative as projection of gradient onto unit direction.' },
    { label: 'Anton Ch15 bridge', detail: 'Directional rates relate to vector-field flow directions.' }
  ],
  multivariable_jacobian: [
    { label: 'Anton Ch14 (pp. 964-980)', detail: 'Jacobian matrix for local linearization of vector maps.' },
    { label: 'Anton Ch16 bridge', detail: 'Jacobian determinant appears in change-of-variables integrals.' }
  ],
  matrix_multiply: [
    { label: 'Anton LA Ch1', detail: 'Compose linear transformations and state updates.' },
    { label: 'Anton LA Ch6 bridge', detail: 'Matrix products govern orthogonal transformations and projections.' }
  ],
  matrix_determinant: [
    { label: 'Anton LA Ch2', detail: 'Determinant as invertibility test and area/volume scaling factor.' },
    { label: 'Anton Calculus Ch14 bridge', detail: 'Jacobian determinant generalizes determinant scaling in calculus.' }
  ],
  matrix_inverse: [
    { label: 'Anton LA Ch3', detail: 'Inverse matrix solves Ax=b and reverses linear transforms.' },
    { label: 'Anton LA Ch1 bridge', detail: 'Inverse existence tied to rank and pivots.' }
  ],
  matrix_rref: [
    { label: 'Anton LA Ch1', detail: 'RREF reveals rank, consistency, and solution family dimension.' },
    { label: 'Gill Ch3 bridge', detail: 'Linear systems from ODE discretizations can be solved via row operations.' }
  ],
  matrix_eigenvalues: [
    { label: 'Anton LA Ch5', detail: 'Eigen spectrum identifies invariant directions and modal behavior.' },
    { label: 'Gill Ch5 bridge', detail: 'Characteristic roots mirror eigenvalue-style stability analysis.' }
  ],
  matrix_lu: [
    { label: 'Anton LA Ch7', detail: 'LU factorization accelerates repeated solves with shared matrix A.' },
    { label: 'Numerical methods bridge', detail: 'Core primitive in finite element and simulation pipelines.' }
  ]
};

const TOOL_VIDEO_RESOURCES = {
  differentiate: [
    { title: 'Chain Rule in Engineering Models', url: 'https://www.youtube.com/results?search_query=chain+rule+engineering+examples' },
    { title: 'Optimization with First and Second Derivatives', url: 'https://www.youtube.com/results?search_query=first+second+derivative+optimization' }
  ],
  integrate: [
    { title: 'Definite Integral as Accumulation', url: 'https://www.youtube.com/results?search_query=definite+integral+accumulation+interpretation' },
    { title: 'Integration by Parts Strategy', url: 'https://www.youtube.com/results?search_query=integration+by+parts+strategy+examples' }
  ],
  multivariable_gradient: [
    { title: 'Gradient and Steepest Ascent Intuition', url: 'https://www.youtube.com/results?search_query=gradient+steepest+ascent+intuition' },
    { title: 'Multivariable Optimization Basics', url: 'https://www.youtube.com/results?search_query=multivariable+optimization+gradient+descent' }
  ],
  multivariable_jacobian: [
    { title: 'Jacobian Matrix and Change of Variables', url: 'https://www.youtube.com/results?search_query=jacobian+change+of+variables+calculus' },
    { title: 'Vector-Valued Derivatives', url: 'https://www.youtube.com/results?search_query=vector+valued+functions+jacobian' }
  ],
  matrix_eigenvalues: [
    { title: 'Eigenvalues and Dynamical Systems', url: 'https://www.youtube.com/results?search_query=eigenvalues+dynamical+systems+stability' },
    { title: 'Geometric Meaning of Eigenvectors', url: 'https://www.youtube.com/results?search_query=geometric+meaning+of+eigenvectors' }
  ],
  matrix_lu: [
    { title: 'LU Decomposition for Fast Solves', url: 'https://www.youtube.com/results?search_query=lu+decomposition+numerical+linear+algebra' },
    { title: 'Pivoting and Numerical Stability', url: 'https://www.youtube.com/results?search_query=partial+pivoting+lu+decomposition' }
  ]
};

const ADVANCED_APPLICATIONS = {
  differentiate: [
    { domain: 'Control Systems', scenario: 'Estimate instantaneous actuator sensitivity around a setpoint.', mathModel: 'S = d y/d u at u=u0' },
    { domain: 'Finance', scenario: 'Compute delta of option value with respect to underlying price.', mathModel: '\u0394 = dV/dS' },
    { domain: 'Biomechanics', scenario: 'Infer peak acceleration from motion-capture displacement curves.', mathModel: 'a(t) = d2x/dt2' }
  ],
  integrate: [
    { domain: 'Signal Processing', scenario: 'Energy of a waveform over a time window.', mathModel: 'E = \u222b |x(t)|^2 dt' },
    { domain: 'Fluid Mechanics', scenario: 'Total volume throughput from time-varying flow.', mathModel: 'V = \u222b Q(t) dt' },
    { domain: 'Econometrics', scenario: 'Aggregate cost from marginal cost curve.', mathModel: 'C(q) = \u222b MC(q) dq' }
  ],
  calculus_limit: [
    { domain: 'Electronics', scenario: 'Compute small-signal gain by taking the limit around nominal voltage.', mathModel: 'g = lim_{h->0} [f(v+h)-f(v)]/h' },
    { domain: 'Numerical Analysis', scenario: 'Check stability of approximation formulas near singular points.', mathModel: 'lim_{x->a} f(x)' },
    { domain: 'Physics', scenario: 'Evaluate near-field behavior when denominator approaches zero.', mathModel: 'asymptotic response' }
  ],
  calculus_taylor: [
    { domain: 'Control Engineering', scenario: 'Linearize nonlinear plants around operating points.', mathModel: 'f(x) \u2248 f(a) + f\'(a)(x-a) + ...' },
    { domain: 'Aerospace', scenario: 'Approximate trigonometric terms for small-angle dynamics.', mathModel: 'sin(theta) \u2248 theta' },
    { domain: 'Computer Graphics', scenario: 'Use polynomial approximation for fast function evaluation.', mathModel: 'P_n(x) from derivatives' }
  ],
  calculus_tangent_line: [
    { domain: 'Optimization', scenario: 'First-order local model for rapid sensitivity estimates.', mathModel: 'L(x)=f(a)+f\'(a)(x-a)' },
    { domain: 'Economics', scenario: 'Marginal approximation near production target q0.', mathModel: 'C(q) \u2248 C(q0)+C\'(q0)(q-q0)' },
    { domain: 'Biomechanics', scenario: 'Estimate local trend in measured movement trajectories.', mathModel: 'instant slope at t0' }
  ],
  algebra_solve: [
    { domain: 'Chemical Engineering', scenario: 'Solve equilibrium equations for unknown concentrations.', mathModel: 'solve F(c)=0' },
    { domain: 'Mechanics', scenario: 'Find roots of characteristic equations for natural frequencies.', mathModel: 'det(K-omega^2 M)=0' },
    { domain: 'Economics', scenario: 'Break-even output where revenue equals cost.', mathModel: 'R(q)-C(q)=0' }
  ],
  multivariable_partial: [
    { domain: 'Thermodynamics', scenario: 'Hold pressure fixed while measuring temperature sensitivity.', mathModel: '(\u2202U/\u2202T)_p' },
    { domain: 'ML Explainability', scenario: 'Feature-wise sensitivity of loss function.', mathModel: '\u2202J/\u2202x_i' },
    { domain: 'Fluid Simulation', scenario: 'Axis-aligned rate of change in scalar fields.', mathModel: '\u2202f/\u2202x, \u2202f/\u2202y' }
  ],
  multivariable_gradient: [
    { domain: 'Machine Learning', scenario: 'Gradient direction drives parameter updates.', mathModel: '\u03b8(k+1)=\u03b8(k)-\u03b7\u2207J(\u03b8)' },
    { domain: 'Geophysics', scenario: 'Steepest terrain ascent from elevation field.', mathModel: '\u2207h(x,y)' },
    { domain: 'Thermal Systems', scenario: 'Direction of maximal temperature rise in a plate.', mathModel: '\u2207T(x,y)' }
  ],
  multivariable_jacobian: [
    { domain: 'Robotics', scenario: 'Map joint velocities to end-effector velocity.', mathModel: 'v = J(q) \u02d9q' },
    { domain: 'Computer Vision', scenario: 'Local warp linearization in image registration.', mathModel: 'x\' \u2248 f(x)+J\u0394x' },
    { domain: 'Economy Models', scenario: 'Sensitivity of multi-output systems to parameters.', mathModel: 'J_ij = \u2202f_i/\u2202x_j' }
  ],
  multivariable_directional: [
    { domain: 'Meteorology', scenario: 'Temperature change along wind direction vectors.', mathModel: 'D_u T = \u2207T \u00b7 u_hat' },
    { domain: 'Material Science', scenario: 'Stress response along fiber orientation.', mathModel: 'directional sensitivity' },
    { domain: 'Medical Imaging', scenario: 'Gradient projection along vessel centerlines.', mathModel: 'projection of \u2207f' }
  ],
  matrix_multiply: [
    { domain: 'Robotics', scenario: 'Compose link transforms through a kinematic chain.', mathModel: 'T_total = T1 T2 ... Tn' },
    { domain: 'Computer Graphics', scenario: 'Apply rotate-scale-translate pipeline to vertices.', mathModel: 'p\' = M p' },
    { domain: 'Econometrics', scenario: 'Batch transform feature vectors by learned weights.', mathModel: 'Y = XW' }
  ],
  matrix_determinant: [
    { domain: 'Geometry', scenario: 'Area/volume scaling under linear transforms.', mathModel: 'scale = |det(A)|' },
    { domain: 'Systems Engineering', scenario: 'Check if linear system has unique solution.', mathModel: 'det(A) != 0' },
    { domain: 'Calculus', scenario: 'Local area distortion in coordinate transformations.', mathModel: 'Jacobian determinant' }
  ],
  matrix_inverse: [
    { domain: 'Navigation', scenario: 'Recover world coordinates from transformed sensor frame.', mathModel: 'x = A^{-1} b' },
    { domain: 'Signal Processing', scenario: 'Undo linear mixing of observed channels.', mathModel: 's = M^{-1} y' },
    { domain: 'Calibration', scenario: 'Reverse mapping after affine correction.', mathModel: 'inverse transform' }
  ],
  matrix_rref: [
    { domain: 'Operations Research', scenario: 'Solve and classify linear constraint systems.', mathModel: 'rank and consistency via RREF' },
    { domain: 'Data Fitting', scenario: 'Determine identifiability in linear models.', mathModel: 'free vs pivot variables' },
    { domain: 'Control', scenario: 'Analyze controllability/observability linear equations.', mathModel: 'row-space structure' }
  ],
  matrix_eigenvalues: [
    { domain: 'Vibration Analysis', scenario: 'Natural frequencies from stiffness/mass matrices.', mathModel: 'det(K-\u03bbM)=0' },
    { domain: 'Recommendation Systems', scenario: 'Principal latent factors from covariance structure.', mathModel: 'C v = \u03bb v' },
    { domain: 'Population Dynamics', scenario: 'Long-term behavior from dominant eigenvalue.', mathModel: 'x_{k+1}=A x_k' }
  ]
  ,
  matrix_lu: [
    { domain: 'Scientific Computing', scenario: 'Efficiently solve Ax=b for many right-hand sides.', mathModel: 'PA=LU, then Ly=Pb and Ux=y' },
    { domain: 'Finite Elements', scenario: 'Factor sparse stiffness matrices repeatedly during simulation.', mathModel: 'factor once, solve many' },
    { domain: 'Optimization', scenario: 'Core linear solve primitive inside Newton iterations.', mathModel: 'J \u0394x = -F' }
  ]
};

async function callAPI(expr, variable = 'x', order = 1, verbosity = 'detailed') {
  const url = new URL(`/differentiate`, window.location.origin);
  url.searchParams.set('expr', expr);
  url.searchParams.set('variable', variable);
  url.searchParams.set('order', order);
  url.searchParams.set('format', 'json');
  url.searchParams.set('verbosity', verbosity);

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

async function callMatrixAPI(operation, matrixA, matrixB = null, verbosity = 'detailed') {
  const url = new URL(`/matrix/${operation.replace('matrix_', '')}`, window.location.origin);
  
  const body = {
    matrix: matrixA,
    format: 'json',
    verbosity
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

async function callIntegrationAPI(expr, variable = 'x', lowerLimit = null, upperLimit = null, verbosity = 'detailed') {
  const url = new URL(`/integrate`, window.location.origin);
  
  const params = {
    expr,
    variable,
    format: 'json',
    verbosity
  };
  
  if (lowerLimit !== null && lowerLimit !== '') {
    params.lower_limit = lowerLimit;
  }
  if (upperLimit !== null && upperLimit !== '') {
    params.upper_limit = upperLimit;
  }
  
  Object.keys(params).forEach(key => url.searchParams.set(key, params[key]));

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

function parseVariablesList(raw) {
  return raw.split(',').map(v => v.trim()).filter(Boolean);
}

function parsePointMap(raw) {
  if (!raw || !raw.trim()) return null;
  const out = {};
  raw.split(',').forEach(piece => {
    const [k, v] = piece.split(':').map(s => s.trim());
    if (!k || v === undefined || v === '') return;
    out[k] = Number(v);
  });
  return Object.keys(out).length ? out : null;
}

function parseDirectionVector(raw) {
  if (!raw || !raw.trim()) return null;
  const vals = raw.split(',').map(v => Number(v.trim())).filter(v => !Number.isNaN(v));
  return vals.length ? vals : null;
}

function normalizeExpressionInput(raw) {
  if (!raw) return '';
  return String(raw)
    .replace(/\u2212/g, '-')
    .replace(/\^/g, '**')
    .replace(/\s*\*\*\s*/g, '**')
    .replace(/\s+/g, ' ')
    .trim();
}

function containsVariable(expr, variable) {
  if (!expr || !variable) return false;
  const escaped = variable.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const pattern = new RegExp(`(^|[^A-Za-z0-9_])${escaped}([^A-Za-z0-9_]|$)`);
  return pattern.test(expr);
}

function replaceStandaloneX(expr, variable) {
  if (!expr || !variable) return expr;
  return expr.replace(/\bx\b/g, variable);
}

async function callMultivariableAPI(operation, payload) {
  const routeMap = {
    multivariable_partial: '/multivariable/partial',
    multivariable_gradient: '/multivariable/gradient',
    multivariable_directional: '/multivariable/directional',
    multivariable_jacobian: '/multivariable/jacobian'
  };
  const route = routeMap[operation];
  if (!route) {
    throw new Error(`Unsupported multivariable operation: ${operation}`);
  }
  const url = new URL(route, window.location.origin);

  const startTime = performance.now();
  const res = await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Accept': 'application/json'
    },
    body: JSON.stringify(payload)
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
  if (data.error) {
    throw new Error(data.error);
  }
  return { data, timing: (endTime - startTime).toFixed(1) };
}

async function callSymbolicAPI(operation, payload) {
  const url = new URL('/symbolic/compute', window.location.origin);
  const startTime = performance.now();
  const res = await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Accept': 'application/json'
    },
    body: JSON.stringify({ operation, ...payload })
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
  if (data.error) {
    throw new Error(data.error);
  }
  return { data, timing: (endTime - startTime).toFixed(1) };
}

function getChapterState() {
  try {
    const raw = localStorage.getItem('calcora-chapter-progress-v1');
    return raw ? JSON.parse(raw) : {};
  } catch {
    return {};
  }
}

function saveChapterState(state) {
  localStorage.setItem('calcora-chapter-progress-v1', JSON.stringify(state));
}

function renderChapterObjectives() {
  const chapterSelect = document.getElementById('chapterSelect');
  const list = document.getElementById('chapterObjectiveList');
  const scoreBadge = document.getElementById('chapterScoreBadge');
  const meta = document.getElementById('chapterObjectiveMeta');
  if (!chapterSelect || !list || !scoreBadge || !meta) return;

  const chapterKey = chapterSelect.value;
  const chapter = CHAPTER_PROGRESSION[chapterKey];
  if (!chapter) return;

  const state = getChapterState();
  const doneMap = state[chapterKey] || {};
  let completed = 0;

  list.innerHTML = chapter.objectives.map((obj, idx) => {
    const isDone = Boolean(doneMap[idx]);
    if (isDone) completed += 1;
    return `<li class="${isDone ? 'done' : ''}" data-idx="${idx}">${obj}</li>`;
  }).join('');

  const total = chapter.objectives.length;
  const pct = total ? Math.round((completed / total) * 100) : 0;
  scoreBadge.textContent = `Mastery: ${pct}%`;
  meta.textContent = `${completed}/${total} objectives completed`;

  renderChapterReferenceContent(chapter);
}

function renderChapterReferenceContent(chapter) {
  const pageMapEl = document.getElementById('chapterPageMap');
  const practiceEl = document.getElementById('chapterPracticeList');
  if (!chapter || !pageMapEl || !practiceEl) return;

  const pageMap = chapter.pageMap || [];
  const practice = chapter.practice || [];

  pageMapEl.innerHTML = pageMap
    .map(item => `<li><strong>${item.section}</strong><br>${item.pages} · Tools: ${item.tools}</li>`)
    .join('');

  practiceEl.innerHTML = practice
    .map((item, idx) => `
      <li>
        <div><strong>${item.ref}</strong></div>
        <div class="chapter-practice-problem">${item.problem || item.matrixA || '(problem data)'}</div>
        <button type="button" class="btn-secondary chapter-practice-action" data-practice-index="${idx}">Load and Run</button>
      </li>
    `)
    .join('');
}

function markNextObjectiveDone() {
  const chapterSelect = document.getElementById('chapterSelect');
  if (!chapterSelect) return;
  const chapterKey = chapterSelect.value;
  const chapter = CHAPTER_PROGRESSION[chapterKey];
  if (!chapter) return;

  const state = getChapterState();
  state[chapterKey] = state[chapterKey] || {};

  const total = chapter.objectives.length;
  for (let i = 0; i < total; i += 1) {
    if (!state[chapterKey][i]) {
      state[chapterKey][i] = true;
      saveChapterState(state);
      renderChapterObjectives();
      return;
    }
  }
  renderChapterObjectives();
}

function startSelectedChapter() {
  const chapterSelect = document.getElementById('chapterSelect');
  if (!chapterSelect) return;
  const chapterKey = chapterSelect.value;
  const chapter = CHAPTER_PROGRESSION[chapterKey];
  if (!chapter) return;

  document.getElementById('operationType').value = chapter.operation;
  suppressChapterAutoSync = true;
  handleOperationTypeChange();
  suppressChapterAutoSync = false;

  const s = chapter.sample || {};
  if (s.expr) document.getElementById('expr').value = s.expr;
  if (s.variable) document.getElementById('variable').value = s.variable;
  if (s.matrixA) document.getElementById('matrixA').value = s.matrixA;
  if (s.multiExpr) document.getElementById('multiExpr').value = s.multiExpr;
  if (s.multiVariables) document.getElementById('multiVariables').value = s.multiVariables;
  if (s.multiPoint) document.getElementById('multiPoint').value = s.multiPoint;
  if (s.multiDirection) document.getElementById('multiDirection').value = s.multiDirection;

  renderChapterObjectives();
  run();
}

function applyChapterPractice(index) {
  const chapterKey = document.getElementById('chapterSelect')?.value;
  const chapter = CHAPTER_PROGRESSION[chapterKey];
  if (!chapter || !chapter.practice || !chapter.practice[index]) return;

  const p = chapter.practice[index];
  document.getElementById('operationType').value = p.op;
  suppressChapterAutoSync = true;
  handleOperationTypeChange();
  suppressChapterAutoSync = false;

  if (p.op.startsWith('matrix_')) {
    if (p.matrixA) document.getElementById('matrixA').value = p.matrixA;
    if (p.matrixB) document.getElementById('matrixB').value = p.matrixB;
  } else if (p.op.startsWith('multivariable_')) {
    if (p.problem) {
      if (p.op === 'multivariable_jacobian') {
        document.getElementById('multiFunctions').value = p.problem;
      } else {
        document.getElementById('multiExpr').value = p.problem;
      }
    }
    if (p.vars) document.getElementById('multiVariables').value = p.vars;
    if (p.point) document.getElementById('multiPoint').value = p.point;
    if (p.direction) document.getElementById('multiDirection').value = p.direction;
  } else {
    if (p.problem) document.getElementById('expr').value = p.problem;
    if (p.variable) document.getElementById('variable').value = p.variable;
    if (typeof p.point === 'number') {
      const pointInput = document.getElementById('lowerLimit');
      if (pointInput && (p.op === 'calculus_limit' || p.op === 'calculus_tangent_line' || p.op === 'calculus_taylor')) {
        pointInput.value = String(p.point);
      }
    }
    if (typeof p.order === 'number') {
      const orderSelect = document.getElementById('order');
      if (orderSelect) orderSelect.value = String(Math.max(1, Math.min(5, p.order)));
    }
  }

  run();
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

  // Show graph for differentiation or integration
  if (payload.operation === 'differentiate') {
    showGraph(payload);
  } else if (payload.operation === 'integrate' && payload.graph) {
    showIntegrationGraph(payload);
  }

  // Clear and render steps
  stepsEl.innerHTML = '';
  
  // Handle both graph.nodes (for differentiate) and steps array (for integrate)
  const nodes = payload.steps || (payload.graph && payload.graph.nodes) || [];
  
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
    
    // Handle both graph nodes (differentiate) and steps (integrate)
    const inputValue = node.input || node.before;
    const outputValue = node.output || node.after;
    
    // Format input and output with matrix support
    const inputFormatted = formatValue(inputValue);
    const outputFormatted = formatValue(outputValue);
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
  } else if (type === 'loading') {
    statusEl.classList.add('loading');
  }
}

let suppressChapterAutoSync = false;
let currentSuggestions = [];

function getRandomItems(list, count) {
  if (!Array.isArray(list) || !list.length) return [];
  const shuffled = [...list].sort(() => Math.random() - 0.5);
  return shuffled.slice(0, Math.min(count, shuffled.length));
}

function normalizeSuggestion(operationType, item) {
  if (typeof item === 'string') {
    return {
      title: `${TOOL_CONTEXT[operationType]?.title || operationType} Drill`,
      expression: item,
      level: 'core',
      goal: 'exam',
      context: 'Core pattern practice.'
    };
  }
  return item;
}

function buildSuggestionExpression(item) {
  if (item.expression) return item.expression;
  if (item.functions) return item.functions;
  if (item.matrixA && item.matrixB) return `${item.matrixA} | ${item.matrixB}`;
  if (item.matrixA) return item.matrixA;
  return '(problem data)';
}

function updateApplicationCards(items, operationType) {
  const grid = document.getElementById('applicationGrid');
  if (!grid) return;

  const advanced = ADVANCED_APPLICATIONS[operationType] || [];
  const source = advanced.length
    ? advanced
    : (Array.isArray(items) ? items.map((text) => ({ domain: 'Applied Math', scenario: text, mathModel: '' })) : []);

  if (!source.length) {
    grid.innerHTML = '<div class="application-card">No real-life applications are mapped yet for this tool.</div>';
    return;
  }

  grid.innerHTML = source
    .map((item) => {
      const domain = item.domain ? `<strong>${item.domain}:</strong> ` : '';
      const model = item.mathModel ? `<div class="micro-note">Model: ${item.mathModel}</div>` : '';
      return `<div class="application-card">${domain}${item.scenario || ''}${model}</div>`;
    })
    .join('');
}

function renderBookConnections(operationType) {
  const list = document.getElementById('bookConnectionList');
  if (!list) return;

  const items = TOOL_BOOK_CONNECTIONS[operationType] || [];
  if (!items.length) {
    list.innerHTML = '<li><strong>Reference:</strong> Chapter mapping currently unavailable for this tool.</li>';
    return;
  }

  list.innerHTML = items
    .map((item) => `<li><strong>${item.label}</strong><br>${item.detail}</li>`)
    .join('');
}

function updateVideoReferences(operationType) {
  const list = document.getElementById('videoReferenceList');
  if (!list) return;

  const title = TOOL_CONTEXT[operationType]?.title || 'math tool';
  const resources = TOOL_VIDEO_RESOURCES[operationType] || [
    { title: `${title} worked examples`, url: `https://www.youtube.com/results?search_query=${encodeURIComponent(`${title} worked examples`)}` },
    { title: `${title} intuition`, url: `https://www.youtube.com/results?search_query=${encodeURIComponent(`${title} intuition`)}` }
  ];

  list.innerHTML = resources
    .map((item) => `<li><a href="${item.url}" target="_blank" rel="noopener noreferrer">${item.title}</a></li>`)
    .join('');
}

function syncChapterFromOperation(operationType) {
  if (suppressChapterAutoSync) return;
  const chapterSelect = document.getElementById('chapterSelect');
  const note = document.getElementById('chapterAutoSyncNote');
  if (!chapterSelect) return;

  const nextChapter = TOOL_TO_CHAPTER[operationType];
  if (!nextChapter || !CHAPTER_PROGRESSION[nextChapter]) {
    if (note) note.textContent = 'Book mapping unavailable for this tool.';
    return;
  }

  if (chapterSelect.value !== nextChapter) {
    chapterSelect.value = nextChapter;
    renderChapterObjectives();
  }
  if (note) note.textContent = `Auto-mapped to ${chapterSelect.options[chapterSelect.selectedIndex].text}.`;
}

function syncLearningContext(operationType) {
  const context = TOOL_CONTEXT[operationType];
  if (!context) return;

  const theoryText = document.getElementById('toolTheoryText');
  const wikiLink = document.getElementById('wikiTheoryLink');
  const chapterText = document.getElementById('chapterReferenceText');
  const chapterLink = document.getElementById('bookReferenceLink');
  const toolBadge = document.getElementById('activeToolBadge');

  if (theoryText) theoryText.textContent = context.theory;
  if (wikiLink) wikiLink.href = context.wiki;
  if (wikiLink) wikiLink.textContent = `${context.title} Theory`;
  if (chapterText) chapterText.textContent = context.chapter;
  if (chapterLink) chapterLink.href = context.chapterLink;
  if (toolBadge) toolBadge.textContent = context.title;

  renderBookConnections(operationType);
  updateVideoReferences(operationType);
  updateApplicationCards(context.applications, operationType);
}

function activateToolChip(operationType) {
  document.querySelectorAll('.tool-chip[data-op]').forEach(chip => {
    chip.classList.toggle('active', chip.getAttribute('data-op') === operationType);
  });
}

function applySuggestion(operationType, payload, runNow = true) {
  const suggestion = normalizeSuggestion(operationType, payload);
  const opEl = document.getElementById('operationType');
  opEl.value = operationType;
  opEl.dispatchEvent(new Event('change', { bubbles: true }));

  if (operationType.startsWith('matrix_')) {
    if (suggestion.matrixA) document.getElementById('matrixA').value = suggestion.matrixA;
    if (suggestion.matrixB) document.getElementById('matrixB').value = suggestion.matrixB;
    if (!suggestion.matrixA && typeof suggestion.expression === 'string') {
      if (suggestion.expression.includes('|')) {
        const [a, b] = suggestion.expression.split('|').map((s) => s.trim());
        document.getElementById('matrixA').value = a;
        document.getElementById('matrixB').value = b;
      } else {
        document.getElementById('matrixA').value = suggestion.expression;
      }
    }
  } else if (operationType.startsWith('multivariable_')) {
    if (operationType === 'multivariable_jacobian') {
      document.getElementById('multiFunctions').value = suggestion.functions || suggestion.expression || '';
    } else {
      document.getElementById('multiExpr').value = suggestion.expression || '';
    }
    document.getElementById('multiVariables').value = suggestion.vars || (operationType === 'multivariable_gradient' ? 'x,y,z' : 'x,y');
    document.getElementById('multiPoint').value = suggestion.point || (operationType === 'multivariable_gradient' ? 'x:1,y:2,z:3' : 'x:1,y:2');
    if (operationType === 'multivariable_directional') {
      document.getElementById('multiDirection').value = suggestion.direction || '1,1';
    }
  } else {
    document.getElementById('expr').value = suggestion.expression || '';
    document.getElementById('variable').value = suggestion.variable || 'x';
    if (typeof suggestion.point === 'number') {
      const pointEl = document.getElementById('lowerLimit');
      if (pointEl) pointEl.value = String(suggestion.point);
    }
    if (typeof suggestion.order === 'number') {
      const orderEl = document.getElementById('order');
      if (orderEl) orderEl.value = String(Math.max(1, Math.min(5, suggestion.order)));
    }
  }
  if (runNow) {
    run();
  } else {
    setStatus('Suggestion loaded. Press Run to solve.', 'success');
  }
}

function generateStudentSuggestions() {
  const operationType = document.getElementById('operationType').value;
  const list = document.getElementById('studentSuggestions');
  const difficulty = document.getElementById('studentDifficulty')?.value || 'all';
  const goal = document.getElementById('studentGoal')?.value || 'all';
  if (!list) return;

  const source = (STUDENT_MODE_BANK[operationType] || []).map((item) => normalizeSuggestion(operationType, item));
  const filtered = source.filter((item) => {
    const levelOk = difficulty === 'all' || item.level === difficulty;
    const goalOk = goal === 'all' || item.goal === goal;
    return levelOk && goalOk;
  });

  const picks = getRandomItems(filtered.length ? filtered : source, 4);
  currentSuggestions = picks;

  if (!source.length) {
    list.innerHTML = '<li>No suggestions available for this toolset yet.</li>';
    return;
  }

  list.innerHTML = picks
    .map((item, idx) => `
      <li>
        <div class="suggestion-top">
          <div class="suggestion-title">${item.title}</div>
          <div class="suggestion-tags">
            <span class="suggestion-tag level-${item.level}">${item.level}</span>
            <span class="suggestion-tag">${item.goal}</span>
          </div>
        </div>
        <div class="suggestion-expression">${buildSuggestionExpression(item)}</div>
        <div class="suggestion-context">${item.context || 'Practice this pattern for fluency.'}</div>
        <div class="suggestion-actions">
          <button type="button" class="use-suggestion-btn" data-action="load" data-index="${idx}">Load</button>
          <button type="button" class="use-suggestion-btn" data-action="run" data-index="${idx}">Load and Run</button>
        </div>
      </li>
    `)
    .join('');
}

function clearVisibleInputs() {
  const operationType = document.getElementById('operationType').value;
  if (operationType.startsWith('matrix_')) {
    document.getElementById('matrixA').value = '';
    if (operationType === 'matrix_multiply') document.getElementById('matrixB').value = '';
  } else if (operationType.startsWith('multivariable_')) {
    document.getElementById('multiExpr').value = '';
    document.getElementById('multiFunctions').value = '';
    document.getElementById('multiPoint').value = '';
    document.getElementById('multiDirection').value = '';
  } else {
    document.getElementById('expr').value = '';
    document.getElementById('lowerLimit').value = '';
    document.getElementById('upperLimit').value = '';
  }
  document.getElementById('resultPanel').style.display = 'none';
  setStatus('Inputs cleared', 'normal');
}

function loadRandomSuggestion(runNow = true) {
  const operationType = document.getElementById('operationType').value;
  if (!currentSuggestions.length) {
    generateStudentSuggestions();
  }
  if (!currentSuggestions.length) {
    setStatus('No suggestions available for this selection.', 'error');
    return;
  }
  const pick = currentSuggestions[Math.floor(Math.random() * currentSuggestions.length)];
  applySuggestion(operationType, pick, runNow);
}

async function run() {
  const operationType = document.getElementById('operationType').value;
  const verbosity = document.getElementById('verbosity').value;
  const showJson = document.getElementById('showJson').checked;

  const jsonWrap = document.getElementById('jsonWrap');
  const jsonEl = document.getElementById('json');

  setStatus('Computing...', 'loading');
  const runBtn = document.getElementById('run');
  runBtn.disabled = true;
  runBtn.classList.add('loading');

  try {
    let payload, timing;

    if (operationType === 'differentiate') {
      let expr = normalizeExpressionInput(document.getElementById('expr').value.trim());
      const variable = document.getElementById('variable').value.trim() || 'x';
      const order = parseInt(document.getElementById('order').value, 10);

      // Convenience: if user selects a non-x variable but expression only uses x,
      // rewrite x -> selected variable to match typical classroom intent.
      if (variable !== 'x' && !containsVariable(expr, variable) && containsVariable(expr, 'x')) {
        expr = replaceStandaloneX(expr, variable);
        document.getElementById('expr').value = expr;
      }

      if (!expr) {
        setStatus('Please enter an expression', 'error');
        runBtn.disabled = false;
        runBtn.classList.remove('loading');
        return;
      }

      const result = await callAPI(expr, variable, order, verbosity);
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
    } else if (operationType === 'integrate') {
      const expr = normalizeExpressionInput(document.getElementById('expr').value.trim());
      const variable = document.getElementById('variable').value.trim() || 'x';
      const lowerLimitEl = document.getElementById('lowerLimit');
      const upperLimitEl = document.getElementById('upperLimit');
      const lowerLimit = lowerLimitEl && lowerLimitEl.value.trim() ? lowerLimitEl.value.trim() : null;
      const upperLimit = upperLimitEl && upperLimitEl.value.trim() ? upperLimitEl.value.trim() : null;

      if (!expr) {
        setStatus('Please enter an expression', 'error');
        runBtn.disabled = false;
        runBtn.classList.remove('loading');
        return;
      }

      const result = await callIntegrationAPI(expr, variable, lowerLimit, upperLimit, verbosity);
      payload = result.data;
      timing = result.timing;
    } else if (operationType.startsWith('multivariable_')) {
      const expression = normalizeExpressionInput(document.getElementById('multiExpr').value.trim());
      const variablesRaw = document.getElementById('multiVariables').value.trim();
      const pointRaw = document.getElementById('multiPoint').value.trim();
      const directionRaw = document.getElementById('multiDirection').value.trim();
      const functionsRaw = normalizeExpressionInput(document.getElementById('multiFunctions').value.trim());

      const variables = parseVariablesList(variablesRaw);
      if (!variables.length) {
        setStatus('Please enter variables as comma-separated values (e.g., x,y)', 'error');
        runBtn.disabled = false;
        runBtn.classList.remove('loading');
        return;
      }

      const point = parsePointMap(pointRaw);
      const direction = parseDirectionVector(directionRaw);
      const basePayload = {
        variables,
        point,
        verbosity,
        format: 'json'
      };

      let payloadBody;
      if (operationType === 'multivariable_jacobian') {
        const expressions = functionsRaw.split(',').map(s => s.trim()).filter(Boolean);
        if (!expressions.length) {
          setStatus('Jacobian requires vector function components (e.g., x*y, x**2+y)', 'error');
          runBtn.disabled = false;
          runBtn.classList.remove('loading');
          return;
        }
        payloadBody = { ...basePayload, expressions };
      } else if (operationType === 'multivariable_directional') {
        if (!expression) {
          setStatus('Please enter an expression for directional derivative', 'error');
          runBtn.disabled = false;
          runBtn.classList.remove('loading');
          return;
        }
        if (!point) {
          setStatus('Directional derivative requires a point (e.g., x:1,y:2)', 'error');
          runBtn.disabled = false;
          runBtn.classList.remove('loading');
          return;
        }
        if (!direction || direction.length !== variables.length) {
          setStatus('Direction vector length must match number of variables', 'error');
          runBtn.disabled = false;
          runBtn.classList.remove('loading');
          return;
        }
        payloadBody = { ...basePayload, expression, direction };
      } else {
        if (!expression) {
          setStatus('Please enter a multivariable expression', 'error');
          runBtn.disabled = false;
          runBtn.classList.remove('loading');
          return;
        }
        payloadBody = { ...basePayload, expression };
      }

      const result = await callMultivariableAPI(operationType, payloadBody);
      payload = result.data;
      timing = result.timing;
    } else if (operationType.startsWith('algebra_') || operationType.startsWith('calculus_')) {
      const expr = normalizeExpressionInput(document.getElementById('expr').value.trim());
      const variable = document.getElementById('variable').value.trim() || 'x';
      const pointRaw = document.getElementById('lowerLimit')?.value?.trim() || '';
      const point = pointRaw !== '' ? Number(pointRaw) : null;
      const orderVal = parseInt(document.getElementById('order')?.value || '5', 10);

      if (!expr) {
        setStatus('Please enter an expression', 'error');
        runBtn.disabled = false;
        runBtn.classList.remove('loading');
        return;
      }

      if ((operationType === 'calculus_limit' || operationType === 'calculus_taylor' || operationType === 'calculus_tangent_line') && (point === null || Number.isNaN(point))) {
        setStatus('Please provide a numeric point in the limits input', 'error');
        runBtn.disabled = false;
        runBtn.classList.remove('loading');
        return;
      }

      const result = await callSymbolicAPI(operationType, {
        expression: expr,
        variable,
        point,
        order: Number.isNaN(orderVal) ? 5 : orderVal,
        verbosity,
        format: 'json'
      });
      payload = result.data;
      timing = result.timing;
    } else {
      // Matrix operations
      const matrixA = document.getElementById('matrixA').value.trim();
      
      if (!matrixA) {
        setStatus('Please enter Matrix A', 'error');
        runBtn.disabled = false;
        runBtn.classList.remove('loading');
        return;
      }

      let matrixB = null;
      if (operationType === 'matrix_multiply') {
        matrixB = document.getElementById('matrixB').value.trim();
        if (!matrixB) {
          setStatus('Please enter Matrix B', 'error');
          runBtn.disabled = false;
          runBtn.classList.remove('loading');
          return;
        }
      }

      const result = await callMatrixAPI(operationType, matrixA, matrixB, verbosity);
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
    runBtn.classList.remove('loading');
  }
}

// Event listeners
document.getElementById('run').addEventListener('click', run);

function handleOperationTypeChange() {
  const operationType = document.getElementById('operationType').value;
  const calcInput = document.getElementById('calcInput');
  const matrixInput = document.getElementById('matrixInput');
  const multivarInput = document.getElementById('multivarInput');
  const variableLabel = document.getElementById('variableLabel');
  const orderLabel = document.getElementById('orderLabel');
  const limitsLabel = document.getElementById('limitsLabel');
  const matrixBLabel = document.getElementById('matrixBLabel');
  const diffExamples = document.getElementById('diffExamples');
  const intExamples = document.getElementById('intExamples');
  const multiFunctionsLabel = document.getElementById('multiFunctionsLabel');
  const multiDirectionLabel = document.getElementById('multiDirectionLabel');

  if (operationType === 'differentiate') {
    calcInput.style.display = 'block';
    matrixInput.style.display = 'none';
    if (multivarInput) multivarInput.style.display = 'none';
    variableLabel.style.display = 'block';
    orderLabel.style.display = 'block';
    if (limitsLabel) limitsLabel.style.display = 'none';
    if (diffExamples) diffExamples.style.display = 'flex';
    if (intExamples) intExamples.style.display = 'none';
  } else if (operationType === 'integrate') {
    calcInput.style.display = 'block';
    matrixInput.style.display = 'none';
    if (multivarInput) multivarInput.style.display = 'none';
    variableLabel.style.display = 'block';
    orderLabel.style.display = 'none';
    if (limitsLabel) {
      limitsLabel.style.display = 'block';
      const limitsCaption = limitsLabel.querySelector('span');
      if (limitsCaption) limitsCaption.textContent = 'to';
      const upper = document.getElementById('upperLimit');
      if (upper) upper.style.display = '';
    }
    if (diffExamples) diffExamples.style.display = 'none';
    if (intExamples) intExamples.style.display = 'flex';
  } else if (operationType.startsWith('algebra_') || operationType.startsWith('calculus_')) {
    calcInput.style.display = 'block';
    matrixInput.style.display = 'none';
    if (multivarInput) multivarInput.style.display = 'none';
    variableLabel.style.display = 'block';
    if (operationType === 'calculus_taylor') {
      orderLabel.style.display = 'block';
    } else if (operationType === 'differentiate') {
      orderLabel.style.display = 'block';
    } else {
      orderLabel.style.display = 'none';
    }
    if (limitsLabel) {
      const limitsCaption = limitsLabel.querySelector('span');
      if (operationType === 'calculus_limit' || operationType === 'calculus_taylor' || operationType === 'calculus_tangent_line') {
        limitsLabel.style.display = 'block';
        const upper = document.getElementById('upperLimit');
        if (upper) upper.style.display = 'none';
        if (limitsCaption) limitsCaption.textContent = 'at';
      } else {
        limitsLabel.style.display = 'none';
        const upper = document.getElementById('upperLimit');
        if (upper) upper.style.display = '';
      }
    }
    if (diffExamples) diffExamples.style.display = operationType.startsWith('calculus_') ? 'flex' : 'none';
    if (intExamples) intExamples.style.display = 'none';
  } else if (operationType.startsWith('multivariable_')) {
    calcInput.style.display = 'none';
    matrixInput.style.display = 'none';
    if (multivarInput) multivarInput.style.display = 'block';
    variableLabel.style.display = 'none';
    orderLabel.style.display = 'none';
    if (limitsLabel) limitsLabel.style.display = 'none';
    if (diffExamples) diffExamples.style.display = 'none';
    if (intExamples) intExamples.style.display = 'none';
    if (multiFunctionsLabel) {
      multiFunctionsLabel.style.display = operationType === 'multivariable_jacobian' ? 'block' : 'none';
    }
    if (multiDirectionLabel) {
      multiDirectionLabel.style.display = operationType === 'multivariable_directional' ? 'block' : 'none';
    }
  } else {
    calcInput.style.display = 'none';
    matrixInput.style.display = 'block';
    if (multivarInput) multivarInput.style.display = 'none';
    variableLabel.style.display = 'none';
    orderLabel.style.display = 'none';
    if (limitsLabel) {
      limitsLabel.style.display = 'none';
      const upper = document.getElementById('upperLimit');
      if (upper) upper.style.display = '';
      const limitsCaption = limitsLabel.querySelector('span');
      if (limitsCaption) limitsCaption.textContent = 'to';
    }
    if (diffExamples) diffExamples.style.display = 'none';
    if (intExamples) intExamples.style.display = 'none';

    // Show/hide Matrix B based on operation
    if (operationType === 'matrix_multiply') {
      matrixBLabel.style.display = 'block';
    } else {
      matrixBLabel.style.display = 'none';
    }
  }
  activateToolChip(operationType);
  syncLearningContext(operationType);
  syncChapterFromOperation(operationType);
  generateStudentSuggestions();
}

document.getElementById('operationType').addEventListener('change', handleOperationTypeChange);

document.querySelectorAll('.tool-chip[data-op]').forEach(btn => {
  btn.addEventListener('click', () => {
    const op = btn.getAttribute('data-op');
    if (!op) return;
    document.getElementById('operationType').value = op;
    handleOperationTypeChange();
    run();
  });
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
    // Keep current operation (integrate or differentiate) - don't force differentiate
    // Trigger change event to show correct inputs
    handleOperationTypeChange();
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
    handleOperationTypeChange();
    run();
  });
});

document.querySelectorAll('.multi-example-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    const op = btn.getAttribute('data-op');
    if (!op) return;
    document.getElementById('operationType').value = op;
    handleOperationTypeChange();

    const expr = btn.getAttribute('data-expr');
    const vars = btn.getAttribute('data-vars');
    const point = btn.getAttribute('data-point');
    const direction = btn.getAttribute('data-direction');
    const funcs = btn.getAttribute('data-functions');

    if (expr) document.getElementById('multiExpr').value = expr;
    if (vars) document.getElementById('multiVariables').value = vars;
    if (point) document.getElementById('multiPoint').value = point;
    if (direction) document.getElementById('multiDirection').value = direction;
    if (funcs) document.getElementById('multiFunctions').value = funcs;

    run();
  });
});

document.querySelectorAll('.assignment-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    const op = btn.getAttribute('data-op');
    if (!op) return;
    document.getElementById('operationType').value = op;
    handleOperationTypeChange();

    if (op.startsWith('matrix_')) {
      const a = btn.getAttribute('data-a');
      const b = btn.getAttribute('data-b');
      if (a) document.getElementById('matrixA').value = a;
      if (b) document.getElementById('matrixB').value = b;
    } else {
      const expr = btn.getAttribute('data-expr');
      const variable = btn.getAttribute('data-var') || 'x';
      if (expr) document.getElementById('expr').value = expr;
      document.getElementById('variable').value = variable;
    }

    run();
  });
});

document.getElementById('suggestProblemsBtn')?.addEventListener('click', generateStudentSuggestions);
document.getElementById('studentDifficulty')?.addEventListener('change', generateStudentSuggestions);
document.getElementById('studentGoal')?.addEventListener('change', generateStudentSuggestions);
document.getElementById('clearInputsBtn')?.addEventListener('click', clearVisibleInputs);
document.getElementById('randomSuggestionBtn')?.addEventListener('click', () => loadRandomSuggestion(true));

document.getElementById('studentSuggestions')?.addEventListener('click', (event) => {
  const btn = event.target.closest('.use-suggestion-btn');
  if (!btn) return;
  const operationType = document.getElementById('operationType').value;
  const action = btn.getAttribute('data-action') || 'run';
  const index = Number(btn.getAttribute('data-index'));
  if (Number.isNaN(index) || !currentSuggestions[index]) return;
  applySuggestion(operationType, currentSuggestions[index], action === 'run');
});

document.getElementById('chapterSelect')?.addEventListener('change', renderChapterObjectives);
document.getElementById('startChapterBtn')?.addEventListener('click', startSelectedChapter);
document.getElementById('completeChapterTaskBtn')?.addEventListener('click', markNextObjectiveDone);
document.getElementById('chapterPracticeList')?.addEventListener('click', (event) => {
  const btn = event.target.closest('.chapter-practice-action');
  if (!btn) return;
  const index = Number(btn.getAttribute('data-practice-index'));
  if (Number.isNaN(index)) return;
  applyChapterPractice(index);
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
  handleOperationTypeChange();
  renderChapterObjectives();
  
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

function showIntegrationGraph(payload) {
  const graphPanel = document.getElementById('graphPanel');
  const canvas = document.getElementById('graphCanvas');
  
  if (!graphPanel || !canvas || !payload.graph || !payload.graph.data) {
    return;
  }
  
  graphPanel.style.display = 'block';

  if (currentChart) {
    currentChart.destroy();
  }

  const graphData = payload.graph.data;
  const limits = payload.graph.limits;
  const isDark = document.body.classList.contains('dark-theme');
  const ctx = canvas.getContext('2d');
  
  const datasets = [];
  
  // Check if this is a definite integral
  const isDefinite = limits && limits.lower !== null && limits.upper !== null;
  
  // Add area under curve for definite integrals
  if (isDefinite && graphData.area && graphData.area.x && graphData.area.y && graphData.area.x.length > 0) {
    // Add shaded area dataset
    datasets.push({
      label: `Area = ${graphData.area.value?.toFixed(4) || '?'}`,
      data: graphData.area.x.map((x, i) => ({
        x: x,
        y: graphData.area.y[i]
      })),
      borderColor: 'rgba(16, 185, 129, 0.6)',
      backgroundColor: 'rgba(16, 185, 129, 0.2)',
      borderWidth: 0,
      tension: 0.4,
      pointRadius: 0,
      fill: 'origin',  // Fill to y=0
      spanGaps: false,
      order: 2  // Draw behind other lines
    });
  } else {
    // For indefinite integrals area shading is intentionally omitted.
  }
  
  // Add integrand curve
  if (graphData.integrand_curve && graphData.x_values) {
    datasets.push({
      label: payload.graph.labels?.integrand || `f(x) = ${payload.input}`,
      data: graphData.x_values.map((x, i) => ({
        x: x,
        y: graphData.integrand_curve[i]
      })),
      borderColor: '#6366f1',
      backgroundColor: 'rgba(99, 102, 241, 0.1)',
      borderWidth: 3,
      tension: 0.4,
      pointRadius: 0,
      fill: false,
      spanGaps: true,
      order: 1
    });
  }
  
  // Add antiderivative curve (only for indefinite integrals or if requested)
  if (!isDefinite && graphData.antiderivative_curve && graphData.x_values) {
    datasets.push({
      label: payload.graph.labels?.antiderivative || `F(x) = ∫f(x)dx`,
      data: graphData.x_values.map((x, i) => ({
        x: x,
        y: graphData.antiderivative_curve[i]
      })),
      borderColor: '#8b5cf6',
      backgroundColor: 'rgba(139, 92, 246, 0.1)',
      borderWidth: 3,
      borderDash: [5, 5],
      tension: 0.4,
      pointRadius: 0,
      fill: false,
      spanGaps: true,
      order: 1
    });
  }
  
  currentChart = new Chart(ctx, {
    type: 'line',
    data: { datasets },
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
  // First, convert all ** to a temporary placeholder to avoid issues with parentheses
  let evaluated = expr.replace(/\*\*/g, '^POWER^');
  
  // Replace x with the actual value
  evaluated = evaluated.replace(/x/g, `(${x})`);
  
  // Now convert ^POWER^ to Math.pow with proper syntax
  // This handles cases like sin((value)^POWER^2)
  while (evaluated.includes('^POWER^')) {
    evaluated = evaluated.replace(/(\([^()]*\)|[\d.]+)\^POWER\^(\([^()]*\)|[\d.]+)/g, 'Math.pow($1,$2)');
  }
  
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
  
  // Error function approximation
  evaluated = evaluated.replace(/\berf\b/g, '__erf');
  
  // Replace constants
  evaluated = evaluated.replace(/\bpi\b/g, 'Math.PI');
  evaluated = evaluated.replace(/\be\b(?!\d)/g, 'Math.E');
  
  try {
    // Define erf function for evaluation
    const __erf = (x) => {
      // Abramowitz and Stegun approximation
      const sign = x >= 0 ? 1 : -1;
      x = Math.abs(x);
      const a1 = 0.254829592;
      const a2 = -0.284496736;
      const a3 = 1.421413741;
      const a4 = -1.453152027;
      const a5 = 1.061405429;
      const p = 0.3275911;
      const t = 1.0 / (1.0 + p * x);
      const y = 1.0 - (((((a5 * t + a4) * t) + a3) * t + a2) * t + a1) * t * Math.exp(-x * x);
      return sign * y;
    };
    
    return eval(evaluated);
  } catch (e) {
    return null;
  }
}

