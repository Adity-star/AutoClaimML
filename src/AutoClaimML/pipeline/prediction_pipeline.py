# prediction_pipeline.py
import sys
from pandas import DataFrame

from AutoClaimML.entity.config_entity import VehiclePredictorConfig
from AutoClaimML.entity.s3_estimator import Proj1Estimator
from AutoClaimML.logger import logging
from AutoClaimML.exception import CustomException


class VehicleData:
    def __init__(
        self,
        Gender: str,
        Age: int,
        Driving_License: int,
        Region_Code: float,
        Previously_Insured: int,
        Annual_Premium: float,
        Policy_Sales_Channel: float,
        Vintage: int,
        Vehicle_Age_lt_1_Year: int,
        Vehicle_Age_gt_2_Years: int,
        Vehicle_Damage_Yes: int
    ):
        """
        VehicleData constructor for preparing input data for prediction.
        """
        try:
            self.Gender = Gender
            self.Age = Age
            self.Driving_License = Driving_License
            self.Region_Code = Region_Code
            self.Previously_Insured = Previously_Insured
            self.Annual_Premium = Annual_Premium
            self.Policy_Sales_Channel = Policy_Sales_Channel
            self.Vintage = Vintage
            self.Vehicle_Age_lt_1_Year = Vehicle_Age_lt_1_Year
            self.Vehicle_Age_gt_2_Years = Vehicle_Age_gt_2_Years
            self.Vehicle_Damage_Yes = Vehicle_Damage_Yes
        except Exception as e:
            raise CustomException(e, sys) from e
        
    def get_vehicle_data_as_dict(self) -> dict:
        """
        Converts input features to a dictionary format suitable for DataFrame creation.
        """
        try:
            logging.info("Creating dictionary from VehicleData input")

            return {
                "Gender": [self.Gender],
                "Age": [self.Age],
                "Driving_License": [self.Driving_License],
                "Region_Code": [self.Region_Code],
                "Previously_Insured": [self.Previously_Insured],
                "Annual_Premium": [self.Annual_Premium],
                "Policy_Sales_Channel": [self.Policy_Sales_Channel],
                "Vintage": [self.Vintage],
                "Vehicle_Age_lt_1_Year": [self.Vehicle_Age_lt_1_Year],
                "Vehicle_Age_gt_2_Years": [self.Vehicle_Age_gt_2_Years],
                "Vehicle_Damage_Yes": [self.Vehicle_Damage_Yes],
            }

        except Exception as e:
            raise CustomException(e, sys) from e

    def get_vehicle_input_data_frame(self) -> DataFrame:
        """
        Converts input features to a pandas DataFrame.
        """
        try:
            vehicle_input_dict = self.get_vehicle_data_as_dict()
            return DataFrame(vehicle_input_dict)
        except Exception as e:
            raise CustomException(e, sys) from e
        

class VehicleDataClassifier:
    def __init__(self, prediction_pipeline_config: VehiclePredictorConfig = VehiclePredictorConfig()) -> None:
        """
        Initializes the classifier with prediction config.
        """
        try:
            self.prediction_pipeline_config = prediction_pipeline_config
        except Exception as e:
            raise CustomException(e, sys) from e

    def predict(self, dataframe: DataFrame) -> str:
        """
        Predicts based on input DataFrame using the model from S3.
        """
        try:
            logging.info("Entered predict method of VehicleDataClassifier")

            model = Proj1Estimator(
                bucket_name=self.prediction_pipeline_config.model_bucket_name,
                model_path=self.prediction_pipeline_config.model_file_path,
            )

            prediction = model.predict(dataframe)

            logging.info("Exited predict method of VehicleDataClassifier")
            return prediction

        except Exception as e:
            raise CustomException(e, sys) from e