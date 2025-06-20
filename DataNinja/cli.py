
import argparse
import sys
import os
import pandas as pd


# Adjust path to import from core and formats, assuming cli.py is in DataNinja/
# This makes sure that DataNinja can be run as a script (python DataNinja/cli.py)
# or as a module (python -m DataNinja)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from DataNinja.core.loader import DataLoader # Abstract, for type hinting or checks
from DataNinja.core.cleaner import DataCleaner
from DataNinja.core.analyzer import DataAnalyzer
from DataNinja.core.transformer import DataTransformer
from DataNinja.core.plotter import DataPlotter
from DataNinja.core.utils import setup_logging, load_config
from DataNinja.formats.csv_handler import CSVHandler # Example concrete loader
# Add other handlers as they are implemented, e.g.:
# from DataNinja.formats.json_handler import JSONHandler
# from DataNinja.formats.excel_handler import ExcelHandler


# Setup a logger for the CLI module
logger = setup_logging(module_name='DataNinjaCLI')

def main(args=None):
    """
    Main function for the DataNinja CLI.
    Parses arguments and orchestrates the data processing workflow.
    """
    parser = argparse.ArgumentParser(description="DataNinja: A command-line tool for data processing and analysis.")

    # --- General Arguments ---
    parser.add_argument(
        "input_file",
        type=str,
        help="Path to the input data file."
    )
    parser.add_argument(
        "--output_file",
        type=str,
        help="Path to save the processed output data. (Optional)"
    )
    parser.add_argument(
        "--config",
        type=str,
        default="config.json",
        help="Path to a JSON configuration file for operations. (Default: config.json)"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="count",
        default=0,
        help="Increase verbosity (e.g., -v for INFO, -vv for DEBUG)."
    )

    # --- Sub-commands for different actions (optional, can be complex) ---
    # For now, let's keep it simple with primary action arguments.
    # Or, one could use subparsers for 'load', 'clean', 'analyze', 'transform', 'plot' actions.

    # --- Action-specific arguments (examples) ---
    parser.add_argument(
        "--load",
        action="store_true",
        help="Perform a load operation (default if input_file is given)."
    )
    parser.add_argument(
        "--clean",
        nargs='*', # 0 or more cleaning operation names or a config key
        help="Perform cleaning operations. Can be followed by specific ops or use config."
    )
    parser.add_argument(
        "--analyze",
        nargs='*', # 0 or more analysis names or a config key
        help="Perform analysis. Can be followed by specific types or use config."
    )
    parser.add_argument(
        "--transform",
        nargs='*',
        help="Perform transformations. Can be followed by specific transformations or use config."
    )
    parser.add_argument(
        "--plot",
        nargs='*', # e.g., --plot histogram:Age scatter:Age:Salary
        help="Generate plots. Specify plot type and columns, like 'histogram:column_name' or 'scatter:x_col:y_col'."
    )

    # Parse arguments
    # If called from __main__.py, sys.argv[1:] will be passed.
    # If called directly for testing, args can be a list of strings.
    parsed_args = parser.parse_args(args=args)

    # --- Configure Logging Verbosity ---
    if parsed_args.verbose == 1:
        logger.setLevel("INFO")
        setup_logging(log_level="INFO", module_name='DataNinjaCLI') # Re-setup with new level
        setup_logging(log_level="INFO", module_name='DataNinjaApp') # Also for general app logger
    elif parsed_args.verbose >= 2:
        logger.setLevel("DEBUG")
        setup_logging(log_level="DEBUG", module_name='DataNinjaCLI')
        setup_logging(log_level="DEBUG", module_name='DataNinjaApp')

    logger.info("DataNinja CLI started.")
    logger.debug(f"Parsed arguments: {parsed_args}")

    # --- Load Configuration ---
    # app_config = load_config(parsed_args.config)
    # if app_config:
    #     logger.info(f"Loaded configuration from {parsed_args.config}")
    # else:
    #     logger.warning(f"Could not load configuration from {parsed_args.config}. Proceeding with defaults/CLI args.")
    #     app_config = {} # Default to empty config

    # --- Core Logic ---
    # For now, just demonstrate loading. A real CLI would build a pipeline.

    data = None

    # 1. Load Data (using CSVHandler as an example)
    # TODO: Add logic to select loader based on file type or argument
    if os.path.exists(parsed_args.input_file):
        logger.info(f"Loading data from: {parsed_args.input_file}")
        try:
            # Simple type detection (can be more sophisticated)
            if parsed_args.input_file.lower().endswith('.csv'):
                loader = CSVHandler(source=parsed_args.input_file)
                data = loader.load_data()
                logger.info(f"Data loaded successfully. Shape: {data.shape if hasattr(data, 'shape') else len(data)} rows/elements.")
                logger.debug(f"Loaded data head:\n{data.head() if hasattr(data, 'head') else data[:5]}")
            # Add elif for other types like .json, .xlsx here
            # elif parsed_args.input_file.lower().endswith('.json'):
            #     loader = JSONHandler(source=parsed_args.input_file) # Assuming JSONHandler exists
            #     data = loader.load_data()
            else:
                logger.error(f"Unsupported file type: {parsed_args.input_file}. Only .csv is currently demonstrated.")
                sys.exit(1)
        except FileNotFoundError:
            logger.error(f"Input file not found: {parsed_args.input_file}")
            sys.exit(1)
        except Exception as e:
            logger.error(f"Error loading data: {e}", exc_info=parsed_args.verbose >=2)
            sys.exit(1)
    else:
        logger.error(f"Input file does not exist: {parsed_args.input_file}")
        sys.exit(1)

    if data is None:
        logger.error("No data loaded. Exiting.")
        sys.exit(1)

    # 2. Clean Data (Example)
    if parsed_args.clean is not None: # Check if --clean was passed
        logger.info("Cleaning data...")
        cleaner = DataCleaner(data)
        # This is a placeholder. Real implementation would parse `parsed_args.clean`
        # or use a config file to determine cleaning operations.
        # Example: remove rows where 'Age' is missing, convert 'Value' to int.
        cleaning_ops_example = [
            # {'method': 'remove_missing_values', 'params': {'subset': ['Age']}},
            # {'method': 'convert_column_type', 'params': {'column': 'Value', 'new_type': int}}
        ]
        if not cleaning_ops_example: # If no specific ops, maybe a default clean
            logger.info("No specific cleaning operations defined in CLI demo. Applying DataCleaner's default (if any).")

        try:
            data = cleaner.clean_data(operations=cleaning_ops_example) # or load from config
            logger.info(f"Data cleaned. Shape: {data.shape if hasattr(data, 'shape') else len(data)}")
            logger.debug(f"Cleaned data head:\n{data.head() if hasattr(data, 'head') else data[:5]}")
        except Exception as e:
            logger.error(f"Error during data cleaning: {e}", exc_info=parsed_args.verbose >=2)
            # Decide whether to exit or continue with uncleaned/partially cleaned data

    # 3. Analyze Data (Example)
    if parsed_args.analyze is not None:
        logger.info("Analyzing data...")
        analyzer = DataAnalyzer(data)
        # Placeholder for analysis logic based on `parsed_args.analyze` or config
        analysis_results = analyzer.analyze_data() # Default analysis
        logger.info("Analysis complete.")
        for key, result in analysis_results.items():
            logger.info(f"--- {key.replace('_', ' ').title()} ---")
            # print(result) # Or save to a file, log more selectively
            if isinstance(result, pd.DataFrame):
                 logger.info(f"\n{result.to_string()}")
            elif isinstance(result, pd.Series):
                 logger.info(f"\n{result.to_string()}")
            else:
                 logger.info(str(result))


    # 4. Transform Data (Example)
    if parsed_args.transform is not None:
        logger.info("Transforming data...")
        transformer = DataTransformer(data)
        # Placeholder for transformation logic
        transform_ops_example = [
            # {'method': 'scale_numerical_features', 'params': {'columns': ['Age', 'Salary']}},
            # {'method': 'encode_categorical_features', 'params': {'columns': ['City']}}
        ]
        if not transform_ops_example:
             logger.info("No specific transformations defined in CLI demo.")
        try:
            data = transformer.transform_data(transformations=transform_ops_example)
            logger.info(f"Data transformed. Shape: {data.shape if hasattr(data, 'shape') else len(data)}")
            logger.debug(f"Transformed data head:\n{data.head() if hasattr(data, 'head') else data[:5]}")
        except Exception as e:
            logger.error(f"Error during data transformation: {e}", exc_info=parsed_args.verbose >=2)

    # 5. Plot Data (Example)
    if parsed_args.plot:
        logger.info("Generating plots...")
        plotter = DataPlotter(data)
        for plot_request in parsed_args.plot:
            parts = plot_request.split(':')
            plot_type = parts[0]
            plot_params = {}
            if plot_type == 'histogram' and len(parts) > 1:
                plot_params['column'] = parts[1]
                if len(parts) > 2: plot_params['bins'] = int(parts[2])
            elif plot_type == 'scatter' and len(parts) > 2:
                plot_params['x_column'] = parts[1]
                plot_params['y_column'] = parts[2]
                if len(parts) > 3: plot_params['hue'] = parts[3] # Optional hue
            elif plot_type == 'bar' and len(parts) > 2:
                plot_params['x_column'] = parts[1]
                plot_params['y_column'] = parts[2]
                if len(parts) > 3: plot_params['estimator'] = parts[3]
            else:
                logger.warning(f"Plot request '{plot_request}' format not recognized or insufficient params. Skipping.")
                continue

            # Default save path for plots from CLI
            # plot_params['save_path'] = f"{plot_type}_{'_'.join(parts[1:])}.png"
            # For demonstration, let DataPlotter handle show/save via its own defaults or specific save_path in plot_params

            # Example: ensure a save path if not provided by user through a more complex mechanism
            if 'save_path' not in plot_params:
                base_filename = "_".join(filter(None, [plot_params.get('column'), plot_params.get('x_column'), plot_params.get('y_column')]))
                plot_params['save_path'] = f"{plot_type}_{base_filename if base_filename else 'plot'}.png"

            plotter.create_plot(plot_type, **plot_params)
        logger.info("Plot generation process completed.")


    # 6. Save Output (if specified)
    if parsed_args.output_file:
        logger.info(f"Saving processed data to: {parsed_args.output_file}")
        try:
            if isinstance(data, pd.DataFrame):
                # TODO: Select saver based on output file type
                if parsed_args.output_file.lower().endswith('.csv'):
                    data.to_csv(parsed_args.output_file, index=False)
                    logger.info("Data saved as CSV.")
                # Add elif for other types like .json, .xlsx here
                else:
                    logger.warning(f"Unsupported output file type: {parsed_args.output_file}. Saving as CSV by default.")
                    data.to_csv(parsed_args.output_file, index=False)
            else:
                # Handle saving other data types (e.g. list of lists, dicts from analysis)
                with open(parsed_args.output_file, 'w') as f:
                    import json
                    try:
                        json.dump(data, f, indent=2) # Assuming JSON serializable if not DataFrame
                        logger.info("Data saved as JSON.")
                    except TypeError:
                        f.write(str(data))
                        logger.info("Data saved as plain text (was not directly JSON serializable).")
            logger.info(f"Output successfully saved to {parsed_args.output_file}")
        except Exception as e:
            logger.error(f"Error saving output data: {e}", exc_info=parsed_args.verbose >=2)

    logger.info("DataNinja CLI finished.")


