import sys
import pandas as pd
import numpy as np
from typing import Optional

from src.configuration.mongo_db_connection import MongoDBClient
from src.constants import DATABASE_NAME, COLLECTION_NAME
from src.exception import CustomException
from src.logger import logging


class VehicleDB:
    """
    A utility class for exporting MongoDB collection data as a pandas DataFrame.
    """

    def __init__(self) -> None:
        """
        Initializes the MongoDB client with the default database.
        """
        try:
            self.mongo_client = MongoDBClient(database_name=DATABASE_NAME)
            logging.info("VehicleDB MongoDB client initialized.")
        except Exception as e:
            raise CustomException(e, sys)
        
    def export_collection_as_dataframe(
        self,
        collection_name: str,
        database_name: Optional[str] = None
    ) -> pd.DataFrame:
        """
        Exports a MongoDB collection as a pandas DataFrame.

        Parameters
        ----------
        collection_name : str
            The name of the MongoDB collection to export.
        database_name : Optional[str]
            The name of the MongoDB database (defaults to the configured DATABASE_NAME).

        Returns
        -------
        pd.DataFrame
            A DataFrame containing the collection data.
            '_id' column is removed.
            String "na" values are replaced with np.nan.

        Raises
        ------
        MyException
            If the database connection or data fetch fails.
        """
        try:
            # Choose the correct database
            db = (
                self.mongo_client.database
                if database_name is None
                else self.mongo_client.get_database(database_name)
            )

            collection = db[COLLECTION_NAME]
            logging.info(f"Fetching data from MongoDB collection: '{collection_name}'")

            # Convert documents to DataFrame
            records = list(collection.find())
            df = pd.DataFrame(records)
            logging.info(f"Fetched {len(df)} records from MongoDB.")

            # Drop MongoDB '_id' field if it exists
            if "_id" in df.columns:
                df.drop(columns=["_id"], inplace=True)

            # Replace "na" strings with np.nan
            df.replace({"na": np.nan}, inplace=True)

            return df

        except Exception as e:
            raise CustomException(e, sys)