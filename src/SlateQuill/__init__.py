"""
SlateQuill - A robust Python CLI tool for converting HTML documents to clean, standards-compliant Markdown.

This package provides:
- HTML to Markdown conversion with support for complex structures
- Extensible plugin system for additional formats
- Security-first approach with input validation
- High-performance async processing
- Beautiful CLI interface with progress reporting
"""

__version__ = "0.1.0"
__author__ = "Niklas Skulll"
__license__ = "MIT"

# Public API exports - using try/except to handle missing dependencies during development
try:
    from .core import convert_file
    from .config import Config, ConversionConfig
    from .exceptions import SlateQuillError, ConversionError, SecurityError
    
    __all__ = [
        "convert_file",
        "Config", 
        "ConversionConfig",
        "SlateQuillError",
        "ConversionError", 
        "SecurityError",
    ]
except ImportError:
    # During development, dependencies might not be installed yet
    __all__ = []
