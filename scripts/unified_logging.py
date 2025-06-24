import logging
import sys
from pathlib import Path
import yaml

def setup_logging(config_path=None):
    """Set up logging for the whole project. Reads config if available."""
    log_level = logging.INFO
    log_file = None
    if config_path:
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                config = yaml.safe_load(f)
            log_level = getattr(logging, config.get("logging", {}).get("level", "INFO"))
            log_file = config.get("logging", {}).get("file")
        except Exception:
            pass
    logger = logging.getLogger()
    logger.setLevel(log_level)
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    # Console handler
    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    # File handler
    if log_file:
        Path(log_file).parent.mkdir(parents=True, exist_ok=True)
        fh = logging.FileHandler(log_file)
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    return logger 