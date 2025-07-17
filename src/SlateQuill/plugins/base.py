"""
SlateQuill plugin system base classes.

This module provides the abstract base class for all SlateQuill plugins,
defining the interface for extensible format converters.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, Optional


class BaseConverter(ABC):
    """Abstract base class for all converters."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """Initialize the converter with optional configuration."""
        self.config = config or {}
    
    @abstractmethod
    def can_handle(self, file_path: Path) -> bool:
        """Check if this converter can handle the given file."""
        pass
    
    @abstractmethod
    async def convert(self, content: bytes, options: Optional[Dict[str, Any]] = None) -> str:
        """Convert content to Markdown."""
        pass
    
    @abstractmethod
    def validate_input(self, content: bytes) -> bool:
        """Validate input for security and format correctness."""
        pass
    
    @property
    @abstractmethod
    def supported_formats(self) -> list[str]:
        """List of supported file formats (extensions)."""
        pass
    
    @property
    def name(self) -> str:
        """Name of the converter."""
        return self.__class__.__name__
    
    @property
    def description(self) -> str:
        """Description of the converter."""
        return self.__doc__ or f"{self.name} converter"


class HTMLConverter(BaseConverter):
    """HTML to Markdown converter."""
    
    def can_handle(self, file_path: Path) -> bool:
        """Check if this converter can handle HTML files."""
        return file_path.suffix.lower() in self.supported_formats
    
    async def convert(self, content: bytes, options: Optional[Dict[str, Any]] = None) -> str:
        """Convert HTML content to Markdown."""
        # This will be implemented in html2md.py
        from ..html2md import html_to_markdown
        
        html_content = content.decode('utf-8')
        
        # Handle both config object and options dict
        if options is not None:
            if hasattr(options, 'preserve_html'):
                # It's a config object
                return await html_to_markdown(html_content, options)
            else:
                # It's a dict of options
                return await html_to_markdown(html_content, options=options)
        else:
            return await html_to_markdown(html_content)
    
    def validate_input(self, content: bytes) -> bool:
        """Validate HTML input."""
        try:
            content.decode('utf-8')
            return True
        except UnicodeDecodeError:
            return False
    
    @property
    def supported_formats(self) -> list[str]:
        """List of supported HTML formats."""
        return ['.html', '.htm', '.xhtml']
