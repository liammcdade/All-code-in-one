import os
import pandas as pd
import logging

# Assuming DataLoader is in ../core/loader.py
from ..core.loader import DataLoader

# from ..core.utils import setup_logging # If you have a centralized logging setup

# Basic module-level logger configuration
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


class ExcelHandler(DataLoader):
    def __init__(self, source):
        super().__init__(source)
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        self.logger.info(f"ExcelHandler initialized for source: {self.source}")

    def load_data(self, sheet_name=0, **kwargs):
        self.logger.info(
            f"Attempting to load Excel data from {self.source}, sheet_name: '{sheet_name}'"
        )
        if not self.source:
            self.logger.error("Source path is None or empty, cannot load data.")
            raise ValueError("Source path is None or empty.")
        if not os.path.exists(self.source):
            self.logger.error(f"File not found: {self.source}")
            raise FileNotFoundError(f"File not found: {self.source}")

        try:
            # sheet_name=None loads all sheets
            # sheet_name=0 loads the first sheet
            # sheet_name="SheetName" loads a specific sheet
            data = pd.read_excel(
                self.source, sheet_name=sheet_name, engine="openpyxl", **kwargs
            )

            if isinstance(data, dict):  # Loaded all sheets
                self.logger.info(
                    f"Successfully loaded all sheets from {self.source}. Sheet names: {list(data.keys())}"
                )
                for sheet, df in data.items():
                    self.logger.debug(f"Sheet: '{sheet}', Shape: {df.shape}")
            else:  # Loaded a single sheet
                self.logger.info(
                    f"Successfully loaded sheet '{sheet_name}' from {self.source}. Shape: {data.shape}"
                )
            return data
        except (
            FileNotFoundError
        ):  # Should be caught by os.path.exists, but as a safeguard
            self.logger.error(f"File not found (pd.read_excel): {self.source}")
            raise
        except (
            ValueError
        ) as ve:  # Handles incorrect sheet names, or other pandas value errors
            self.logger.error(
                f"ValueError loading Excel file {self.source} (sheet_name: {sheet_name}): {ve}"
            )
            raise
        except (
            Exception
        ) as e:  # Catch other potential errors (e.g., openpyxl specific, corrupted file)
            # xlrd.biffh.XLRDError might occur if trying to load .xls with openpyxl engine (which is for .xlsx)
            # For openpyxl, errors might be more generic or specific like zipfile.BadZipFile for corrupted .xlsx
            self.logger.error(
                f"An unexpected error occurred while loading {self.source} (sheet_name: {sheet_name}): {e}"
            )
            raise

    def save_data(self, data, target_path=None, sheet_name="Sheet1", **kwargs):
        if target_path is None:
            self.logger.error("Target path for saving Excel data is required.")
            raise ValueError("Target path for saving Excel data is required.")

        self.logger.info(f"Attempting to save data to Excel file: {target_path}")

        target_dir = os.path.dirname(target_path)
        if target_dir:
            os.makedirs(target_dir, exist_ok=True)
            self.logger.debug(f"Ensured directory exists: {target_dir}")

        # Default index=False unless specified in kwargs
        index = kwargs.pop("index", False)

        try:
            if isinstance(data, pd.DataFrame):
                data.to_excel(
                    target_path,
                    sheet_name=sheet_name,
                    index=index,
                    engine="openpyxl",
                    **kwargs,
                )
                self.logger.info(
                    f"Successfully saved single DataFrame to {target_path} in sheet '{sheet_name}'"
                )
            elif isinstance(data, dict):
                # Ensure all values in dict are DataFrames
                if not all(isinstance(df, pd.DataFrame) for df in data.values()):
                    self.logger.error(
                        "If data is a dict, all its values must be pandas DataFrames."
                    )
                    raise TypeError(
                        "If data is a dict, all its values must be pandas DataFrames."
                    )

                with pd.ExcelWriter(target_path, engine="openpyxl") as writer:
                    for sheet, df in data.items():
                        df.to_excel(writer, sheet_name=sheet, index=index, **kwargs)
                self.logger.info(
                    f"Successfully saved dictionary of DataFrames to {target_path}. Sheets: {list(data.keys())}"
                )
            else:
                self.logger.error(
                    f"Unsupported data type: {type(data)}. Must be a pandas DataFrame or a dictionary of DataFrames."
                )
                raise TypeError(
                    "Data must be a pandas DataFrame or a dictionary of DataFrames."
                )
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
    main_logger = logging.getLogger(__name__)
    if not main_logger.handlers or not logging.getLogger().handlers:
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            force=True,
        )
    main_logger.setLevel(logging.DEBUG)

    temp_dir = "temp_excel_test_data"
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
        main_logger.info(f"Created temporary directory: {temp_dir}")

    sample_excel_path = os.path.join(temp_dir, "sample_data.xlsx")
    output_single_sheet_path = os.path.join(temp_dir, "output_single_sheet.xlsx")
    output_multi_sheet_path = os.path.join(temp_dir, "output_multiple_sheets.xlsx")

    # 1. Create a dummy Excel file for testing load_data
    df1_to_create = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
    df2_to_create = pd.DataFrame({"X": [5, 6, 7], "Y": [8, 9, 10]})

    try:
        with pd.ExcelWriter(sample_excel_path, engine="openpyxl") as writer:
            df1_to_create.to_excel(writer, sheet_name="SheetAlpha", index=False)
            df2_to_create.to_excel(writer, sheet_name="SheetBeta", index=False)
        main_logger.info(
            f"Created dummy Excel file: {sample_excel_path} with sheets: SheetAlpha, SheetBeta"
        )
    except Exception as e:
        main_logger.error(f"Could not create dummy excel: {e}", exc_info=True)
        # If openpyxl is not installed, this will fail. We should ensure it is.
        # For now, proceed assuming it might be handled by later bash command.

    # --- Test load_data ---
    main_logger.info("\n--- Testing load_data (Specific Sheet 'SheetAlpha') ---")
    handler_load = ExcelHandler(source=sample_excel_path)
    try:
        loaded_df_alpha = handler_load.load_data(sheet_name="SheetAlpha")
        main_logger.info(f"Loaded 'SheetAlpha' data type: {type(loaded_df_alpha)}")
        if isinstance(loaded_df_alpha, pd.DataFrame):
            main_logger.info("Loaded 'SheetAlpha' content:")
            print(loaded_df_alpha)
    except Exception as e:
        main_logger.error(f"Error loading 'SheetAlpha': {e}", exc_info=True)

    main_logger.info("\n--- Testing load_data (First sheet by index 0) ---")
    try:
        loaded_df_first = handler_load.load_data(sheet_name=0)  # First sheet
        main_logger.info(
            f"Loaded first sheet (index 0) data type: {type(loaded_df_first)}"
        )
        if isinstance(loaded_df_first, pd.DataFrame):
            main_logger.info("Loaded first sheet content:")
            print(loaded_df_first)
            # Basic check, content should match df1_to_create
            pd.testing.assert_frame_equal(loaded_df_first, df1_to_create)

    except Exception as e:
        main_logger.error(f"Error loading first sheet by index: {e}", exc_info=True)

    main_logger.info("\n--- Testing load_data (All sheets: sheet_name=None) ---")
    try:
        loaded_all_sheets = handler_load.load_data(sheet_name=None)
        main_logger.info(f"Loaded all sheets. Data type: {type(loaded_all_sheets)}")
        if isinstance(loaded_all_sheets, dict):
            main_logger.info(f"Sheet names: {list(loaded_all_sheets.keys())}")
            for sheet_name, df_content in loaded_all_sheets.items():
                main_logger.info(f"Content of sheet '{sheet_name}':")
                print(df_content)
            # Basic check for content
            pd.testing.assert_frame_equal(
                loaded_all_sheets["SheetAlpha"], df1_to_create
            )
            pd.testing.assert_frame_equal(loaded_all_sheets["SheetBeta"], df2_to_create)

    except Exception as e:
        main_logger.error(f"Error loading all sheets: {e}", exc_info=True)

    main_logger.info("\n--- Testing load_data (Non-existent sheet name) ---")
    try:
        handler_load.load_data(sheet_name="NonExistentSheet")
    except (
        ValueError
    ) as e:  # openpyxl/pandas typically raises ValueError for non-existent sheet
        main_logger.error(f"Caught expected ValueError for non-existent sheet: {e}")
    except KeyError as e:  # Alternative if specific pandas version raises KeyError
        main_logger.error(f"Caught expected KeyError for non-existent sheet: {e}")
    except Exception as e:
        main_logger.error(
            f"Caught unexpected error for non-existent sheet: {e}", exc_info=True
        )

    main_logger.info("\n--- Testing load_data (Non-existent file) ---")
    handler_non_existent_file = ExcelHandler(
        source=os.path.join(temp_dir, "non_existent.xlsx")
    )
    try:
        handler_non_existent_file.load_data()
    except FileNotFoundError as e:
        main_logger.error(f"Caught expected FileNotFoundError: {e}")
    except Exception as e:
        main_logger.error(
            f"Caught unexpected error for non-existent file: {e}", exc_info=True
        )

    # --- Test save_data ---
    df_single_save = pd.DataFrame(
        {"Name": ["ProductA", "ProductB"], "Price": [100, 150]}
    )
    dict_multi_save = {
        "Sales": pd.DataFrame({"Rep": ["John", "Jane"], "Amount": [1000, 2000]}),
        "Inventory": pd.DataFrame({"Item": ["XPS13", "MacBookPro"], "Stock": [50, 30]}),
    }

    # Generic handler for saving
    handler_save = ExcelHandler(
        source="dummy_source_for_saving.xlsx"
    )  # Source not used for saving with target_path

    main_logger.info("\n--- Testing save_data (Single DataFrame to new file) ---")
    try:
        handler_save.save_data(
            df_single_save, target_path=output_single_sheet_path, sheet_name="Products"
        )
        main_logger.info(f"Single DataFrame saved to {output_single_sheet_path}")
        if os.path.exists(output_single_sheet_path):
            main_logger.info(f"Verified: {output_single_sheet_path} exists.")
            # Verify content by reloading
            reloaded_single = pd.read_excel(
                output_single_sheet_path, sheet_name="Products", engine="openpyxl"
            )
            pd.testing.assert_frame_equal(reloaded_single, df_single_save)
            main_logger.info("Content verified by reloading.")
    except Exception as e:
        main_logger.error(f"Error saving single DataFrame: {e}", exc_info=True)

    main_logger.info(
        "\n--- Testing save_data (Dictionary of DataFrames to new file) ---"
    )
    try:
        handler_save.save_data(dict_multi_save, target_path=output_multi_sheet_path)
        main_logger.info(f"Dictionary of DataFrames saved to {output_multi_sheet_path}")
        if os.path.exists(output_multi_sheet_path):
            main_logger.info(f"Verified: {output_multi_sheet_path} exists.")
            # Verify content by reloading
            reloaded_multi = pd.read_excel(
                output_multi_sheet_path, sheet_name=None, engine="openpyxl"
            )
            assert "Sales" in reloaded_multi
            assert "Inventory" in reloaded_multi
            pd.testing.assert_frame_equal(
                reloaded_multi["Sales"], dict_multi_save["Sales"]
            )
            pd.testing.assert_frame_equal(
                reloaded_multi["Inventory"], dict_multi_save["Inventory"]
            )
            main_logger.info("Content verified by reloading all sheets.")
    except Exception as e:
        main_logger.error(f"Error saving dictionary of DataFrames: {e}", exc_info=True)

    main_logger.info("\n--- Testing save_data (Missing target_path) ---")
    try:
        handler_save.save_data(df_single_save)
    except ValueError as e:
        main_logger.error(f"Caught expected ValueError for missing target_path: {e}")
    except Exception as e:
        main_logger.error(
            f"Caught unexpected error (missing target_path): {e}", exc_info=True
        )

    main_logger.info("\n--- Testing save_data (Unsupported data type) ---")
    try:
        handler_save.save_data(
            [1, 2, 3], target_path=os.path.join(temp_dir, "unsupported.xlsx")
        )
    except TypeError as e:
        main_logger.error(f"Caught expected TypeError for unsupported data type: {e}")
    except Exception as e:
        main_logger.error(
            f"Caught unexpected error (unsupported type): {e}", exc_info=True
        )

    main_logger.info("\n--- Testing save_data (Dict with non-DataFrame value) ---")
    try:
        bad_dict_data = {
            "Sheet1": pd.DataFrame({"A": [1]}),
            "Sheet2": "not a dataframe",
        }
        handler_save.save_data(
            bad_dict_data, target_path=os.path.join(temp_dir, "bad_dict.xlsx")
        )
    except TypeError as e:
        main_logger.error(f"Caught expected TypeError for dict with non-DataFrame: {e}")
    except Exception as e:
        main_logger.error(
            f"Caught unexpected error (dict with non-DataFrame): {e}", exc_info=True
        )

    # Clean up
    main_logger.info("\n--- Cleaning up test files ---")
    try:
        paths_to_remove = [
            sample_excel_path,
            output_single_sheet_path,
            output_multi_sheet_path,
            os.path.join(temp_dir, "unsupported.xlsx"),
            os.path.join(temp_dir, "bad_dict.xlsx"),
        ]
        for p in paths_to_remove:
            if os.path.exists(p):
                os.remove(p)
                main_logger.debug(f"Removed file: {p}")

        if os.path.exists(temp_dir) and not os.listdir(temp_dir):
            os.rmdir(temp_dir)
            main_logger.info(f"Removed directory: {temp_dir}")
        elif os.path.exists(temp_dir):
            main_logger.warning(
                f"Directory {temp_dir} not removed (possibly not empty or other issue)."
            )
    except Exception as e:
        main_logger.error(f"Error during cleanup: {e}", exc_info=True)

    main_logger.info("\n--- ExcelHandler tests finished ---")
