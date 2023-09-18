from ippredictor.logger import logging
from ippredictor.exception import IPPPredictorException
import os, sys

def test_logger_and_exception():
    try:
        logging.info("Starting test_logger_and_exception")
        result = 3 / 0
        print(result)
        logging.info("End of test_logger_and_exception")
    except Exception as e:
        logging.error(str(e))
        raise IPPPredictorException(e, sys)
    
if __name__ == "__main__":
    test_logger_and_exception()
