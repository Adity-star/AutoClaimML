import os
import joblib

def save_artifact(artifact, path: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    joblib.dump(artifact, path)

def load_artifact(path: str):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Artifact not found at {path}")
    return joblib.load(path)
