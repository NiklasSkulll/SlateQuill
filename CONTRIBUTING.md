# Contributing to SlateQuill

We welcome contributions to SlateQuill! This document provides guidelines for contributing to the project.

## Development Setup

1. **Fork and Clone**
   ```bash
   git clone https://github.com/your-username/SlateQuill.git
   cd SlateQuill
   ```

2. **Install Dependencies**
   ```bash
   poetry install
   ```

3. **Set up Pre-commit Hooks**
   ```bash
   poetry run pre-commit install
   ```

## Development Workflow

### Running Tests
```bash
# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=SlateQuill --cov-report=html

# Run specific test types
poetry run pytest tests/unit/      # Unit tests only
poetry run pytest tests/integration/  # Integration tests only
poetry run pytest tests/performance/ --benchmark-only  # Performance tests
```

### Code Quality
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

### Making Changes

1. **Create a Feature Branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```

2. **Make Your Changes**
   - Follow PEP 8 style guide (enforced by Black)
   - Write tests for new features
   - Update documentation as needed
   - Use conventional commits for commit messages

3. **Test Your Changes**
   ```bash
   poetry run pytest
   poetry run pre-commit run --all-files
   ```

4. **Submit a Pull Request**
   - Ensure CI passes
   - Update README if needed
   - Provide clear description of changes

## Code Style

- **Formatter**: Black (line length 88)
- **Import Sorter**: isort (compatible with Black)
- **Linter**: Ruff (comprehensive rules)
- **Type Checker**: mypy with strict settings

## Commit Messages

We use conventional commits:
- `feat:` for new features
- `fix:` for bug fixes
- `docs:` for documentation changes
- `test:` for adding/modifying tests
- `refactor:` for code refactoring
- `perf:` for performance improvements

## Pull Request Process

1. Update documentation if needed
2. Add tests for new functionality
3. Ensure all tests pass
4. Update the README if you've added new features
5. Request review from maintainers

## Questions?

Feel free to open an issue for any questions or concerns!
