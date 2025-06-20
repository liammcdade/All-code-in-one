import logging
import sqlite3
import pandas as pd

# from ..core.utils import setup_logging # If a centralized logging setup is used

# Basic module-level logger configuration
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


class SQLProcessor:
    def __init__(self, db_connection_string=None, db_type="sqlite"):
        """
        Initializes the SQLProcessor.

        Args:
            db_connection_string (str, optional): Database connection string.
                                                 For SQLite, this is the file path or ':memory:'.
            db_type (str, optional): Type of the database. Defaults to 'sqlite'.
        """
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        self.db_connection_string = db_connection_string
        self.db_type = db_type.lower()
        self.connection = None
        self.logger.info(
            f"SQLProcessor initialized. DB Type: '{self.db_type}', Connection String: '{self.db_connection_string}'"
        )

    def connect(self):
        """Establishes a connection to the database."""
        if self.connection:
            self.logger.info("Connection already established.")
            return

        self.logger.info(
            f"Attempting to connect to {self.db_type} database: {self.db_connection_string}"
        )
        if not self.db_connection_string:
            self.logger.error("Database connection string is not set.")
            raise ValueError("Database connection string must be provided.")

        if self.db_type == "sqlite":
            try:
                self.connection = sqlite3.connect(self.db_connection_string)
                self.logger.info("Successfully connected to SQLite database.")
            except sqlite3.Error as e:
                self.logger.error(f"Error connecting to SQLite database: {e}")
                self.connection = None  # Ensure connection is None on failure
                raise
        else:
            self.logger.warning(
                f"Database type '{self.db_type}' is not yet supported. Only 'sqlite' is available."
            )
            raise NotImplementedError(f"Database type '{self.db_type}' not supported.")

    def disconnect(self):
        """Closes the database connection."""
        if self.connection:
            self.logger.info(f"Attempting to disconnect from {self.db_type} database.")
            try:
                self.connection.close()
                self.logger.info("Successfully disconnected.")
            except sqlite3.Error as e:
                self.logger.error(f"Error disconnecting from database: {e}")
                raise
            finally:
                self.connection = None
        else:
            self.logger.info("No active connection to disconnect.")

    def execute_query(self, query: str, params=None, fetch_results=True):
        """
        Executes a SQL query.

        Args:
            query (str): The SQL query to execute.
            params (tuple or dict, optional): Parameters for parameterized queries.
            fetch_results (bool, optional): True to fetch results (for SELECT),
                                            False for DML/DDL. Defaults to True.

        Returns:
            pd.DataFrame or int/bool: DataFrame for SELECT, rowcount or True for DML/DDL.

        Raises:
            RuntimeError: If no connection is active.
            sqlite3.Error: For database-related errors.
        """
        if not self.connection:
            self.logger.info("No active connection. Attempting to auto-connect.")
            self.connect()  # Attempt to connect if not already connected
            if not self.connection:  # If connect still fails
                self.logger.error("Failed to establish a database connection.")
                raise RuntimeError("Database connection is not active.")

        self.logger.debug(
            f"Executing query: {query} with params: {params}, fetch_results: {fetch_results}"
        )
        cursor = None
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params if params else ())

            if fetch_results:
                results = cursor.fetchall()
                columns = (
                    [desc[0] for desc in cursor.description]
                    if cursor.description
                    else []
                )
                df = pd.DataFrame(results, columns=columns)
                self.logger.info(
                    f"Query executed successfully. Fetched {len(df)} rows."
                )
                return df
            else:
                self.connection.commit()
                rowcount = cursor.rowcount
                self.logger.info(
                    f"DML/DDL query executed successfully. Affected rows: {rowcount if rowcount != -1 else 'N/A'}"
                )
                return (
                    rowcount if rowcount != -1 else True
                )  # Return True for DDL that don't have rowcount
        except sqlite3.Error as e:
            self.logger.error(f"Error executing query '{query[:100]}...': {e}")
            # Optionally rollback on error for transactional integrity, though not always needed for SELECTs
            # if not fetch_results: self.connection.rollback() # Example
            raise
        except (
            pd.errors.PandasError
        ) as pe:  # Catch pandas specific errors during DataFrame creation
            self.logger.error(
                f"Pandas error during DataFrame creation from query results: {pe}"
            )
            raise
        finally:
            if cursor:
                cursor.close()

    def execute_script(self, sql_script: str):
        """
        Executes a string containing multiple SQL statements.

        Args:
            sql_script (str): SQL script with statements separated by ';'.

        Raises:
            RuntimeError: If no connection is active.
            sqlite3.Error: For database-related errors.
        """
        if not self.connection:
            self.logger.info(
                "No active connection for script execution. Attempting to auto-connect."
            )
            self.connect()
            if not self.connection:
                self.logger.error(
                    "Failed to establish a database connection for script execution."
                )
                raise RuntimeError(
                    "Database connection is not active for script execution."
                )

        self.logger.info("Executing SQL script.")
        try:
            self.connection.executescript(sql_script)
            self.connection.commit()
            self.logger.info("SQL script executed successfully.")
        except sqlite3.Error as e:
            self.logger.error(f"Error executing SQL script: {e}")
            # self.connection.rollback() # Example rollback
            raise


