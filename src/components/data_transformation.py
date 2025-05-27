# data_transformation.py
import sys 
import numpy as np
import pandas as pd
from imblearn.combine import SMOTEENN
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.compose import ColumnTransformer

from src.constants import TARGET_COLUMN, SCHEMA_FILE_PATH, CURRENT_YEAR
from src.entity.config_entity import DataTransformationConfig
from src.entity.artifact_entity import (DataIngestionArtifact,
                                        DataValidationArtifact,
                                        DataTransformationArtifact)

from src.exception import CustomException
from src.logger import logging
from src.utils.main_utils import read_yaml_file, save_numpy_array_data,save_object



class DataTransformation:
    """
    Performs feature transformation including scaling, encoding, and balancing.
    """
    def __init__(
        self,
        data_ingestion_artifact: DataIngestionArtifact,
        data_transformation_config: DataTransformationConfig,
        data_validation_artifact: DataValidationArtifact
    ):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_transformation_config = data_transformation_config
            self.data_validation_artifact = data_validation_artifact

            logging.info(f"Reading schema from: {SCHEMA_FILE_PATH}")
            self._schema_config = read_yaml_file(file_path=SCHEMA_FILE_PATH)

            if not self._schema_config:
                raise ValueError("Schema file is empty or invalid.")

        except Exception as e:
            raise CustomException(f"Error initializing DataTransformation: {e}", sys)



    @staticmethod
    def read_data(file_path: str) -> pd.DataFrame:
        """
        Reads a CSV file and returns a DataFrame.
        """
        try:
            logging.info(f"Reading data from file: {file_path}")
            df = pd.read_csv(file_path)
            logging.info(f"Data shape: {df.shape}")
            return df
        except Exception as e:
            raise CustomException(f"Failed to read data from {file_path}: {e}", sys)

     

    def get_data_transformer_object(self) -> Pipeline:
        """
        Creates and returns a data transformer pipeline that includes:
        - Standard scaling for numerical features
        - Min-Max scaling for specified columns
        - Leave remaining columns untouched (passthrough)
        
        NOTE: Dummy variable creation, gender mapping, or type adjustments
        are expected to be handled earlier or in separate custom transformers.
        """
        logging.info("Entered get_data_transformer_object method of DataTransformation class")

        try:
            # Load column config from schema
            num_features = self._schema_config.get('num_features', [])
            mm_columns = self._schema_config.get('mm_columns', [])
            logging.info(f"Schema columns loaded: num_features={num_features}, mm_columns={mm_columns}")

            # Ensure there is no overlap
            overlap = set(num_features) & set(mm_columns)
            if overlap:
                raise ValueError(f"Columns found in both scalers: {overlap}")

            # Define individual transformers
            numeric_transformer = StandardScaler()
            minmax_transformer = MinMaxScaler()

            # Define column-wise transformer
            preprocessor = ColumnTransformer(
                transformers=[
                    ("standard_scaler", numeric_transformer, num_features),
                    ("minmax_scaler", minmax_transformer, mm_columns),
                ],
                remainder='passthrough'  # Other columns stay unchanged
            )

            # Build final pipeline
            pipeline = Pipeline(steps=[
                ("preprocessor", preprocessor)
            ])

            logging.info("Data transformation pipeline created successfully.")
            return pipeline

        except Exception as e:
            logging.exception("Exception occurred in get_data_transformer_object")
            raise CustomException(f"Failed to create transformer pipeline: {e}", sys) from e



    def _map_gender_column(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Maps 'Gender' column values:
        - 'Female' → 0
        - 'Male' → 1
        """
        try:
            logging.info("Mapping 'Gender' column to binary values (Female=0, Male=1)")
            if 'Gender' in df.columns:
                df['Gender'] = df['Gender'].map({'Female': 0, 'Male': 1}).astype(int)
            else:
                logging.warning("'Gender' column not found in dataframe.")
            return df
        except Exception as e:
            logging.exception("Failed to map 'Gender' column")
            raise CustomException(e, sys)



    def _create_dummy_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Applies one-hot encoding to categorical columns, dropping the first category to avoid multicollinearity.
        """
        try:
            logging.info("Creating dummy variables (one-hot encoding) for categorical features")
            df = pd.get_dummies(df, drop_first=True)
            return df
        except Exception as e:
            logging.exception("Failed to create dummy variables")
            raise CustomException(e, sys)



    def _rename_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Renames columns to make them compatible (e.g., replacing symbols) and casts dummy columns to int.
        """
        try:
            logging.info("Renaming specific columns and casting dummy columns to int")

            rename_map = {
                "Vehicle_Age_< 1 Year": "Vehicle_Age_lt_1_Year",
                "Vehicle_Age_> 2 Years": "Vehicle_Age_gt_2_Years"
            }
            df.rename(columns=rename_map, inplace=True)

            dummy_cols_to_cast = [
                "Vehicle_Age_lt_1_Year",
                "Vehicle_Age_gt_2_Years",
                "Vehicle_Damage_Yes"
            ]
            for col in dummy_cols_to_cast:
                if col in df.columns:
                    df[col] = df[col].astype(int)

            return df
        except Exception as e:
            logging.exception("Failed to rename or cast dummy columns")
            raise CustomException(e, sys)
        


    def _drop_id_column(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Drops the 'id' column or any column specified in the schema's 'drop_columns' field.
        """
        try:
            drop_col = self._schema_config.get('drop_columns')

            if drop_col and drop_col in df.columns:
                logging.info(f"Dropping column '{drop_col}' as specified in schema.")
                df = df.drop(drop_col, axis=1)
            else:
                logging.warning(f"Column '{drop_col}' not found in dataframe or not specified in schema.")

            return df

        except Exception as e:
            logging.exception("Exception occurred while dropping ID column.")
            raise CustomException(e, sys)
        
    def initiate_data_transformation(self) -> DataTransformationArtifact:
        """
        Executes the full data transformation process:
        - Validates input status
        - Reads and processes train/test datasets
        - Applies custom transformations
        - Scales features
        - Handles class imbalance using SMOTEENN
        - Saves transformed arrays and preprocessing object
        
        Returns:
            DataTransformationArtifact: Paths to saved preprocessor and datasets
        """
        try:
            logging.info("Data Transformation process started.")

            # Validation check
            if not self.data_validation_artifact.validation_status:
                raise ValueError(f"Data Validation Failed: {self.data_validation_artifact.message}")

            # Load raw data
            train_df = self.read_data(self.data_ingestion_artifact.trained_file_path)
            test_df = self.read_data(self.data_ingestion_artifact.test_file_path)
            logging.info("Train and test datasets loaded successfully.")

            # Separate input and target features
            input_feature_train_df = train_df.drop(columns=[TARGET_COLUMN])
            target_feature_train_df = train_df[TARGET_COLUMN]

            input_feature_test_df = test_df.drop(columns=[TARGET_COLUMN])
            target_feature_test_df = test_df[TARGET_COLUMN]

            logging.info("Input and target features separated.")

            # Apply preprocessing steps
            def preprocess(df: pd.DataFrame) -> pd.DataFrame:
                df = self._drop_id_column(df)
                df = self._map_gender_column(df)
                df = self._create_dummy_columns(df)
                df = self._rename_columns(df)
                return df

            input_feature_train_df = preprocess(input_feature_train_df)
            input_feature_test_df = preprocess(input_feature_test_df)
            logging.info("Custom transformations applied to train and test datasets.")

            # Get preprocessor pipeline
            preprocessor = self.get_data_transformer_object()

            # Apply transformation
            input_feature_train_arr = preprocessor.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessor.transform(input_feature_test_df)
            logging.info("Feature scaling transformation applied.")

            # Address class imbalance
            logging.info("Applying SMOTEENN for class imbalance...")
            smt = SMOTEENN(sampling_strategy="minority", random_state=42)
            input_feature_train_final, target_feature_train_final = smt.fit_resample(
                input_feature_train_arr, target_feature_train_df)
            input_feature_test_final, target_feature_test_final = smt.fit_resample(
                input_feature_test_arr, target_feature_test_df)
            logging.info("SMOTEENN applied on training and test datasets.")

            # Combine features and labels
            train_arr = np.c_[input_feature_train_final, target_feature_train_final]
            test_arr = np.c_[input_feature_test_final, target_feature_test_final]

            # Save preprocessor and arrays
            save_object(self.data_transformation_config.transformed_object_file_path, preprocessor)
            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path, array=train_arr)
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path, array=test_arr)
            logging.info("Transformed data and preprocessor object saved successfully.")

            # Return artifact
            logging.info("Data Transformation completed.")
            return DataTransformationArtifact(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path
            )

        except Exception as e:
            logging.exception("Exception occurred during data transformation")
            raise CustomException(e, sys) from e






