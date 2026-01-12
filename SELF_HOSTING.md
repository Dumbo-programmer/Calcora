# Self-Hosting Calcora

This guide covers all methods to run Calcora on your own infrastructure.

## Table of Contents

1. [Local Development](#local-development)
2. [Self-Hosted Web Server](#self-hosted-web-server)
3. [Network Access](#network-access-lan)
4. [Cloud Deployment](#cloud-deployment)
5. [Troubleshooting](#troubleshooting)

---

## Local Development

### Prerequisites

- **Python**: 3.11, 3.12, or 3.13
- **Git**: For cloning the repository
- **Operating System**: Windows, macOS, or Linux

### Step-by-Step Setup

```bash
# 1. Clone repository
git clone https://github.com/YOUR-USERNAME/calcora.git
cd calcora

# 2. Create virtual environment
python -m venv .venv

# 3. Activate virtual environment
# Windows PowerShell:
.\.venv\Scripts\Activate.ps1
# Windows CMD:
.venv\Scripts\activate.bat
# macOS/Linux:
source .venv/bin/activate

# 4. Install Calcora
pip install --upgrade pip
pip install -e ".[engine-sympy,cli,api]"

# 5. Verify installation
calcora --help
```

### Running the CLI

```bash
# Differentiation
calcora differentiate "sin(x**2)" --verbosity detailed

# Matrix operations
calcora matrix-determinant "[[1,2],[3,4]]"
calcora matrix-inverse "[[1,2],[3,4]]"
calcora matrix-multiply "[[1,2],[3,4]]" "[[5,6],[7,8]]"
calcora matrix-eigenvalues "[[3,1],[1,3]]"

# Symbolic matrices
calcora matrix-determinant '[["a","b"],["c","d"]]'
```

---

## Self-Hosted Web Server

### Development Mode (Auto-Reload)

Best for development - automatically reloads on code changes:

```bash
uvicorn calcora.api.main:app --reload --host 127.0.0.1 --port 8000
```

Access at: http://127.0.0.1:8000/static/index.html

### Production Mode (Single Worker)

```bash
uvicorn calcora.api.main:app --host 0.0.0.0 --port 8000
```

### Production Mode (Multiple Workers)

For better performance under load:

```bash
uvicorn calcora.api.main:app --host 0.0.0.0 --port 8000 --workers 4
```

**Note**: Use `--workers` based on your CPU cores. Generally: `workers = (2 * cpu_cores) + 1`

### Running as Background Service

#### Using nohup (Linux/macOS)

```bash
nohup uvicorn calcora.api.main:app --host 0.0.0.0 --port 8000 --workers 4 > calcora.log 2>&1 &
```

Check status:
```bash
ps aux | grep uvicorn
tail -f calcora.log
```

Stop:
```bash
kill $(ps aux | grep 'uvicorn calcora' | awk '{print $2}')
```

#### Using systemd (Linux)

Create `/etc/systemd/system/calcora.service`:

```ini
[Unit]
Description=Calcora Mathematics Engine
After=network.target

[Service]
Type=simple
User=YOUR_USER
WorkingDirectory=/path/to/calcora
Environment="PATH=/path/to/calcora/.venv/bin"
ExecStart=/path/to/calcora/.venv/bin/uvicorn calcora.api.main:app --host 0.0.0.0 --port 8000 --workers 4
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable calcora
sudo systemctl start calcora
sudo systemctl status calcora
```

View logs:
```bash
sudo journalctl -u calcora -f
```

#### Using PM2 (Node.js process manager)

```bash
# Install PM2
npm install -g pm2

# Start Calcora
pm2 start "uvicorn calcora.api.main:app --host 0.0.0.0 --port 8000 --workers 4" --name calcora

# View status
pm2 status

# View logs
pm2 logs calcora

# Restart
pm2 restart calcora

# Stop
pm2 stop calcora

# Auto-start on boot
pm2 startup
pm2 save
```

---

## Network Access (LAN)

### Allow Local Network Access

```bash
# Bind to all interfaces
uvicorn calcora.api.main:app --host 0.0.0.0 --port 8000
```

Access from other devices on your network:
```
http://YOUR-COMPUTER-IP:8000/static/index.html
```

Find your IP:
```bash
# Windows
ipconfig

# macOS/Linux
ip addr show  # or: ifconfig
```

### Firewall Configuration

#### Windows Firewall

```powershell
# Allow inbound on port 8000
New-NetFirewallRule -DisplayName "Calcora Web Server" -Direction Inbound -LocalPort 8000 -Protocol TCP -Action Allow
```

#### Linux (ufw)

```bash
sudo ufw allow 8000/tcp
sudo ufw reload
```

#### Linux (firewalld)

```bash
sudo firewall-cmd --permanent --add-port=8000/tcp
sudo firewall-cmd --reload
```

---

## Cloud Deployment

### Netlify (Serverless - Free Tier)

See [DEPLOYMENT.md](DEPLOYMENT.md) for full Netlify deployment guide.

Quick deploy:
1. Push repository to GitHub
2. Connect to Netlify
3. Auto-deploys from `netlify.toml`

**Best for**: Demo sites, portfolio projects, low-traffic applications

### VPS (DigitalOcean, Linode, etc.)

#### 1. Provision Server

- Ubuntu 22.04 LTS recommended
- Minimum: 1GB RAM, 1 CPU core
- Recommended: 2GB RAM, 2 CPU cores

#### 2. Initial Server Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python 3.11
sudo apt install python3.11 python3.11-venv python3-pip git -y

# Create application user
sudo useradd -m -s /bin/bash calcora
sudo su - calcora
```

#### 3. Deploy Application

```bash
# Clone repository
git clone https://github.com/YOUR-USERNAME/calcora.git
cd calcora

# Setup virtual environment
python3.11 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -e ".[engine-sympy,cli,api]"
pip install gunicorn  # Production WSGI server

# Test
uvicorn calcora.api.main:app --host 0.0.0.0 --port 8000
```

#### 4. Setup Reverse Proxy (Nginx)

```bash
# Exit calcora user
exit

# Install Nginx
sudo apt install nginx -y

# Create Nginx configuration
sudo nano /etc/nginx/sites-available/calcora
```

Add this configuration:

```nginx
server {
    listen 80;
    server_name your-domain.com;  # Or server IP

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /home/calcora/calcora/src/calcora/web;
        expires 30d;
    }
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/calcora /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### 5. Setup SSL (Let's Encrypt)

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d your-domain.com
```

#### 6. Setup Systemd Service

Follow [systemd instructions above](#using-systemd-linux)

### Docker (Coming Soon)

Docker support is planned for v0.2. Expected format:

```bash
docker compose up -d
```

---

## Troubleshooting

### Port Already in Use

```bash
# Find process using port 8000
# Linux/macOS:
lsof -i :8000
# Windows:
netstat -ano | findstr :8000

# Kill process
# Linux/macOS:
kill -9 <PID>
# Windows:
taskkill /PID <PID> /F

# Or use different port
uvicorn calcora.api.main:app --port 8080
```

### Module Not Found Errors

```bash
# Ensure you're in virtual environment
which python  # Should show .venv path

# Reinstall
pip install --upgrade pip
pip install -e ".[engine-sympy,cli,api]"
```

### Permission Denied (Linux)

```bash
# Don't run as root - use application user
sudo useradd -m calcora
sudo chown -R calcora:calcora /path/to/calcora
sudo su - calcora
```

### High Memory Usage

Matrix operations and symbolic computation can be memory-intensive:

- **Limit workers**: Use fewer uvicorn workers
- **Increase RAM**: Upgrade server to 2GB+ RAM
- **Add swap**: Create swap file on Linux

```bash
# Create 2GB swap
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

### CORS Errors (Web UI)

If accessing from different domain:

```python
# In src/calcora/api/main.py
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specific domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Static Files Not Loading

Ensure correct path in browser:
- ✅ `http://localhost:8000/static/index.html`
- ❌ `http://localhost:8000/index.html`

### Performance Tuning

**For high traffic**:
```bash
# More workers
uvicorn calcora.api.main:app --workers 8

# Or use Gunicorn with uvicorn workers
gunicorn calcora.api.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

**Resource limits**:
```bash
# Limit per-process memory (Linux)
ulimit -v 1048576  # 1GB per process
```

---

## Security Best Practices

1. **Don't expose to internet directly** - Use reverse proxy (Nginx/Apache)
2. **Enable HTTPS** - Use Let's Encrypt for free SSL
3. **Firewall** - Only allow necessary ports
4. **Rate limiting** - Implement at reverse proxy level
5. **Updates** - Keep Python and dependencies updated
6. **User isolation** - Run as dedicated non-root user
7. **Authentication** - Add auth layer if exposing publicly (not built-in)

---

## Monitoring

### Basic Health Check

```bash
curl http://localhost:8000/static/index.html
```

### Logs

```bash
# With PM2
pm2 logs calcora

# With systemd
journalctl -u calcora -f

# Direct uvicorn
uvicorn calcora.api.main:app --log-level info
```

### Uptime Monitoring

Use services like:
- UptimeRobot (free)
- Pingdom
- StatusCake

---

## Updating Deployment

```bash
# Navigate to repository
cd /path/to/calcora

# Pull latest changes
git pull origin main

# Activate virtual environment
source .venv/bin/activate

# Update dependencies
pip install --upgrade pip
pip install -e ".[engine-sympy,cli,api]"

# Restart service
# PM2:
pm2 restart calcora

# Systemd:
sudo systemctl restart calcora

# Direct:
# Kill old process and start new one
```

---

## Need Help?

- **Documentation**: Check [README.md](README.md), [ARCHITECTURE.md](ARCHITECTURE.md)
- **Issues**: Open GitHub issue
- **Community**: Check discussions on GitHub

---

## Summary of Commands

**Quick local setup**:
```bash
git clone <repo> && cd calcora
python -m venv .venv && source .venv/bin/activate
pip install -e ".[engine-sympy,cli,api]"
uvicorn calcora.api.main:app --reload
```

**Production server**:
```bash
uvicorn calcora.api.main:app --host 0.0.0.0 --port 8000 --workers 4
```

**Background service** (PM2):
```bash
pm2 start "uvicorn calcora.api.main:app --host 0.0.0.0 --port 8000 --workers 4" --name calcora
```

That's it! You now have multiple options for self-hosting Calcora based on your needs.
