# training_pipeline.py

import sys
from AutoClaimML.exception import CustomException
from AutoClaimML.logger import logging 

from AutoClaimML.configuration.configuration import ConfigurationManager
from AutoClaimML.components.data_ingestion import DataIngestion
from AutoClaimML.components.data_validation import DataValidation
from AutoClaimML.components.data_transformation import DataTransformation
from AutoClaimML.components.model_trainer import ModelTrainer

from AutoClaimML.entity.config_entity import (DataIngestionConfig,
                                       DataValidationConfig,
                                       DataTransformationConfig,
                                       ModelTrainerConfig)



from AutoClaimML.entity.artifact_entity import (DataIngestionArtifact,
                                         DataValidationArtifact,
                                         DataTransformationArtifact,
                                         ModelTrainerArtifact)

class TrainingPipeline:
    def __init__(self):
        try:
            logging.info("Initializing ConfigurationManager in TrainingPipeline.")
            self.config = ConfigurationManager()

            self.data_transformation_config = self.config.get_data_transformation_config()
            self.model_trainer_config = self.config.get_model_trainer_config()
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
        
    def start_data_transformation(
        self, 
        data_ingestion_artifact: DataIngestionArtifact, 
        data_validation_artifact: DataValidationArtifact
    ) -> DataTransformationArtifact:
        """
        Starts the Data Transformation component of the pipeline.
        """
        try:
            logging.info("Initializing Data Transformation component...")

            data_transformation = DataTransformation(
                data_ingestion_artifact=data_ingestion_artifact,
                data_transformation_config=self.data_transformation_config,
                data_validation_artifact=data_validation_artifact
            )

            data_transformation_artifact = data_transformation.initiate_data_transformation()
            logging.info("Data Transformation completed and artifact generated.")
            return data_transformation_artifact

        except Exception as e:
            logging.exception("Failed to execute data transformation in TrainPipeline.")
            raise CustomException(f"Error in start_data_transformation: {e}", sys) from e
        
    def start_model_trainer(self, data_transformation_artifact: DataTransformationArtifact) -> ModelTrainerArtifact:
        """
        This method of TrainPipeline class is responsible for starting model training
        """
        try:
            model_trainer = ModelTrainer(
                data_transformation_artifact=data_transformation_artifact,
                model_trainer_config=self.model_trainer_config
            )
            model_trainer_artifact = model_trainer.initiate_model_trainer()
            return model_trainer_artifact

        except Exception as e:
            raise CustomException(e, sys) from e
        
    def run_pipeline(self, ) -> None:
        """
        This method of TrainPipeline class is responsible for running complete pipeline
        """
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
            data_transformation_artifact = self.start_data_transformation(
                    data_ingestion_artifact=data_ingestion_artifact, data_validation_artifact=data_validation_artifact) 
            model_trainer_artifact = self.start_model_trainer(data_transformation_artifact=data_transformation_artifact)  
        except Exception as e:
            raise CustomException(e, sys)
