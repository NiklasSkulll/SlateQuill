"""
SlateQuill HTML to Markdown converter.

This module provides the core HTML to Markdown conversion functionality
with support for various HTML elements and structures.
"""

import asyncio
from typing import Any, Dict, Optional

from bs4 import BeautifulSoup
from markdownify import markdownify as md

from .config import ConversionConfig
from .exceptions import ConversionError
from .security import validate_input, SecurityConfig


async def html_to_markdown(
    html_content: str,
    config: Optional[ConversionConfig] = None,
    options: Optional[Dict[str, Any]] = None
) -> str:
    """
    Convert HTML content to Markdown.
    
    Args:
        html_content: HTML content to convert
        config: Conversion configuration
        options: Additional conversion options
    
    Returns:
        Markdown string
    
    Raises:
        ConversionError: If conversion fails
    """
    if config is None:
        config = ConversionConfig()
    
    if options is None:
        options = {}
    
    try:
        # Parse HTML with BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Remove script and style tags if not preserving HTML
        if not config.preserve_html:
            for tag in soup(['script', 'style']):
                tag.decompose()
        
        # Remove comments if configured
        if config.strip_comments:
            for comment in soup.find_all(string=lambda text: isinstance(text, type(soup.find_all(string=True)[0])) and text.strip().startswith('<!--')):
                comment.extract()
        
        # Convert to markdown
        markdown_content = md(
            str(soup),
            heading_style=config.heading_style,
            bullets='-' if config.emphasis_style == 'asterisk' else '*',
            strip=['script', 'style'] if not config.preserve_html else [],
            convert=['p', 'br', 'strong', 'em', 'u', 'i', 'b', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
                    'ul', 'ol', 'li', 'blockquote', 'pre', 'code', 'a', 'img', 'table', 'thead',
                    'tbody', 'tr', 'th', 'td', 'div', 'span', 'hr']
        )
        
        # Clean whitespace if configured
        if config.clean_whitespace:
            markdown_content = _clean_whitespace(markdown_content)
        
        # Apply line length limit if configured
        if config.line_length > 0:
            markdown_content = _wrap_lines(markdown_content, config.line_length)
        
        return markdown_content
        
    except Exception as e:
        raise ConversionError(f"Failed to convert HTML to Markdown: {e}")


def _clean_whitespace(content: str) -> str:
    """Clean extra whitespace from markdown content."""
    import re
    
    # Remove excessive blank lines (more than 2 consecutive)
    content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
    
    # Remove trailing whitespace from lines
    content = re.sub(r'[ \t]+$', '', content, flags=re.MULTILINE)
    
    # Remove leading/trailing whitespace from entire content
    content = content.strip()
    
    return content


def _wrap_lines(content: str, max_length: int) -> str:
    """Wrap lines to specified maximum length."""
    import textwrap
    
    lines = content.split('\n')
    wrapped_lines = []
    
    for line in lines:
        # Don't wrap code blocks or headings
        if line.startswith(('```', '    ', '#')):
            wrapped_lines.append(line)
        elif len(line) <= max_length:
            wrapped_lines.append(line)
        else:
            # Wrap long lines
            wrapped = textwrap.fill(line, width=max_length, break_long_words=False)
            wrapped_lines.append(wrapped)
    
    return '\n'.join(wrapped_lines)


async def convert_html_file(
    file_path: str,
    output_path: Optional[str] = None,
    config: Optional[ConversionConfig] = None,
    security_config: Optional[SecurityConfig] = None
) -> str:
    """
    Convert HTML file to Markdown.
    
    Args:
        file_path: Path to HTML file
        output_path: Optional output path for Markdown file
        config: Conversion configuration
        security_config: Security configuration
    
    Returns:
        Markdown content
    """
    from pathlib import Path
    
    input_path = Path(file_path)
    
    if not input_path.exists():
        raise ConversionError(f"Input file not found: {file_path}")
    
    if security_config is None:
        security_config = SecurityConfig()
    
    # Read and validate input
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
    except Exception as e:
        raise ConversionError(f"Failed to read input file: {e}")
    
    # Validate input for security
    validated_content = validate_input(html_content, input_path, security_config)
    
    # Convert to markdown
    markdown_content = await html_to_markdown(validated_content, config)
    
    # Write output if path specified
    if output_path:
        output_file = Path(output_path)
        try:
            output_file.parent.mkdir(parents=True, exist_ok=True)
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
        except Exception as e:
            raise ConversionError(f"Failed to write output file: {e}")
    
    return markdown_content
