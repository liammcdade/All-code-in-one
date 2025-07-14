# Technology Stack

## Core Technologies
- **Language**: Python 3.8+
- **CLI Framework**: Typer for command-line interfaces
- **Data Processing**: pandas, numpy
- **Visualization**: plotext (ASCII plots), rich (terminal formatting)
- **File Formats**: openpyxl (Excel), PyYAML, sqlite3, json

## Key Libraries
- **DataNinja**: typer, pandas, rich, plotext, scikit-learn
- **Sports Analysis**: Standard Python libraries, custom analytics
- **System Utilities**: pathlib, subprocess, os operations
- **Scientific Computing**: numpy, pandas for data analysis

## Build System
- **Package Management**: pip with requirements.txt files
- **Entry Points**: setuptools console_scripts for CLI tools
- **Module Structure**: Standard Python packages with __init__.py

## Common Commands

### Development
```bash
# Check dependencies across all projects
python scripts/checkdeps.py

# Install DataNinja dependencies
pip install -r DataNinja/requirements.txt

# Run DataNinja CLI
python -m DataNinja
# or after installation:
dataninja

# Launch unified tool launcher
python launcher.py
```

### Testing
```bash
# Run tests (when available)
pytest DataNinja/tests/
python test_launcher.py
```

### Project Management
```bash
# Generate documentation
python scripts/gendocs.py

# Load plugins dynamically
python scripts/plugin_loader.py
```

## Architecture Patterns
- **Plugin Architecture**: DataNinja uses modular plugins for ML, geo, SQL functionality
- **CLI-First Design**: All tools prioritize command-line interfaces
- **Session Management**: DataNinja maintains state between commands using pickle
- **Unified Launcher**: Central access point for all project tools
- **Format Handlers**: Abstracted file format processing with dedicated handlers