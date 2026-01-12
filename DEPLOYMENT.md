# Deploying Calcora to Netlify

This guide explains how to deploy Calcora's interactive demo to Netlify for sharing with universities and other users.

## Overview

The Netlify deployment includes:
- **Static site** (`site/`) - Documentation and landing page
- **Interactive demo** (`site/demo.html`) - Browser-based computation interface
- **Serverless function** (`netlify/functions/calcora_engine.py`) - Python backend for computations

## Prerequisites

- GitHub account
- Netlify account (free tier works fine)
- Repository pushed to GitHub

## Deployment Steps

### 1. Push to GitHub

```bash
git add .
git commit -m "Add Netlify deployment configuration"
git push origin main
```

### 2. Connect to Netlify

1. Go to [netlify.com](https://netlify.com) and sign in
2. Click "Add new site" → "Import an existing project"
3. Select GitHub and authorize Netlify
4. Choose your `calcora` repository
5. Netlify will auto-detect the configuration from `netlify.toml`

### 3. Configure Build Settings

Netlify should automatically detect these settings from `netlify.toml`:

- **Build command**: `pip install --upgrade pip && pip install '.[engine-sympy]'`
- **Publish directory**: `site`
- **Functions directory**: `netlify/functions`
- **Python version**: 3.11

If not, manually set them in the build settings.

### 4. Deploy

Click "Deploy site". The first build takes 3-5 minutes.

### 5. Custom Domain (Optional)

After deployment:
1. Go to Site settings → Domain management
2. Add a custom domain like `calcoralive.netlify.app` or your own domain
3. Netlify provides free HTTPS certificates

## Testing the Deployment

Once deployed, you'll get a URL like: `https://YOUR-SITE-NAME.netlify.app`

Test these endpoints:

1. **Landing page**: `https://YOUR-SITE-NAME.netlify.app/`
2. **Interactive demo**: `https://YOUR-SITE-NAME.netlify.app/demo.html`
3. **API function** (POST request):
   ```bash
   curl -X POST https://YOUR-SITE-NAME.netlify.app/.netlify/functions/calcora_engine \
     -H "Content-Type: application/json" \
     -d '{"operation":"differentiate","expression":"sin(x**2)","verbosity":"detailed"}'
   ```

## Features Available in Demo

### Differentiation
- Symbolic differentiation with step-by-step explanations
- Chain rule, product rule, power rule
- Trigonometric, exponential, logarithmic functions
- Multiple verbosity levels (concise, detailed, teacher)

### Matrix Operations
- **Determinants**: 2×2, 3×3, and general matrices
- **Inverse**: Matrix inversion with steps
- **Multiplication**: Matrix-matrix multiplication
- **RREF**: Row Reduced Echelon Form
- **Eigenvalues**: Eigenvalue computation
- **LU Decomposition**: LU factorization
- **Symbolic matrices**: Variables as matrix entries (e.g., [["a","b"],["c","d"]])

## Sharing with Universities

### Example Email Template

```
Subject: Calcora Demo - Step-by-Step Math Computation Engine

Hi [Professor/Admissions Committee],

I'd like to share Calcora, an open-source computational mathematics 
engine I've been developing. It provides step-by-step explanations for 
mathematical operations, making it useful for education and learning.

Live Demo: https://YOUR-SITE-NAME.netlify.app/demo.html

Try these examples:
- Differentiate: sin(x^2), x^3*cos(x), exp(x^2)
- Matrix determinant: [[1,2],[3,4]]
- Symbolic matrix: [["a","b"],["c","d"]]

The demo runs entirely in your browser with no installation required.

Source code: https://github.com/YOUR-USERNAME/calcora
Documentation: https://YOUR-SITE-NAME.netlify.app/

Key features:
✓ Step-by-step reasoning DAG
✓ Symbolic and numeric computation
✓ Plugin architecture for extensibility
✓ CLI, API, and web interfaces
✓ Offline-capable (self-hostable)

I'm happy to discuss the technical architecture or provide additional 
examples.

Best regards,
[Your Name]
```

## Monitoring and Logs

### View Function Logs

1. Go to Netlify dashboard → Functions
2. Click on `calcora_engine`
3. View real-time logs and invocation stats

### Monitor Usage

Free tier includes:
- 125K function requests/month
- 100GB bandwidth
- Unlimited sites

## Troubleshooting

### Function Timeout

If computations take >10 seconds, they'll timeout. This is a Netlify limitation. For complex operations, suggest local installation:

```
For larger computations, please try the desktop version:
pip install calcora[engine-sympy,cli]
calcora differentiate "your_expression"
```

### Build Failures

**Issue**: `ModuleNotFoundError: No module named 'calcora'`

**Solution**: Ensure `pyproject.toml` is in repository root and build command installs the package:
```toml
[build]
  command = "pip install --upgrade pip && pip install '.[engine-sympy]'"
```

**Issue**: SymPy import errors

**Solution**: Check that `sympy>=1.12` is in dependencies and `netlify/functions/requirements.txt`

### CORS Errors

If the demo can't reach the API function, check:
1. Function includes CORS headers (already configured)
2. Browser console for errors
3. Function logs in Netlify dashboard

## Local Testing Before Deploy

Test the Netlify function locally:

```bash
# Install Netlify CLI
npm install -g netlify-cli

# Start local dev server
netlify dev
```

This runs the function at `http://localhost:8888/.netlify/functions/calcora_engine`

## Continuous Deployment

Once connected, every push to `main` branch triggers automatic deployment:

```bash
git add .
git commit -m "Update demo examples"
git push origin main
# Netlify auto-deploys within 1-2 minutes
```

## Cost

Free tier is sufficient for university demo purposes:
- **Cost**: $0/month
- **Limits**: 125K function calls, 100GB bandwidth
- **Performance**: Cold starts ~1-2s, warm ~200ms

For production use or higher traffic, consider Netlify Pro ($19/month).

## Security Considerations

### Input Validation

The function validates:
- Expression syntax (SymPy parsing)
- Operation names (whitelist)
- JSON structure

### Rate Limiting

Netlify automatically rate-limits abusive requests. For additional protection:
1. Add Netlify Identity with rate limiting
2. Use Cloudflare in front of Netlify

### Privacy

- No data is logged or stored
- All computation happens serverless (stateless)
- No analytics tracking by default

## Next Steps

1. **Custom branding**: Update site colors/logo in `site/style.css`
2. **Analytics**: Add privacy-friendly analytics (Plausible, Simple Analytics)
3. **Feedback form**: Add form for university feedback
4. **Performance**: Monitor function execution times in Netlify dashboard
5. **Documentation**: Link to GitHub repo for source code exploration

## Support

If universities have questions:
- Point to GitHub Issues: `https://github.com/YOUR-USERNAME/calcora/issues`
- Provide this deployment guide
- Share source code architecture: `ARCHITECTURE.md`
