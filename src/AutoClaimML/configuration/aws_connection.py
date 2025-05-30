import boto3
from botocore.exceptions import ProfileNotFound
from AutoClaimML.constants import REGION_NAME


class S3Client:
    """
    Initializes an S3 client and resource.
    Attempts environment variables first, then falls back to AWS CLI default profile.
    """
    _s3_client = None
    _s3_resource = None

    def __init__(self, region_name=REGION_NAME):
        if S3Client._s3_client is None or S3Client._s3_resource is None:
            try:
                import os
                access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
                secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")

                if access_key_id and secret_access_key:
                    # Use credentials from environment
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
                else:
                    # Fallback: use AWS CLI profile
                    session = boto3.Session(profile_name='default')
                    S3Client._s3_resource = session.resource('s3')
                    S3Client._s3_client = session.client('s3')

            except ProfileNotFound as e:
                raise EnvironmentError(
                    "AWS credentials not found in environment variables or default profile."
                ) from e

        self.s3_resource = S3Client._s3_resource
        self.s3_client = S3Client._s3_client
