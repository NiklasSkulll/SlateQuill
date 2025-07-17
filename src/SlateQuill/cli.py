"""
SlateQuill CLI interface.

This module provides the command-line interface for SlateQuill using Typer,
offering a beautiful and user-friendly experience for converting files.
"""

import asyncio
from pathlib import Path
from typing import List, Optional

import typer
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

from . import __version__
from .config import Config, load_config
from .core import convert_file, convert_directory, batch_convert, list_supported_formats
from .exceptions import SlateQuillError

app = typer.Typer(
    name="SlateQuill",
    help="A robust Python CLI tool for converting HTML documents to clean, standards-compliant Markdown",
    add_completion=False
)

console = Console()


def version_callback(ctx: typer.Context, param: typer.CallbackParam, value: bool) -> None:
    """Show version information."""
    if not value or ctx.resilient_parsing:
        return
    console.print(f"SlateQuill version {__version__}")
    raise typer.Exit()


@app.callback()
def main(
    ctx: typer.Context,
    version: bool = typer.Option(
        False,
        "--version",
        "-v",
        callback=version_callback,
        is_eager=True,
        help="Show version and exit"
    )
) -> None:
    """SlateQuill - Convert HTML to Markdown with style."""
    pass


@app.command()
def convert(
    input_file: Path = typer.Argument(..., help="Input HTML file to convert"),
    output_file: Optional[Path] = typer.Option(
        None,
        "--output",
        "-o",
        help="Output Markdown file (default: input filename with .md extension)"
    ),
    config_file: Optional[Path] = typer.Option(
        None,
        "--config",
        "-c",
        help="Configuration file path"
    ),
    markdown_flavor: Optional[str] = typer.Option(
        None,
        "--flavor",
        "-f",
        help="Markdown flavor (github, commonmark, strict)"
    ),
    preserve_html: bool = typer.Option(
        False,
        "--preserve-html",
        help="Preserve HTML tags in output"
    ),
    line_length: Optional[int] = typer.Option(
        None,
        "--line-length",
        "-l",
        help="Maximum line length for output"
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Enable verbose output"
    )
) -> None:
    """Convert a single HTML file to Markdown."""
    
    # Load configuration
    config = load_config(config_file)
    
    # Override config with command line options
    if markdown_flavor:
        config.conversion.markdown_flavor = markdown_flavor
    if preserve_html:
        config.conversion.preserve_html = preserve_html
    if line_length:
        config.conversion.line_length = line_length
    
    # Set default output file
    if output_file is None:
        output_file = input_file.with_suffix('.md')
    
    # Convert file
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
            transient=True
        ) as progress:
            task = progress.add_task("Converting file...", total=None)
            
            result = asyncio.run(convert_file(input_file, output_file, config))
            
            progress.update(task, description="✅ Conversion completed!")
        
        console.print(f"✅ Successfully converted [bold]{input_file}[/bold] to [bold]{output_file}[/bold]")
        
        if verbose:
            console.print(f"📊 Output length: {len(result)} characters")
            
    except SlateQuillError as e:
        console.print(f"❌ Error: {e.message}", style="bold red")
        if verbose and e.details:
            console.print(f"Details: {e.details}")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"❌ Unexpected error: {e}", style="bold red")
        raise typer.Exit(1)


