# data_ingestion.py

import os
import sys

from pandas import DataFrame
from src.entity.config_entity import DataIngestionConfig
from src.data_access.vehicle_db import VehicleDB
from src.entity.artifact_entity import DataIngestionArtifact
from src.logger import logging
from src.exception import CustomException
from src.configuration.configuration import ConfigurationManager