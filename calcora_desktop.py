#!/usr/bin/env python3
"""
Calcora Desktop Launcher - v0.3

Unified desktop application that:
1. Starts Flask API server on localhost (OS-assigned port)
2. Auto-opens browser to web UI
3. Runs completely offline
4. No external dependencies needed from user

Security:
- Binds ONLY to 127.0.0.1 (localhost) - not exposed to internet
- Uses OS-assigned ephemeral port (more secure than port scanning)
- Clean shutdown on Ctrl+C
- Top-level exception handling prevents raw tracebacks
"""
import sys
import os
import webbrowser
import threading
import time
import socket
import traceback
from pathlib import Path
from datetime import datetime

# Version constant (keep in sync with pyproject.toml)
VERSION = "0.3.0"

# Add src to path for imports
if getattr(sys, 'frozen', False):
    # Running as PyInstaller bundle
    BASE_DIR = Path(sys._MEIPASS)
else:
    # Running as script
    BASE_DIR = Path(__file__).parent
    sys.path.insert(0, str(BASE_DIR / 'src'))

def get_available_port() -> int:
    """
    Get an available port using OS-assigned ephemeral port.
    
    This is cleaner than scanning a range - the OS knows what's available.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('127.0.0.1', 0))  # 0 = OS assigns available port
        s.listen(1)
        port = s.getsockname()[1]
    return port

def show_error_dialog(title: str, message: str, details: str = None):
    """
    Show a GUI error dialog. Falls back to console if GUI unavailable.
    
    This prevents raw tracebacks from appearing in desktop mode.
    """
    try:
        import tkinter as tk
        from tkinter import messagebox
        
        # Create hidden root window
        root = tk.Tk()
        root.withdraw()
        
        # Show error dialog
        error_msg = message
        if details:
            error_msg += f"\n\nDetails:\n{details}"
        
        messagebox.showerror(title, error_msg)
        root.destroy()
    except Exception:
        # Fallback to console if tkinter unavailable (should never happen on Windows/Mac)
        print(f"\n{'=' * 60}")
        print(f"ERROR: {title}")
        print(f"{'=' * 60}")
        print(message)
        if details:
            print(f"\nDetails:\n{details}")
        print(f"{'=' * 60}\n")
        input("Press Enter to exit...")

def log_error(error: Exception, context: str = ""):
    """Log error to file for debugging (hidden from user)."""
    log_file = Path.home() / ".calcora" / "error.log"
    log_file.parent.mkdir(exist_ok=True)
    
    try:
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(f"\n{'=' * 80}\n")
            f.write(f"Timestamp: {datetime.now().isoformat()}\n")
            f.write(f"Version: {VERSION}\n")
            f.write(f"Context: {context}\n")
            f.write(f"Error: {type(error).__name__}: {error}\n")
            f.write(f"{'=' * 80}\n")
            f.write(traceback.format_exc())
            f.write(f"{'=' * 80}\n\n")
    except Exception:
        # If logging fails, continue silently (don't crash on logging failure)
        pass

def open_browser(port: int, delay: float = 1.5):
    """
    Open browser after short delay to ensure server is ready.
    
    Includes health check and fallback strategies for maximum reliability.
    """
    time.sleep(delay)
    
    # Health check: Verify server is responding before opening browser
    url = f"http://127.0.0.1:{port}/"
    max_retries = 5
    for i in range(max_retries):
        try:
            import urllib.request
            urllib.request.urlopen(url, timeout=1)
            break  # Server is ready
        except:
            if i < max_retries - 1:
                time.sleep(0.5)  # Wait and retry
            else:
                # Server didn't respond, but still try to open browser
                # (server might start just after this check)
                pass
    
    # Try to open browser with fallback strategies
    try:
        # Strategy 1: Default browser
        if webbrowser.open(url):
            return  # Success
        
        # Strategy 2: Explicitly try common browsers (in order of preference)
        browsers = [
            'windows-default',  # Windows default
            'chrome',
            'firefox',
            'edge',
            'safari',
        ]
        
        for browser_name in browsers:
            try:
                browser = webbrowser.get(browser_name)
                if browser.open(url):
                    return  # Success
            except:
                continue  # Try next browser
        
        # If we get here, we couldn't open any browser
        # Print URL for manual access
        print(f"\n⚠ Could not automatically open browser.")
        print(f"  Please manually open: {url}")
        print()
        
    except Exception as e:
        print(f"\n⚠ Browser launch failed: {e}")
        print(f"  Please manually open: {url}")
        print()

def main():
    """Main entry point for Calcora Desktop."""
    # Try to use colorama for colored output (fallback gracefully if not available)
    try:
        from colorama import init, Fore, Style
        init(autoreset=True)
        use_colors = True
    except ImportError:
        # Fallback: no colors
        class Fore:
            GREEN = YELLOW = CYAN = RED = RESET = ''
        class Style:
            BRIGHT = RESET_ALL = ''
        use_colors = False
    
    # Header
    print()
    print(f"{Fore.CYAN}{'=' * 70}")
    print(f"{Fore.CYAN}{Style.BRIGHT}  🧮 Calcora Desktop v{VERSION}")
    print(f"{Fore.CYAN}  Computational Mathematics Engine — Privacy-First, Offline")
    print(f"{Fore.CYAN}{'=' * 70}")
    print()
    
    # Get available port from OS (cleaner than scanning)
    try:
        port = get_available_port()
        print(f"{Fore.GREEN}✓ Network port assigned: {Style.BRIGHT}{port}{Style.RESET_ALL} (OS-managed)")
    except Exception as e:
        log_error(e, "Port assignment failed")
        show_error_dialog(
            "Calcora Startup Error",
            "Could not assign network port.\n\nThis usually means your system is low on resources.",
            str(e)
        )
        return 1
    
    # Import Flask app (do this after port check to fail fast)
    try:
        from flask import Flask
        from flask_cors import CORS
        from api_server import app
        print(f"{Fore.GREEN}✓ Mathematical engine loaded")
    except ImportError as e:
        log_error(e, "Failed to import server components")
        show_error_dialog(
            "Calcora Installation Error",
            "Missing required components.\n\nThe application may be corrupted.\nPlease re-download from GitHub.",
            f"Missing module: {e.name if hasattr(e, 'name') else str(e)}"
        )
        return 1
    
    # Start browser opener in background thread
    browser_thread = threading.Thread(target=open_browser, args=(port,), daemon=True)
    browser_thread.start()
    print(f"{Fore.GREEN}✓ Browser will open automatically in 1-2 seconds...")
    
    print()
    print(f"{Fore.YELLOW}{'─' * 70}")
    print(f"{Fore.YELLOW}{Style.BRIGHT}  Server Status:")
    print(f"{Fore.YELLOW}  • Running at: {Fore.CYAN}{Style.BRIGHT}http://127.0.0.1:{port}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}  • Mode: {Fore.GREEN}Private{Style.RESET_ALL} (localhost only, not exposed to internet)")
    print(f"{Fore.YELLOW}  • Computation: {Fore.GREEN}100% Offline{Style.RESET_ALL} (no data sent externally)")
    print(f"{Fore.YELLOW}{'─' * 70}")
    print()
    print(f"{Fore.CYAN}  How to use:")
    print(f"  • The calculator will open in your browser automatically")
    print(f"  • Click {Style.BRIGHT}'Quit Calcora'{Style.RESET_ALL} button in the footer to shut down")
    print(f"  • Or press {Style.BRIGHT}Ctrl+C{Style.RESET_ALL} in this window to stop the server")
    print()
    print(f"{Fore.CYAN}{'=' * 70}")
    print(f"{Fore.GREEN}{Style.BRIGHT}  ✓ Calcora is now running — enjoy mathematical computation!")
    print(f"{Fore.CYAN}{'=' * 70}")
    print()

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
        # Graceful shutdown on Ctrl+C
        try:
            from colorama import Fore, Style
        except:
            class Fore:
                YELLOW = CYAN = ''
            class Style:
                BRIGHT = RESET_ALL = ''
        
        print(f"\n\n{Fore.YELLOW}{'─' * 70}")
        print(f"{Fore.YELLOW}  Shutting down Calcora...")
        print(f"{Fore.CYAN}{'─' * 70}")
        print(f"{Fore.CYAN}  Thank you for using Calcora!")
        print(f"{Fore.CYAN}  https://github.com/Dumbo-programmer/Calcora")
        print(f"{Fore.CYAN}{'─' * 70}\n")
        return 0
    except Exception as e:
        log_error(e, "Server runtime error")
        show_error_dialog(
            "Calcora Server Error",
            "The server encountered an unexpected error.\n\nPlease check the error log for details.",
            f"Error: {type(e).__name__}: {e}\n\nLog file: {Path.home() / '.calcora' / 'error.log'}"
        )
        return 1

def run_with_error_boundary():
    """
    Top-level error boundary - catches ALL unhandled exceptions.
    
    This prevents raw Python tracebacks from appearing to desktop users.
    """
    try:
        sys.exit(main())
    except Exception as e:
        # CRITICAL: This should NEVER be reached in normal operation
        # If we get here, something catastrophic happened
        log_error(e, "CRITICAL: Unhandled top-level exception")
        show_error_dialog(
            "Calcora Critical Error",
            "A critical error occurred during startup.\n\nPlease report this issue on GitHub with the error log.",
            f"Error: {type(e).__name__}: {e}\n\nLog: {Path.home() / '.calcora' / 'error.log'}"
        )
        sys.exit(1)

if __name__ == "__main__":
    run_with_error_boundary()