@app.command()
def batch_convert_cmd(
    input_files: List[Path] = typer.Argument(..., help="Input files to convert"),
    output_dir: Path = typer.Option(
        Path("./output"),
        "--output-dir",
        "-o",
        help="Output directory for converted files"
    ),
    config_file: Optional[Path] = typer.Option(
        None,
        "--config",
        "-c",
        help="Configuration file path"
    ),
    max_concurrent: int = typer.Option(
        5,
        "--max-concurrent",
        "-j",
        help="Maximum number of concurrent conversions"
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Enable verbose output"
    )
) -> None:
    """Convert multiple files to Markdown."""
    
    # Load configuration
    config = load_config(config_file)
    
    # Convert files
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task(f"Converting {len(input_files)} files...", total=len(input_files))
            
            results = asyncio.run(batch_convert(input_files, output_dir, config, max_concurrent))
            
            progress.update(task, completed=len(results), description="✅ Batch conversion completed!")
        
        # Display results
        if results:
            table = Table(title="Conversion Results")
            table.add_column("Input File", style="cyan")
            table.add_column("Output File", style="green")
            table.add_column("Status", style="bold")
            
            for input_path, output_path in results:
                table.add_row(str(input_path), str(output_path), "✅ Success")
            
            console.print(table)
            console.print(f"✅ Successfully converted {len(results)} out of {len(input_files)} files")
        else:
            console.print("⚠️  No files were converted", style="yellow")
            
    except SlateQuillError as e:
        console.print(f"❌ Error: {e.message}", style="bold red")
        if verbose and e.details:
            console.print(f"Details: {e.details}")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"❌ Unexpected error: {e}", style="bold red")
        raise typer.Exit(1)


@app.command()
def convert_dir(
    input_dir: Path = typer.Argument(..., help="Input directory to convert"),
    output_dir: Path = typer.Option(
        Path("./output"),
        "--output-dir",
        "-o",
        help="Output directory for converted files"
    ),
    config_file: Optional[Path] = typer.Option(
        None,
        "--config",
        "-c",
        help="Configuration file path"
    ),
    recursive: bool = typer.Option(
        True,
        "--recursive/--no-recursive",
        "-r",
        help="Process subdirectories recursively"
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Enable verbose output"
    )
) -> None:
    """Convert all supported files in a directory to Markdown."""
    
    # Load configuration
    config = load_config(config_file)
    
    # Convert directory
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Scanning directory...", total=None)
            
            results = asyncio.run(convert_directory(input_dir, output_dir, config, recursive))
            
            progress.update(task, description="✅ Directory conversion completed!")
        
        # Display results
        if results:
            table = Table(title="Directory Conversion Results")
            table.add_column("Input File", style="cyan")
            table.add_column("Output File", style="green")
            
            for input_path, output_path in results:
                table.add_row(str(input_path), str(output_path))
            
            console.print(table)
            console.print(f"✅ Successfully converted {len(results)} files")
        else:
            console.print("⚠️  No supported files found in directory", style="yellow")
            
    except SlateQuillError as e:
        console.print(f"❌ Error: {e.message}", style="bold red")
        if verbose and e.details:
            console.print(f"Details: {e.details}")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"❌ Unexpected error: {e}", style="bold red")
        raise typer.Exit(1)


@app.command()
def formats() -> None:
    """List all supported file formats."""
    
    supported = list_supported_formats()
    
    if supported:
        table = Table(title="Supported File Formats")
        table.add_column("Extension", style="cyan")
        table.add_column("Description", style="green")
        
        format_descriptions = {
            '.html': 'HTML files',
            '.htm': 'HTML files',
            '.xhtml': 'XHTML files',
        }
        
        for fmt in supported:
            description = format_descriptions.get(fmt, "Supported format")
            table.add_row(fmt, description)
        
        console.print(table)
    else:
        console.print("⚠️  No supported formats found", style="yellow")


@app.command()
def config_example() -> None:
    """Show example configuration file."""
    
    example_config = """
[conversion]
markdown_flavor = "github"
line_length = 80
heading_style = "atx"
preserve_html = false
strip_comments = true

[security]
max_file_size = 104857600  # 100MB
sanitize_html = true
allow_external_links = true

[performance]
use_streaming = true
max_workers = 4
cache_results = true
"""
    
    console.print("[bold]Example .slateQuill.toml configuration:[/bold]")
    console.print(example_config)
    console.print("\n💡 Copy this to [bold].slateQuill.toml[/bold] in your project root and customize as needed.")


if __name__ == "__main__":
    app()
