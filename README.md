<div align="center">

```
  ███████╗██╗      █████╗ ████████╗███████╗ ██████╗ ██╗   ██╗██╗██╗     ██╗     
  ██╔════╝██║     ██╔══██╗╚══██╔══╝██╔════╝██╔═══██╗██║   ██║██║██║     ██║     
  ███████╗██║     ███████║   ██║   █████╗  ██║   ██║██║   ██║██║██║     ██║     
  ╚════██║██║     ██╔══██║   ██║   ██╔══╝  ██║▄▄ ██║██║   ██║██║██║     ██║     
  ███████║███████╗██║  ██║   ██║   ███████╗╚██████╔╝╚██████╔╝██║███████╗███████╗
  ╚══════╝╚══════╝╚═╝  ╚═╝   ╚═╝   ╚══════╝ ╚══▀▀═╝  ╚═════╝ ╚═╝╚══════╝╚══════╝
```

**A robust Python CLI tool for converting HTML documents to clean, standards-compliant Markdown**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Support](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Development Status](https://img.shields.io/badge/status-in%20development-orange)](https://github.com/NiklasSkulll/SlateQuill)

[Installation](#installation) • [Quick Start](#quick-start) • [Features](#features) • [Documentation](#documentation) • [Contributing](#contributing)

</div>

---

# SlateQuill

## 🚀 Overview

SlateQuill is a Python-based CLI tool that reliably transforms HTML documents into clean, standards-compliant Markdown with full support for:

- **Complex tables** with proper alignment and formatting
- **Nested lists** with accurate indentation
- **Footnotes** and reference links
- **Embedded content** (images, videos, code blocks)
- **Extensible plugin system** for future format support (PDF, DOCX, EPUB, etc.)

### Why SlateQuill?

- 🔒 **Security-First**: Built-in input validation and sanitization
- ⚡ **Performance**: Async I/O and streaming support for large files
- 🔧 **Extensible**: Plugin architecture for custom converters
- 🎨 **Configurable**: Flexible output formatting options
- 📱 **User-Friendly**: Beautiful CLI with progress bars and clear error messages

---

## 📦 Installation

### PyPI (Recommended)

```bash
pip install SlateQuill
```

### Development Version

```bash
pip install git+https://github.com/NiklasSkulll/SlateQuill.git
```

### Other Package Managers

```bash
# Homebrew (macOS)
brew install SlateQuill

# Conda
conda install -c conda-forge SlateQuill
```

### Docker (Optional)

For users who prefer containerized environments or want to avoid Python installation:

```bash
docker run -v $(pwd):/workspace SlateQuill:latest convert input.html -o output.md
```

---

## 🏃 Quick Start

### Basic Usage

```bash
# Convert HTML file to Markdown
SlateQuill input.html output.md

# Convert with auto-generated output name
SlateQuill input.html

# Show version
SlateQuill --version

# Show help
SlateQuill --help
```

### Python API

```python
from SlateQuill import convert_file
from pathlib import Path
import asyncio

# Simple conversion
async def convert():
    await convert_file(Path("input.html"), Path("output.md"))

# Run the conversion
asyncio.run(convert())

# With custom configuration
from SlateQuill.config import Config, ConversionConfig, load_config

config = load_config()  # Load from .slateQuill.toml or use defaults
await convert_file(Path("input.html"), Path("output.md"), config)
```

---

## ✨ Features

### Core Capabilities

- **HTML to Markdown Conversion**: Clean, standards-compliant output
- **Security-First**: Input validation and HTML sanitization
- **Async Processing**: Efficient handling of files
- **Configuration System**: TOML-based configuration
- **Plugin Architecture**: Extensible converter system (planned)

### Current Status (v0.1.0)

- ✅ Basic HTML to Markdown conversion
- ✅ Configuration system with TOML support
- ✅ Security validation and HTML sanitization
- ✅ Simple CLI interface
- ✅ Async core functionality
- 🚧 Advanced CLI features (planned)
- 🚧 Batch processing (planned)
- 🚧 Multiple output formats (planned)

### Security & Reliability

- **Input Validation**: Comprehensive security checks
- **HTML Sanitization**: XSS prevention and content cleaning
- **Error Handling**: Detailed error messages and recovery
- **Memory Management**: Efficient processing of large documents
- **Plugin Sandboxing**: Safe execution of third-party plugins

### Performance

- **Streaming Support**: Memory-efficient processing (planned)
- **Async I/O**: Non-blocking file operations
- **Memory Management**: Efficient processing of documents
- **Current Performance**: 
  - Small files (<1MB): Fast conversion
  - Medium files (1-10MB): Efficient processing
  - Large files (>10MB): Planned optimizations

---

## 🛠 Configuration

Create a `.slateQuill.toml` file in your project root:

```toml
[conversion]
markdown_flavor = "github"
preserve_html = false
strip_comments = true

[security]
max_file_size = 104857600  # 100MB
sanitize_html = true
validate_encoding = true

[logging]
level = "INFO"
```

*Note: Advanced configuration options are planned for future versions.*

---

## 📚 Documentation

- **[User Guide](https://SlateQuill.readthedocs.io/en/latest/user-guide/)**: Installation, configuration, and usage
- **[API Reference](https://SlateQuill.readthedocs.io/en/latest/api/)**: Complete API documentation
- **[Plugin Development](https://SlateQuill.readthedocs.io/en/latest/plugins/)**: Creating custom converters
- **[Contributing Guide](CONTRIBUTING.md)**: Development setup and workflow

---

## 🔌 Plugin System

SlateQuill includes a plugin architecture for future extensibility:

### Plugin Architecture (Planned)

The plugin system is designed to support different input formats in future versions:

```python
from SlateQuill.plugins.base import BaseConverter
from pathlib import Path

class CustomConverter(BaseConverter):
    def can_handle(self, file_path: Path) -> bool:
        return file_path.suffix.lower() == '.custom'
    
    async def convert(self, content: bytes, options=None) -> str:
        # Your conversion logic here
        return markdown_content
    
    def validate_input(self, content: bytes) -> bool:
        # Input validation logic
        return True
    
    @property
    def supported_formats(self) -> list[str]:
        return ['.custom']
```

*Note: Plugin system is currently in development. Current version focuses on HTML to Markdown conversion.*

---

## 🏗 Technical Architecture

### Core Components

SlateQuill is built with a modular architecture that separates concerns and enables extensibility:

```python
# Core conversion pipeline
from SlateQuill.core import convert_file
from SlateQuill.config import Config
from SlateQuill.security import validate_input
from SlateQuill.plugins import load_plugins

# Exception hierarchy for robust error handling
class SlateQuillError(Exception):
    """Base exception for SlateQuill"""
    pass

class ConversionError(SlateQuillError):
    """Raised when conversion fails"""
    pass

class InvalidInputError(ConversionError):
    """Raised when input is malformed"""
    pass

class SecurityError(SlateQuillError):
    """Raised when security validation fails"""
    pass
```

### Plugin Architecture

The plugin system uses Python's entry-points mechanism for extensibility:

```python
# plugins/base.py
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, Any, Optional

class BaseConverter(ABC):
    """Abstract base class for all converters."""
    
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
        """List of supported file formats."""
        pass
```

### Configuration System

Configuration is handled through Pydantic models for type safety:

```python
# config.py
from pydantic import BaseModel, Field
from typing import Dict, Any

class ConversionConfig(BaseModel):
    """Configuration for conversion process."""
    markdown_flavor: str = Field(default="github")
    preserve_html: bool = Field(default=False)
    strip_comments: bool = Field(default=True)
    max_file_size: int = Field(default=100_000_000)
    line_length: int = Field(default=80)
    
class Config(BaseModel):
    """Main configuration class."""
    conversion: ConversionConfig = ConversionConfig()
    plugins: Dict[str, Any] = Field(default_factory=dict)
    logging_level: str = Field(default="INFO")
```

---

## 🛠 Development Setup

### Prerequisites

- Python 3.10 or higher
- Poetry for dependency management
- Git for version control

### Project Initialization

```bash
# Create new project (for contributors)
poetry new --src SlateQuill
cd SlateQuill

# Clone existing project
git clone https://github.com/NiklasSkulll/SlateQuill.git
cd SlateQuill

# Install dependencies
poetry install

# Set up development tools
poetry run pre-commit install
```

### Development Tools

- **Formatter**: Black (line length 88, PEP 8 compliant)
- **Import Sorter**: isort (compatible with Black)
- **Linter**: Ruff (faster than flake8, comprehensive rules)
- **Type Checker**: mypy with strict settings
- **Security**: bandit for security linting, safety for dependencies

### Quality Gates

```bash
# Run all quality checks
poetry run pre-commit run --all-files

# Individual checks
poetry run black --check src/
poetry run ruff check src/
poetry run mypy src/
poetry run bandit -r src/
poetry run safety check
```

---

## 🧪 Testing Strategy

### Current Test Setup

```
tests/
├── fixtures/                # Test data
│   ├── test_input.html      # Sample HTML input
│   └── test_output.md       # Expected output
└── (unit tests planned)     # Test modules for v0.2.0
```

### Running Tests

```bash
# Install development dependencies
poetry install

# Run tests (when implemented)
poetry run pytest

# Run with coverage (planned)
poetry run pytest --cov=SlateQuill
```

*Comprehensive testing suite will be implemented in v0.2.0*

---

## 🔒 Security Implementation

### Input Validation

- **File Size Limits**: Configurable maximum file size (default 100MB)
- **Content Sanitization**: HTML sanitization to prevent XSS
- **Encoding Detection**: Proper handling of various text encodings
- **Path Validation**: Directory traversal attack prevention

### Plugin Security

- **Sandboxing**: Isolated execution environment for plugins
- **API Restrictions**: Limited system resource access
- **Dependency Scanning**: Automated vulnerability checks
- **Code Signing**: Optional plugin authenticity verification

### Best Practices

- Secure temporary file cleanup
- Memory leak prevention
- Sensitive data logging avoidance
- Internal system detail protection in error messages

---

## 🚀 CI/CD Pipeline

### GitHub Actions Workflows

#### Test Suite (`test-suite.yml`)
- **Triggers**: `push`, `pull_request`
- **Matrix**: Python 3.10, 3.11, 3.12 on Ubuntu, macOS, Windows
- **Steps**:
  1. Install Poetry and cache dependencies
  2. Run security checks (`bandit`, `safety`)
  3. Run quality checks (`pre-commit`)
  4. Execute full test suite with coverage
  5. Upload coverage to Codecov
  6. Run performance benchmarks

#### Release (`release.yml`)
- **Triggers**: Git tag `v*`
- **Steps**:
  1. Validate tag format and changelog
  2. Build and test package
  3. Publish to PyPI (trusted publishing)
  4. Build Docker image (optional)
  5. Generate GitHub release
  6. Deploy documentation

#### Security (`security.yml`)
- **Schedule**: Weekly
- **Scans**: Dependencies, CodeQL, container images

---

## 📋 Complete Configuration

### Full `.slateQuill.toml` Example

```toml
[conversion]
markdown_flavor = "github"          # "github", "commonmark", "strict"
line_length = 80
heading_style = "atx"               # "atx" (#) or "setext" (===)
emphasis_style = "asterisk"         # "asterisk" (*) or "underscore" (_)
preserve_html = false
strip_comments = true
clean_whitespace = true

[security]
max_file_size = 104_857_600         # 100MB in bytes
allow_external_links = true
sanitize_html = true

[plugins]
pdf.ocr_enabled = true
pdf.language = "en"
docx.preserve_styles = false

[output]
create_backup = false
overwrite_existing = true
output_directory = "./output"

[logging]
level = "INFO"
format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
file = "./SlateQuill.log"

[performance]
use_streaming = true
max_workers = 4
cache_results = true
cache_ttl = 3600                    # seconds
```

---

## 📦 Dependencies

### Core Dependencies

```toml
[tool.poetry.dependencies]
python = "^3.10"
beautifulsoup4 = "^4.12.0"
lxml = "^4.9.0"
markdownify = "^0.11.0"
typer = "^0.9.0"
rich = "^13.0.0"
pydantic = "^2.0.0"
aiofiles = "^23.0.0"
click-completion = "^0.5.0"
bleach = "^6.0.0"
tomli = "^2.0.0"
tomli-w = "^1.0.0"
```

### Development Dependencies

```toml
[tool.poetry.group.dev.dependencies]
pytest = "^7.0.0"
pytest-asyncio = "^0.21.0"
pytest-cov = "^4.0.0"
pytest-benchmark = "^4.0.0"
hypothesis = "^6.0.0"
black = "^23.0.0"
ruff = "^0.1.0"
mypy = "^1.0.0"
pre-commit = "^3.0.0"
bandit = "^1.7.0"
safety = "^2.0.0"
mkdocs = "^1.5.0"
mkdocs-material = "^9.0.0"
mkdocstrings = {extras = ["python"], version = "^0.23.0"}
```

### System Requirements

- **Python**: 3.10 or higher
- **RAM**: 512MB minimum (2GB recommended for large files)
- **Storage**: 100MB for installation
- **Network**: Optional for plugin downloads

---

## 🧪 Development

### Prerequisites

- Python 3.10 or higher
- Poetry for dependency management
- Git for version control

### Setup

```bash
# Clone the repository
git clone https://github.com/NiklasSkulll/SlateQuill.git
cd SlateQuill

# Install dependencies
poetry install

# Set up pre-commit hooks
pre-commit install

# Run tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=SlateQuill
```

### Project Structure

```
SlateQuill/
├── src/SlateQuill/          # Main package
│   ├── __init__.py          # Package initialization
│   ├── simple_cli.py        # Simple CLI interface
│   ├── cli.py               # Advanced CLI (planned)
│   ├── core.py              # Core conversion logic
│   ├── html2md.py           # HTML to Markdown converter
│   ├── config.py            # Configuration management
│   ├── security.py          # Security validation
│   ├── exceptions.py        # Exception hierarchy
│   └── plugins/             # Plugin system
│       └── base.py          # Base plugin class
├── tests/                   # Test suite
│   ├── fixtures/            # Test data
│   ├── test_input.html      # Sample input
│   └── test_output.md       # Sample output
├── docs/                    # Documentation (planned)
├── pyproject.toml          # Poetry configuration
├── .gitignore              # Git ignore rules
├── .pre-commit-config.yaml # Pre-commit hooks
├── CONTRIBUTING.md         # Contributing guidelines
├── SECURITY.md             # Security policy
└── CHANGELOG.md            # Version history
```

---

## 📊 Performance Benchmarks

*Performance benchmarks will be added as the project matures.*

Current status:
- Basic HTML to Markdown conversion: Working
- Small files (<1MB): Fast conversion
- Async processing: Implemented
- Memory efficiency: Under development

*Detailed benchmarks will be provided in v0.2.0*

---

## 🔒 Security

SlateQuill takes security seriously:

- **Input Validation**: All inputs are validated before processing
- **HTML Sanitization**: Dangerous HTML elements are removed or escaped
- **Plugin Sandboxing**: Third-party plugins run in isolated environments
- **Dependency Scanning**: Regular security audits of dependencies

To report security vulnerabilities, please see our [Security Policy](SECURITY.md).

---

## 🗺 Roadmap

### v0.1.0 (Current) - Core Foundation
- ✅ Basic HTML to Markdown conversion
- ✅ Configuration system with TOML support
- ✅ Security validation and HTML sanitization
- ✅ Simple CLI interface
- ✅ Async core functionality
- ✅ Exception hierarchy
- ✅ Plugin base architecture

### v0.2.0 - Enhanced CLI & Features
- 🚧 Advanced CLI with Typer framework
- 🚧 Batch processing support
- 🚧 Multiple output formats
- 🚧 Configuration validation
- 🚧 Comprehensive test suite

### v0.3.0 - Performance & Plugins
- 📋 Streaming support for large files
- 📋 First official plugin (PDF support)
- 📋 Performance optimizations
- 📋 Memory usage improvements
- 📋 Docker image (optional deployment method)

### v1.0.0 - Production Ready
- 📋 Stable API
- 📋 Enterprise features
- 📋 Comprehensive documentation
- 📋 Performance guarantees

### Future Releases
- **Advanced Formats**: EPUB, DOCX, LaTeX, AsciiDoc → Markdown
- **AI Integration**: Smart content extraction and formatting
- **Language Bindings**: Node.js, Go, Rust libraries
- **Cloud Integration**: AWS Lambda, Google Cloud Functions
- **Enterprise Features**: Bulk processing, monitoring, collaboration

---

## 🏷 Versioning

SlateQuill follows [Semantic Versioning](https://semver.org/) (`MAJOR.MINOR.PATCH`):

- **MAJOR**: Incompatible API changes
- **MINOR**: New functionality in backward-compatible manner
- **PATCH**: Backward-compatible bug fixes

Releases are automated through GitHub Actions with conventional commits generating changelogs automatically.

---

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Quick Contribute

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes and add tests
4. Run the test suite: `poetry run pytest`
5. Submit a pull request

### Development Guidelines

- Follow PEP 8 style guide (enforced by Black)
- Write tests for new features
- Update documentation as needed
- Use conventional commits for commit messages

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) for HTML parsing
- [markdownify](https://github.com/matthewwithanm/python-markdownify) for base conversion
- [Typer](https://typer.tiangolo.com/) for the CLI framework
- [Rich](https://rich.readthedocs.io/) for beautiful terminal output

---

<div align="center">

**[⬆ Back to Top](#slatequill)**

Made by [Niklas Skulll](https://github.com/NiklasSkulll)

</div>