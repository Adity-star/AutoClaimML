# data_ingestion.py

import os
import sys
from typing import Optional

import pandas as pd
from pandas import DataFrame
from sklearn.model_selection import train_test_split


from src.logger import logging
from src.data_access.vehicle_db import VehicleDB
from src.entity.config_entity import DataIngestionConfig
from src.entity.artifact_entity import DataIngestionArtifact
from src.exception import CustomException
from src.configuration.configuration import ConfigurationManager


class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig):
        """
        Initializes the DataIngestion component with the given configuration.

        :param data_ingestion_config: DataIngestionConfig object from ConfigurationManager.
        """
        try:
            self.data_ingestion_config = data_ingestion_config
            logging.info(f"DataIngestionConfig: {self.data_ingestion_config}")
        except Exception as e:
            raise CustomException(e, sys)
        
    def export_data_into_feature_store(self) -> DataFrame:
        """
        Export data from MongoDB to the feature store CSV path.

        :return: DataFrame of exported data.
        """
        try:
            logging.info("Exporting data from MongoDB collection.")
            proj_data = VehicleDB()
            dataframe = proj_data.export_collection_as_dataframe(
                collection_name=self.data_ingestion_config.collection_name
            )
            logging.info(f"Exported data shape: {dataframe.shape}")

            # Save to feature store path
            feature_store_path = self.data_ingestion_config.feature_store_file_path
            os.makedirs(os.path.dirname(feature_store_path), exist_ok=True)
            dataframe.to_csv(feature_store_path, index=False)
            logging.info(f"Data saved to feature store at: {feature_store_path}")

            return dataframe

        except Exception as e:
            logging.error("Failed during data export from MongoDB.")
            raise CustomException(e, sys)
        
    def _save_dataframe_to_csv(self, dataframe: DataFrame, file_path: str) -> None:
        """
        Save a DataFrame to the specified file path.

        :param dataframe: DataFrame to save.
        :param file_path: Target CSV file path.
        """
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            dataframe.to_csv(file_path, index=False, header=True)
            logging.info(f"Data saved to: {file_path}")
        except Exception as e:
            logging.error(f"Failed to save data to {file_path}")
            raise CustomException(e, sys)
        
    def split_data_as_train_test(self, dataframe: DataFrame) -> None:
        """
        Splits the dataset into train and test sets and saves them.

        :param dataframe: The complete dataset as a DataFrame.
        """
        try:
            logging.info("Splitting data into train and test sets.")
            train_df, test_df = train_test_split(
                dataframe,
                test_size=self.data_ingestion_config.train_test_split_ratio,
                random_state=42
            )

            train_path = self.data_ingestion_config.training_file_path
            test_path = self.data_ingestion_config.testing_file_path
            os.makedirs(os.path.dirname(train_path), exist_ok=True)

            train_df.to_csv(train_path, index=False)
            test_df.to_csv(test_path, index=False)
            logging.info(f"Train data saved at: {train_path}")
            logging.info(f"Test data saved at: {test_path}")


        except Exception as e:
            logging.error("Failed during train-test splitting.")
            raise CustomException(e, sys)
        
    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        """
        Executes the entire data ingestion pipeline.

        :return: DataIngestionArtifact containing paths to the train and test sets.
        """
        try:
            logging.info("Starting data ingestion pipeline.")
            df = self.export_data_into_feature_store()
            self.split_data_as_train_test(df)

            artifact = DataIngestionArtifact(
                trained_file_path=self.data_ingestion_config.training_file_path,
                test_file_path=self.data_ingestion_config.testing_file_path
            )

            logging.info(f"Data ingestion completed. Artifact: {artifact}")
            return artifact
        
        except Exception as e:
            logging.error("Data ingestion failed.")
            raise CustomException(e, sys)
