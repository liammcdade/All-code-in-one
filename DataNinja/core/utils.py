```python
import logging
import os
import json
from datetime import datetime

# --- Configuration Loading ---
def load_config(config_path='config.json'):
    """
    Loads a JSON configuration file.

    Args:
        config_path (str): Path to the configuration file.

    Returns:
        dict: Configuration dictionary, or None if loading fails.
    """
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        return config
    except FileNotFoundError:
        print(f"Warning: Configuration file '{config_path}' not found.")
        return None
    except json.JSONDecodeError:
        print(f"Warning: Error decoding JSON from '{config_path}'.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred while loading config '{config_path}': {e}")
        return None

# --- Logging Setup ---
DEFAULT_LOG_LEVEL = logging.INFO
DEFAULT_LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
DEFAULT_LOG_FILE = 'dataninja_app.log'

def setup_logging(log_level=None, log_format=None, log_file=None, module_name=__name__):
    """
    Sets up basic logging for the application or specific modules.

    Args:
        log_level (int, str, optional): The logging level (e.g., logging.INFO, 'DEBUG').
                                       Defaults to DEFAULT_LOG_LEVEL.
        log_format (str, optional): The format string for log messages.
                                    Defaults to DEFAULT_LOG_FORMAT.
        log_file (str, optional): Path to the log file. If None, logs to console.
                                  If provided, logs to both file and console.
                                  Defaults to DEFAULT_LOG_FILE for file logging.
        module_name (str, optional): The name of the logger. Defaults to the name of the
                                     module calling this function.

    Returns:
        logging.Logger: Configured logger instance.
    """
    # Determine effective logging settings
    level = log_level if log_level is not None else DEFAULT_LOG_LEVEL
    fmt = log_format if log_format is not None else DEFAULT_LOG_FORMAT

    # Get or create the logger
    logger = logging.getLogger(module_name)

    # Prevent adding multiple handlers if already configured
    if logger.hasHandlers():
        # Check if it's the root logger and has a basicConfig handler
        if logger.name == "root" and any(isinstance(h, logging.StreamHandler) and h.formatter is None for h in logger.handlers):
             # This might be from a previous basicConfig call. Clear it.
             logger.handlers = []
        elif logger.name != "root": # For non-root loggers, clear existing to reconfigure
            logger.handlers = []


    logger.setLevel(level)

    # Create formatter
    formatter = logging.Formatter(fmt)

    # Console Handler (always add for visibility, can be configured further)
    ch = logging.StreamHandler()
    ch.setLevel(level) # Console can have its own level if desired, here same as logger
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    # File Handler (optional)
    actual_log_file = log_file if log_file is not None else (DEFAULT_LOG_FILE if log_file is None and module_name == "DataNinjaApp" else None)

    if actual_log_file:
        try:
            fh = logging.FileHandler(actual_log_file, mode='a') # Append mode
            fh.setLevel(level) # File can also have its own specific level
            fh.setFormatter(formatter)
            logger.addHandler(fh)
            logger.info(f"Logging initialized. Outputting to console and file: {actual_log_file}")
        except Exception as e:
            logger.error(f"Failed to set up file logging for {actual_log_file}: {e}", exc_info=True)
            logger.info("Logging initialized. Outputting to console only.")
    else:
        logger.info("Logging initialized. Outputting to console only.")

    # If this is the first time configuring the root logger via this function
    # avoid basicConfig if we are manually setting handlers.
    # However, if no handlers are configured for root by now, basicConfig might be implicitly called by libraries.
    # For robust control, applications usually call setup_logging early for their main app logger.

    return logger

# --- File System Utilities ---
def ensure_directory_exists(dir_path):
    """
    Ensures that a directory exists, creating it if necessary.

    Args:
        dir_path (str): The path to the directory.

    Returns:
        bool: True if the directory exists or was created successfully, False otherwise.
    """
    if not os.path.exists(dir_path):
        try:
            os.makedirs(dir_path)
            print(f"Directory created: {dir_path}")
            return True
        except OSError as e:
            print(f"Error creating directory {dir_path}: {e}")
            return False
    return True

def generate_timestamped_filename(base_name, extension, prefix=""):
    """
    Generates a filename with a timestamp. E.g., "prefix_basename_YYYYMMDD_HHMMSS.extension"

    Args:
        base_name (str): The main part of the filename.
        extension (str): The file extension (e.g., "csv", "png").
        prefix (str, optional): A prefix for the filename.

    Returns:
        str: The generated timestamped filename.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    clean_extension = extension.lstrip('.')
    if prefix:
        return f"{prefix}_{base_name}_{timestamp}.{clean_extension}"
    else:
        return f"{base_name}_{timestamp}.{clean_extension}"


if __name__ == '__main__':
    print("--- Utilities Demonstration ---")

    # --- Logging Demo ---
    print("\n--- Logging Demo ---")
    # Setup a general application logger
    app_logger = setup_logging(log_level=logging.DEBUG, module_name="DataNinjaApp")
    app_logger.debug("This is a debug message from the app logger.")
    app_logger.info("This is an info message from the app logger.")
    app_logger.warning("This is a warning from the app logger.")

    # Setup a logger for a specific module (will inherit app_logger's file if not specified)
    # or configure its own.
    module_logger = setup_logging(log_level='INFO', module_name="MyModule", log_file="module_specific.log")
    module_logger.info("Info message from MyModule logger.")
    module_logger.debug("This debug message from MyModule should NOT appear if its level is INFO.") # Will not show

    another_logger = setup_logging(log_level=logging.ERROR, module_name="CriticalErrors", log_file=None) # Console only
    another_logger.error("An error message from CriticalErrors logger (console only).")


    # --- Config Loading Demo ---
    print("\n--- Config Loading Demo ---")
    # Create a dummy config file for testing
    dummy_config = {"setting1": "value1", "feature_enabled": True, "threshold": 42}
    dummy_config_path = "temp_config.json"
    with open(dummy_config_path, 'w') as f:
        json.dump(dummy_config, f, indent=2)

    loaded_cfg = load_config(dummy_config_path)
    if loaded_cfg:
        print(f"Loaded config: {loaded_cfg}")
        print(f"Setting1: {loaded_cfg.get('setting1')}")

    non_existent_cfg = load_config("non_existent_config.json")
    if non_existent_cfg is None:
        print("Correctly handled non-existent config.")

    # Clean up dummy config
    if os.path.exists(dummy_config_path):
        os.remove(dummy_config_path)

    # --- Filesystem Demo ---
    print("\n--- Filesystem Demo ---")
    test_dir = "temp_test_dir/subdir"
    print(f"Ensuring directory '{test_dir}' exists...")
    ensure_directory_exists(test_dir)

    # Check if created (basic check, real test would use os.path.isdir)
    if os.path.exists(test_dir):
        print(f"Directory '{test_dir}' now exists.")
        # Clean up by removing the directory structure
        try:
            os.removedirs("temp_test_dir") # removes empty parent dirs too
            print(f"Cleaned up '{test_dir}' and its parents.")
        except OSError as e: # Might fail if not empty or other reasons
            print(f"Could not remove temp_test_dir: {e}")
            if os.path.exists(test_dir): os.rmdir(test_dir) # Try removing just the subdir
            if os.path.exists("temp_test_dir"): os.rmdir("temp_test_dir")


    ts_filename = generate_timestamped_filename("report", "csv", prefix="daily")
    print(f"Generated timestamped filename: {ts_filename}")
    ts_filename_no_prefix = generate_timestamped_filename("output", "txt")
    print(f"Generated timestamped filename (no prefix): {ts_filename_no_prefix}")

    print("\n--- Demonstration Complete ---")

```
