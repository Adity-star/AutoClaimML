import sys
import argparse
from AutoClaimML.pipeline.training_pipeline import TrainingPipeline
from AutoClaimML.exception import CustomException
from AutoClaimML.logger import logging


# Updated to adjuct to version control
def run_pipeline(stage: str):
    """
    Runs specific pipeline stage(s) based on the input argument.
    """
    try:
        logging.info(f"Pipeline execution started for stage: {stage}")
        pipeline = TrainingPipeline()
        
        # -------------------- Stage 1: Data Ingesion --------------------
        if stage == "data_ingestion":
            logging.info("Stage: Data Ingestion started.")
            data_ingestion_artifact = pipeline.start_data_ingestion()
            print(f"   - Train Data Path: {data_ingestion_artifact.trained_file_path}")
            print(f"   - Test Data Path:  {data_ingestion_artifact.test_file_path}")
            logging.info("Stage: Data Ingestion completed.")

        # -------------------- Stage 2: Data Validation --------------------
        elif stage == "data_validation":
            logging.info("Stage: Data Validation started.")
            data_ingestion_artifact = pipeline.start_data_ingestion()
            data_validation_artifact = pipeline.start_data_validation(data_ingestion_artifact)
            print(f"   - Report Path:      {data_validation_artifact.report_file_path}")
            print(f"   - Validation Status:{data_validation_artifact.validation_status}")
            logging.info("Stage: Data Validation completed.")

        # -------------------- Stage 3: Data Transformation --------------------
        elif stage == "data_transformation":
            logging.info("Stage: Data Transformation started.")
            data_ingestion_artifact = pipeline.start_data_ingestion()
            data_validation_artifact = pipeline.start_data_validation(data_ingestion_artifact)
            data_transformation_artifact = pipeline.start_data_transformation(
                data_ingestion_artifact, data_validation_artifact)
            print(f"   - Train Array Path: {data_transformation_artifact.transformed_train_file_path}")
            print(f"   - Test Array Path:  {data_transformation_artifact.transformed_test_file_path}")
            print(f"   - Preprocessor Path:{data_transformation_artifact.transformed_object_file_path}")
            logging.info("Stage: Data Transformation completed.")(">>>>>> Stage 3: Data Transformation completed <<<<<<\n\nx==========x")
        
          # -------------------- Stage 4: Model Training --------------------
        elif stage == "model_trainer":
            logging.info("Stage: Model Trainer started.")
            data_ingestion_artifact = pipeline.start_data_ingestion()
            data_validation_artifact = pipeline.start_data_validation(data_ingestion_artifact)
            data_transformation_artifact = pipeline.start_data_transformation(
                data_ingestion_artifact, data_validation_artifact)
            model_trainer_artifact = pipeline.start_model_trainer(data_transformation_artifact)
            logging.info("Stage: Model Trainer completed.")

        # -------------------- Stage 5: Model Evaluation --------------------
        elif stage == "model_evaluation":
            logging.info("Stage: Model Evaluation started.")
            data_ingestion_artifact = pipeline.start_data_ingestion()
            data_validation_artifact = pipeline.start_data_validation(data_ingestion_artifact)
            data_transformation_artifact = pipeline.start_data_transformation(
                data_ingestion_artifact, data_validation_artifact)
            model_trainer_artifact = pipeline.start_model_trainer(data_transformation_artifact)
            model_evaluation_artifact = pipeline.start_model_evaluation(
                data_ingestion_artifact, model_trainer_artifact)
            logging.info("Stage: Model Evaluation completed.")

        # -------------------- Stage 6: Model Pusher --------------------
        elif stage == "model_pusher":
            logging.info("Stage: Model Pusher started.")
            data_ingestion_artifact = pipeline.start_data_ingestion()
            data_validation_artifact = pipeline.start_data_validation(data_ingestion_artifact)
            data_transformation_artifact = pipeline.start_data_transformation(
                data_ingestion_artifact, data_validation_artifact)
            model_trainer_artifact = pipeline.start_model_trainer(data_transformation_artifact)
            model_evaluation_artifact = pipeline.start_model_evaluation(
                data_ingestion_artifact, model_trainer_artifact)
            if model_evaluation_artifact.is_model_accepted:
                model_pusher_artifact = pipeline.start_model_pusher(model_evaluation_artifact)
                logging.info("Stage: Model Pusher completed.")
            else:
                logging.warning("Model was not accepted. Deployment skipped.")

        elif stage == "all":
            logging.info("Stage: Full Pipeline started.")
            data_ingestion_artifact = pipeline.start_data_ingestion()
            data_validation_artifact = pipeline.start_data_validation(data_ingestion_artifact)
            data_transformation_artifact = pipeline.start_data_transformation(
                data_ingestion_artifact, data_validation_artifact)
            model_trainer_artifact = pipeline.start_model_trainer(data_transformation_artifact)
            model_evaluation_artifact = pipeline.start_model_evaluation(
                data_ingestion_artifact, model_trainer_artifact)
            if model_evaluation_artifact.is_model_accepted:
                model_pusher_artifact = pipeline.start_model_pusher(model_evaluation_artifact)
            else:
                logging.warning("Model was not accepted. Deployment skipped.")
            logging.info("Stage: Full Pipeline completed.")

        else:
            raise ValueError(f"Unknown stage: {stage}")

        logging.info(f"Pipeline stage '{stage}' completed successfully.")

    except CustomException as e:
        logging.error(f"Pipeline failed due to a custom exception: {e}")
        print(f"Pipeline failed: {e}")
    except Exception as e:
        logging.error(f"Pipeline failed due to an unexpected error: {e}")
        print(f"Pipeline failed: {e}")



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--stage",
        type=str,
        required=True,
        choices=[
            "data_ingestion", "data_validation", "data_transformation",
            "model_trainer", "model_evaluation", "model_pusher", "all"
        ],
        help="Specify which pipeline stage to run"
    )
    args = parser.parse_args()
    run_pipeline(args.stage)
