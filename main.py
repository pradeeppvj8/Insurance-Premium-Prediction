from ippredictor.logger import logging
from ippredictor.exception import IPPPredictorException
import os, sys
from ippredictor.utils import get_collection_as_data_frame
from ippredictor.entity.config_entity import DataIngestionConfig
from ippredictor.entity.config_entity import TrainingPipelineConfig

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
    #test_logger_and_exception()
    #get_collection_as_data_frame("INSURANCE","INSURANCE_DETAILS")
    training_pipeline_config = TrainingPipelineConfig()
    data_ingestion_config = DataIngestionConfig(training_pipeline_config=training_pipeline_config)
    logging.info(data_ingestion_config.to_dict())