# config_entity.py
import os
from src.constants import *
from dataclasses import dataclass 
from datetime import datetime 


@dataclass
class TrainingPipelineConfig:
    """
    Configuration for the overall ML pipeline.
    """
    pipeline_name: str = PIPELINE_NAME
    artifact_dir: str = os.path.join(ARTIFACT_DIR)
    



@dataclass
class DataIngestionConfig:
    """
    Configuration for the data ingestion stage of the pipeline.
    """
    data_ingestion_dir: str
    feature_store_file_path: str
    training_file_path: str
    testing_file_path: str
    train_test_split_ratio: float
    collection_name: str
 