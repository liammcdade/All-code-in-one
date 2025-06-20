import pandas as pd


class DataCleaner:
    """
    Handles cleaning operations on datasets.

    The class can be initialized with data (e.g., a pandas DataFrame or a list of lists).
    It provides methods to perform various cleaning tasks.
    """

    def __init__(self, data):
        """
        Initializes the DataCleaner with the dataset.

        Args:
            data: The data to be cleaned. Can be a pandas DataFrame,
                  list of lists, or other common data structures.
                  For robust handling, methods will often try to convert
                  input to a pandas DataFrame if applicable.
        """
        if data is None:
            raise ValueError("Input data cannot be None.")

        # For flexibility, we can store data as is, or try to convert to DataFrame
        # For now, let's assume if it's not a DataFrame, it's a list of lists
        if isinstance(data, pd.DataFrame):
            self.data = data
        elif isinstance(data, list):
            try:
                # Attempt to convert list of lists to DataFrame
                # This assumes a simple structure (e.g., first list is header)
                if data and isinstance(data[0], list):
                    self.data = pd.DataFrame(data[1:], columns=data[0])
                else:
                    # Fallback or raise error if structure is not as expected
                    self.data = pd.DataFrame(data)
            except Exception as e:
                # If conversion fails, store as is, but some methods might not work
                print(
                    f"Warning: Could not convert input list to DataFrame: {e}. Storing as is."
                )
                self.data = data
        else:
            # Potentially support other types or raise error
            raise TypeError(
                "Unsupported data type. Please provide a pandas DataFrame or a list of lists."
            )

    def clean_data(self, operations=None):
        """
        Applies a series of cleaning operations to the data.

        Args:
            operations (list of dict, optional): A list of operations to perform.
                Each operation can be a dictionary specifying the method and its arguments.
                Example: [{'method': 'remove_missing_values', 'params': {'threshold': 1}},
                          {'method': 'convert_column_type', 'params': {'column': 'age', 'new_type': int}}]
                If None, this method might apply a default set of cleaning steps or do nothing.

        Returns:
            The cleaned data (typically a pandas DataFrame).
        """
        if not isinstance(self.data, pd.DataFrame):
            print(
                "Warning: Data is not a pandas DataFrame. Some cleaning operations may not apply or may fail."
            )
            return self.data

        cleaned_df = self.data.copy()

        if operations:
            for op in operations:
                method_name = op.get("method")
                params = op.get("params", {})
                if hasattr(self, method_name) and callable(getattr(self, method_name)):
                    print(f"Applying operation: {method_name} with params: {params}")
                    cleaned_df = getattr(self, method_name)(cleaned_df, **params)
                else:
                    print(
                        f"Warning: Unknown cleaning method '{method_name}'. Skipping."
                    )
        else:
            # Placeholder for default cleaning if no operations are specified
            print(
                "No specific cleaning operations provided. Applying default steps (if any)."
            )
            # Example: cleaned_df = self.remove_missing_values(cleaned_df)
            # cleaned_df = self.remove_duplicates(cleaned_df)
            pass

        self.data = cleaned_df  # Update internal data
        return self.data

    def remove_missing_values(
        self, df, threshold=None, subset=None, strategy="drop_rows"
    ):
        """
        Removes rows or columns with missing values.

        Args:
            df (pd.DataFrame): The DataFrame to clean.
            threshold (int, optional): The minimum number of non-NA values a row/column must have.
                                      If None, any NA will cause a drop.
            subset (list, optional): Labels along other axis to consider, e.g., if dropping rows,
                                     these would be a list of columns to include.
            strategy (str): 'drop_rows' to drop rows with NA,
                            'drop_cols' to drop columns with NA,
                            'fill' to impute missing values (requires 'fill_value' or method).

        Returns:
            pd.DataFrame: DataFrame with missing values handled.
        """
        if not isinstance(df, pd.DataFrame):
            print("Data is not a DataFrame. Cannot remove missing values effectively.")
            return df

        print(
            f"Removing missing values (strategy: {strategy}, threshold: {threshold}, subset: {subset})..."
        )
        if strategy == "drop_rows":
            return df.dropna(thresh=threshold, subset=subset, axis=0)
        elif strategy == "drop_cols":
            return df.dropna(thresh=threshold, subset=subset, axis=1)
        # Add 'fill' strategy later
        else:
            print(f"Warning: Unknown strategy '{strategy}' for missing value removal.")
            return df

    def convert_column_type(self, df, column, new_type, **kwargs):
        """
        Converts the data type of a specified column.

        Args:
            df (pd.DataFrame): The DataFrame to modify.
            column (str): The name of the column to convert.
            new_type (type or str): The target data type (e.g., int, float, str, 'datetime64').
            **kwargs: Additional arguments to pass to astype (e.g., errors='raise'/'ignore').

        Returns:
            pd.DataFrame: DataFrame with the column type converted.
        """
        if not isinstance(df, pd.DataFrame):
            print("Data is not a DataFrame. Cannot convert column type.")
            return df

        if column not in df.columns:
            print(
                f"Warning: Column '{column}' not found in DataFrame. Skipping type conversion."
            )
            return df

        print(f"Converting column '{column}' to type '{new_type}'...")
        try:
            df[column] = df[column].astype(new_type, **kwargs)
        except Exception as e:
            print(f"Error converting column '{column}' to {new_type}: {e}")
        return df

    def remove_duplicates(self, df, subset=None, keep="first"):
        """
        Removes duplicate rows from the DataFrame.

        Args:
            df (pd.DataFrame): The DataFrame to clean.
            subset (column label or sequence of labels, optional): Only consider certain columns for identifying duplicates, by default use all of the columns.
            keep ({'first', 'last', False}, default 'first'): Determines which duplicates (if any) to keep.
                - first : Drop duplicates except for the first occurrence.
                - last : Drop duplicates except for the last occurrence.
                - False : Drop all duplicates.
        Returns:
            pd.DataFrame: DataFrame with duplicate rows removed.
        """
        if not isinstance(df, pd.DataFrame):
            print("Data is not a DataFrame. Cannot remove duplicates.")
            return df

        print(f"Removing duplicates (subset: {subset}, keep: {keep})...")
        return df.drop_duplicates(subset=subset, keep=keep)

    def get_cleaned_data(self):
        """
        Returns the current state of the cleaned data.
        """
        return self.data


