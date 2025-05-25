import sys
import traceback
import logging


# Function to Format Exception Details
def format_exception_details(error: Exception, tb_info=None) -> str:
    """
    Extracts detailed error information including file name, line number, and the error message.

    Args:
        error (Exception): The original exception object.
        tb_info (traceback): Optional traceback object (defaults to current traceback).

    Returns:
        str: Formatted error message.
    """

     # If traceback isn't passed, extract the current one
    if tb_info is None:
        _, _, tb_info = sys.exc_info()

    if tb_info is not None:
        file_name = tb_info.tb_frame.f_code.co_filename
        line_number = tb_info.tb_lineno
        error_message = f"Exception occurred in file [{file_name}], line [{line_number}]: {error}"
    else:
        error_message = f"Exception: {error}"
    # Log the error message
    logging.error(error_message)

    return error_message

class CustomException(Exception):
    """
    Custom exception class that includes detailed traceback information.
    """

    def __init__(self, error: Exception, tb_info=None):
        """
        Initialize the exception with detailed error info.

        Args:
            error (Exception): The original exception.
            tb_info (traceback, optional): A traceback object, defaults to sys.exc_info().
        """
        # Format and store the detailed error message
        self.message = format_exception_details(error, tb_info)
        super().__init__(self.message)

    def __str__(self) -> str:
        """
        Returns the string representation of the error message.
        """
        return self.message
