"""
SlateQuill core conversion functionality.

This module provides the main conversion functions and workflow orchestration
for converting various file formats to Markdown.
"""

import asyncio
from pathlib import Path
from typing import Dict, Any, Optional, List

from .config import Config, ConversionConfig, SecurityConfig
from .exceptions import ConversionError, SecurityError
from .html2md import convert_html_file
from .plugins.base import BaseConverter, HTMLConverter
from .security import validate_input


# Registry of available converters
_converters: Dict[str, BaseConverter] = {}


def register_converter(converter: BaseConverter) -> None:
    """Register a converter for use in the conversion process."""
    for format_ext in converter.supported_formats:
        _converters[format_ext.lower()] = converter


def get_converter(file_path: Path) -> Optional[BaseConverter]:
    """Get the appropriate converter for a file based on its extension."""
    file_ext = file_path.suffix.lower()
    return _converters.get(file_ext)


def list_supported_formats() -> List[str]:
    """List all supported file formats."""
    return sorted(list(_converters.keys()))


async def convert_file(
    input_path: Path,
    output_path: Path,
    config: Optional[Config] = None
) -> str:
    """
    Convert a file to Markdown.
    
    Args:
        input_path: Path to input file
        output_path: Path to output Markdown file
        config: Conversion configuration
    
    Returns:
        Markdown content
    
    Raises:
        ConversionError: If conversion fails
        SecurityError: If security validation fails
    """
    if config is None:
        config = Config()
    
    # Validate input file exists
    if not input_path.exists():
        raise ConversionError(f"Input file not found: {input_path}")
    
    # Get appropriate converter
    converter = get_converter(input_path)
    if converter is None:
        raise ConversionError(f"No converter available for file type: {input_path.suffix}")
    
    # Read input file
    try:
        with open(input_path, 'rb') as f:
            content = f.read()
    except Exception as e:
        raise ConversionError(f"Failed to read input file: {e}")
    
    # Validate input
    if not converter.validate_input(content):
        raise SecurityError(f"Input validation failed for file: {input_path}")
    
    # Security validation
    content_str = validate_input(content, input_path, config.security)
    
    # Convert to markdown
    markdown_content = await converter.convert(content_str.encode('utf-8'), config.conversion.dict())
    
    # Create output directory if it doesn't exist
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Write output file
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
    except Exception as e:
        raise ConversionError(f"Failed to write output file: {e}")
    
    return markdown_content


async def convert_directory(
    input_dir: Path,
    output_dir: Path,
    config: Optional[Config] = None,
    recursive: bool = True
) -> List[tuple[Path, Path]]:
    """
    Convert all supported files in a directory to Markdown.
    
    Args:
        input_dir: Input directory path
        output_dir: Output directory path
        config: Conversion configuration
        recursive: Whether to process subdirectories
    
    Returns:
        List of (input_path, output_path) tuples for converted files
    """
    if config is None:
        config = Config()
    
    if not input_dir.exists() or not input_dir.is_dir():
        raise ConversionError(f"Input directory not found: {input_dir}")
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    converted_files = []
    supported_formats = set(list_supported_formats())
    
    # Find all supported files
    pattern = "**/*" if recursive else "*"
    for file_path in input_dir.glob(pattern):
        if file_path.is_file() and file_path.suffix.lower() in supported_formats:
            # Calculate relative path and output path
            rel_path = file_path.relative_to(input_dir)
            output_path = output_dir / rel_path.with_suffix('.md')
            
            try:
                await convert_file(file_path, output_path, config)
                converted_files.append((file_path, output_path))
            except Exception as e:
                print(f"Failed to convert {file_path}: {e}")
    
    return converted_files


async def batch_convert(
    input_files: List[Path],
    output_dir: Path,
    config: Optional[Config] = None,
    max_concurrent: int = 5
) -> List[tuple[Path, Path]]:
    """
    Convert multiple files to Markdown concurrently.
    
    Args:
        input_files: List of input file paths
        output_dir: Output directory path
        config: Conversion configuration
        max_concurrent: Maximum number of concurrent conversions
    
    Returns:
        List of (input_path, output_path) tuples for converted files
    """
    if config is None:
        config = Config()
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    semaphore = asyncio.Semaphore(max_concurrent)
    converted_files = []
    
    async def convert_single(input_path: Path) -> Optional[tuple[Path, Path]]:
        async with semaphore:
            try:
                output_path = output_dir / f"{input_path.stem}.md"
                await convert_file(input_path, output_path, config)
                return (input_path, output_path)
            except Exception as e:
                print(f"Failed to convert {input_path}: {e}")
                return None
    
    # Execute conversions concurrently
    tasks = [convert_single(path) for path in input_files]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Filter out None results and exceptions
    converted_files = [result for result in results if result is not None and not isinstance(result, Exception)]
    
    return converted_files


# Initialize default converters
def _initialize_converters() -> None:
    """Initialize the default converter registry."""
    # Register HTML converter
    html_converter = HTMLConverter()
    register_converter(html_converter)


# Initialize converters on module import
_initialize_converters()
