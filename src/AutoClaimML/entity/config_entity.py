# config_entity.py
import os
import yaml
from AutoClaimML.constants import *
from dataclasses import dataclass 
from datetime import datetime 


@dataclass
class TrainingPipelineConfig:
    pipeline_name: str = PIPELINE_NAME
    artifact_dir: str = os.path.join(ARTIFACT_DIR)
    

@dataclass
class DataIngestionConfig:
    data_ingestion_dir: str
    feature_store_file_path: str
    training_file_path: str
    testing_file_path: str
    train_test_split_ratio: float
    collection_name: str

@dataclass
class DataValidationConfig:
    data_validation_dir: str
    report_file_path: str
    schema_file_path: str

@dataclass
class DataTransformationConfig:
    data_transformation_dir: str
    transformed_train_file_path: str
    transformed_test_file_path: str
    transformed_object_file_path: str

@dataclass
class ModelTrainerConfig:
    model_trainer_dir: str
    trained_model_file_path: str
    expected_accuracy: float
    model_config_file_path: str

@dataclass
class ModelEvaluationConfig:
    changed_threshold_score: float = MODEL_EVALUATION_CHANGED_THRESHOLD_SCORE
    bucket_name: str = MODEL_BUCKET_NAME
    s3_model_key_path: str = MODEL_FILE_NAME
    
@dataclass
class ModelPusherConfig:
    bucket_name: str = MODEL_BUCKET_NAME
    s3_model_key_path: str = MODEL_FILE_NAME
    
    
 