# configuration.py
import os
from src.constants import *
from src.entity.config_entity import TrainingPipelineConfig, DataIngestionConfig
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
