# Calcora Web Demo

This directory contains the static website and interactive demo for Calcora.

## Files

- **index.html** - Landing page with project overview
- **demo.html** - Interactive demo for testing Calcora in the browser
- **style.css** - Shared styles for both pages

## Local Development

To test locally, you can use Python's built-in HTTP server:

```bash
cd site
python -m http.server 8000
```

Then open: http://localhost:8000

Note: The demo won't work locally without the Netlify function. Use `netlify dev` for full local testing.

## Netlify Deployment

This site automatically deploys to Netlify when pushed to GitHub. The Netlify function (`netlify/functions/calcora_engine.py`) provides the computation backend.

See [DEPLOYMENT.md](../DEPLOYMENT.md) for full deployment guide.

## Demo Features

The interactive demo supports:

### Differentiation
- Symbolic expressions (sin, cos, exp, log, etc.)
- Step-by-step explanations
- Multiple verbosity levels

### Matrix Operations
- Determinants (numeric and symbolic)
- Matrix inverse
- Matrix multiplication
- RREF
- Eigenvalues
- LU decomposition

## Customization

To customize branding:
1. Edit colors in `style.css`
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
