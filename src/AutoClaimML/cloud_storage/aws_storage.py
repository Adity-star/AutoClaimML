# aws_storage.py

import os
import boto3
from io import StringIO
from typing import Union, List
import sys
import pickle
from pathlib import Path

from pandas import DataFrame, read_csv
from mypy_boto3_s3.service_resource import Bucket
from botocore.exceptions import ClientError

from AutoClaimML.logger import logging
from AutoClaimML.configuration.aws_connection import S3Client
from AutoClaimML.exception import CustomException

class SimpleStorageService:
    """
    Provides utility functions for interacting with AWS S3, including
    key existence checking, data uploads/downloads, and DataFrame handling.
    """

    def __init__(self):
        """
        Initializes the SimpleStorageService instance with S3 resource and client
        from the S3Client class.
        """
        try:
            s3_client = S3Client()
            self.s3_resource = s3_client.s3_resource
            self.s3_client = s3_client.s3_client
        except Exception as e:
            raise CustomException(f"Failed to initialize S3Client: {e}", sys)

    def get_bucket(self, bucket_name: str) -> Bucket:
        """
        Retrieves the S3 bucket object.

        Args:
            bucket_name (str): Name of the S3 bucket.

        Returns:
            Bucket: S3 Bucket resource.
        """
        try:
            return self.s3_resource.Bucket(bucket_name)
        except Exception as e:
            raise CustomException(f"Could not retrieve bucket: {e}", sys)
     
    def s3_key_path_available(self, bucket_name: str, s3_key: str) -> bool:
        """
        Checks if a specified S3 key path exists.

        Args:
            bucket_name (str): S3 bucket name.
            s3_key (str): S3 object key (file path).

        Returns:
            bool: True if key exists, False otherwise.
        """
        try:
            bucket = self.get_bucket(bucket_name)
            return any(bucket.objects.filter(Prefix=s3_key))
        except Exception as e:
            raise CustomException(e, sys)
        
    def get_file_object(self, filename: str, bucket_name: str) -> Union[List[ObjectSummary], ObjectSummary]:
        """
        Retrieves one or multiple S3 objects matching a prefix.

        Args:
            filename (str): File name or prefix.
            bucket_name (str): S3 bucket name.

        Returns:
            Union[List[ObjectSummary], ObjectSummary]: File object(s).
        """
        try:
            bucket = self.get_bucket(bucket_name)
            file_objects = list(bucket.objects.filter(Prefix=filename))
            return file_objects[0] if len(file_objects) == 1 else file_objects
        except Exception as e:
            raise CustomException(e, sys)
       

    @staticmethod
    def read_object(obj: object, decode: bool = True, make_readable: bool = False) -> Union[StringIO, str, bytes]:
        """
        Reads an S3 object and returns its content.

        Args:
            obj (object): S3 object to read.
            decode (bool): If True, decodes as string.
            make_readable (bool): If True, returns a StringIO object.

        Returns:
            Union[StringIO, str, bytes]: Object content.
        """
        try:
            data = obj.get()["Body"].read()
            if decode:
                data = data.decode()
            return StringIO(data) if make_readable else data
        except Exception as e:
            raise CustomException(e, sys)
        
    def load_model(self, model_name: str, bucket_name: str, model_dir: str = None) -> object:
        """
        Loads a pickled model from S3.

        Args:
            model_name (str): Name of the model file.
            bucket_name (str): S3 bucket name.
            model_dir (str): Optional subfolder path.

        Returns:
            object: Loaded model.
        """
        try:
            key = f"{model_dir}/{model_name}" if model_dir else model_name
            file_obj = self.get_file_object(key, bucket_name)
            model_bytes = self.read_object(file_obj, decode=False)
            return pickle.loads(model_bytes)
        except Exception as e:
            raise CustomException(e, sys)
        
    def create_folder(self, folder_name: str, bucket_name: str) -> None:
        """
        Creates a folder in the S3 bucket (folders are just prefixes).

        Args:
            folder_name (str): Folder name.
            bucket_name (str): Bucket name.
        """
        try:
            self.s3_resource.Object(bucket_name, f"{folder_name}/").load()
        except ClientError as e:
            if e.response["Error"]["Code"] == "404":
                self.s3_client.put_object(Bucket=bucket_name, Key=f"{folder_name}/")
            else:
                raise CustomException(e, sys)
        
    def upload_file(self, from_filename: str, to_filename: str, bucket_name: str, remove: bool = True) -> None:
        """
        Uploads a local file to S3.

        Args:
            from_filename (str): Local file path.
            to_filename (str): S3 destination key.
            bucket_name (str): Bucket name.
            remove (bool): If True, deletes local file after upload.
        """
        try:
            self.s3_resource.meta.client.upload_file(from_filename, bucket_name, to_filename)
            if remove:
                Path(from_filename).unlink()
        except Exception as e:
            raise CustomException(e, sys)
        
    def upload_df_as_csv(self, data_frame: DataFrame, local_filename: str, bucket_filename: str, bucket_name: str) -> None:
        """
        Uploads a DataFrame to S3 as a CSV.

        Args:
            data_frame (DataFrame): Data to upload.
            local_filename (str): Temporary local file name.
            bucket_filename (str): Destination filename in S3.
            bucket_name (str): Bucket name.
        """
        try:
            data_frame.to_csv(local_filename, index=False)
            self.upload_file(local_filename, bucket_filename, bucket_name)
        except Exception as e:
            raise CustomException(e, sys)
        
    def get_df_from_object(self, object_: object) -> DataFrame:
        """
        Converts an S3 object to a pandas DataFrame.

        Args:
            object_ (object): S3 object.

        Returns:
            DataFrame: Parsed DataFrame.
        """
        try:
            content = self.read_object(object_, make_readable=True)
            return read_csv(content, na_values="na")
        except Exception as e:
            raise CustomException(e, sys)
        
    def read_csv(self, filename: str, bucket_name: str) -> DataFrame:
        """
        Reads a CSV file from S3 as a DataFrame.

        Args:
            filename (str): S3 object key.
            bucket_name (str): Bucket name.

        Returns:
            DataFrame: Parsed DataFrame.
        """
        try:
            obj = self.get_file_object(filename, bucket_name)
            return self.get_df_from_object(obj)
        except Exception as e:
            raise CustomException(e, sys)



    
    