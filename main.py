from ippredictor.logger import logging
from ippredictor.exception import IPPPredictorException
import os, sys
from ippredictor.utils import get_collection_as_data_frame
from ippredictor.entity.config_entity import DataIngestionConfig,DataValidationConfig
from ippredictor.entity.config_entity import TrainingPipelineConfig
from ippredictor.components.data_ingestion import DataIngestion
from ippredictor.components.data_validation import DataValidation

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
    # Testing loggers and exception
    #test_logger_and_exception()

    # Transfer data to database
    #get_collection_as_data_frame("INSURANCE","INSURANCE_DETAILS")

    # Instatiation of TrainingPipelineConfig
    training_pipeline_config = TrainingPipelineConfig()

    # Data Ingestion
    data_ingestion_config = DataIngestionConfig(training_pipeline_config=training_pipeline_config)
    data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
    data_ingestion_artifact = data_ingestion.initiate_data_ingestion()

    # Data Validation
    data_validation_config = DataValidationConfig(training_pipeline_config=training_pipeline_config)
    data_validation = DataValidation(data_validation_config= data_validation_config, data_ingestion_artifact=data_ingestion_artifact)
    data_validation.initiate_data_validation()