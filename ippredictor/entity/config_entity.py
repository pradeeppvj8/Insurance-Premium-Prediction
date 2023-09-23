import os, sys
from datetime import datetime
from ippredictor.logger import logging
from ippredictor.exception import IPPPredictorException
from pathlib import Path

FILE_NAME = "insurance.csv"
TRAIN_FILE_NAME = "train.csv"
TEST_FILE_NAME = "test.csv"
TRANSFORMER_OBJECT_PATH = "transformer.pkl"
LABEL_ENCODER_PATH = "label_encoder.pkl"

class TrainingPipelineConfig:
    def __init__(self):
        try:
            self.artifacts_dir = os.path.join(os.getcwd(), "artifacts", f"{datetime.now().strftime('%m%d%Y__%H%M%S')}")
        except Exception as e:
            logging.error(e)
            raise IPPPredictorException(e, sys)
        
class DataIngestionConfig:
    def __init__(self, training_pipeline_config : TrainingPipelineConfig):
        try:
            self.database_name = "INSURANCE"
            self.collection_name = "INSURANCE_DETAILS"
            self.data_ingestion_dir = os.path.join(training_pipeline_config.artifacts_dir, "data_ingestion")
            self.feature_store_file_path = os.path.join(self.data_ingestion_dir, "feature_store", FILE_NAME)
            self.train_file_path = os.path.join(self.data_ingestion_dir,"dataset", TRAIN_FILE_NAME)
            self.test_file_path = os.path.join(self.data_ingestion_dir,"dataset", TEST_FILE_NAME)
            self.test_size = 0.2
        except Exception as e:
            logging.error(e)
            raise IPPPredictorException(e, sys)
        
    def to_dict(self) -> dict:
        try:
            return self.__dict__
        except Exception as e:
            logging.error(e)
            raise IPPPredictorException(e, sys)
        
class DataValidationConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        self.data_validation_dir = os.path.join(training_pipeline_config.artifacts_dir, "data_validation")
        self.report_file_path = os.path.join(self.data_validation_dir, "report.yaml")
        self.missing_value_threshold : float = 0.2
        self.base_df_path = Path("insurance.csv")

class DataTransformationConfig:
    def __init__(self, training_pipeline_config:TrainingPipelineConfig):
        self.data_transformation_dir = os.path.join(training_pipeline_config.artifacts_dir,"data_transformation")
        self.data_transformer_object_path = os.path.join(self.data_transformation_dir, "transformed", TRANSFORMER_OBJECT_PATH)        
        self.data_transformer_train_path = os.path.join(self.data_transformation_dir, "transformed", TRAIN_FILE_NAME.replace("csv","npz"))
        self.data_transformer_test_path = os.path.join(self.data_transformation_dir, "transformed", TEST_FILE_NAME.replace("csv","npz"))
        self.encoder_object_path = os.path.join(self.data_transformation_dir, "label_encoder", LABEL_ENCODER_PATH)