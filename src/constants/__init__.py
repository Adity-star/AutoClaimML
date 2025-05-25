# __init__.py

import os
import sys
from datetime import date 


# For MongoDB connection
DATABASE_NAME = "VehicleDB"
COLLECTION_NAME = "VehicleDB-Data"
MONGODB_URL_KEY = "MONGODB_URL"


PIPELINE_NAME: str = ""
ARTIFACT_DIR: str = "artifact"

MODEL_FILE_NAME = "model.pkl"

TARGET_COLUMN = "Response"
CURRENT_YEAR = date.today().year
PREPROCSSING_OBJECT_FILE_NAME = "preprocessing.pkl"

# Data Ingestion stage
DATA_INGESTION_COLLECTION_NAME = "Vehicle-Data"
DATA_INGESTION_DIR_NAME = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR = "feature_store"
DATA_INGESTION_INGESTED_DIR = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO = 0.25
