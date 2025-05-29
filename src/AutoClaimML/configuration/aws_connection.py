import os
import boto3
from AutoClaimML.constants import (
    AWS_SECRET_ACCESS_KEY_ENV_KEY,
    AWS_ACCESS_KEY_ID_ENV_KEY,
    REGION_NAME
)

class S3Client:
    """
    This class initializes an S3 client and resource using AWS credentials
    from environment variables. Raises an exception if credentials are missing.
    """

    _s3_client = None
    _s3_resource = None

    def __init__(self, region_name=REGION_NAME):
        if S3Client._s3_client is None or S3Client._s3_resource is None:
            access_key_id = os.getenv(AWS_ACCESS_KEY_ID_ENV_KEY)
            secret_access_key = os.getenv(AWS_SECRET_ACCESS_KEY_ENV_KEY)

            if not access_key_id:
                raise EnvironmentError(f"Environment variable '{AWS_ACCESS_KEY_ID_ENV_KEY}' is not set.")
            if not secret_access_key:
                raise EnvironmentError(f"Environment variable '{AWS_SECRET_ACCESS_KEY_ENV_KEY}' is not set.")

            S3Client._s3_resource = boto3.resource(
                's3',
                aws_access_key_id=access_key_id,
                aws_secret_access_key=secret_access_key,
                region_name=region_name
            )

            S3Client._s3_client = boto3.client(
                's3',
                aws_access_key_id=access_key_id,
                aws_secret_access_key=secret_access_key,
                region_name=region_name
            )

        self.s3_resource = S3Client._s3_resource
        self.s3_client = S3Client._s3_client

