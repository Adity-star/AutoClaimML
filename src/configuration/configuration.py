# configuration.py
import os
from src.constants import *
from src.entity.config_entity import (TrainingPipelineConfig,
                                       DataIngestionConfig,
                                       DataValidationConfig,
                                       DataTransformationConfig)

from src.constants import SCHEMA_FILE_PATH
from dotenv import load_dotenv

load_dotenv()

class ConfigurationManager:
    """
    Manages creation of all pipeline configuration objects.
    """

    def __init__(self) -> None:
        """
        Initializes the base training pipeline config used across all other configurations.
        """
        self.training_pipeline_config = TrainingPipelineConfig()

    def get_training_pipeline_config(self) -> TrainingPipelineConfig:
        """
        Returns the base TrainingPipelineConfig object.
        """
        return self.training_pipeline_config

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        """
        Creates and returns the DataIngestionConfig using the base pipeline config.
        """
        ingestion_dir = os.path.join(
            self.training_pipeline_config.artifact_dir,
            DATA_INGESTION_DIR_NAME
        )

        return DataIngestionConfig(
            data_ingestion_dir=ingestion_dir,
            feature_store_file_path=os.path.join(ingestion_dir, DATA_INGESTION_FEATURE_STORE_DIR, FILE_NAME),
            training_file_path=os.path.join(ingestion_dir, DATA_INGESTION_INGESTED_DIR, TRAIN_FILE_NAME),
            testing_file_path=os.path.join(ingestion_dir, DATA_INGESTION_INGESTED_DIR, TEST_FILE_NAME),
            train_test_split_ratio=DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO,
            collection_name=DATA_INGESTION_COLLECTION_NAME
        )
    
    def get_data_validation_config(self) -> DataValidationConfig:
        data_validation_dir = os.path.join(
            self.training_pipeline_config.artifact_dir,
            DATA_VALIDATION_DIR_NAME
        )

        report_file_path = os.path.join(
            data_validation_dir,
            DATA_VALIDATION_REPORT_FILE_NAME
        )

        return DataValidationConfig(
            data_validation_dir=data_validation_dir,
            report_file_path=report_file_path,
            schema_file_path=SCHEMA_FILE_PATH
        )
    
    def get_data_transformation_config(self) -> DataTransformationConfig:
        """
        Creates and returns the DataTransformationConfig using the base pipeline config.
        """
        data_transformation_dir = os.path.join(
            self.training_pipeline_config.artifact_dir,
            DATA_TRANSFORMATION_DIR_NAME
        )

        transformed_data_dir = os.path.join(
            data_transformation_dir,
            DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR
        )
        transformed_object_dir = os.path.join(
            data_transformation_dir,
            DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR
        )

        transformed_train_file_path = os.path.join(
            transformed_data_dir,
            TRAIN_FILE_NAME.replace("csv", "npy")
        )

        transformed_test_file_path = os.path.join(
            transformed_data_dir,
            TEST_FILE_NAME.replace("csv", "npy")
        )

        transformed_object_file_path = os.path.join(
            transformed_object_dir,
            PREPROCSSING_OBJECT_FILE_NAME
        )

        return DataTransformationConfig(
            data_transformation_dir=data_transformation_dir,
            transformed_train_file_path=transformed_train_file_path,
            transformed_test_file_path=transformed_test_file_path,
            transformed_object_file_path=transformed_object_file_path
        )

    



    

