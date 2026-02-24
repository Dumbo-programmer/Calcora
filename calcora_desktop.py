#!/usr/bin/env python3
"""
Calcora Desktop Launcher - v0.3

Unified desktop application that:
1. Starts Flask API server on localhost:8000
2. Auto-opens browser to web UI
3. Runs completely offline
4. No external dependencies needed from user

Security:
- Binds ONLY to 127.0.0.1 (localhost) - not exposed to internet
- Checks port availability before starting
- Clean shutdown on Ctrl+C
"""
import sys
import os
import webbrowser
import threading
import time
import socket
from pathlib import Path

# Add src to path for imports
if getattr(sys, 'frozen', False):
    # Running as PyInstaller bundle
    BASE_DIR = Path(sys._MEIPASS)
else:
    # Running as script
    BASE_DIR = Path(__file__).parent
    sys.path.insert(0, str(BASE_DIR / 'src'))

def check_port_available(port: int = 8000) -> bool:
    """Check if port is available for binding."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('127.0.0.1', port))
            return True
    except OSError:
        return False

def find_available_port(start_port: int = 8000, max_attempts: int = 10) -> int:
    """Find an available port starting from start_port."""
    for port in range(start_port, start_port + max_attempts):
        if check_port_available(port):
            return port
    raise RuntimeError(f"Could not find available port in range {start_port}-{start_port + max_attempts}")

def open_browser(port: int, delay: float = 1.5):
    """Open browser after short delay to ensure server is ready."""
    time.sleep(delay)
    url = f"http://127.0.0.1:{port}"
    print(f"Opening browser to {url}...")
    webbrowser.open(url)

def main():
    """Main entry point for Calcora Desktop."""
    print("=" * 60)
    print("  Calcora Desktop - Computational Mathematics Engine")
    print("  Version 0.3.0")
    print("=" * 60)
    print()
    
    # Find available port
    try:
        port = find_available_port()
        print(f"✓ Using port {port}")
    except RuntimeError as e:
        print(f"✗ Error: {e}")
        print("  Close other applications and try again.")
        input("Press Enter to exit...")
        return 1
    
    # Start browser opener in background thread
    browser_thread = threading.Thread(target=open_browser, args=(port,), daemon=True)
    browser_thread.start()
    
    print()
    print("Starting Calcora server...")
    print(f"Server running at: http://127.0.0.1:{port}")
    print()
    print("=" * 60)
    print("  Tips:")
    print("  - Your browser will open automatically")
    print("  - All computation runs locally (offline)")
    print("  - Press Ctrl+C to stop the server")
    print("=" * 60)
    print()
    
    # Import Flask app (do this after port check to fail fast)
    try:
        from flask import Flask
        from flask_cors import CORS
        from api_server import app
    except ImportError as e:
        print(f"✗ Error importing server components: {e}")
        print("  The application may be corrupted. Please re-download.")
        input("Press Enter to exit...")
        return 1
    
    # Override Flask settings for desktop mode
    app.config.update(
        DEBUG=False,
        TESTING=False,
        ENV='production',
    )
    
    # Disable Flask startup banner in production
    import logging
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.WARNING)
    
    try:
        # Start Flask server
        # CRITICAL: bind to 127.0.0.1 ONLY (not 0.0.0.0)
        app.run(
            host='127.0.0.1',
            port=port,
            debug=False,
            use_reloader=False,
            threaded=True,
        )
    except KeyboardInterrupt:
        print("\n\nShutting down Calcora...")
        print("Goodbye!")
        return 0
    except Exception as e:
        print(f"\n✗ Server error: {e}")
        input("Press Enter to exit...")
        return 1

if __name__ == "__main__":
    sys.exit(main())
