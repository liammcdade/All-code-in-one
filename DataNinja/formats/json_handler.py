import os
import json
import pandas as pd
import logging

# Assuming DataLoader is in ../core/loader.py
from ..core.loader import DataLoader
# Assuming setup_logging might be in ../core/utils.py (if used)
# from ..core.utils import setup_logging # Example, adjust if needed

# Basic module-level logger configuration
# For more sophisticated logging, integrate with a project-wide setup if available.
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class JSONHandler(DataLoader):
    def __init__(self, source):
        super().__init__(source)
        # Instance-specific logger
        # The name will be something like 'DataNinja.formats.json_handler.JSONHandler'
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        self.logger.info(f"JSONHandler initialized for source: {self.source}")

    def load_data(self, **kwargs):
        self.logger.info(f"Attempting to load JSON data from {self.source}")
        if not self.source: # Added check for empty source path from init
             self.logger.error("Source path is None or empty, cannot load data.")
             raise ValueError("Source path is None or empty.")
        if not os.path.exists(self.source):
            self.logger.error(f"File not found: {self.source}")
            raise FileNotFoundError(f"File not found: {self.source}")

        try:
            # Try loading with pandas.read_json first, suitable for table-like JSON.
            # common kwargs: orient, lines, dtype, convert_dates etc.
            # Default orient for read_json can often infer, but 'records' is common.
            df = pd.read_json(self.source, **kwargs)
            self.logger.info(f"Successfully loaded JSON data into DataFrame from {self.source}. Shape: {df.shape}")
            return df
        except ValueError as ve: # pandas raises ValueError for many JSON parsing issues
            self.logger.warning(f"Pandas failed to parse JSON from {self.source} directly into DataFrame: {ve}. Attempting with json.load.")
            try:
                # Remove pandas-specific kwargs before passing to json.load
                json_load_kwargs = {k: v for k, v in kwargs.items() if k not in ['orient', 'lines', 'dtype', 'convert_dates', 'keep_default_dates', 'numpy', 'precise_float', 'date_unit', 'encoding', 'encoding_errors', 'compression', 'storage_options', 'chunksize', 'nrows']}
                with open(self.source, 'r', encoding=kwargs.get('encoding', 'utf-8')) as f: # use encoding from kwargs if present
                    data = json.load(f, **json_load_kwargs)
                self.logger.info(f"Successfully loaded JSON data as {type(data)} from {self.source}")
                return data
            except json.JSONDecodeError as jde:
                self.logger.error(f"JSONDecodeError parsing {self.source}: {jde}")
                raise
            except Exception as e_json_load:
                self.logger.error(f"An unexpected error occurred with json.load for {self.source}: {e_json_load}")
                raise
        except Exception as e_pd:
            self.logger.error(f"An unexpected error occurred with pd.read_json for {self.source}: {e_pd}")
            raise

    def save_data(self, data, target_path=None, **kwargs):
        if target_path is None:
            self.logger.error("Target path for saving JSON data is required.")
            raise ValueError("Target path for saving JSON data is required.")

        self.logger.info(f"Attempting to save data to {target_path}")

        # Ensure the target directory exists
        target_dir = os.path.dirname(target_path)
        if target_dir: # Ensure target_dir is not an empty string (e.g. if target_path is just a filename)
            os.makedirs(target_dir, exist_ok=True)
            self.logger.debug(f"Ensured directory exists: {target_dir}")

        try:
            if isinstance(data, pd.DataFrame):
                # Default to orient='records' and lines=True for JSONL if not specified in kwargs
                # these are good defaults for tabular data.
                orient = kwargs.pop('orient', 'records')
                # lines=True is typically used with orient='records'.
                # For other orients like 'table', lines should usually be False.
                default_lines = True if orient == 'records' else False
                lines = kwargs.pop('lines', default_lines)

                # Indent is typically None if lines=True, or a value (e.g., 4) if lines=False for pretty printing
                default_indent = None if lines else 4
                indent = kwargs.pop('indent', default_indent)


                data.to_json(target_path, orient=orient, lines=lines, indent=indent, **kwargs)
                self.logger.info(f"Successfully saved pandas DataFrame to JSON: {target_path} (orient='{orient}', lines={lines}, indent={indent})")
            elif isinstance(data, (dict, list)):
                indent = kwargs.pop('indent', 4) # Default to pretty-printing for dict/list
                with open(target_path, 'w', encoding=kwargs.get('encoding', 'utf-8')) as f:
                    json.dump(data, f, indent=indent, **kwargs)
                self.logger.info(f"Successfully saved dict/list to JSON: {target_path} (indent={indent})")
            else:
                self.logger.error(f"Unsupported data type for saving to JSON: {type(data)}. Must be DataFrame, dict, or list.")
                raise TypeError(f"Unsupported data type for saving to JSON: {type(data)}")
        except IOError as e:
            self.logger.error(f"IOError occurred while saving data to {target_path}: {e}")
            raise
        except TypeError as e: # e.g. if data contains non-serializable types for json.dump
            self.logger.error(f"TypeError during JSON serialization for {target_path}: {e}")
            raise
        except Exception as e:
            self.logger.error(f"An unexpected error occurred while saving data to {target_path}: {e}")
            raise

