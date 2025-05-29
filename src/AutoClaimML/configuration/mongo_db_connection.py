# mongo_db_connection.py

import os
import sys
import pymongo
import certifi

from AutoClaimML.exception import CustomException
from AutoClaimML.logger import logging
from AutoClaimML.constants import DATABASE_NAME, MONGODB_URL_KEY

# Load the certificate authority file to avoid timeout errors when connecting to MongoDB
ca = certifi.where()

class MongoDBClient:
    """
    MongoDBClient is responsible for creating and managing a secure connection to a MongoDB database.
    
    Attributes
    ----------
    client : MongoClient
        A class-level MongoClient instance shared across all MongoDBClient instances.
    database : Database
        The connected MongoDB database instance.
    
    Methods
    -------
    __init__(database_name: str = DATABASE_NAME) -> None
        Initializes the MongoDB connection to the specified database.
    get_database(name: str)
        Returns a reference to another MongoDB database if needed.
    """

    client = None  # Shared MongoDB client instance

    def __init__(self, database_name: str = DATABASE_NAME) -> None:
        """
        Initializes a connection to the MongoDB database.

        Parameters
        ----------
        database_name : str, optional
            The name of the database to connect to (default is DATABASE_NAME).

        Raises
        ------
        MyException
            If the MongoDB URL is missing or the connection fails.
        """
        try:
            # Load MongoDB URL from environment variable
            mongo_db_url = os.getenv(MONGODB_URL_KEY)
            if not mongo_db_url:
                raise ValueError(f"Environment variable '{MONGODB_URL_KEY}' is not set.")
            

             # Load TLS certificate
            ca_file = certifi.where()
            if not ca_file:
                raise RuntimeError("Unable to locate TLS CA certificate using certifi.")

            # Create MongoClient only once
            if MongoDBClient.client is None:
                MongoDBClient.client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca_file)
                logging.info("MongoDB client initialized.")

            # Assign client and database reference
            self.client = MongoDBClient.client
            self.database = self.client[database_name]
            self.database_name = database_name

            logging.info(f"Connected to MongoDB database: '{database_name}'")

            
        except Exception as e:
            raise CustomException(e, sys)
        
    def get_database(self, name: str):
        """
        Returns a MongoDB database instance by name.

        Parameters
        ----------
        name : str
            The name of the database to retrieve.

        Returns
        -------
        Database
            A reference to the requested MongoDB database.
        """
        try:
            logging.info(f"Switching to MongoDB database: '{name}'")
            return self.client[name]
        except Exception as e:
            raise CustomException(e, sys)