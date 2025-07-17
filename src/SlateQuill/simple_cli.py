"""
Simple CLI interface for SlateQuill.

This module provides a basic command-line interface for testing purposes.
"""

import asyncio
import sys
from pathlib import Path

from . import __version__
from .config import Config, load_config
from .core import convert_file, list_supported_formats
from .exceptions import SlateQuillError


def main():
    """Main CLI entry point."""
    if len(sys.argv) < 2:
        print(f"SlateQuill v{__version__}")
        print("Usage: SlateQuill <input_file> [output_file]")
        print("       SlateQuill --version")
        print("       SlateQuill --help")
        return
    
    if sys.argv[1] == "--version":
        print(f"SlateQuill version {__version__}")
        return
    
    if sys.argv[1] == "--help":
        print(f"SlateQuill v{__version__}")
        print("A robust Python CLI tool for converting HTML documents to clean, standards-compliant Markdown")
        print()
        print("Usage:")
        print("  SlateQuill <input_file> [output_file]")
        print("  SlateQuill --version")
        print("  SlateQuill --help")
        print()
        print("Supported formats:")
        for fmt in list_supported_formats():
            print(f"  {fmt}")
        return
    
    input_file = Path(sys.argv[1])
    output_file = Path(sys.argv[2]) if len(sys.argv) > 2 else input_file.with_suffix('.md')
    
    try:
        config = load_config()
        result = asyncio.run(convert_file(input_file, output_file, config))
        print(f"✅ Successfully converted {input_file} to {output_file}")
        print(f"📊 Output length: {len(result)} characters")
    except SlateQuillError as e:
        print(f"❌ Error: {e.message}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
