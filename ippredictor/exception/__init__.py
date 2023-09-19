import os, sys
from ippredictor.logger import logging

class IPPPredictorException(Exception):
    def __init__(self, error_message : Exception, error_detail: sys):
        super().__init__(error_message)
        self.error_message = IPPPredictorException.get_error_message_detail(error_message, error_detail)
        logging.exception(self.error_message)


    @staticmethod
    def get_error_message_detail(error_message : Exception, error_detail: sys) -> str:
        _,_,exc_tb = error_detail.exc_info()
        # Line number where error occurred
        line_no = exc_tb.tb_frame.f_lineno
        # File name where error occurred
        file_name = exc_tb.tb_frame.f_code.co_filename
        # Preparing error message
        error_message = f" Error [{error_message}] occurred in [{file_name}:{line_no}]"
        return error_message
    
    def __str__(self) -> str:
        """
        Method responsible for showing error message when the exception is raised
        """
        return self.error_message

