# demo.py


from src.logger import logging
from src.exception import CustomException
import sys

try:
     a = 1+'Z'
except Exception as e:
     logging.info(e)
     raise CustomException(e, sys) from e