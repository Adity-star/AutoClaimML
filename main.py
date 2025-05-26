# main.py

import sys
from src.pipeline.training_pipeline import TrainingPipeline
from src.exception import CustomException
from src.logger import logging


def run_pipeline():
    """
    Entry point for executing the ML training pipeline.
    Currently executes only the data ingestion component.
    """
    try:
        logging.info("Pipeline execution started.")

        pipeline = TrainingPipeline()
        data_ingestion_artifact = pipeline.start_data_ingestion()

        logging.info("Pipeline execution completed successfully.")
        print(f"✅ Data Ingestion Completed!")
        print(f"Train Data Path: {data_ingestion_artifact.trained_file_path}")
        print(f"Test Data Path: {data_ingestion_artifact.test_file_path}")

    except CustomException as e:
        logging.error(f"Pipeline failed due to a custom exception: {e}")
        print(f"❌ Pipeline failed: {e}")

    except Exception as e:
        logging.error(f"Pipeline failed due to an unexpected error: {e}")
        print(f"❌ Pipeline failed: {e}")


if __name__ == "__main__":
    run_pipeline()
