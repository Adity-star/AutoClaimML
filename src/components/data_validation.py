# data_validation.py

import json
import os
import sys

import pandas as pd
import numpy as np 
from pandas import DataFrame


from src.exception import CustomException
from src.logger import logging
from src.utils.main_utils import read_yaml_file
from src.entity.config_entity import DataValidationConfig
from src.entity.artifact_entity import (DataIngestionArtifact,
                                        DataValidationArtifact)

from src.constants import SCHEMA_FILE_PATH


class DataValidation:
    def __init__(self,
                 data_ingestion_artifact: DataIngestionArtifact, 
                 data_validation_config: DataValidationConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml_file(file_path=SCHEMA_FILE_PATH)
        except Exception as e:
            raise CustomException(e, sys)
        
    def validate_column_count(self, dataframe: DataFrame) -> bool:
        """
        Validates that the number of columns matches the schema.
        """
        try:
            expected_col_count = len(self._schema_config["columns"])
            actual_col_count = len(dataframe.columns)
            status = actual_col_count == expected_col_count
            logging.info(f"Expected columns: {expected_col_count}, Actual: {actual_col_count} → Valid: {status}")
            return status
        except Exception as e:
            raise CustomException(e, sys)
    
    def validate_column_names(self, df: DataFrame) -> bool:
        """
        Validates that all required numerical and categorical columns exist.
        """
        try:
            dataframe_columns = df.columns.tolist()
            missing_numerical = [col for col in self._schema_config["numerical_columns"] if col not in dataframe_columns]
            missing_categorical = [col for col in self._schema_config["categorical_columns"] if col not in dataframe_columns]

            if missing_numerical:
                logging.warning(f"Missing numerical columns: {missing_numerical}")
            if missing_categorical:
                logging.warning(f"Missing categorical columns: {missing_categorical}")

            return not (missing_numerical or missing_categorical)
        except Exception as e:
            raise CustomException(e, sys)
        
   
    @staticmethod
    def read_data(file_path: str) -> DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise CustomException(e, sys)
        
    def initiate_data_validation(self) -> DataValidationArtifact:
        """
        Orchestrates data validation by checking:
        - Column count
        - Column name presence (numerical and categorical)

        Saves a JSON report.
        """
        try:
            validation_error_msg = ""

            logging.info("🔍 Starting data validation...")

            # Load data
            train_df = self.read_data(self.data_ingestion_artifact.training_file_path)
            test_df = self.read_data(self.data_ingestion_artifact.testing_file_path)

            # Validate train and test column count
            if not self.validate_column_count(train_df):
                validation_error_msg += "Mismatch in number of columns in training data. "
            if not self.validate_column_count(test_df):
                validation_error_msg += "Mismatch in number of columns in test data. "

            # Validate column existence
            if not self.validate_column_names(train_df):
                validation_error_msg += "Missing required columns in training data. "
            if not self.validate_column_names(test_df):
                validation_error_msg += "Missing required columns in test data. "

            validation_status = validation_error_msg == ""

            # Create artifact
            data_validation_artifact = DataValidationArtifact(
                validation_status=validation_status,
                message=validation_error_msg.strip(),
                validation_report_file_path=self.data_validation_config.validation_report_file_path
            )

            # Save validation report
            os.makedirs(os.path.dirname(self.data_validation_config.validation_report_file_path), exist_ok=True)
            with open(self.data_validation_config.validation_report_file_path, "w") as f:
                json.dump({
                    "validation_status": validation_status,
                    "message": validation_error_msg.strip()
                }, f, indent=4)

            logging.info(f"✅ Data validation completed. Result: {validation_status}")
            return data_validation_artifact

        except Exception as e:
            raise CustomException(e, sys)
