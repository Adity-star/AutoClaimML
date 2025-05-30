import sys
import argparse
import os
import joblib
from AutoClaimML.utils.artifact_io import save_artifact, load_artifact
from AutoClaimML.pipeline.training_pipeline import TrainingPipeline
from AutoClaimML.exception import CustomException
from AutoClaimML.logger import logging


def get_or_run_stage(func, artifact_path):
    if os.path.exists(artifact_path):
        logging.info(f"Loading artifact from {artifact_path}")
        return load_artifact(artifact_path)
    else:
        logging.info(f"Artifact not found. Running function to generate: {artifact_path}")
        artifact = func()
        save_artifact(artifact, artifact_path)
        return artifact
    
# Updated to adjuct to version control
def run_pipeline(stage: str):
    try:
        logging.info(f"Pipeline execution started for stage: {stage}")
        pipeline = TrainingPipeline()

        paths = {
            "data_ingestion": "artifacts/data_ingestion/artifact.pkl",
            "data_validation": "artifacts/data_validation/artifact.pkl",
            "data_transformation": "artifacts/data_transformation/artifact.pkl",
            "model_trainer": "artifacts/model_trainer/artifact.pkl",
            "model_evaluation": "artifacts/model_evaluation/artifact.pkl",
        }
        
        # -------------------- Stage 1: Data Ingesion --------------------
        if stage == "data_ingestion":
            logging.info("Stage: Data Ingestion started.")
            data_ingestion_artifact = get_or_run_stage(pipeline.start_data_ingestion, paths["data_ingestion"])
            print(f"   - Train Data Path: {data_ingestion_artifact.trained_file_path}")
            print(f"   - Test Data Path:  {data_ingestion_artifact.test_file_path}")

            logging.info("Stage: Data Ingestion completed.")

        # -------------------- Stage 2: Data Validation --------------------
        elif stage == "data_validation":
            logging.info("Stage: Data Validation started.")
            data_ingestion_artifact = get_or_run_stage(pipeline.start_data_ingestion, paths["data_ingestion"])
            data_validation_artifact = get_or_run_stage(
                lambda: pipeline.start_data_validation(data_ingestion_artifact), paths["data_validation"]
            )
            print(f"   - Report Path:      {data_validation_artifact.report_file_path}")
            print(f"   - Validation Status:{data_validation_artifact.validation_status}")

            logging.info("Stage: Data Validation completed.")

        # -------------------- Stage 3: Data Transformation --------------------
        elif stage == "data_transformation":
            logging.info("Stage: Data Transformation started.")
            data_ingestion_artifact = get_or_run_stage(pipeline.start_data_ingestion, paths["data_ingestion"])
            data_validation_artifact = get_or_run_stage(
                lambda: pipeline.start_data_validation(data_ingestion_artifact), paths["data_validation"]
            )
            data_transformation_artifact = get_or_run_stage(
                lambda: pipeline.start_data_transformation(data_ingestion_artifact, data_validation_artifact),
                paths["data_transformation"]
            )
            print(f"   - Train Array Path: {data_transformation_artifact.transformed_train_file_path}")
            print(f"   - Test Array Path:  {data_transformation_artifact.transformed_test_file_path}")
            print(f"   - Preprocessor Path:{data_transformation_artifact.transformed_object_file_path}")

            logging.info("Stage: Data Transformation completed.")(">>>>>> Stage 3: Data Transformation completed <<<<<<\n\nx==========x")
        
          # -------------------- Stage 4: Model Training --------------------
        elif stage == "model_trainer":
            logging.info("Stage: Model Trainer started.")
            data_ingestion_artifact = get_or_run_stage(pipeline.start_data_ingestion, paths["data_ingestion"])
            data_validation_artifact = get_or_run_stage(
                lambda: pipeline.start_data_validation(data_ingestion_artifact), paths["data_validation"]
            )
            data_transformation_artifact = get_or_run_stage(
                lambda: pipeline.start_data_transformation(data_ingestion_artifact, data_validation_artifact),
                paths["data_transformation"]
            )
            model_trainer_artifact = get_or_run_stage(
                lambda: pipeline.start_model_trainer(data_transformation_artifact), paths["model_trainer"]
            )
            logging.info("Stage: Model Trainer completed.")

        # -------------------- Stage 5: Model Evaluation --------------------
        elif stage == "model_evaluation":
            logging.info("Stage: Model Evaluation started.")
            data_ingestion_artifact = get_or_run_stage(pipeline.start_data_ingestion, paths["data_ingestion"])
            data_validation_artifact = get_or_run_stage(
                lambda: pipeline.start_data_validation(data_ingestion_artifact), paths["data_validation"]
            )
            data_transformation_artifact = get_or_run_stage(
                lambda: pipeline.start_data_transformation(data_ingestion_artifact, data_validation_artifact),
                paths["data_transformation"]
            )
            model_trainer_artifact = get_or_run_stage(
                lambda: pipeline.start_model_trainer(data_transformation_artifact), paths["model_trainer"]
            )
            model_evaluation_artifact = get_or_run_stage(
                lambda: pipeline.start_model_evaluation(data_ingestion_artifact, model_trainer_artifact),
                paths["model_evaluation"]
            )
            logging.info("Stage: Model Evaluation completed.")

        # -------------------- Stage 6: Model Pusher --------------------
        elif stage == "model_pusher":
            logging.info("Stage: Model Pusher started.")
            data_ingestion_artifact = get_or_run_stage(pipeline.start_data_ingestion, paths["data_ingestion"])
            data_validation_artifact = get_or_run_stage(
                lambda: pipeline.start_data_validation(data_ingestion_artifact), paths["data_validation"]
            )
            data_transformation_artifact = get_or_run_stage(
                lambda: pipeline.start_data_transformation(data_ingestion_artifact, data_validation_artifact),
                paths["data_transformation"]
            )
            model_trainer_artifact = get_or_run_stage(
                lambda: pipeline.start_model_trainer(data_transformation_artifact), paths["model_trainer"]
            )
            model_evaluation_artifact = get_or_run_stage(
                lambda: pipeline.start_model_evaluation(data_ingestion_artifact, model_trainer_artifact),
                paths["model_evaluation"]
            )

            if model_evaluation_artifact.is_model_accepted:
                pipeline.start_model_pusher(model_evaluation_artifact)
            else:
                logging.warning("Model not accepted. Skipping model push.")

        elif stage == "all":
            run_pipeline("data_ingestion")
            run_pipeline("data_validation")
            run_pipeline("data_transformation")
            run_pipeline("model_trainer")
            run_pipeline("model_evaluation")
            run_pipeline("model_pusher")

        else:
            raise ValueError(f"Unknown stage: {stage}")

        logging.info(f"Pipeline stage '{stage}' completed successfully.")

    except CustomException as e:
        logging.error(f"Pipeline failed due to a custom exception: {e}")
        print(f"Pipeline failed: {e}")
    except Exception as e:
        logging.error(f"Pipeline failed due to an unexpected error: {e}")
        print(f"Pipeline failed: {e}")

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
