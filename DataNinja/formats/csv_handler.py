import os
import pandas as pd
import logging

# Configure basic logging for the module
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Adjust the import path based on your project structure
# If DataNinja is a package and core is a submodule:
from ..core.loader import DataLoader

# If DataNinja is in PYTHONPATH and you run scripts from outside DataNinja:
# from DataNinja.core.loader import DataLoader


class CSVHandler(DataLoader):
    def __init__(self, source):
        super().__init__(source)
        # Add a logger specific to this class instance if desired, or use module logger
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        self.logger.info(f"CSVHandler initialized for source: {source}")

    def load_data(self, **kwargs):
        self.logger.info(f"Attempting to load CSV data from {self.source}")
        if not os.path.exists(self.source):
            self.logger.error(f"File not found: {self.source}")
            raise FileNotFoundError(f"File not found: {self.source}")

        try:
            df = pd.read_csv(self.source, **kwargs)
            self.logger.info(
                f"Successfully loaded CSV data from {self.source}. Shape: {df.shape}"
            )
            return df
        except pd.errors.EmptyDataError:
            self.logger.error(f"No data in CSV file: {self.source}")
            # Return an empty DataFrame or re-raise, depending on desired behavior
            return pd.DataFrame()  # Or raise
        except pd.errors.ParserError as e:
            self.logger.error(f"Error parsing CSV file: {self.source} - {e}")
            raise  # Re-raise the parser error
        except Exception as e:
            self.logger.error(
                f"An unexpected error occurred while loading {self.source}: {e}"
            )
            raise  # Re-raise the caught exception

    def save_data(self, data, target_path=None, **kwargs):
        if target_path is None:
            self.logger.error("Target path for saving data is required.")
            raise ValueError("Target path for saving data is required.")

        self.logger.info(f"Attempting to save data to {target_path}")

        if not isinstance(data, pd.DataFrame):
            self.logger.error("Invalid data type. Data must be a pandas DataFrame.")
            raise ValueError("Invalid data type. Data must be a pandas DataFrame.")

        try:
            # Ensure the directory for the target path exists
            target_dir = os.path.dirname(target_path)
            if target_dir and not os.path.exists(target_dir):
                os.makedirs(target_dir)
                self.logger.info(f"Created directory: {target_dir}")

            data.to_csv(
                target_path, index=False, **kwargs
            )  # index=False is a common default
            self.logger.info(f"Successfully saved data to {target_path}")
        except IOError as e:
            self.logger.error(
                f"IOError occurred while saving data to {target_path}: {e}"
            )
            raise
        except Exception as e:
            self.logger.error(
                f"An unexpected error occurred while saving data to {target_path}: {e}"
            )
            raise


