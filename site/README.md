# Calcora Web Demo

This directory contains the static website and interactive demo for Calcora v0.2.

## Files

- **index.html** - Landing page with project overview
- **demo.html** - Interactive demo for testing Calcora in the browser
- **modern-theme.css** - Glassmorphism design system (shared)
- **media/** - Demo videos and assets

## Local Development

To test locally:

```bash
# Terminal 1: Start backend
cd ..
python -m uvicorn calcora.api.main:app --reload

# Terminal 2: Start frontend
cd site
python -m http.server 5000
```

Then open: http://localhost:5000/demo.html

## Deployment

See [DEPLOYMENT_GUIDE.md](../DEPLOYMENT_GUIDE.md) for complete deployment instructions:
- **Frontend**: Netlify (static site)
- **Backend**: Render.com (FastAPI)

## Demo Features

The interactive demo supports:

### Differentiation
- Symbolic expressions (sin, cos, exp, log, etc.)
- Step-by-step explanations with rule names
- Multiple verbosity levels (concise, detailed, teacher)
- Interactive graphs showing f(x) and f'(x)

### Integration (NEW in v0.2!)
- Indefinite integrals with automatic technique detection
- Definite integrals with bounds
- Multiple techniques: power rule, substitution, by parts, trigonometric
- Step-by-step explanations showing integration technique
- Area under curve visualization

### Matrix Operations
- Determinants (numeric and symbolic)
- Matrix inverse
- Matrix multiplication
- RREF (Row Reduced Echelon Form)
- Eigenvalues
- LU decomposition

## Customization

To customize branding:
1. Edit CSS variables in `modern-theme.css`
2. Update colors: `--primary`, `--secondary`, etc.
3. Modify logo in header section of HTML files

## API Integration

The demo connects to the backend API:
```javascript
const API_URL = 'https://calcora.onrender.com/api/compute';

// Example request
fetch(API_URL, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    operation: 'integrate',
    expression: 'x**2',
    variable: 'x',
    verbosity: 'detailed'
  })
})
```

## Browser Support

- Chrome 90+ ✅
- Firefox 88+ ✅
- Safari 14+ ✅
- Edge 90+ ✅

Requires:
- ES6 JavaScript
- CSS backdrop-filter support (glassmorphism)
- Chart.js for graphs
- KaTeX for math rendering
2. Update text in `index.html` and `demo.html`
3. Add logo/favicon if desired

## API Endpoint

The demo calls: `/.netlify/functions/calcora_engine`

Request format:
```json
{
  "operation": "differentiate",
  "expression": "sin(x**2)",
  "variable": "x",
  "verbosity": "detailed"
}
```

Response format:
```json
{
  "operation": "differentiate",
  "input": "sin(x**2)",
  "output": "2*x*cos(x**2)",
  "graph": {
    "nodes": [
      {
        "id": "step_001",
        "rule": "chain_rule_sin",
        "explanation": "..."
      }
    ]
  }
}
```
