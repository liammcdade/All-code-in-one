"""Sports analysis collection with various sport-specific analyzers."""

__version__ = "1.0.0"

# Import main analyzers
try:
    from .baseball.baseball_analyzer import BaseballAnalyzer
except ImportError:
    BaseballAnalyzer = None

try:
    from .tennis.tennis_analyzer import process_player
except ImportError:
    process_player = None

try:
    from .basketball.basketball_analyzer import BasketballAnalyzer
except ImportError:
    BasketballAnalyzer = None

__all__ = ['BaseballAnalyzer', 'process_player', 'BasketballAnalyzer']
