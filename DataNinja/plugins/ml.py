import logging
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score
# from ..core.utils import setup_logging # If a centralized logging setup is used

# Basic module-level logger configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class MLModel:
    def __init__(self, model_type: str = 'logistic_regression', params: dict = None):
        """
        Initializes the MLModel.

        Args:
            model_type (str, optional): Type of the model. Defaults to 'logistic_regression'.
                                        Currently only 'logistic_regression' is supported.
            params (dict, optional): Parameters for the model constructor. Defaults to None.
        """
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        self.model_type = model_type
        self.params = params if params is not None else {}
        self.model = None

        if self.model_type == 'logistic_regression':
            self.model = LogisticRegression(**self.params)
            self.logger.info(
                f"LogisticRegression model initialized with params: {self.params}"
            )
        else:
            self.logger.warning(
                f"Model type '{self.model_type}' is not explicitly supported. "
                f"No model instance created during initialization."
            )
            # Optionally raise an error or default to a generic model
            # raise ValueError(f"Unsupported model_type: {self.model_type}")

        self.logger.info(
            f"MLModel setup complete. Model instance: {self.model}"
        )

    def train(self, X: np.ndarray, y: np.ndarray) -> None:
        """
        Trains the model using the provided features (X) and target (y).

        Args:
            X (np.ndarray): Features for training.
            y (np.ndarray): Target variable for training.
        """
        self.logger.info(f"Attempting to train model of type '{self.model_type}'.")

        if not isinstance(X, np.ndarray) or not isinstance(y, np.ndarray):
            self.logger.warning(
                f"Expected X and y to be numpy arrays. Got {type(X)} and {type(y)}. "
                "Scikit-learn might handle this, but explicit conversion is safer."
            )

        if self.model is None:
            self.logger.error("Model is not initialized. Cannot train.")
            raise RuntimeError("Model must be initialized before training. Check model_type.")

        try:
            self.logger.info(f"Training with X (shape {X.shape}, dtype {X.dtype}) and y (shape {y.shape}, dtype {y.dtype}).")
            self.model.fit(X, y)
            self.logger.info("Model training complete.")
        except Exception as e:
            self.logger.error(f"Error during model training: {e}", exc_info=True)
            raise  # Re-raise the exception after logging

    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Makes predictions using the trained model.

        Args:
            X (np.ndarray): New data for prediction.

        Returns:
            np.ndarray: Predicted class labels.

        Raises:
            RuntimeError: If the model has not been trained or initialized.
            ValueError: If X is None or not a np.ndarray.
        """
        self.logger.info("Attempting to make predictions.")

        if not isinstance(X, np.ndarray):
            self.logger.error(f"Input data X must be a numpy array. Got {type(X)}.")
            raise ValueError("Input data X for prediction must be a numpy array.")

        if self.model is None:
            self.logger.error("Model has not been initialized. Cannot predict.")
            raise RuntimeError("Model must be initialized before making predictions.")

        # Check if model is trained (sklearn models often have `classes_` or `coef_` attribute after fit)
        if not hasattr(self.model, 'classes_') and not hasattr(self.model, 'coef_'):
             self.logger.warning("Model does not appear to be trained yet (missing typical attributes like 'classes_' or 'coef_'). Predictions might be based on initial state or fail.")
        # It's hard to have a universal "is_trained" check for all sklearn models without calling fit.
        # For now, we'll rely on the user to call train() first. A more robust check might involve
        # trying to access an attribute that only exists after fitting, specific to the model type.


        try:
            self.logger.info(f"Predicting on X (shape {X.shape}, dtype {X.dtype}).")
            predictions = self.model.predict(X)
            self.logger.info(f"Predictions generated with shape {predictions.shape}.")

            if hasattr(self.model, 'predict_proba'):
                # Log availability, but don't return proba by default from this method
                # proba_predictions = self.model.predict_proba(X)
                self.logger.info(f"Probability predictions are also available via model.predict_proba(X). First 5 probas: {self.model.predict_proba(X)[:5]}")
            return predictions
        except Exception as e:
            self.logger.error(f"Error during model prediction: {e}", exc_info=True)
            raise

    def evaluate(self, X_test: np.ndarray, y_test: np.ndarray, average_method: str = 'binary') -> dict:
        """
        Evaluates the model using test data.

        Args:
            X_test (np.ndarray): Test features.
            y_test (np.ndarray): True labels for test data.
            average_method (str, optional): Averaging method for precision and recall scores.
                                          Defaults to 'binary'. Other options: 'micro', 'macro', 'weighted'.

        Returns:
            dict: A dictionary containing accuracy, precision, and recall scores.
        Raises:
            RuntimeError: If the model has not been trained or initialized.
            ValueError: If X_test or y_test are not numpy arrays or are None.
        """
        self.logger.info("Attempting to evaluate model.")

        if not isinstance(X_test, np.ndarray) or not isinstance(y_test, np.ndarray):
            self.logger.error(f"X_test and y_test must be numpy arrays. Got {type(X_test)} and {type(y_test)}.")
            raise ValueError("X_test and y_test must be numpy arrays for evaluation.")

        if self.model is None:
            self.logger.error("Model has not been initialized. Cannot evaluate.")
            raise RuntimeError("Model must be initialized before evaluation.")

        # Similar check as in predict for trained status
        if not hasattr(self.model, 'classes_') and not hasattr(self.model, 'coef_'):
             self.logger.warning("Model does not appear to be trained yet. Evaluation might be based on initial state or fail.")


        try:
            self.logger.info(f"Evaluating with X_test (shape {X_test.shape}) and y_test (shape {y_test.shape}).")
            y_pred = self.model.predict(X_test)

            accuracy = accuracy_score(y_test, y_pred)
            # For binary classification, common practice. For multiclass, 'weighted' or 'macro' might be better.
            precision = precision_score(y_test, y_pred, average=average_method, zero_division=0)
            recall = recall_score(y_test, y_pred, average=average_method, zero_division=0)

            scores = {'accuracy': accuracy, 'precision': precision, 'recall': recall}
            self.logger.info(f"Evaluation scores ({average_method} averaging): {scores}")
            return scores
        except Exception as e:
            self.logger.error(f"Error during model evaluation: {e}", exc_info=True)
            raise

if __name__ == '__main__':
    main_exec_logger = logging.getLogger(__name__)
    # Ensure logger is configured for script execution
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - [%(levelname)s] - %(name)s - %(message)s', force=True)
    main_exec_logger.setLevel(logging.DEBUG)

    main_exec_logger.info("--- MLModel Example Usage ---")

    # Instantiate model - Logistic Regression
    # Parameters for LogisticRegression can be passed here
    model_params = {'solver': 'liblinear', 'random_state': 42, 'C': 1.0}
    ml_model = MLModel(model_type='logistic_regression', params=model_params)
    main_exec_logger.info(f"Initialized MLModel with type: {ml_model.model_type}, underlying model: {ml_model.model}")

    # Create more realistic dummy data for binary classification
    main_exec_logger.info("\n--- Generating Sample Data ---")
    n_samples, n_features = 100, 5
    X = np.random.rand(n_samples, n_features)  # Features
    # Create a simple binary target variable y based on some condition
    # e.g., if sum of first two features > 0.7, then class 1, else 0
    y = (X[:, 0] + X[:, 1] > 0.7).astype(int)
    main_exec_logger.info(f"Generated data: X shape {X.shape}, y shape {y.shape}, {np.sum(y)} positive samples")

    # Split data into train and test sets
    try:
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        main_exec_logger.info(f"Data split: X_train {X_train.shape}, X_test {X_test.shape}, y_train {y_train.shape}, y_test {y_test.shape}")
    except Exception as e:
        main_exec_logger.error(f"Error during data splitting: {e}", exc_info=True)
        # Exit or skip further tests if data splitting fails
        exit()

    # Test predict before train (should ideally raise an error or warn, depending on sklearn model's default behavior)
    main_exec_logger.info("\n--- Testing predict before explicit train call ---")
    try:
        # LogisticRegression might allow predict before fit if initialized, but predictions would be naive.
        # Let's see what our wrapper does or if sklearn model throws an error.
        # Scikit-learn's LogisticRegression will raise NotFittedError if not fit. Our check should catch this.
        initial_predictions = ml_model.predict(X_test)
        main_exec_logger.info(f"Predictions before explicit train call (might be naive or error): {initial_predictions[:5]}")
    except Exception as e: # Catching generic Exception as sklearn might raise NotFittedError
        main_exec_logger.info(f"Caught expected behavior or error when predicting before train: {type(e).__name__} - {e}")


    # Train model
    main_exec_logger.info("\n--- Testing train ---")
    try:
        ml_model.train(X_train, y_train)
        # Check if the model instance in our class has been fitted (e.g. coef_ attribute exists for LogisticRegression)
        if hasattr(ml_model.model, 'coef_'):
            main_exec_logger.info(f"Model training seems successful. Coefs shape: {ml_model.model.coef_.shape}")
        else:
            main_exec_logger.warning("Model training finished, but coef_ attribute not found (unexpected for LogisticRegression).")
    except Exception as e:
        main_exec_logger.error(f"Error during model.train: {e}", exc_info=True)
        main_exec_logger.warning("Skipping further tests due to training error.")
        exit() # Exit if training fails

    # Predict
    main_exec_logger.info("\n--- Testing predict ---")
    try:
        predictions = ml_model.predict(X_test)
        main_exec_logger.info(f"Predictions on test set (first 5): {predictions[:5]}")
        assert len(predictions) == len(X_test), "Number of predictions should match number of test samples."
    except Exception as e:
        main_exec_logger.error(f"Error during model.predict: {e}", exc_info=True)
        main_exec_logger.warning("Skipping evaluation due to prediction error.")
        exit() # Exit if prediction fails

    # Evaluate
    main_exec_logger.info("\n--- Testing evaluate ---")
    try:
        # For binary classification, 'binary' is fine.
        # If it were multiclass, one might use 'weighted' or 'macro'.
        eval_scores = ml_model.evaluate(X_test, y_test, average_method='binary')
        main_exec_logger.info(f"Evaluation scores: {eval_scores}")
        assert 'accuracy' in eval_scores and 'precision' in eval_scores and 'recall' in eval_scores
    except Exception as e:
        main_exec_logger.error(f"Error during model.evaluate: {e}", exc_info=True)

    main_exec_logger.info("\n--- MLModel tests finished ---")
