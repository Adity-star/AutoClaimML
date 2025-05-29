# s3_estimator.py

import sys
from pandas import DataFrame

from AutoClaimML.entity.estimator import MyModel
from AutoClaimML.cloud_storage.aws_storage import SimpleStorageService
from AutoClaimML.exception import CustomException
from AutoClaimML.logger import logging

class Proj1Estimator:
    """
    Class to handle model operations: saving, loading, checking presence,
    and making predictions using a model stored in S3.
    """

    def __init__(self, bucket_name: str, model_path: str):
        """
        Initialize estimator with S3 bucket details.

        Args:
            bucket_name (str): Name of S3 bucket.
            model_path (str): Key path to model in S3.
        """
        self.bucket_name = bucket_name
        self.model_path = model_path
        self.s3 = SimpleStorageService()
        self.loaded_model: MyModel = None

    def is_model_present(self, model_path: str = None) -> bool:
        """
        Checks if the model exists in S3.

        Args:
            model_path (str): Optional alternate model path.

        Returns:
            bool: True if model exists.
        """
        try:
            model_path = model_path or self.model_path
            return self.s3.s3_key_path_available(bucket_name=self.bucket_name, s3_key=model_path)
        except CustomException as e:
            logging.error(f"Error checking model presence: {e}")
            return False
        
    def load_model(self) -> MyModel:
        """
        Loads the model from S3.

        Returns:
            MyModel: The loaded model object.
        """
        try:
            self.loaded_model = self.s3.load_model(
                model_name=self.model_path,
                bucket_name=self.bucket_name
            )
            return self.loaded_model
        except Exception as e:
            raise CustomException(e, sys)
        
    def save_model(self, from_file: str, remove: bool = False) -> None:
        """
        Saves a model file to S3.

        Args:
            from_file (str): Local path to the model file.
            remove (bool): If True, removes the local file after upload.
        """
        try:
            self.s3.upload_file(
                from_filename=from_file,
                to_filename=self.model_path,
                bucket_name=self.bucket_name,
                remove=remove
            )
        except Exception as e:
            raise CustomException(e, sys)
        
    def predict(self, dataframe: DataFrame):
        """
        Makes predictions using the loaded model.

        Args:
            dataframe (DataFrame): Input data.

        Returns:
            Any: Model predictions.
        """
        try:
            if self.loaded_model is None:
                self.load_model()
            return self.loaded_model.predict(dataframe)
        except Exception as e:
            raise CustomException(e, sys)