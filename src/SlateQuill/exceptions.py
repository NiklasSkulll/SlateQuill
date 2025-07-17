"""
SlateQuill exception hierarchy.

This module defines the exception classes used throughout the SlateQuill package
for robust error handling and debugging.
"""

from typing import Any, Optional


class SlateQuillError(Exception):
    """Base exception for SlateQuill."""
    
    def __init__(self, message: str, details: Optional[dict[str, Any]] = None) -> None:
        super().__init__(message)
        self.message = message
        self.details = details or {}


class ConversionError(SlateQuillError):
    """Raised when conversion fails."""
    pass


class InvalidInputError(ConversionError):
    """Raised when input is malformed or invalid."""
    pass


class SecurityError(SlateQuillError):
    """Raised when security validation fails."""
    pass


class PluginError(SlateQuillError):
    """Raised when plugin operations fail."""
    pass


class ConfigurationError(SlateQuillError):
    """Raised when configuration is invalid."""
    pass


class FileProcessingError(SlateQuillError):
    """Raised when file processing fails."""
    pass
