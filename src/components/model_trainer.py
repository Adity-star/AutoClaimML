# model_trainer.py

import sys
from typing import Tuple
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score,precision_score, recall_score

from src.exception import CustomException
from src.logger import logging
from src.utils.main_utils import load_numpy_array_data, load_object, save_object
from src.entity.config_entity import ModelTrainerConfig
from src.entity.artifact_entity import DataTransformationArtifact, ModelTrainerArtifact,ClassificationMetricArtifact

from src.entity.estimator import MyModel
import mlflow

class ModelTrainer:
    def __init__(self, data_transformation_artifact: DataTransformationArtifact,
                 model_trainer_config: ModelTrainerConfig):
        """
        :param data_transformation_artifact: Output reference of data transformation artifact stage
        :param model_trainer_config: Configuration for model training
        """
        self.data_transformation_artifact = data_transformation_artifact
        self.model_trainer_config = model_trainer_config

    def get_model_object_and_report(self, train: np.array, test: np.array) -> Tuple[object, ClassificationMetricArtifact]:
        """
        Trains RandomForestClassifier on train data and evaluates on test data.

        Returns:
            - trained model object
            - ClassificationMetricArtifact with f1, precision, recall scores
        """
        
        try:
            logging.info("Training RandomForestClassifier with specified parameters")

            # Split features and target variables
            x_train, y_train = train[:, :-1], train[:, -1]
            x_test, y_test = test[:, :-1], test[:, -1]
            logging.info("Train-test split done.")

             # Initialize and train the model
            model = RandomForestClassifier(
                n_estimators=self.model_trainer_config.n_estimators,
                min_samples_split=self.model_trainer_config.min_samples_split,
                min_samples_leaf=self.model_trainer_config.min_samples_leaf,
                max_depth=self.model_trainer_config.max_depth,
                criterion=self.model_trainer_config.criterion,
                random_state=self.model_trainer_config.random_state
            )
            logging.info("Model training started.")
            model.fit(x_train, y_train)
            logging.info("Model training completed.")

             # Predict and evaluate
            y_pred = model.predict(x_test)
            f1 = f1_score(y_test, y_pred)
            precision = precision_score(y_test, y_pred)
            recall = recall_score(y_test, y_pred)
            accuracy = accuracy_score(y_test, y_pred)
            logging.info(f"Evaluation metrics - Accuracy: {accuracy:.4f}, F1: {f1:.4f}, Precision: {precision:.4f}, Recall: {recall:.4f}")

            metric_artifact = ClassificationMetricArtifact(f1_score=f1, precision_score=precision, recall_score=recall)
            return model, metric_artifact
        except Exception as e:
            logging.error("Error in get_model_object_and_report", exc_info=True)
            raise CustomException(e, sys) from e
        
   
        
    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        """
        Loads transformed data, trains model, evaluates and saves it.
        Also logs parameters, metrics, and artifacts with MLflow.

        Returns:
            - ModelTrainerArtifact containing trained model filepath and metrics
        
        Raises:
            - MyException on failure
        """
        logging.info("Entered initiate_model_trainer method of ModelTrainer class")
        try:
            print("-" * 100)
            print("Starting Model Trainer Component")

             # Load train and test numpy arrays
            train_arr = load_numpy_array_data(file_path=self.data_transformation_artifact.transformed_train_file_path)
            test_arr = load_numpy_array_data(file_path=self.data_transformation_artifact.transformed_test_file_path)
            logging.info("Loaded transformed train and test data.")
            
            mlflow.set_tracking_uri("http://127.0.0.1:5000") 
            mlflow.set_experiment("AutoClaim Vehicle")
            
            # Start MLflow run
            with mlflow.start_run() as run:
                logging.info(f"MLflow run started with run_id={run.info.run_id}")

                # Log hyperparameters
                mlflow.log_param("n_estimators", self.model_trainer_config.n_estimators)
                mlflow.log_param("min_samples_split", self.model_trainer_config.min_samples_split)
                mlflow.log_param("min_samples_leaf", self.model_trainer_config.min_samples_leaf)
                mlflow.log_param("max_depth", self.model_trainer_config.max_depth)
                mlflow.log_param("criterion", self.model_trainer_config.criterion)
                mlflow.log_param("random_state", self.model_trainer_config.random_state)

                # Train the model and get metrics
                trained_model, metric_artifact = self.get_model_object_and_report(train=train_arr, test=test_arr)
                logging.info("Trained model and evaluation metrics obtained.")

                # Log metrics
                mlflow.log_metric("f1_score", metric_artifact.f1_score)
                mlflow.log_metric("precision_score", metric_artifact.precision_score)
                mlflow.log_metric("recall_score", metric_artifact.recall_score)

                # Load preprocessing object
                preprocessing_obj = load_object(file_path=self.data_transformation_artifact.transformed_object_file_path)
                logging.info("Preprocessing object loaded.")

                # Validate if model meets expected accuracy on train data
                train_accuracy = accuracy_score(train_arr[:, -1], trained_model.predict(train_arr[:, :-1]))
                logging.info(f"Train accuracy: {train_accuracy:.4f}")

                if train_accuracy < self.model_trainer_config.expected_accuracy:
                    logging.error(f"Train accuracy {train_accuracy:.4f} is below expected {self.model_trainer_config.expected_accuracy}")
                    raise Exception("No model found with score above the base score")

                # Save combined model (preprocessing + model)
                my_model = MyModel(preprocessing_object=preprocessing_obj, trained_model_object=trained_model)
                save_object(self.model_trainer_config.trained_model_file_path, my_model)
                logging.info("Saved final model object (preprocessing + trained model).")

                # Log sklearn model artifact separately for MLflow
                mlflow.sklearn.log_model(trained_model, artifact_path="random_forest_model")
                logging.info("Logged RandomForestClassifier model to MLflow.")

                # Log preprocessing object as an artifact
                mlflow.log_artifact(self.data_transformation_artifact.transformed_object_file_path, artifact_path="preprocessing")
                logging.info("Logged preprocessing object as artifact to MLflow.")

                # Return the artifact with path and metrics
                model_trainer_artifact = ModelTrainerArtifact(
                    trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                    metric_artifact=metric_artifact,
                )
                logging.info(f"Model trainer artifact created: {model_trainer_artifact}")
                return model_trainer_artifact

        except Exception as e:
            logging.error("Error in initiate_model_trainer", exc_info=True)
            raise CustomException(e, sys) from e