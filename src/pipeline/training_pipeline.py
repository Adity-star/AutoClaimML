# training_pipeline.py

import sys
from src.exception import CustomException
from src.logger import logging 

from src.configuration.configuration import ConfigurationManager
from src.components.data_ingestion import DataIngestion


from src.entity.config_entity import DataIngestionConfig


from src.entity.artifact_entity import DataIngestionArtifact

class TrainingPipeline:
    def __init__(self):
        try:
            logging.info("Initializing ConfigurationManager in TrainingPipeline.")
            self.config = ConfigurationManager()
        except Exception as e:
            raise CustomException(e, sys)

    def start_data_ingestion(self) -> DataIngestionArtifact:
        """
        Starts the data ingestion process using the DataIngestion component.
        """
        try:
            logging.info("Starting data ingestion process in TrainingPipeline.")

            data_ingestion_config = self.config.get_data_ingestion_config()
            data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
            artifact = data_ingestion.initiate_data_ingestion()

            logging.info("Data ingestion completed successfully.")
            return artifact

        except Exception as e:
            logging.error("Data ingestion failed in TrainingPipeline.")
            raise CustomException(e,sys)