if __name__ == '__main__':
    # Setup basic logging for the __main__ block
    # This logger will be named 'DataNinja.formats.json_handler'
    main_logger = logging.getLogger(__name__)
    # Check if handlers are already configured by basicConfig at module level
    if not main_logger.handlers or not logging.getLogger().handlers:
        # If basicConfig was called at module level, it configures the root logger.
        # We might want a specific handler for __main__ if module's basicConfig isn't sufficient.
        # For simplicity here, we assume module-level basicConfig is okay, or we re-apply.
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', force=True)
    main_logger.setLevel(logging.DEBUG) # Ensure this specific logger is at DEBUG if needed.


    # 0. Define paths & Create a temporary directory for test files
    temp_dir = "temp_json_test_data"
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
        main_logger.info(f"Created temporary directory: {temp_dir}")

    # Paths for various test files
    sample_df_json_path = os.path.join(temp_dir, 'sample_df.json') # For DataFrame-like JSON (list of records)
    sample_obj_json_path = os.path.join(temp_dir, 'sample_object.json') # For dict-like JSON
    malformed_json_path = os.path.join(temp_dir, 'malformed.json')
    output_df_jsonl_path = os.path.join(temp_dir, 'output_df.jsonl') # JSON Lines
    output_df_json_path = os.path.join(temp_dir, 'output_df.json') # Standard JSON
    output_dict_json_path = os.path.join(temp_dir, 'output_dict.json')


    # 1. Create dummy JSON files for testing load_data
    # DataFrame-like JSON (list of records) - suitable for pd.read_json(orient='records')
    df_data_list = [
        {'id': 1, 'name': 'Alice', 'score': 95},
        {'id': 2, 'name': 'Bob', 'score': 88},
        {'id': 3, 'name': 'Charlie', 'score': 92}
    ]
    with open(sample_df_json_path, 'w') as f:
        # For pd.read_json to easily parse as a table, often it's a JSON array of records.
        json.dump(df_data_list, f) # Not indented, more compact for pd.read_json
    main_logger.info(f"Created DataFrame-like JSON (list of records): {sample_df_json_path}")

    # Dict-like JSON (nested object) - suitable for json.load()
    obj_data = {
        'project': 'DataNinja', 'version': 1.0,
        'settings': {'isActive': True, 'parameters': [10, 20, 30]},
        'files': ['file1.txt', 'file2.csv']
    }
    with open(sample_obj_json_path, 'w') as f:
        json.dump(obj_data, f, indent=4)
    main_logger.info(f"Created dict-like JSON: {sample_obj_json_path}")

    # Malformed JSON
    with open(malformed_json_path, 'w') as f:
        f.write('{"name": "test", "value": 123,}') # Trailing comma, but valid JSON for json.load with Python 3.9+
                                                 # For pd.read_json this might be an issue.
                                                 # Let's make it more clearly malformed for json.load too.
    with open(malformed_json_path, 'w') as f:
        f.write('{"name": "test" "value": 123}') # Missing comma between key-value pairs
    main_logger.info(f"Created malformed JSON: {malformed_json_path}")


    # --- Test load_data ---
    main_logger.info("\n--- Testing load_data (DataFrame-like JSON) ---")
    handler_df_json = JSONHandler(source=sample_df_json_path)
    try:
        # Explicitly pass orient='records' if that's the expected format
        loaded_data_df = handler_df_json.load_data(orient='records')
        main_logger.info(f"Loaded data type: {type(loaded_data_df)}")
        if isinstance(loaded_data_df, pd.DataFrame):
            main_logger.info("Loaded DataFrame content:")
            print(loaded_data_df)
        else:
            main_logger.info(f"Loaded data: {loaded_data_df}")
    except Exception as e:
        main_logger.error(f"Error loading DataFrame-like JSON: {e}", exc_info=True)

    main_logger.info("\n--- Testing load_data (Dict-like JSON, should use json.load fallback) ---")
    handler_obj_json = JSONHandler(source=sample_obj_json_path)
    try:
        # pd.read_json would fail or produce undesired structure for typical nested JSON object.
        # The load_data method should catch ValueError from pd.read_json and fall back to json.load.
        loaded_data_obj = handler_obj_json.load_data()
        main_logger.info(f"Loaded data type: {type(loaded_data_obj)}")
        main_logger.info(f"Loaded data content: {loaded_data_obj}")
        assert isinstance(loaded_data_obj, dict), "Data should be a dict"
        assert loaded_data_obj['project'] == 'DataNinja', "Incorrect data loaded"
    except Exception as e:
        main_logger.error(f"Error loading dict-like JSON: {e}", exc_info=True)

    main_logger.info("\n--- Testing load_data (Non-existent file) ---")
    handler_non_existent = JSONHandler(source=os.path.join(temp_dir, 'non_existent.json'))
    try:
        handler_non_existent.load_data()
    except FileNotFoundError as e:
        main_logger.error(f"Caught expected FileNotFoundError: {e}")
    except Exception as e:
        main_logger.error(f"Caught unexpected error for non-existent file: {e}", exc_info=True)

    main_logger.info("\n--- Testing load_data (Malformed JSON) ---")
    handler_malformed = JSONHandler(source=malformed_json_path)
    try:
        handler_malformed.load_data()
    except json.JSONDecodeError as e: # Expecting this from the json.load fallback
        main_logger.error(f"Caught expected JSONDecodeError for malformed JSON: {e}")
    except ValueError as e: # Or ValueError from pandas if it doesn't fallback for some reason
        main_logger.error(f"Caught ValueError for malformed JSON (possibly from pandas): {e}")
    except Exception as e:
        main_logger.error(f"Caught unexpected error for malformed JSON: {e}", exc_info=True)


    # --- Test save_data ---
    df_to_save = pd.DataFrame({
        'item': ['apple', 'banana', 'cherry'], 'price': [1.0, 0.5, 2.0], 'quantity': [100, 150, 75]
    })
    dict_to_save = {
        'user': 'test_user', 'permissions': {'read': True, 'write': False},
        'history': [{'action': 'login', 'timestamp': '2023-01-01T12:00:00Z'}]
    }

    # Using a generic handler instance for saving operations
    # Source is not strictly needed if DataLoader.__init__ allows None or if we only call save_data
    # For safety, provide a dummy source or ensure DataLoader handles it.
    # Let's assume DataLoader's __init__ requires a source, so provide a dummy one.
    generic_handler = JSONHandler(source="dummy_source_for_saving.json")


    main_logger.info("\n--- Testing save_data (DataFrame to JSONL - orient='records', lines=True) ---")
    try:
        # Explicitly using orient='records', lines=True which are defaults in save_data for DataFrame
        generic_handler.save_data(df_to_save, target_path=output_df_jsonl_path, orient='records', lines=True)
        main_logger.info(f"DataFrame saved to JSONL: {output_df_jsonl_path}")
        if os.path.exists(output_df_jsonl_path):
            main_logger.info(f"Verified: {output_df_jsonl_path} exists. First line:")
            with open(output_df_jsonl_path, 'r') as f: print(f.readline().strip())
    except Exception as e:
        main_logger.error(f"Error saving DataFrame to JSONL: {e}", exc_info=True)

    main_logger.info("\n--- Testing save_data (DataFrame to standard JSON - orient='table', indent=4) ---")
    try:
        generic_handler.save_data(df_to_save, target_path=output_df_json_path, orient='table', indent=4, lines=False)
        main_logger.info(f"DataFrame saved to standard JSON: {output_df_json_path}")
        if os.path.exists(output_df_json_path):
            main_logger.info(f"Verified: {output_df_json_path} exists. First 100 chars:")
            with open(output_df_json_path, 'r') as f: print(f.read(100) + "...")
    except Exception as e:
        main_logger.error(f"Error saving DataFrame to standard JSON: {e}", exc_info=True)

    main_logger.info("\n--- Testing save_data (Dict to JSON - indent=4) ---")
    try:
        generic_handler.save_data(dict_to_save, target_path=output_dict_json_path) # Uses default indent=4
        main_logger.info(f"Dict saved to JSON: {output_dict_json_path}")
        if os.path.exists(output_dict_json_path):
            main_logger.info(f"Verified: {output_dict_json_path} exists. First 100 chars:")
            with open(output_dict_json_path, 'r') as f: print(f.read(100) + "...")
    except Exception as e:
        main_logger.error(f"Error saving dict to JSON: {e}", exc_info=True)

    main_logger.info("\n--- Testing save_data (Missing target_path) ---")
    try:
        generic_handler.save_data(df_to_save) # No target_path
    except ValueError as e:
        main_logger.error(f"Caught expected ValueError: {e}")
    except Exception as e:
        main_logger.error(f"Caught unexpected error (missing target_path): {e}", exc_info=True)

    main_logger.info("\n--- Testing save_data (Unsupported data type) ---")
    try:
        generic_handler.save_data(set([1,2,3]), target_path=os.path.join(temp_dir,"unsupported.json"))
    except TypeError as e:
        main_logger.error(f"Caught expected TypeError: {e}")
    except Exception as e:
        main_logger.error(f"Caught unexpected error (unsupported type): {e}", exc_info=True)

    # Clean up
    main_logger.info("\n--- Cleaning up test files ---")
    try:
        paths_to_remove = [
            sample_df_json_path, sample_obj_json_path, malformed_json_path,
            output_df_jsonl_path, output_df_json_path, output_dict_json_path,
            os.path.join(temp_dir, "unsupported.json")
        ]
        for p in paths_to_remove:
            if os.path.exists(p):
                os.remove(p)
                main_logger.debug(f"Removed file: {p}")

        if os.path.exists(temp_dir) and not os.listdir(temp_dir): # Check if dir is empty
            os.rmdir(temp_dir)
            main_logger.info(f"Removed directory: {temp_dir}")
        elif os.path.exists(temp_dir):
            main_logger.warning(f"Directory {temp_dir} not removed (possibly not empty or other issue).")

    except Exception as e:
        main_logger.error(f"Error during cleanup: {e}", exc_info=True)

    main_logger.info("\n--- JSONHandler tests finished ---")
