import os
import sqlite3
import pandas as pd
import logging

# Assuming DataLoader is in ../core/loader.py
from ..core.loader import DataLoader

# from ..core.utils import setup_logging # If you have a centralized logging setup

# Basic module-level logger configuration
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


class SQLiteHandler(DataLoader):
    def __init__(self, source):  # source is the database file path
        super().__init__(source)
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        self.logger.info(f"SQLiteHandler initialized for database: {self.source}")

    def _connect(self, connect_args=None):
        if connect_args is None:
            connect_args = {}
        return sqlite3.connect(self.source, **connect_args)

    def load_data(self, table_name=None, query=None, **kwargs):
        self.logger.info(f"Attempting to load data from SQLite database: {self.source}")

        if not self.source:
            self.logger.error("Database source path is None or empty.")
            raise ValueError("Database source path is None or empty.")

        if table_name is None and query is None:
            self.logger.error(
                "Either 'table_name' or 'query' must be provided to load_data."
            )
            raise ValueError("Either 'table_name' or 'query' must be provided.")
        if table_name and query:
            self.logger.error("Provide either 'table_name' or 'query', not both.")
            raise ValueError("Provide either 'table_name' or 'query', not both.")

        # For loading, the database file should ideally exist.
        # However, sqlite3.connect() will create it if it doesn't.
        # Pandas read_sql_query might not fail on an empty DB with no table.
        # Add an explicit check if strict "must exist" policy is desired.
        # For now, rely on sqlite3/pandas behavior.
        # if not os.path.exists(self.source):
        #     self.logger.error(f"Database file {self.source} not found.")
        #     raise FileNotFoundError(f"Database file {self.source} not found.")

        sql = ""
        if table_name:
            # Basic sanitization for table_name: ensure it's a valid identifier.
            # For robust sanitization, a more comprehensive check or different approach is needed.
            # This is a simple check; complex names with spaces/special chars might need quoting.
            if not table_name.replace("_", "").isalnum():
                self.logger.error(
                    f"Invalid table_name: '{table_name}'. Should be alphanumeric with underscores."
                )
                raise ValueError(f"Invalid table_name: '{table_name}'.")
            sql = f"SELECT * FROM {table_name}"
            self.logger.debug(f"Loading data from table: {table_name} (Query: {sql})")
        elif query:
            sql = query
            self.logger.debug(f"Loading data with custom query: {sql}")

        conn = None
        try:
            connect_args = kwargs.pop("connect_args", {})
            conn = self._connect(connect_args)
            df = pd.read_sql_query(sql, conn, **kwargs)
            self.logger.info(
                f"Successfully loaded data from {self.source}. Shape: {df.shape}"
            )
            return df
        except (
            sqlite3.OperationalError
        ) as e:  # Often indicates table not found, SQL error
            self.logger.error(
                f"SQLite operational error (e.g., table not found, SQL syntax): {e} on query: {sql}"
            )
            raise  # Re-raise as it's a significant issue
        except Exception as e:
            self.logger.error(
                f"An unexpected error occurred while loading data from {self.source}: {e} on query: {sql}"
            )
            raise
        finally:
            if conn:
                conn.close()
                self.logger.debug("SQLite connection closed after loading.")

    def save_data(self, data, table_name, if_exists="fail", index=False, **kwargs):
        self.logger.info(
            f"Attempting to save data to table '{table_name}' in SQLite database: {self.source}"
        )

        if not self.source:
            self.logger.error("Database source path is None or empty.")
            raise ValueError("Database source path is None or empty.")
        if not isinstance(data, pd.DataFrame):
            self.logger.error(
                f"Data to save must be a pandas DataFrame. Got: {type(data)}"
            )
            raise TypeError(
                f"Data to save must be a pandas DataFrame. Got: {type(data)}"
            )
        if not table_name or not isinstance(table_name, str):
            self.logger.error("'table_name' must be provided as a non-empty string.")
            raise ValueError("'table_name' must be provided as a non-empty string.")

        # Ensure the directory for the database file exists
        db_dir = os.path.dirname(self.source)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir)
            self.logger.info(f"Created directory for database file: {db_dir}")

        conn = None
        try:
            connect_args = kwargs.pop("connect_args", {})
            conn = self._connect(connect_args)

            # pandas to_sql handles table creation and data insertion
            data.to_sql(table_name, conn, if_exists=if_exists, index=index, **kwargs)

            self.logger.info(
                f"Successfully saved DataFrame to table '{table_name}' in {self.source} (if_exists='{if_exists}')."
            )
        except (
            ValueError
        ) as ve:  # e.g. if data is empty and table structure cannot be inferred
            self.logger.error(
                f"ValueError during save_data to table '{table_name}': {ve}"
            )
            raise
        except sqlite3.OperationalError as e:
            self.logger.error(
                f"SQLite operational error during save_data to table '{table_name}': {e}"
            )
            raise
        except Exception as e:
            self.logger.error(
                f"An unexpected error occurred while saving data to table '{table_name}' in {self.source}: {e}"
            )
            raise
        finally:
            if conn:
                conn.close()
                self.logger.debug("SQLite connection closed after saving.")


