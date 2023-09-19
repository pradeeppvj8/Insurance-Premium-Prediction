import numpy as np
import pandas as pd
import os, sys
from ippredictor.exception import IPPPredictorException
from ippredictor.entity.config_entity import DataIngestionConfig
from ippredictor.entity.artifact_entity import DataIngestionArtifact
from ippredictor.logger import logging
from ippredictor.utils import get_collection_as_data_frame
from sklearn.model_selection import train_test_split

class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise IPPPredictorException(e, sys)
        
    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        try:
            logging.info("Exporting collection as dataframe")
            df: pd.DataFrame = get_collection_as_data_frame(
                database_name= self.data_ingestion_config.database_name,
                collection_name= self.data_ingestion_config.collection_name
            )

            # Replace 'na' with Nan
            df.replace(to_replace = "na", value = np.NAN, inplace = True)

            logging.info("Creating feature store directory")
            feature_store_dir = os.path.dirname(self.data_ingestion_config.feature_store_file_path)
            os.makedirs(feature_store_dir, exist_ok=True)

            logging.info("Saving dataframe into feature store file")
            df.to_csv(self.data_ingestion_config.feature_store_file_path, index=False, header=True)

            logging.info("Performing train test split")
            train_df, test_df = train_test_split(df, test_size=self.data_ingestion_config.test_size, random_state=32)
            
            logging.info("Creating dataset directory")
            df_dir = os.path.dirname(self.data_ingestion_config.train_file_path)
            os.makedirs(df_dir, exist_ok=True)

            logging.info("Storing dataset as csv files")
            train_df.to_csv(self.data_ingestion_config.train_file_path, index = False, header = True)
            test_df.to_csv(self.data_ingestion_config.test_file_path, index = False, header = True)

            # Preparing data artifact entity
            data_ingestion_artifact = DataIngestionArtifact(
                feature_store_path=self.data_ingestion_config.feature_store_file_path,
                train_file_path=self.data_ingestion_config.train_file_path,
                test_file_path=self.data_ingestion_config.test_file_path
            )
            return data_ingestion_artifact
        except Exception as e:
            raise IPPPredictorException(e, sys)