if __name__ == "__main__":
    print("--- DataCleaner Demonstration ---")

    # Example 1: List of lists
    print("\n--- Example 1: List of Lists ---")
    data_lol = [
        ["Name", "Age", "City", "Value"],
        ["Alice", 28, "New York", "100"],
        ["Bob", 35, "Los Angeles", "200"],
        ["Charlie", 22, "Chicago", "150"],
        ["David", None, "New York", "100"],  # Missing age
        ["Eve", 35, "Los Angeles", "200"],  # Duplicate of Bob for demonstration
        ["Frank", 40, None, "300"],  # Missing City
    ]
    try:
        cleaner1 = DataCleaner(data_lol)
        print("Initial DataFrame from list of lists:")
        print(cleaner1.get_cleaned_data())

        # Define operations
        ops1 = [
            {
                "method": "remove_missing_values",
                "params": {"subset": ["Age"]},
            },  # Remove rows where Age is NA
            {
                "method": "convert_column_type",
                "params": {"column": "Value", "new_type": int},
            },
            {
                "method": "remove_duplicates",
                "params": {"subset": ["Age", "City"], "keep": "first"},
            },
        ]
        cleaner1.clean_data(operations=ops1)
        print("\nCleaned DataFrame (from list of lists):")
        print(cleaner1.get_cleaned_data())
    except Exception as e:
        print(f"Error in Example 1: {e}")

    # Example 2: Pandas DataFrame
    print("\n--- Example 2: Pandas DataFrame ---")
    data_df = pd.DataFrame(
        {
            "ID": [1, 2, 3, 4, 5, 6, 7],
            "Product": ["A", "B", "A", "C", "B", "D", "A"],
            "Price": [10.0, 20.5, 10.0, 5.0, 21.0, 15.5, 9.99],
            "Quantity": [5, None, 3, 10, 2, 6, 5],  # Missing quantity
            "Status": [
                "Active",
                "Inactive",
                "Active",
                "Active",
                None,
                "Shipped",
                "Active",
            ],  # Missing Status
        }
    )
    try:
        cleaner2 = DataCleaner(
            data_df.copy()
        )  # Use .copy() to avoid modifying original df outside class
        print("Initial DataFrame:")
        print(cleaner2.get_cleaned_data())

        # Clean by calling methods directly
        df_cleaned = cleaner2.remove_missing_values(
            cleaner2.get_cleaned_data(), subset=["Quantity"]
        )
        df_cleaned = cleaner2.convert_column_type(
            df_cleaned, column="Price", new_type=float
        )
        df_cleaned = cleaner2.remove_duplicates(
            df_cleaned, subset=["Product"], keep="last"
        )

        # Update cleaner's internal data if desired (or just use df_cleaned)
        cleaner2.data = df_cleaned

        print("\nCleaned DataFrame (direct method calls):")
        print(cleaner2.get_cleaned_data())
    except Exception as e:
        print(f"Error in Example 2: {e}")

    # Example 3: Handling initialization errors
    print("\n--- Example 3: Initialization with None ---")
    try:
        cleaner3 = DataCleaner(None)
    except ValueError as e:
        print(f"Caught expected error: {e}")

    print("\n--- Example 4: Unsupported data type ---")
    try:
        cleaner4 = DataCleaner("just a string")
    except TypeError as e:
        print(f"Caught expected error: {e}")
