# estimator.py

import sys
import pandas as pd
from pandas import DataFrame
from sklearn.pipeline import Pipeline

from AutoClaimML.exception import CustomException
from AutoClaimML.logger import logging


# -------------------------
# TargetValueMapping Class
# -------------------------
class TargetValueMapping:
    """
    Maps categorical target values to numeric for classification
    and supports reverse mapping for interpretation.
    """
    def __init__(self):
        self.yes: int = 0
        self.no: int = 1
    def _asdict(self) -> dict:
        """Returns mapping as a dictionary: {'yes': 0, 'no': 1}"""
        return self.__dict__

    def reverse_mapping(self) -> dict:
        """Reverses the dictionary: {0: 'yes', 1: 'no'}"""
        mapping_response = self._asdict()
        return {v: k for k, v in mapping_response.items()}

# ---------------------
# MyModel Wrapper Class
# ---------------------
class MyModel:
    """
    Custom model class that wraps both the preprocessing pipeline
    and the trained prediction model.
    """

    def __init__(self, preprocessing_object: Pipeline, trained_model_object: object):
        """
        :param preprocessing_object: Fitted preprocessing pipeline (e.g., scaler, encoder)
        :param trained_model_object: Fitted model (e.g., RandomForestClassifier)
        """
        self.preprocessing_object = preprocessing_object
        self.trained_model_object = trained_model_object
    def predict(self, dataframe: DataFrame) -> pd.Series:
        """
        Applies preprocessing to input DataFrame and returns model predictions.
        
        :param dataframe: Raw input features
        :return: Predicted values as a pandas Series
        """
        try:
            logging.info("Starting prediction process.")

            # Transform input using the saved preprocessing pipeline
            logging.info("Applying preprocessing transformations.")
            transformed_features = self.preprocessing_object.transform(dataframe)
              
             # Predict using the trained model
            logging.info("Making predictions with the trained model.")
            predictions = self.trained_model_object.predict(transformed_features)

            return pd.Series(predictions)

        except Exception as e:
            logging.error("Error occurred in predict method", exc_info=True)
            raise CustomException(e, sys) from e

    def __repr__(self) -> str:
        return f"MyModel(trained_model_object={type(self.trained_model_object).__name__})"

    def __str__(self) -> str:
        return self.__repr__()