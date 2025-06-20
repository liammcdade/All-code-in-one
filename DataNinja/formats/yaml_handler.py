import os
import yaml  # PyYAML
import logging

# Assuming DataLoader is in ../core/loader.py
from ..core.loader import DataLoader

# from ..core.utils import setup_logging # If you have a centralized logging setup

# Basic module-level logger configuration
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


class YAMLHandler(DataLoader):
    def __init__(self, source):
        super().__init__(source)
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        self.logger.info(f"YAMLHandler initialized for source: {self.source}")

    def load_data(self, **kwargs):
        self.logger.info(f"Attempting to load YAML data from {self.source}")
        if not self.source:
            self.logger.error("Source path is None or empty, cannot load data.")
            raise ValueError("Source path is None or empty.")
        if not os.path.exists(self.source):
            self.logger.error(f"File not found: {self.source}")
            raise FileNotFoundError(f"File not found: {self.source}")

        encoding = kwargs.pop("encoding", "utf-8")

        try:
            with open(self.source, "r", encoding=encoding) as stream:
                # kwargs can be passed to safe_load if relevant ones exist (e.g. Loader)
                data = yaml.safe_load(stream, **kwargs)
            self.logger.info(
                f"Successfully loaded YAML data from {self.source}. Type: {type(data)}"
            )
            return data
        except (
            FileNotFoundError
        ):  # Should be caught by os.path.exists, but as a safeguard
            self.logger.error(f"File not found (yaml.safe_load): {self.source}")
            raise
        except yaml.YAMLError as ye:  # Base error for PyYAML
            self.logger.error(f"YAML parsing error in {self.source}: {ye}")
            raise
        except Exception as e:
            self.logger.error(
                f"An unexpected error occurred while loading YAML from {self.source}: {e}"
            )
            raise

    def save_data(self, data, target_path=None, **kwargs):
        if target_path is None:
            self.logger.error("Target path for saving YAML data is required.")
            raise ValueError("Target path for saving YAML data is required.")

        self.logger.info(f"Attempting to save YAML data to {target_path}")

        target_dir = os.path.dirname(target_path)
        if target_dir:
            os.makedirs(target_dir, exist_ok=True)
            self.logger.debug(f"Ensured directory exists: {target_dir}")

        # Default settings for yaml.dump
        encoding = kwargs.pop("encoding", "utf-8")
        sort_keys = kwargs.pop("sort_keys", False)
        allow_unicode = kwargs.pop("allow_unicode", True)  # Good default

        try:
            with open(target_path, "w", encoding=encoding) as stream:
                yaml.dump(
                    data,
                    stream,
                    sort_keys=sort_keys,
                    allow_unicode=allow_unicode,
                    **kwargs,
                )
            self.logger.info(f"Successfully saved YAML data to {target_path}")
        except IOError as e:
            self.logger.error(
                f"IOError occurred while saving YAML data to {target_path}: {e}"
            )
            raise
        except yaml.YAMLError as ye:  # Error during dumping
            self.logger.error(
                f"YAML formatting error while saving to {target_path}: {ye}"
            )
            raise
        except TypeError as te:  # Data not serializable
            self.logger.error(
                f"TypeError: Data not serializable to YAML for {target_path}. {te}"
            )
            raise
        except Exception as e:
            self.logger.error(
                f"An unexpected error occurred while saving YAML data to {target_path}: {e}"
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

    temp_dir = "temp_yaml_test_data"
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
        main_logger.info(f"Created temporary directory: {temp_dir}")

    sample_yaml_path = os.path.join(temp_dir, "sample_data.yaml")
    malformed_yaml_path = os.path.join(temp_dir, "malformed_data.yaml")
    output_dict_yaml_path = os.path.join(temp_dir, "output_dict.yaml")
    output_list_yaml_path = os.path.join(temp_dir, "output_list.yaml")

    # 1. Create a dummy YAML file for testing load_data
    sample_data_to_write = {
        "project": "DataNinja",
        "version": 1.2,
        "tags": ["data", "yaml", "python"],
        "users": [
            {"id": 1, "name": "Alice", "active": True},
            {"id": 2, "name": "Bob", "active": False},
        ],
    }
    try:
        with open(sample_yaml_path, "w") as f:
            yaml.dump(sample_data_to_write, f, sort_keys=False)
        main_logger.info(f"Created dummy YAML file: {sample_yaml_path}")
    except Exception as e:
        main_logger.error(f"Could not create dummy YAML: {e}", exc_info=True)
        # This might fail if PyYAML isn't installed yet.

    # Create a malformed YAML file
    with open(malformed_yaml_path, "w") as f:
        f.write(
            "project: DataNinja\nversion: 1.2\n  tags: [data, yaml, python]\nusers: - id: 1"
        )  # Bad indentation for tags
    main_logger.info(f"Created malformed YAML file: {malformed_yaml_path}")

    # --- Test load_data ---
    main_logger.info("\n--- Testing load_data (Valid YAML) ---")
    handler_load = YAMLHandler(source=sample_yaml_path)
    try:
        loaded_data = handler_load.load_data()
        main_logger.info(f"Loaded data type: {type(loaded_data)}")
        main_logger.info("Loaded data content:")
        # Basic check for content by comparing with original after loading
        if loaded_data == sample_data_to_write:
            main_logger.info("Content verified successfully after loading.")
        else:
            main_logger.error("Content mismatch after loading.")
            print("Original:", sample_data_to_write)
            print("Loaded:", loaded_data)

    except Exception as e:
        main_logger.error(f"Error loading valid YAML: {e}", exc_info=True)

    main_logger.info("\n--- Testing load_data (Non-existent file) ---")
    handler_non_existent = YAMLHandler(
        source=os.path.join(temp_dir, "non_existent.yaml")
    )
    try:
        handler_non_existent.load_data()
    except FileNotFoundError as e:
        main_logger.error(f"Caught expected FileNotFoundError: {e}")
    except Exception as e:
        main_logger.error(
            f"Caught unexpected error for non-existent file: {e}", exc_info=True
        )

    main_logger.info("\n--- Testing load_data (Malformed YAML) ---")
    handler_malformed = YAMLHandler(source=malformed_yaml_path)
    try:
        handler_malformed.load_data()
    except yaml.YAMLError as e:
        main_logger.error(f"Caught expected YAMLError for malformed file: {e}")
    except Exception as e:
        main_logger.error(
            f"Caught unexpected error for malformed file: {e}", exc_info=True
        )

    # --- Test save_data ---
    dict_to_save = {
        "name": "Test Report",
        "score": 85.5,
        "details": {"items": 5, "valid": True},
    }
    list_to_save = [
        {"task": "Setup", "status": "Done"},
        {"task": "Run", "status": "Pending"},
    ]

    handler_save = YAMLHandler(
        source="dummy_source_for_saving.yaml"
    )  # Source not used for saving

    main_logger.info("\n--- Testing save_data (Dictionary to YAML) ---")
    try:
        handler_save.save_data(dict_to_save, target_path=output_dict_yaml_path)
        main_logger.info(f"Dictionary saved to {output_dict_yaml_path}")
        if os.path.exists(output_dict_yaml_path):
            main_logger.info(f"Verified: {output_dict_yaml_path} exists.")
            # Verify content by reloading
            reloaded_dict = YAMLHandler(output_dict_yaml_path).load_data()
            if reloaded_dict == dict_to_save:
                main_logger.info("Dict content verified by reloading.")
            else:
                main_logger.error("Dict content mismatch after reloading.")
    except Exception as e:
        main_logger.error(f"Error saving dictionary: {e}", exc_info=True)

    main_logger.info("\n--- Testing save_data (List to YAML) ---")
    try:
        handler_save.save_data(list_to_save, target_path=output_list_yaml_path)
        main_logger.info(f"List saved to {output_list_yaml_path}")
        if os.path.exists(output_list_yaml_path):
            main_logger.info(f"Verified: {output_list_yaml_path} exists.")
            # Verify content by reloading
            reloaded_list = YAMLHandler(output_list_yaml_path).load_data()
            if reloaded_list == list_to_save:
                main_logger.info("List content verified by reloading.")
            else:
                main_logger.error("List content mismatch after reloading.")
    except Exception as e:
        main_logger.error(f"Error saving list: {e}", exc_info=True)

    main_logger.info("\n--- Testing save_data (Missing target_path) ---")
    try:
        handler_save.save_data(dict_to_save)
    except ValueError as e:
        main_logger.error(f"Caught expected ValueError for missing target_path: {e}")
    except Exception as e:
        main_logger.error(
            f"Caught unexpected error (missing target_path): {e}", exc_info=True
        )

    main_logger.info(
        "\n--- Testing save_data (Potentially non-serializable - though basic types are fine) ---"
    )

    # PyYAML is quite flexible with standard Python objects.
    # To test non-serializability, one might need a custom object without a representer.
    class NonSerializableObject:
        def __init__(self):
            self.x = 10

    non_serializable_data = {"data": NonSerializableObject()}
    try:
        handler_save.save_data(
            non_serializable_data,
            target_path=os.path.join(temp_dir, "unsupported.yaml"),
        )
    except (
        yaml.YAMLError
    ) as e:  # PyYAML raises YAMLError (specifically RepresenterError) for non-serializable
        main_logger.error(f"Caught expected YAMLError for non-serializable type: {e}")
    except TypeError as e:  # Fallback, though YAMLError is more specific from PyYAML
        main_logger.error(f"Caught TypeError for non-serializable type: {e}")
    except Exception as e:
        main_logger.error(
            f"Caught unexpected error (non-serializable type): {e}", exc_info=True
        )

    # Clean up
    main_logger.info("\n--- Cleaning up test files ---")
    try:
        paths_to_remove = [
            sample_yaml_path,
            malformed_yaml_path,
            output_dict_yaml_path,
            output_list_yaml_path,
            os.path.join(temp_dir, "unsupported.yaml"),
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

    main_logger.info("\n--- YAMLHandler tests finished ---")