if __name__ == "__main__":
    # This allows running cli.py directly for testing
    # Example: python DataNinja/cli.py sample.csv --clean --analyze --plot histogram:Age -vv
    # Create a dummy sample.csv for testing
    if not os.path.exists("sample.csv"):
        dummy_df = pd.DataFrame({
            'ID': range(1, 6),
            'Name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
            'Age': [28, 35, 22, None, 30],
            'Salary': [70000, 80000, 55000, 120000, 75000],
            'City': ['New York', 'Los Angeles', 'Chicago', 'New York', 'Chicago']
        })
        dummy_df.to_csv("sample.csv", index=False)
        print("Created dummy sample.csv for CLI testing.")

    # Example command line arguments for direct script execution:
    # test_args = ["sample.csv", "--load", "--clean", "--analyze", "--plot", "histogram:Age:10", "scatter:Age:Salary", "-vv", "--output_file", "processed_sample.csv"]
    # main(test_args)

    # If running the script directly without arguments, argparse will use sys.argv[1:]
    # which would be empty if you just run `python DataNinja/cli.py`
    # For a more interactive test, you might want to prompt or define default test_args here.
    if len(sys.argv) == 1: # No arguments provided to script
        print("No input file provided. Running with default test arguments for 'sample.csv'.")
        print("Usage: python DataNinja/cli.py <input_file> [options]")
        test_args = ["sample.csv", "--clean", "--analyze",
                     "--plot", "histogram:Age", "scatter:Age:Salary:City", "bar:City:Salary",
                     "--output_file", "cli_output.csv", "-vv"]
        print(f"Running with: {' '.join(['python DataNinja/cli.py'] + test_args)}")
        main(test_args)
    else:
        main() # Uses sys.argv[1:] by default

