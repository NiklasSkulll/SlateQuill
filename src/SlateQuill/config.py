"""
SlateQuill configuration management.

This module provides configuration classes using Pydantic for type safety
and validation of SlateQuill settings.
"""

from pathlib import Path
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field, validator


class ConversionConfig(BaseModel):
    """Configuration for conversion process."""
    
    markdown_flavor: str = Field(default="github", description="Markdown flavor to use")
    preserve_html: bool = Field(default=False, description="Whether to preserve HTML tags")
    strip_comments: bool = Field(default=True, description="Whether to strip HTML comments")
    max_file_size: int = Field(default=100_000_000, description="Maximum file size in bytes")
    line_length: int = Field(default=80, description="Maximum line length")
    heading_style: str = Field(default="atx", description="Heading style: atx (#) or setext (===)")
    emphasis_style: str = Field(default="asterisk", description="Emphasis style: asterisk (*) or underscore (_)")
    clean_whitespace: bool = Field(default=True, description="Whether to clean extra whitespace")
    
    @validator("markdown_flavor")
    def validate_markdown_flavor(cls, v: str) -> str:
        valid_flavors = ["github", "commonmark", "strict"]
        if v not in valid_flavors:
            raise ValueError(f"Invalid markdown flavor: {v}. Must be one of {valid_flavors}")
        return v
    
    @validator("heading_style")
    def validate_heading_style(cls, v: str) -> str:
        valid_styles = ["atx", "setext"]
        if v not in valid_styles:
            raise ValueError(f"Invalid heading style: {v}. Must be one of {valid_styles}")
        return v
    
    @validator("emphasis_style")
    def validate_emphasis_style(cls, v: str) -> str:
        valid_styles = ["asterisk", "underscore"]
        if v not in valid_styles:
            raise ValueError(f"Invalid emphasis style: {v}. Must be one of {valid_styles}")
        return v


class SecurityConfig(BaseModel):
    """Configuration for security settings."""
    
    max_file_size: int = Field(default=104_857_600, description="Maximum file size in bytes (100MB)")
    sanitize_html: bool = Field(default=True, description="Whether to sanitize HTML")
    allow_external_links: bool = Field(default=True, description="Whether to allow external links")
    allowed_schemes: list[str] = Field(default_factory=lambda: ["http", "https", "ftp"], description="Allowed URL schemes")


class PerformanceConfig(BaseModel):
    """Configuration for performance settings."""
    
    use_streaming: bool = Field(default=True, description="Whether to use streaming processing")
    max_workers: int = Field(default=4, description="Maximum number of worker threads")
    cache_results: bool = Field(default=True, description="Whether to cache results")
    cache_ttl: int = Field(default=3600, description="Cache TTL in seconds")


class OutputConfig(BaseModel):
    """Configuration for output settings."""
    
    create_backup: bool = Field(default=False, description="Whether to create backup files")
    overwrite_existing: bool = Field(default=True, description="Whether to overwrite existing files")
    output_directory: str = Field(default="./output", description="Default output directory")


class LoggingConfig(BaseModel):
    """Configuration for logging settings."""
    
    level: str = Field(default="INFO", description="Logging level")
    format: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        description="Logging format"
    )
    file: Optional[str] = Field(default=None, description="Log file path")
    
    @validator("level")
    def validate_level(cls, v: str) -> str:
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if v.upper() not in valid_levels:
            raise ValueError(f"Invalid log level: {v}. Must be one of {valid_levels}")
        return v.upper()


class Config(BaseModel):
    """Main configuration class."""
    
    conversion: ConversionConfig = Field(default_factory=ConversionConfig)
    security: SecurityConfig = Field(default_factory=SecurityConfig)
    performance: PerformanceConfig = Field(default_factory=PerformanceConfig)
    output: OutputConfig = Field(default_factory=OutputConfig)
    logging: LoggingConfig = Field(default_factory=LoggingConfig)
    plugins: Dict[str, Any] = Field(default_factory=dict, description="Plugin configurations")
    
    @classmethod
    def from_file(cls, config_path: Path) -> "Config":
        """Load configuration from a TOML file."""
        try:
            import tomllib
        except ImportError:
            import tomli as tomllib
        
        try:
            with open(config_path, "rb") as f:
                data = tomllib.load(f)
            return cls(**data)
        except FileNotFoundError:
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        except Exception as e:
            raise ValueError(f"Failed to load configuration: {e}")
    
    def to_file(self, config_path: Path) -> None:
        """Save configuration to a TOML file."""
        try:
            import tomli_w
        except ImportError:
            raise ImportError("tomli_w is required for writing TOML files")
        
        data = self.dict()
        with open(config_path, "wb") as f:
            tomli_w.dump(data, f)


def load_config(config_path: Optional[Path] = None) -> Config:
    """Load configuration from file or return default configuration."""
    if config_path and config_path.exists():
        return Config.from_file(config_path)
    
    # Look for default config files
    default_paths = [
        Path(".slateQuill.toml"),
        Path("slateQuill.toml"),
        Path("pyproject.toml"),  # Look for [tool.slateQuill] section
    ]
    
    for path in default_paths:
        if path.exists():
            try:
                return Config.from_file(path)
            except Exception:
                continue
    
    # Return default configuration
    return Config()
