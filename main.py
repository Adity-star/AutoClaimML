import sys
from src.pipeline.training_pipeline import TrainingPipeline
from src.exception import CustomException
from src.logger import logging


def run_pipeline():
    """
    Entry point for executing the ML training pipeline.
    Executes data ingestion and validation stages with logging.
    """
    try:
        logging.info("Pipeline execution started.")
        pipeline = TrainingPipeline()

        # -------------------- Stage 1: Data Ingestion --------------------
        logging.info("Stage 1: Data Ingestion started.")
        data_ingestion_artifact = pipeline.start_data_ingestion()
        logging.info("✅ Stage 1: Data Ingestion completed.")
        print(f"✅ Data Ingestion Completed!")
        print(f"📁 Train Data Path: {data_ingestion_artifact.trained_file_path}")
        print(f"📁 Test Data Path: {data_ingestion_artifact.test_file_path}")

        # -------------------- Stage 2: Data Validation --------------------
        logging.info("Stage 2: Data Validation started.")
        data_validation_artifact = pipeline.start_data_validation(data_ingestion_artifact)
        logging.info("✅ Stage 2: Data Validation completed.")
        print(f"✅ Data Validation Completed!")
        print(f"📄 Validation Report: {data_validation_artifact.validation_report_file_path}")
        print(f"✔️ Validation Status: {data_validation_artifact.validation_status}")

        logging.info("🏁 Pipeline execution completed successfully.")

    except CustomException as e:
        logging.error(f"🔥 Pipeline failed due to a custom exception: {e}")
        print(f"❌ Pipeline failed: {e}")

    except Exception as e:
        logging.error(f"🔥 Pipeline failed due to an unexpected error: {e}")
        print(f"❌ Pipeline failed: {e}")


if __name__ == "__main__":
    run_pipeline()
