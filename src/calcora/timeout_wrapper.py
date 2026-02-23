"""
Execution timeout wrapper for symbolic computation

Purpose: Prevent DoS attacks from computationally expensive expressions.
Provides platform-independent timeout mechanism.

This is critical for production use where:
- Students may paste extremely complex expressions
- Malicious actors may craft pathological inputs
- Recursive symbolic operations may hang indefinitely

Note: Uses signal on Unix, threading on Windows.
For production web servers, use Gunicorn/uWSGI timeout as primary defense.
"""

import threading
import signal
import sys
import platform
from typing import Callable, Any, Optional
from functools import wraps


class TimeoutError(Exception):
    """Raised when computation exceeds timeout"""
    pass


# Determine which timeout mechanism to use
IS_UNIX = platform.system() in ('Linux', 'Darwin')  # Linux or macOS
IS_WINDOWS = platform.system() == 'Windows'


def timeout(seconds: float = 3.0):
    """
    Decorator to add timeout to a function.
    
    Uses signal.alarm on Unix (accurate, low overhead)
    Uses threading.Timer on Windows (approximate, higher overhead)
    
    Args:
        seconds: Maximum execution time in seconds
    
    Example:
        >>> @timeout(2.0)
        ... def slow_operation(x):
        ...     return integrate(x)
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Extract timeout from kwargs if provided
            timeout_value = kwargs.pop('_timeout', seconds)
            
            if timeout_value <= 0:
                # No timeout enforcement
                return func(*args, **kwargs)
            
            if IS_UNIX:
                # Unix: Use signal.alarm (precise, lightweight)
                def _timeout_handler(signum, frame):
                    raise TimeoutError(f'Operation exceeded {timeout_value:.1f}s timeout')
                
                # Set signal handler
                old_handler = signal.signal(signal.SIGALRM, _timeout_handler)
                signal.alarm(int(timeout_value))  # alarm() only accepts integers
                
                try:
                    result = func(*args, **kwargs)
                finally:
                    # Cancel alarm and restore old handler
                    signal.alarm(0)
                    signal.signal(signal.SIGALRM, old_handler)
                
                return result
            
            else:
                # Windows: Use threading.Timer (less precise but portable)
                result = [None]
                exception = [None]
                
                def target():
                    try:
                        result[0] = func(*args, **kwargs)
                    except Exception as e:
                        exception[0] = e
                
                thread = threading.Thread(target=target, daemon=True)
                thread.start()
                thread.join(timeout=timeout_value)
                
                if thread.is_alive():
                    # Timeout occurred
                    # Note: We can't actually kill the thread, it will continue
                    # in background until completion. This is a Python limitation.
                    raise TimeoutError(f'Operation exceeded {timeout_value:.1f}s timeout')
                
                if exception[0]:
                    raise exception[0]
                
                return result[0]
        
        return wrapper
    return decorator


def enforce_timeout(func: Callable, args: tuple = (), kwargs: dict = None, 
                   timeout_seconds: float = 3.0) -> Any:
    """
    Run function with enforced timeout.
    
    This is a functional interface (not decorator) for timeout enforcement.
    
    Args:
        func: Function to execute
        args: Positional arguments
        kwargs: Keyword arguments
        timeout_seconds: Maximum execution time
    
    Returns:
        Function result
    
    Raises:
        TimeoutError: If execution exceeds timeout
    
    Example:
        >>> result = enforce_timeout(integrate, args=("x**2", "x"), timeout_seconds=2.0)
    """
    if kwargs is None:
        kwargs = {}
    
    # Apply timeout decorator and execute
    wrapped = timeout(timeout_seconds)(func)
    return wrapped(*args, **kwargs)


def validate_timeout_value(timeout_val: Optional[float], min_val: float = 0.1, 
                           max_val: float = 30.0) -> float:
    """
    Validate and normalize timeout value.
    
    Args:
        timeout_val: User-provided timeout (None means use default)
        min_val: Minimum allowed timeout (default: 0.1s)
        max_val: Maximum allowed timeout (default: 30s)
    
    Returns:
        Validated timeout value
    
    Raises:
        ValueError: If timeout is invalid
    """
    # Default timeout if not provided
    if timeout_val is None:
        return 3.0
    
    try:
        timeout_float = float(timeout_val)
    except (TypeError, ValueError):
        raise ValueError(f"Timeout must be a number, got: {type(timeout_val).__name__}")
    
    if timeout_float <= 0:
        # Zero or negative means no timeout
        return 0
    
    if timeout_float < min_val:
        raise ValueError(f"Timeout too small (min: {min_val}s, got: {timeout_float}s)")
    
    if timeout_float > max_val:
        raise ValueError(f"Timeout too large (max: {max_val}s, got: {timeout_float}s)")
    
    return timeout_float
