from abc import ABC, abstractmethod


class DataLoader(ABC):
    """
    Abstract base class for data loaders.

    Subclasses must implement the `load_data` method to handle specific
    file types or data sources.
    """

    def __init__(self, source):
        """
        Initializes the DataLoader with the data source.

        Args:
            source (str): The path to the file or data source.
        """
        self.source = source
        if not self.source:
            raise ValueError("Data source cannot be empty.")

    @abstractmethod
    def load_data(self):
        """
        Loads data from the specified source.

        This method must be implemented by subclasses.

        Returns:
            data: The loaded data (e.g., list of lists, pandas DataFrame).

        Raises:
            NotImplementedError: If the subclass does not implement this method.
            FileNotFoundError: If the specified source file does not exist.
            Exception: For other data loading errors.
        """
        pass

    def get_source_info(self):
        """
        Returns information about the data source.

        Returns:
            str: Information about the data source.
        """
        return f"Data source: {self.source}"


# Example of how a specific loader might be structured (for illustration)
# class SpecificFileLoader(DataLoader):
# def load_data(self):
# # Check if file exists
# # import os
# # if not os.path.exists(self.source):
# # raise FileNotFoundError(f"File not found: {self.source}")
#         #
#         # try:
#         #     # Add specific loading logic here, e.g., for a CSV file
#         #     # with open(self.source, 'r') as f:
#         #     #     # Example: reading lines from a file
#         #     #     data = [line.strip().split(',') for line in f.readlines()]
#         #     # return data
#         #     print(f"Loading data from {self.source} using a specific loader...")
#         #     # Replace with actual data loading
#         #     return [["example", "data"], ["another", "row"]]
#         # except Exception as e:
#         #     raise Exception(f"Error loading data from {self.source}: {e}")

if __name__ == "__main__":
    # This section is for demonstration and testing purposes.
    # It won't run when the module is imported.

    # Note: You can't instantiate DataLoader directly because it's an ABC.
    # To test, you would create a concrete subclass:

    class MyCustomLoader(DataLoader):
        def load_data(self):
            # Simulate loading data
            print(f"Attempting to load data from: {self.source}")
            if self.source == "test.txt":
                return [["line1", "data1"], ["line2", "data2"]]
            elif self.source == "nonexistent.txt":
                raise FileNotFoundError(f"Simulated: {self.source} not found.")
            else:
                raise ValueError(f"Simulated: Cannot load from {self.source}")

    print("--- DataLoader Demonstration ---")

    # Test with a valid source
    try:
        loader1 = MyCustomLoader("test.txt")
        print(loader1.get_source_info())
        data1 = loader1.load_data()
        print(f"Loaded data: {data1}")
    except Exception as e:
        print(f"Error: {e}")

    print("\n--- Test with a non-existent file ---")
    try:
        loader2 = MyCustomLoader("nonexistent.txt")
        loader2.load_data()  # This should raise FileNotFoundError
    except FileNotFoundError as e:
        print(f"Caught expected error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

    print("\n--- Test with an invalid source for the custom loader ---")
    try:
        loader3 = MyCustomLoader("invalid_source.csv")
        loader3.load_data()  # This should raise ValueError based on MyCustomLoader's logic
    except ValueError as e:
        print(f"Caught expected error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

    print("\n--- Test with empty source init ---")
    try:
        loader4 = MyCustomLoader(
            ""
        )  # This should raise ValueError from DataLoader's __init__
    except ValueError as e:
        print(f"Caught expected error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
