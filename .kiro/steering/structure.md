# Project Structure

## Root Level Organization
```
├── launcher.py              # Unified tool launcher with menu system
├── DataNinja/              # Main data processing toolkit
├── sportsanalysis/         # Sports analytics collection
├── streamyutilities/       # System utility tools
├── scripts/                # Development and build scripts
├── space/                  # Scientific computing tools
├── extra/                  # Additional utilities and tools
├── sample_code/            # Reference implementations
└── .kiro/                  # Kiro IDE configuration
```

## DataNinja Structure
```
DataNinja/
├── cli.py                  # Main CLI entry point
├── setup.py               # Package configuration
├── requirements.txt       # Dependencies
├── core/                  # Core processing modules
├── formats/               # File format handlers (CSV, JSON, Excel, etc.)
├── plugins/               # Extensible plugin system
├── data/                  # Sample/test data
└── tests/                 # Test suite
```

## Sports Analysis Organization
```
sportsanalysis/
├── worldcup26/           # World Cup 2026 analysis
├── premier-league/       # Premier League analytics
├── NFL/                  # American football analysis
├── F1/                   # Formula 1 analytics
├── tennis/               # Tennis match analysis
├── basketball/           # Basketball statistics
├── baseball/             # Baseball analytics
├── olympic/              # Olympic games analysis
├── chess/                # Chess engine and analysis
└── [sport]/              # Each sport has dedicated folder
```

## Naming Conventions
- **Folders**: lowercase with hyphens for multi-word names
- **Python files**: snake_case.py
- **Main entry points**: main.py or [tool]_analyzer.py
- **CLI modules**: cli.py for command-line interfaces
- **Utilities**: [purpose]_[action].py (e.g., analyze_emissions.py)

## File Organization Patterns
- Each major tool/project has its own top-level directory
- Main entry points are clearly named (main.py, cli.py, launcher.py)
- Related functionality is grouped in subdirectories
- Configuration and setup files at package root level
- Tests and documentation alongside source code

## Plugin Architecture
- DataNinja plugins in `DataNinja/plugins/`
- Each plugin is self-contained module
- Plugins follow naming: [functionality].py (ml.py, geo.py, sql.py)
- Plugin loading handled by `scripts/plugin_loader.py`

## Development Scripts Location
- `scripts/` contains development utilities
- `checkdeps.py` for dependency management
- `gendocs.py` for documentation generation
- Configuration templates in `scripts/`