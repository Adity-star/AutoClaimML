# model_pusher.py

import sys

from AutoClaimML.logger import logging
from AutoClaimML.exception import CustomException

from AutoClaimML.entity.config_entity import ModelPusherConfig
from AutoClaimML.entity.artifact_entity import (ModelEvaluationArtifact,
                                                ModelPusherArtifact)

from AutoClaimML.entity.s3_estimator import Proj1Estimator

from AutoClaimML.cloud_storage.aws_storage import SimpleStorageService


class ModelPusher:
    def __init__(
        self,
        model_evaluation_artifact: ModelEvaluationArtifact,
        model_pusher_config: ModelPusherConfig
    ):
        """
        :param model_evaluation_artifact: Output artifact from model evaluation stage.
        :param model_pusher_config: Configuration for the model pusher.
        """
        self.s3 = SimpleStorageService()
        self.model_evaluation_artifact = model_evaluation_artifact
        self.model_pusher_config = model_pusher_config
        self.proj1_estimator = Proj1Estimator(
            bucket_name=model_pusher_config.bucket_name,
            model_path=model_pusher_config.s3_model_key_path
        )

    def initiate_model_pusher(self) -> ModelPusherArtifact:
        """
        Method Name : initiate_model_pusher
        Description : Initiates the model pushing process by uploading the trained model
                      to the specified S3 bucket path.

        Output      : Returns ModelPusherArtifact containing S3 upload details.
        On Failure  : Logs and raises exception.
        """
        logging.info("Entered initiate_model_pusher method of ModelPusher class")

        try:
            print("------------------------------------------------------------------------------------------------")
            logging.info("Uploading trained model artifact to S3 bucket...")

            trained_model_path = self.model_evaluation_artifact.trained_model_path
            if not trained_model_path:
                raise CustomException("Trained model path is missing in ModelEvaluationArtifact", sys)
            
            logging.info(f"Uploading model from local path: {trained_model_path}")
            self.proj1_estimator.save_model(from_file=trained_model_path)

            model_pusher_artifact = ModelPusherArtifact(
                bucket_name=self.model_pusher_config.bucket_name,
                s3_model_path=self.model_pusher_config.s3_model_key_path
            )

            logging.info(f"Model successfully uploaded to S3 at: {self.model_pusher_config.s3_model_key_path}")
            logging.info(f"ModelPusherArtifact: {model_pusher_artifact}")
            logging.info("Exited initiate_model_pusher method of ModelPusher class")

            return model_pusher_artifact
        
        except Exception as e:
                logging.error(f"Error in initiate_model_pusher: {e}")
                raise CustomException(e, sys) from e