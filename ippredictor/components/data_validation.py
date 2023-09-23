from ippredictor.entity.config_entity import DataValidationConfig
from ippredictor.entity import artifact_entity
from ippredictor.logger import logging
from ippredictor.exception import IPPPredictorException
import sys
import pandas as pd
from scipy.stats import ks_2samp
import numpy as np
from ippredictor.config import TARGET_COLUMN
from ippredictor.utils import convert_columns_to_float,write_yaml_file

class DataValidation:
    def __init__(self, data_validation_config: DataValidationConfig, 
                 data_ingestion_artifact: artifact_entity.DataIngestionArtifact):
        try:
            logging.info("######### DataValidation #########")
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.validation_error = dict()
        except Exception as e:
            raise IPPPredictorException(e, sys)

    def drop_missing_value_columns(self, df:pd.DataFrame, report_key_name: str) -> pd.DataFrame:
        try:
            threshold = self.data_validation_config.missing_value_threshold
            null_report = df.isna().sum() / df.shape[0]
            drop_column_names = null_report[null_report > threshold].index
            self.validation_error[report_key_name] = list(drop_column_names)
            
            logging.info("Dropping columns whose missing value size is greater than the threshold")
            df.drop(list(drop_column_names), axis=1)

            if len(df.columns) == 0:
                return None
            else:
                return df
        except Exception as e:
            raise IPPPredictorException(e, sys)
        
    def required_columns_exist(self, base_df: pd.DataFrame, current_df : pd.DataFrame, report_key_name:str) -> bool:  
        try:
            base_df_columns = list(base_df.columns)
            current_df_columns = list(current_df.columns)
            missing_columns = []

            for base_df_column in base_df_columns:
                if base_df_column not in current_df_columns:
                    logging.info(f"Base column [{base_df_column}] is not available")
                    missing_columns.append(base_df_column)

            if len(missing_columns) > 0:
                self.validation_error[report_key_name] = missing_columns
                return False
            
            return True
        except Exception as e:
            raise IPPPredictorException(e, sys)

    def data_drift(self, base_df: pd.DataFrame, current_df: pd.DataFrame, report_key_name: str):
        try:
            base_columns = base_df.columns
            current_columns = current_df.columns
            drift_report = dict()

            for base_column in base_columns:
                base_data, current_data = base_df[base_column], current_df[base_column]
                same_distribution = ks_2samp(base_data, current_data)

                if same_distribution.pvalue > 0.05:
                    drift_report[base_column] = {
                        "pvalue" : float(same_distribution.pvalue),
                        "same_distribution" : True
                    }
                else:
                    drift_report[base_column] = {
                        "pvalue" : float(same_distribution.pvalue),
                        "same_distribution" : False
                    }

            self.validation_error[report_key_name] = drift_report
        except Exception as e:
            raise IPPPredictorException(e, sys)

    def initiate_data_validation(self):
        try:
            logging.info("Getting required data frames")
            base_df = pd.read_csv(self.data_validation_config.base_df_path)
            train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path)
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)

            logging.info("Replacing 'na' with 'Nan'")
            base_df.replace(to_replace='na', value= np.nan, inplace=True)

            logging.info("Dropping missing values from the datasets")
            base_df = self.drop_missing_value_columns(df=base_df, report_key_name="missing_values_base_df")
            train_df = self.drop_missing_value_columns(df=train_df, report_key_name="missing_values_train_df")
            test_df = self.drop_missing_value_columns(df=test_df, report_key_name="missing_values_test_df")

            logging.info("Converting required columns to float")
            exclude_columns = [TARGET_COLUMN]
            base_df = convert_columns_to_float(base_df, exclude_columns=exclude_columns)
            train_df = convert_columns_to_float(train_df, exclude_columns=exclude_columns)
            test_df = convert_columns_to_float(test_df, exclude_columns=exclude_columns)

            logging.info("Checking if required columns exist")
            train_df_columns_status = self.required_columns_exist(base_df=base_df, current_df=train_df,
                                                                report_key_name="missing_columns_train_df")
            test_df_columns_status = self.required_columns_exist(base_df=base_df, current_df=test_df,
                                                                report_key_name="missing_columns_test_df")
            
            logging.info("Performing data drift")
            if train_df_columns_status:
                self.data_drift(base_df=base_df, current_df=train_df, report_key_name="data_drift_train_df")

            if test_df_columns_status:
                self.data_drift(base_df=base_df, current_df=test_df, report_key_name="data_drift_test_df")

            logging.info("Writing report.yaml file")
            write_yaml_file(self.data_validation_config.report_file_path, self.validation_error)

            logging.info("Preparing data validation artifact")
            data_validation_artifact = artifact_entity.DataValidationArtifact(
                report_file_path=self.data_validation_config.report_file_path
            )

            return data_validation_artifact
        except Exception as e:
            raise IPPPredictorException(e, sys)