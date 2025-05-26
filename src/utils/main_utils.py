# main_utils.py

import os 
import sys
import numpy as np 
from pandas import DataFrame
import dill 
import yaml 


from src.exception import CustomException
import src.logger as logging


def read_yaml_file(file_path: str) -> dict:
    """
    Reads a YAML file and returns its contents as a dictionary.

    :param file_path: Path to the YAML file.
    :return: Parsed YAML content.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as yaml_file:
            return yaml.safe_load(yaml_file) or {}
            logging.info(f'YAML file read successfully: {file_path}')
    except Exception as e:
        logging.error(f"Failed to read YAML file: {file_path}")
        raise CustomException(e, sys)
    


def write_yaml_file(file_path: str, content: dict, replace: bool = False) -> None:
    """
    Writes the given content to a YAML file.

    :param file_path: Path to the output YAML file.
    :param content: Data to write (must be YAML-serializable).
    :param replace: If True, will overwrite an existing file.
    """
    try:
        if replace and os.path.exists(file_path):
            os.remove(file_path)
        
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "w", encoding="utf-8") as file:
            yaml.dump(content, file, default_flow_style=False, allow_unicode=True)
    except Exception as e:
        logging.error(f"Failed to write YAML file: {file_path}")
        raise CustomException(e, sys)
    
    

def load_object(file_path: str) -> object:
    """
    Loads and returns a serialized object from the specified file path.

    Args:
        file_path (str): Path to the serialized file.

    Returns:
        object: The deserialized Python object.
    """
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found at path: {file_path}")
        
        with open(file_path, "rb") as file_obj:
            return dill.load(file_obj)

    except Exception as e:
        logging.error(f"Failed to load object from file: {file_path}")
        raise CustomException(e, sys)
    

    
def save_numpy_array_data(file_path: str, array: np.ndarray) -> None:
    """
    Saves a numpy array to the specified file path.

    Args:
        file_path (str): Path to the file where data will be saved.
        array (np.ndarray): Numpy array to save.
    """
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'wb') as file_obj:
            np.save(file_obj, array)
    except Exception as e:
        raise CustomException(e, sys)
    


def load_numpy_array_data(file_path: str) -> np.ndarray:
    """
    Loads a numpy array from the specified file path.

    Args:
        file_path (str): Path to the file from which data will be loaded.

    Returns:
        np.ndarray: Loaded numpy array.
    """
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        with open(file_path, 'rb') as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise CustomException(e, sys)



def save_object(file_path: str, obj: object) -> None:
    """
    Saves a Python object to a file using dill.

    Args:
        file_path (str): Path where the object should be saved.
        obj (object): The Python object to serialize.
    """
    logging.info("🔧 Starting save_object...")

    try:
        # Ensure the directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Save the object
        with open(file_path, "wb") as file_obj:
            dill.dump(obj, file_obj)

        logging.info(f"✅ Object saved successfully at {file_path}")

    except Exception as e:
        logging.error("❌ Failed to save object.")
        raise CustomException(e, sys)


    




