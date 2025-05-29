import os
from pathlib import Path
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

project_name = "AutoClaimML"

def create_project_structure(project_name: str = "src"):
    list_of_files = [
        f"src/{project_name}/__init__.py",
        f"src/{project_name}/components/__init__.py",
        f"src/{project_name}/components/data_ingestion.py",  
        f"src/{project_name}/components/data_validation.py",
        f"src/{project_name}/components/data_transformation.py",
        f"src/{project_name}/components/model_trainer.py",
        f"src/{project_name}/components/model_evaluation.py",
        f"src/{project_name}/components/model_pusher.py",
        f"src/{project_name}/configuration/__init__.py",
        f"src/{project_name}/configuration/mongo_db_connection.py",
        f"src/{project_name}/configuration/aws_connection.py",
        f"src/{project_name}/cloud_storage/__init__.py",
        f"src/{project_name}/cloud_storage/aws_storage.py",
        f"src/{project_name}/data_access/__init__.py",
        f"src/{project_name}/constants/__init__.py",
        f"src/{project_name}/entity/__init__.py",
        f"src/{project_name}/entity/config_entity.py",
        f"src/{project_name}/entity/artifact_entity.py",
        f"src/{project_name}/entity/estimator.py",
        f"src/{project_name}/entity/s3_estimator.py",
        f"src/{project_name}/exception/__init__.py",
        f"src/{project_name}/logger/__init__.py",
        f"src/{project_name}/pipeline/__init__.py",
        f"src/{project_name}/pipeline/training_pipeline.py",
        f"src/{project_name}/pipeline/prediction_pipeline.py",
        f"src/{project_name}/utils/__init__.py",
        f"src/{project_name}/utils/main_utils.py",
        "app.py",
        "requirements.txt",
        "Dockerfile",
        ".dockerignore",
        "demo.py",
        "setup.py",
        "pyproject.toml",
        "config/model.yaml",
        "config/schema.yaml",
    ]

    for filepath in list_of_files:
        filepath = Path(filepath)
        filedir, filename = os.path.split(filepath)
        
        if filedir != "":
            os.makedirs(filedir, exist_ok=True)
            logging.info(f"Directory created or already exists: {filedir}")

        if not os.path.exists(filepath) or os.path.getsize(filepath) == 0:
            with open(filepath, "w") as f:
                f.write(f"# {filename}\n")
            logging.info(f"Created new file: {filepath}")
        else:
            logging.info(f"File already exists and is not empty: {filepath}")

def main():
    create_project_structure(project_name=project_name)

if __name__ == "__main__":
    main()