if __name__ == "__main__":
    main_exec_logger = logging.getLogger(__name__)
    if not main_exec_logger.handlers or not logging.getLogger().handlers:
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            force=True,
        )
    main_exec_logger.setLevel(logging.DEBUG)

    main_exec_logger.info("--- SQLProcessor Example Usage (In-Memory SQLite) ---")

    # Use in-memory SQLite for easy testing
    processor = SQLProcessor(db_connection_string=":memory:", db_type="sqlite")

    try:
        # 1. Connect
        main_exec_logger.info("\n--- Testing Connect ---")
        processor.connect()

        # 2. Test execute_query (DDL/DML)
        main_exec_logger.info("\n--- Testing DDL (CREATE TABLE) ---")
        create_table_query = (
            "CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, email TEXT UNIQUE)"
        )
        create_result = processor.execute_query(create_table_query, fetch_results=False)
        main_exec_logger.info(
            f"CREATE TABLE result: {create_result} (rowcount may be -1 or 0 for DDL)"
        )

        main_exec_logger.info("\n--- Testing DML (INSERT) ---")
        insert_query = "INSERT INTO users (name, email) VALUES (?, ?)"
        insert_params1 = ("Alice Wonderland", "alice@example.com")
        insert_params2 = ("Bob The Builder", "bob@example.com")

        affected_rows1 = processor.execute_query(
            insert_query, params=insert_params1, fetch_results=False
        )
        main_exec_logger.info(f"INSERT 1 affected rows: {affected_rows1}")
        affected_rows2 = processor.execute_query(
            insert_query, params=insert_params2, fetch_results=False
        )
        main_exec_logger.info(f"INSERT 2 affected rows: {affected_rows2}")

        # 3. Test execute_query (SELECT)
        main_exec_logger.info("\n--- Testing SELECT (all data) ---")
        df_all = processor.execute_query("SELECT id, name, email FROM users")
        main_exec_logger.info("All users DataFrame:")
        print(df_all)
        assert len(df_all) == 2

        main_exec_logger.info("\n--- Testing SELECT (specific data with params) ---")
        select_specific_query = "SELECT id, name FROM users WHERE email = ?"
        df_specific = processor.execute_query(
            select_specific_query, params=("bob@example.com",)
        )
        main_exec_logger.info("Specific user DataFrame (bob@example.com):")
        print(df_specific)
        assert len(df_specific) == 1
        assert df_specific["name"].iloc[0] == "Bob The Builder"

        # 4. Test execute_script
        main_exec_logger.info(
            "\n--- Testing execute_script (DROP and CREATE new table) ---"
        )
        script = """
        DROP TABLE IF EXISTS users;
        CREATE TABLE products (
            product_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            price REAL
        );
        INSERT INTO products (name, price) VALUES ('Laptop', 999.99);
        INSERT INTO products (name, price) VALUES ('Mouse', 25.00);
        """
        processor.execute_script(script)
        main_exec_logger.info("Script executed. Verifying new table 'products'.")
        df_products = processor.execute_query("SELECT * FROM products")
        main_exec_logger.info("Products DataFrame:")
        print(df_products)
        assert len(df_products) == 2
        assert "Laptop" in df_products["name"].values

        # 5. Test error handling
        main_exec_logger.info("\n--- Testing Error Handling ---")
        main_exec_logger.info("Attempting query with invalid syntax...")
        try:
            processor.execute_query("SELEC * FROM products")  # Intentional typo
        except sqlite3.Error as e:
            main_exec_logger.info(
                f"Caught expected sqlite3.Error for invalid syntax: {e}"
            )

        main_exec_logger.info("Attempting query on non-existent table...")
        try:
            processor.execute_query("SELECT * FROM non_existent_table")
        except sqlite3.Error as e:
            main_exec_logger.info(
                f"Caught expected sqlite3.Error for non-existent table: {e}"
            )

        main_exec_logger.info("Attempting to connect with unsupported DB type...")
        unsupported_processor = SQLProcessor(
            db_type="mysql", db_connection_string="dummy"
        )
        try:
            unsupported_processor.connect()
        except NotImplementedError as e:
            main_exec_logger.info(f"Caught expected NotImplementedError: {e}")

    except Exception as e:
        main_exec_logger.error(
            f"An error occurred during SQLProcessor tests: {e}", exc_info=True
        )
    finally:
        # 6. Disconnect
        main_exec_logger.info("\n--- Testing Disconnect ---")
        processor.disconnect()

    main_exec_logger.info("\n--- SQLProcessor tests finished ---")
