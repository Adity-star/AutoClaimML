# demo.py

'''
from src.logger import logging
from src.exception import CustomException
import sys

from src.exception import CustomException
import traceback
import sys

def test_traceback():
    try:
        1 / 0
    except Exception as e:
        print("traceback.extract_tb:", traceback.extract_tb(sys.exc_info()[2]))
        print("traceback.format_exc:", traceback.format_exc())

test_traceback()
'''


from AutoClaimML.pipeline.training_pipeline import TrainingPipeline

pipeline = TrainingPipeline()
pipeline.run_pipeline()

import boto3

# Use default profile (same as AWS CLI)
#session = boto3.Session()
#s3 = session.client('s3')

#response = s3.list_buckets()
#print("Buckets:", [bucket['Name'] for bucket in response['Buckets']])






