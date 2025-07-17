"""
SlateQuill plugin system.

This module provides the base classes and utilities for the SlateQuill plugin system,
allowing extensible support for different input formats.
"""

try:
    from .base import BaseConverter
    __all__ = ["BaseConverter"]
except ImportError:
    # During development, dependencies might not be installed yet
    __all__ = []
