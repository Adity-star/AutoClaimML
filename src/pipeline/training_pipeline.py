# training_pipeline.py

import sys
from src.exception import CustomException
from src.logger import logging 

from src.configuration.configuration import ConfigurationManager
from src.components.data_ingestion import DataIngestion
from src.components.data_validation import DataValidation

from src.entity.config_entity import DataIngestionConfig, DataValidationConfig



from src.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact

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
        
    def start_data_validation(self, data_ingestion_artifact: DataIngestionArtifact) -> DataValidationArtifact:
        """
        Starts the data validation process using the DataValidation component.
        """
        try:
            logging.info("Starting data validation process in TrainingPipeline.")

            # Get data validation config
            data_validation_config = self.config.get_data_validation_config()

            # Create data validation component and run it
            data_validation = DataValidation(
                data_ingestion_artifact=data_ingestion_artifact,
                data_validation_config=data_validation_config
            )

            data_validation_artifact = data_validation.initiate_data_validation()

            logging.info("Data validation completed successfully.")
            return data_validation_artifact

        except Exception as e:
            logging.error("Data validation failed in TrainingPipeline.")
            raise CustomException(e, sys)