if __name__ == "__main__":
    # Setup basic logging for the __main__ block execution
    # This will configure the root logger, which is fine for a simple script.
    # For more complex applications, you might want to configure loggers more granularly.
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    main_logger = logging.getLogger(
        __name__
    )  # Gets a logger named after the current module

    # Example usage:

    # 0. Define paths for dummy files
    # Place dummy files in a temporary directory to keep the root clean
    temp_dir = "temp_test_data"
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
        main_logger.info(f"Created temporary directory: {temp_dir}")

    sample_csv_path = os.path.join(temp_dir, "sample_data.csv")
    output_csv_path = os.path.join(temp_dir, "output_data.csv")
    empty_csv_path = os.path.join(temp_dir, "empty_data.csv")
    malformed_csv_path = os.path.join(temp_dir, "malformed_data.csv")

    # 1. Create a dummy CSV file for testing load_data
    sample_df_to_create = pd.DataFrame(
        {
            "col1": [1, 2, 3, 4],
            "col2": ["a", "b", "c", "d"],
            "col3": [1.1, 2.2, 3.3, 4.4],
        }
    )
    sample_df_to_create.to_csv(sample_csv_path, index=False)
    main_logger.info(f"Created dummy CSV: {sample_csv_path}")

    # Create an empty CSV for testing EmptyDataError
    with open(empty_csv_path, "w") as f:
        pass  # Just create an empty file
    main_logger.info(f"Created empty CSV: {empty_csv_path}")

    # Create a malformed CSV for testing ParserError
    with open(malformed_csv_path, "w") as f:
        f.write("col1,col2\n1,two,extra\n3,four")
    main_logger.info(f"Created malformed CSV: {malformed_csv_path}")

    # Instantiate CSVHandler
    csv_handler_valid = CSVHandler(source=sample_csv_path)

    # Test load_data (valid case)
    main_logger.info("\n--- Testing load_data (valid file) ---")
    try:
        loaded_df = csv_handler_valid.load_data(sep=",")  # Example of passing kwargs
        if loaded_df is not None:
            main_logger.info("Loaded DataFrame head:")
            print(loaded_df.head())  # print for direct output
    except Exception as e:
        main_logger.error(f"An error occurred during loading: {e}", exc_info=True)

    # Test load_data with a non-existent file
    main_logger.info("\n--- Testing load_data (non-existent file) ---")
    non_existent_handler = CSVHandler(source=os.path.join(temp_dir, "non_existent.csv"))
    try:
        non_existent_handler.load_data()
    except FileNotFoundError as e:
        main_logger.error(f"Caught expected error: {e}")
    except Exception as e:
        main_logger.error(f"Caught unexpected error: {e}", exc_info=True)

    # Test load_data with an empty file
    main_logger.info("\n--- Testing load_data (empty file) ---")
    empty_handler = CSVHandler(source=empty_csv_path)
    try:
        empty_df = empty_handler.load_data()
        main_logger.info(
            f"Loaded DataFrame from empty file. Is empty: {empty_df.empty}. Shape: {empty_df.shape}"
        )
        print(empty_df)
    except Exception as e:
        main_logger.error(f"Error loading empty CSV: {e}", exc_info=True)

    # Test load_data with a malformed file
    main_logger.info("\n--- Testing load_data (malformed file) ---")
    malformed_handler = CSVHandler(source=malformed_csv_path)
    try:
        malformed_handler.load_data()
    except pd.errors.ParserError as e:
        main_logger.error(f"Caught expected ParserError: {e}")
    except Exception as e:
        main_logger.error(f"Caught unexpected error: {e}", exc_info=True)

    # 2. Create a sample DataFrame for testing save_data
    data_to_save = pd.DataFrame(
        {
            "id": [101, 102, 103, 104],
            "name": ["Alice Smith", "Bob Johnson", "Charlie Brown", "David Wilson"],
            "score": [85.5, 90.0, 78.2, 92.1],
        }
    )

    # Test save_data (valid case)
    main_logger.info("\n--- Testing save_data (valid case) ---")
    try:
        # Use the handler for the original sample file, but save to a new target
        csv_handler_valid.save_data(data_to_save, target_path=output_csv_path)
        main_logger.info(f"Data saved to {output_csv_path}")
        if os.path.exists(output_csv_path):
            main_logger.info(f"Verified: {output_csv_path} exists.")
            verify_df = pd.read_csv(output_csv_path)
            main_logger.info("Verified data head:")
            print(verify_df.head())
        else:
            main_logger.error(f"Verification failed: {output_csv_path} does not exist.")
    except Exception as e:
        main_logger.error(f"An error occurred during saving: {e}", exc_info=True)

    # Test save_data with invalid data type
    main_logger.info("\n--- Testing save_data (invalid data type) ---")
    try:
        csv_handler_valid.save_data(
            [1, 2, 3, "not a DataFrame"],
            target_path=os.path.join(temp_dir, "invalid_output.csv"),
        )
    except ValueError as e:
        main_logger.error(f"Caught expected ValueError: {e}")
    except Exception as e:
        main_logger.error(f"Caught unexpected error: {e}", exc_info=True)

    # Test save_data without target_path
    main_logger.info("\n--- Testing save_data (without target_path) ---")
    try:
        csv_handler_valid.save_data(data_to_save)  # No target_path
    except ValueError as e:
        main_logger.error(f"Caught expected ValueError: {e}")
    except Exception as e:
        main_logger.error(f"Caught unexpected error: {e}", exc_info=True)

    # Clean up created files and directory
    main_logger.info("\n--- Cleaning up test files ---")
    try:
        if os.path.exists(sample_csv_path):
            os.remove(sample_csv_path)
            main_logger.info(f"Cleaned up: removed {sample_csv_path}")
        if os.path.exists(output_csv_path):
            os.remove(output_csv_path)
            main_logger.info(f"Cleaned up: removed {output_csv_path}")
        if os.path.exists(empty_csv_path):
            os.remove(empty_csv_path)
            main_logger.info(f"Cleaned up: removed {empty_csv_path}")
        if os.path.exists(malformed_csv_path):
            os.remove(malformed_csv_path)
            main_logger.info(f"Cleaned up: removed {malformed_csv_path}")

        # Remove the temporary directory if it's empty
        if os.path.exists(temp_dir) and not os.listdir(temp_dir):
            os.rmdir(temp_dir)
            main_logger.info(f"Cleaned up: removed directory {temp_dir}")
        elif os.path.exists(temp_dir):
            main_logger.warning(
                f"Directory {temp_dir} not empty, did not remove. Check for leftover files."
            )

    except Exception as e:
        main_logger.error(f"Error during cleanup: {e}", exc_info=True)

    main_logger.info("\n--- CSVHandler tests finished ---")
