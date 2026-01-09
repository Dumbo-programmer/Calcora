"""Entry point script for running the Calcora API server as a standalone executable."""
import sys
import time
import webbrowser
import threading
import uvicorn
from calcora.api.main import app

def open_browser(url, delay=1.5):
    """Open browser after a delay to ensure server is ready."""
    time.sleep(delay)
    webbrowser.open(url)

if __name__ == "__main__":
    # Default arguments for the server
    host = "127.0.0.1"
    port = 8000
    open_browser_flag = True  # Auto-open by default
    
    # Parse simple command line arguments
    i = 0
    while i < len(sys.argv[1:]):
        arg = sys.argv[i + 1]
        if arg == "--host" and i + 1 < len(sys.argv[1:]):
            host = sys.argv[i + 2]
            i += 2
        elif arg == "--port" and i + 1 < len(sys.argv[1:]):
            try:
                port = int(sys.argv[i + 2])
                i += 2
            except (ValueError, IndexError):
                print(f"Invalid port: {sys.argv[i + 2] if i + 2 < len(sys.argv) else 'missing'}")
                sys.exit(1)
        elif arg == "--no-browser":
            open_browser_flag = False
            i += 1
        elif arg in ("-h", "--help"):
            print("Calcora API Server")
            print("Usage: calcora-server [OPTIONS]")
            print()
            print("Options:")
            print("  --host HOST       Host to bind to (default: 127.0.0.1)")
            print("  --port PORT       Port to bind to (default: 8000)")
            print("  --no-browser      Don't open browser automatically")
            print("  -h, --help        Show this help message")
            sys.exit(0)
        else:
            i += 1
    
    url = f"http://{host}:{port}/static/index.html"
    
    print("=" * 60)
    print("Calcora - Computational Mathematics Engine")
    print("=" * 60)
    print(f"Server starting at http://{host}:{port}")
    print(f"Web UI: {url}")
    print()
    
    if open_browser_flag:
        print("Opening browser...")
        # Open browser in background thread after delay
        browser_thread = threading.Thread(target=open_browser, args=(url,), daemon=True)
        browser_thread.start()
    else:
        print("Tip: Open your browser and navigate to the URL above")
    
    print()
    print("Press CTRL+C to stop the server")
    print("=" * 60)
    print()
    
    try:
        uvicorn.run(
            app,
            host=host,
            port=port,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\nServer stopped.")