if __name__ == "__main__":
    main_logger = logging.getLogger(__name__)
    if not main_logger.handlers or not logging.getLogger().handlers:
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            force=True,
        )
    main_logger.setLevel(logging.DEBUG)

    temp_dir = "temp_sqlite_test_data"
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
        main_logger.info(f"Created temporary directory: {temp_dir}")

    db_path = os.path.join(temp_dir, "sample_data.db")

    # Instantiate handler
    sqlite_handler = SQLiteHandler(source=db_path)

    # --- Test save_data first ---
    df_to_save1 = pd.DataFrame(
        {"id": [1, 2], "name": ["Alice", "Bob"], "value": [10.1, 20.2]}
    )
    df_to_save2 = pd.DataFrame(
        {"id": [3, 4], "name": ["Charlie", "David"], "value": [30.3, 40.4]}
    )
    df_to_save3 = pd.DataFrame(
        {"id": [5, 6], "name": ["Eve", "Frank"], "value": [50.5, 60.6]}
    )

    main_logger.info("\n--- Testing save_data (if_exists='fail' - first time) ---")
    try:
        sqlite_handler.save_data(df_to_save1, table_name="test_table", if_exists="fail")
        main_logger.info("Save 'fail' (1st time) successful.")
    except Exception as e:
        main_logger.error(f"Error in save 'fail' (1st time): {e}", exc_info=True)

    main_logger.info(
        "\n--- Testing save_data (if_exists='fail' - second time, expect error) ---"
    )
    try:
        sqlite_handler.save_data(df_to_save1, table_name="test_table", if_exists="fail")
    except (
        ValueError
    ) as e:  # pandas to_sql raises ValueError if table exists and if_exists='fail'
        main_logger.info(f"Caught expected ValueError for save 'fail' (2nd time): {e}")
    except Exception as e:
        main_logger.error(
            f"Caught unexpected error for save 'fail' (2nd time): {e}", exc_info=True
        )

    main_logger.info("\n--- Testing save_data (if_exists='replace') ---")
    try:
        sqlite_handler.save_data(
            df_to_save2, table_name="test_table", if_exists="replace"
        )
        main_logger.info("Save 'replace' successful.")
        # Verify content after replace
        df_after_replace = sqlite_handler.load_data(table_name="test_table")
        assert len(df_after_replace) == len(
            df_to_save2
        ), "Length mismatch after replace"
        assert (
            df_after_replace["name"].iloc[0] == "Charlie"
        ), "Content mismatch after replace"
        main_logger.info(
            f"Loaded after replace (len {len(df_after_replace)}): Head:\n{df_after_replace.head()}"
        )
    except Exception as e:
        main_logger.error(f"Error in save 'replace': {e}", exc_info=True)

    main_logger.info("\n--- Testing save_data (if_exists='append') ---")
    try:
        sqlite_handler.save_data(
            df_to_save3, table_name="test_table", if_exists="append"
        )
        main_logger.info("Save 'append' successful.")
        # Verify content after append
        df_after_append = sqlite_handler.load_data(table_name="test_table")
        expected_len = len(df_to_save2) + len(df_to_save3)
        assert len(df_after_append) == expected_len, "Length mismatch after append"
        main_logger.info(
            f"Loaded after append (len {len(df_after_append)}): Head:\n{df_after_append.head()}"
        )
        main_logger.info(f"Tail after append:\n{df_after_append.tail()}")

    except Exception as e:
        main_logger.error(f"Error in save 'append': {e}", exc_info=True)

    # --- Test load_data ---
    main_logger.info("\n--- Testing load_data (table_name='test_table') ---")
    try:
        loaded_df_table = sqlite_handler.load_data(table_name="test_table")
        main_logger.info(f"Loaded from 'test_table'. Shape: {loaded_df_table.shape}")
        main_logger.info("Content from 'test_table':")
        print(loaded_df_table)
    except Exception as e:
        main_logger.error(f"Error loading from 'test_table': {e}", exc_info=True)

    main_logger.info("\n--- Testing load_data (query) ---")
    try:
        query = "SELECT * FROM test_table WHERE value > 35"
        loaded_df_query = sqlite_handler.load_data(query=query)
        main_logger.info(f"Loaded from query '{query}'. Shape: {loaded_df_query.shape}")
        main_logger.info(f"Content from query (value > 35):")
        print(loaded_df_query)
        assert all(loaded_df_query["value"] > 35), "Query condition not met"
    except Exception as e:
        main_logger.error(f"Error loading from query: {e}", exc_info=True)

    main_logger.info("\n--- Testing load_data (non-existent table) ---")
    try:
        sqlite_handler.load_data(table_name="non_existent_table")
    except (
        sqlite3.OperationalError,
        pd.errors.DatabaseError,
    ) as e:  # Pandas may wrap sqlite3.OperationalError
        main_logger.info(f"Caught expected error for non-existent table: {e}")
    except Exception as e:
        main_logger.error(
            f"Caught unexpected error for non-existent table: {e}", exc_info=True
        )

    main_logger.info("\n--- Testing load_data (invalid query) ---")
    try:
        sqlite_handler.load_data(
            query="SELECT FROM table_that_does_not_matter"
        )  # Invalid SQL
    except (
        sqlite3.OperationalError,
        pd.errors.DatabaseError,
    ) as e:  # Pandas may wrap sqlite3.OperationalError
        main_logger.info(f"Caught expected error for invalid query: {e}")
    except Exception as e:
        main_logger.error(
            f"Caught unexpected error for invalid query: {e}", exc_info=True
        )

    main_logger.info("\n--- Testing load_data (no table_name or query) ---")
    try:
        sqlite_handler.load_data()
    except ValueError as e:
        main_logger.error(f"Caught expected ValueError: {e}")
    except Exception as e:
        main_logger.error(f"Caught unexpected error: {e}", exc_info=True)

    main_logger.info("\n--- Testing load_data (both table_name and query) ---")
    try:
        sqlite_handler.load_data(
            table_name="test_table", query="SELECT * FROM test_table"
        )
    except ValueError as e:
        main_logger.error(f"Caught expected ValueError: {e}")
    except Exception as e:
        main_logger.error(f"Caught unexpected error: {e}", exc_info=True)

    # --- Test error conditions for save_data ---
    main_logger.info("\n--- Testing save_data (non-DataFrame input) ---")
    try:
        sqlite_handler.save_data([1, 2, 3], table_name="bad_input_table")
    except TypeError as e:
        main_logger.error(f"Caught expected TypeError: {e}")
    except Exception as e:
        main_logger.error(f"Caught unexpected error: {e}", exc_info=True)

    main_logger.info("\n--- Testing save_data (no table_name) ---")
    try:
        sqlite_handler.save_data(df_to_save1, table_name=None)
    except ValueError as e:
        main_logger.error(f"Caught expected ValueError: {e}")
    except Exception as e:
        main_logger.error(f"Caught unexpected error: {e}", exc_info=True)

    main_logger.info("\n--- Testing save_data (empty DataFrame, if_exists='fail') ---")
    empty_df = pd.DataFrame(
        {"colA": pd.Series(dtype="int"), "colB": pd.Series(dtype="str")}
    )
    try:
        sqlite_handler.save_data(
            empty_df, table_name="empty_table_test", if_exists="fail"
        )
        # Pandas to_sql with an empty DataFrame and no existing table might raise a ValueError
        # because it cannot determine the schema. If the table exists, it might append nothing.
        main_logger.info("Saving empty DataFrame (fail) completed.")
        # Check if table was created (it might be, without data)
        empty_table_df = sqlite_handler.load_data(table_name="empty_table_test")
        assert empty_table_df.empty, "Empty table should be empty"
        main_logger.info(
            f"Loaded 'empty_table_test' (should be empty). Shape: {empty_table_df.shape}"
        )

    except ValueError as e:  # This is expected if table cannot be created from empty DF
        main_logger.error(f"Caught expected ValueError for empty DataFrame: {e}")
    except Exception as e:
        main_logger.error(f"Error saving empty DataFrame: {e}", exc_info=True)

    # Clean up
    main_logger.info("\n--- Cleaning up test files ---")
    try:
        if os.path.exists(db_path):
            os.remove(db_path)
            main_logger.info(f"Removed database file: {db_path}")

        if os.path.exists(temp_dir) and not os.listdir(temp_dir):
            os.rmdir(temp_dir)
            main_logger.info(f"Removed directory: {temp_dir}")
        elif os.path.exists(temp_dir):
            main_logger.warning(
                f"Directory {temp_dir} not removed (possibly not empty or other issue)."
            )

    except Exception as e:
        main_logger.error(f"Error during cleanup: {e}", exc_info=True)

    main_logger.info("\n--- SQLiteHandler tests finished ---")
