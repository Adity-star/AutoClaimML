# model_evaluation.py
import sys
import pandas as pd
from typing import Optional
from dataclasses import dataclass
from sklearn.metrics import f1_score

from AutoClaimML.logger import logging
from AutoClaimML.exception import CustomException
from AutoClaimML.constants import TARGET_COLUMN
from AutoClaimML.entity.config_entity import ModelEvaluationConfig
from AutoClaimML.entity.artifact_entity import (ModelEvaluationArtifact,
                                                DataIngestionArtifact,
                                                DataTransformationArtifact,
                                                ModelTrainerArtifact)
from AutoClaimML.utils.main_utils import load_object
from AutoClaimML.entity.s3_estimator import Proj1Estimator


@dataclass
class EvaluateModelResponse:
    trained_model_f1_score: float
    best_model_f1_score: Optional[float]
    is_model_accepted: bool
    difference: float

class ModelEvaluation:
    """
    Evaluates the trained model against the best production model from S3 and
    decides whether to accept the new model based on performance metrics.
    """

    def __init__(
        self,
        model_eval_config: ModelEvaluationConfig,
        data_ingestion_artifact: DataIngestionArtifact,
        model_trainer_artifact: ModelTrainerArtifact
    ):
        self.model_eval_config = model_eval_config
        self.data_ingestion_artifact = data_ingestion_artifact
        self.model_trainer_artifact = model_trainer_artifact

    def _map_gender_column(self, df: pd.DataFrame) -> pd.DataFrame:
        logging.info("Mapping 'Gender' column to binary values")
        if 'Gender' in df.columns:
            df['Gender'] = df['Gender'].map({'Female': 0, 'Male': 1}).astype(int)
        return df 
    
    def _drop_id_column(self, df: pd.DataFrame) -> pd.DataFrame:
        logging.info("Dropping 'id' or '_id' column if exists")
        for col in ['id', '_id']:
            if col in df.columns:
                df = df.drop(col, axis=1)
        return df

    def _create_dummy_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        logging.info("Creating dummy variables for categorical features")
        return pd.get_dummies(df, drop_first=True)
    
    def _rename_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        logging.info("Renaming and casting specific dummy columns to integer")
        rename_map = {
            "Vehicle_Age_< 1 Year": "Vehicle_Age_lt_1_Year",
            "Vehicle_Age_> 2 Years": "Vehicle_Age_gt_2_Years"
        }
        df.rename(columns=rename_map, inplace=True)

        for col in ["Vehicle_Age_lt_1_Year", "Vehicle_Age_gt_2_Years", "Vehicle_Damage_Yes"]:
            if col in df.columns:
                df[col] = df[col].astype(int)

        return df
    
    def _preprocess_test_data(self, df: pd.DataFrame) -> pd.DataFrame:
        logging.info("Preprocessing test data")
        df = self._map_gender_column(df)
        df = self._drop_id_column(df)
        df = self._create_dummy_columns(df)
        df = self._rename_columns(df)
        return df
    
    def get_best_model(self) -> Optional[Proj1Estimator]:
        try:
            estimator = Proj1Estimator(
                bucket_name=self.model_eval_config.bucket_name,
                model_path=self.model_eval_config.s3_model_key_path
            )
            return estimator if estimator.is_model_present() else None
        except Exception as e:
            raise CustomException(e, sys)
        
    def evaluate_model(self) -> EvaluateModelResponse:
        try:
            # Load test data
            logging.info("Loading test data from: %s", self.data_ingestion_artifact.test_file_path)
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)
            logging.info("Test data shape: %s", test_df.shape)
            
            X_test, y_test = test_df.drop(TARGET_COLUMN, axis=1), test_df[TARGET_COLUMN]
            logging.info("X_test shape: %s, y_test shape: %s", X_test.shape, y_test.shape)
            
            X_test = self._preprocess_test_data(X_test)
            logging.info("Preprocessed X_test shape: %s", X_test.shape)

            # Load trained model and get f1 score
            logging.info("Loading trained model from: %s", self.model_trainer_artifact.trained_model_file_path)
            trained_model = load_object(self.model_trainer_artifact.trained_model_file_path)
            trained_model_f1_score = self.model_trainer_artifact.metric_artifact.f1_score
            logging.info(f"F1 Score - Trained model: {trained_model_f1_score}")
            
            # Check best model
            best_model_estimator = self.get_best_model()
            best_model_f1_score = None
            if best_model_estimator:
                logging.info("Evaluating current production model from S3")
                y_pred_best = best_model_estimator.predict(X_test)
                logging.info("Best model predictions shape: %s", y_pred_best.shape if y_pred_best is not None else None)
                best_model_f1_score = f1_score(y_test, y_pred_best)
                logging.info(f"F1 Score - Production model: {best_model_f1_score}")
            
            # Compare scores
            best_f1 = best_model_f1_score if best_model_f1_score is not None else 0
            is_accepted = trained_model_f1_score > best_f1
            difference = trained_model_f1_score - best_f1

            return EvaluateModelResponse(
                trained_model_f1_score=trained_model_f1_score,
                best_model_f1_score=best_model_f1_score,
                is_model_accepted=is_accepted,
                difference=difference
            )
        
        except Exception as e:
            raise CustomException(e, sys)
        
    def initiate_model_evaluation(self) -> ModelEvaluationArtifact:
        try:
            logging.info("Starting model evaluation...")
            eval_response = self.evaluate_model()

            return ModelEvaluationArtifact(
                is_model_accepted=eval_response.is_model_accepted,
                s3_model_path=self.model_eval_config.s3_model_key_path,
                trained_model_path=self.model_trainer_artifact.trained_model_file_path,
                changed_accuracy=eval_response.difference
            )

        except Exception as e:
            raise CustomException(e, sys)
        

    


