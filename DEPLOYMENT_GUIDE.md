# Deployment & Distribution Guide

Complete guide for deploying Calcora's frontend, backend, and creating distributable executables.

## Quick Links
- [Frontend Deployment (Netlify)](#frontend-deployment-netlify)
- [Backend Deployment (Render)](#backend-deployment-render)
- [Building Executables](#building-executables)
- [Self-Hosting](#self-hosting)

---

## Frontend Deployment (Netlify)

### Overview
The frontend includes:
- **Static site** (`site/`) - Landing page and documentation
- **Interactive demo** (`site/demo.html`) - Browser-based computation interface
- **Modern UI** with glassmorphism design, KaTeX rendering, and Chart.js graphs

### Prerequisites
- GitHub account
- Netlify account (free tier)
- Repository pushed to GitHub

### Deployment Steps

#### 1. Push to GitHub
```bash
git add .
git commit -m "Deploy frontend"
git push origin main
```

#### 2. Connect to Netlify
1. Go to [netlify.com](https://netlify.com) and sign in
2. Click "Add new site" → "Import an existing project"
3. Select GitHub and authorize Netlify
4. Choose your `calcora` repository

#### 3. Configure Build Settings
- **Build command**: Leave empty (static site)
- **Publish directory**: `site`
- **Build settings**: None needed

#### 4. Deploy
Click "Deploy site". Build takes ~1 minute.

#### 5. Update API URL
After deployment, update the API URL in `site/demo.html`:
```javascript
const API_URL = 'https://YOUR-BACKEND-URL.onrender.com/api/compute';
```

### Testing
Visit your Netlify URL (e.g., `https://calcoralive.netlify.app`):
- Landing page: `/`
- Demo: `/demo.html`
- Test all three tabs: Differentiation, Integration, Matrices

---

## Backend Deployment (Render)

### Overview
FastAPI backend with:
- Unified `/api/compute` endpoint
- Integration engine with step-by-step explanations
- Differentiation and matrix operations
- CORS enabled for Netlify frontend

### Prerequisites
- GitHub account
- Render account (free tier)
- Repository pushed to GitHub

### Deployment Steps

#### 1. Create New Web Service
1. Go to [render.com](https://render.com) and sign in
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Select the `calcora` repository

#### 2. Configure Service
- **Name**: `calcora`
- **Region**: Choose nearest to your users
- **Branch**: `main`
- **Root Directory**: Leave empty
- **Runtime**: Python 3
- **Build Command**:
  ```bash
  pip install sympy fastapi "uvicorn[standard]" && pip install -e .
  ```
- **Start Command**:
  ```bash
  uvicorn calcora.api.main:app --host 0.0.0.0 --port $PORT
  ```

#### 3. Environment Variables
No environment variables needed for basic deployment.

#### 4. Deploy
Click "Create Web Service". First build takes 3-5 minutes.

#### 5. Update Frontend
Update the API URL in your frontend (Netlify):
```javascript
const API_URL = 'https://calcora.onrender.com/api/compute';
```
Commit and push to trigger Netlify rebuild.

### Testing
Test the API endpoint:
```bash
# Differentiation
curl -X POST https://calcora.onrender.com/api/compute \
  -H "Content-Type: application/json" \
  -d '{"operation":"differentiate","expression":"x**2","variable":"x","verbosity":"detailed"}'

# Integration
curl -X POST https://calcora.onrender.com/api/compute \
  -H "Content-Type: application/json" \
  -d '{"operation":"integrate","expression":"x**2","variable":"x","verbosity":"detailed"}'
```

---

## Building Executables

Create standalone executables for Windows distribution.

### Prerequisites
- Python 3.11+ with virtual environment activated
- All dependencies installed: `pip install -e .[engine-sympy,cli,api]`
- PyInstaller: `pip install pyinstaller`

### Build Everything
```powershell
.\build.ps1
```

This creates in `dist/`:
- `calcora.exe` - Command-line interface
- `calcora-server.exe` - Web server with UI

### Build Individual Components
```powershell
# Build only CLI
.\build.ps1 cli

# Build only server
.\build.ps1 server
```

### Using the Executables

#### CLI
```powershell
# Differentiate
.\calcora.exe differentiate "x**2 + sin(x)"

# Integrate
.\calcora.exe integrate "x**2" --lower 0 --upper 1

# Matrix operations
.\calcora.exe matrix-multiply "[[1,2],[3,4]]" "[[5,6],[7,8]]"
```

#### Web Server
```powershell
# Start server (opens browser automatically)
.\calcora-server.exe
```

Or use the launcher:
```powershell
.\Start-WebUI.bat
```

Server runs on `http://127.0.0.1:8000/static/index.html`

### Distribution Package
Create a distribution folder:
```
calcora-distribution/
├── calcora.exe
├── calcora-server.exe
├── Start-WebUI.bat
├── README.txt
└── LICENSE.txt
```

Zip this folder for distribution.

---

## Self-Hosting

Run Calcora on your own infrastructure.

### Option 1: Docker (Recommended)

#### Frontend
```dockerfile
# Dockerfile.frontend
FROM nginx:alpine
COPY site/ /usr/share/nginx/html/
EXPOSE 80
```

```bash
docker build -f Dockerfile.frontend -t calcora-frontend .
docker run -d -p 80:80 calcora-frontend
```

#### Backend
```dockerfile
# Dockerfile.backend
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install sympy fastapi "uvicorn[standard]" && pip install -e .
EXPOSE 8000
CMD ["uvicorn", "calcora.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```bash
docker build -f Dockerfile.backend -t calcora-backend .
docker run -d -p 8000:8000 calcora-backend
```

### Option 2: systemd (Linux)

#### Backend Service
Create `/etc/systemd/system/calcora-api.service`:
```ini
[Unit]
Description=Calcora API Server
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/calcora
Environment="PATH=/opt/calcora/.venv/bin"
ExecStart=/opt/calcora/.venv/bin/uvicorn calcora.api.main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable calcora-api
sudo systemctl start calcora-api
sudo systemctl status calcora-api
```

#### Frontend with nginx
```nginx
# /etc/nginx/sites-available/calcora
server {
    listen 80;
    server_name calcora.yourdomain.com;
    
    root /var/www/calcora/site;
    index index.html;
    
    location / {
        try_files $uri $uri/ =404;
    }
    
    # Proxy API requests to backend
    location /api/ {
        proxy_pass http://localhost:8000/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/calcora /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### Option 3: Python HTTP Server (Development)

#### Frontend
```bash
cd site
python -m http.server 5000
# Visit http://localhost:5000
```

#### Backend
```bash
python -m uvicorn calcora.api.main:app --reload
# API available at http://localhost:8000
```

---

## Monitoring

### Netlify
- Dashboard → Site overview → Analytics
- Function logs → Real-time invocations
- Deploy logs → Build output

### Render
- Dashboard → Service → Logs
- Metrics → CPU, Memory, Request rate
- Events → Deployment history

### Self-Hosted
```bash
# Check systemd status
sudo systemctl status calcora-api

# View logs
sudo journalctl -u calcora-api -f

# Check nginx access
sudo tail -f /var/log/nginx/access.log

# Check nginx errors
sudo tail -f /var/log/nginx/error.log
```

---

## Troubleshooting

### Netlify Issues
**Problem**: Build fails with "Module not found"
- **Solution**: Check `netlify.toml` build command includes all dependencies

**Problem**: API calls fail with CORS errors
- **Solution**: Verify backend CORS allows your Netlify domain

### Render Issues
**Problem**: Service crashes on startup
- **Solution**: Check logs for import errors, ensure all dependencies in build command

**Problem**: Slow cold starts
- **Solution**: Free tier sleeps after 15 min inactivity, upgrade for always-on

### Build Issues
**Problem**: PyInstaller fails
- **Solution**: Ensure all dependencies installed in venv, try `--clean` flag

**Problem**: Executable too large
- **Solution**: Use UPX compression: `pip install pyinstaller[compression]`

---

## Security Considerations

### API Security
- Enable rate limiting for production
- Add API key authentication for sensitive deployments
- Use HTTPS only (Netlify/Render provide free SSL)

### Self-Hosted
- Keep dependencies updated: `pip install --upgrade -e .`
- Use firewall to restrict access
- Configure nginx security headers
- Regular security audits

---

## Cost Estimation

### Free Tier Limits
- **Netlify**: 100 GB bandwidth, 300 build minutes/month
- **Render**: 750 hours/month, sleeps after 15 min inactivity
- **Total**: $0/month for moderate usage

### Paid Plans
- **Netlify Pro**: $19/month - 400 GB bandwidth, faster builds
- **Render Starter**: $7/month - Always-on, no sleep
- **Self-hosted VPS**: $5-10/month - Full control, unlimited usage

---

## Best Practices

1. **Use environment variables** for configuration
2. **Enable monitoring** and alerting
3. **Set up backup** for self-hosted deployments
4. **Document custom configurations**
5. **Test deployments** before announcing
6. **Keep dependencies updated** for security
7. **Monitor resource usage** to prevent overages

---

## Support

- **GitHub Issues**: https://github.com/Dumbo-programmer/Calcora/issues
- **Documentation**: See `CLONE_AND_RUN.md` for development setup
- **Community**: Join discussions on GitHub

For academic institutions interested in self-hosting, see [ACADEMIC_STRATEGY.md](ACADEMIC_STRATEGY.md) for partnership opportunities.
