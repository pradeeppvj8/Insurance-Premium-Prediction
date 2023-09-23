from ippredictor.entity import artifact_entity, config_entity
from ippredictor.logger import logging
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import RobustScaler
from ippredictor.exception import IPPPredictorException
import sys
import pandas as pd
import numpy as np
from ippredictor.logger import logging
from ippredictor.config import TARGET_COLUMN
from sklearn.preprocessing import LabelEncoder
from ippredictor import utils

class DataTransformation:
    def __init__(self, data_transformation_config:config_entity.DataTransformationConfig,
                 data_ingestion_artifact: artifact_entity.DataIngestionArtifact):
        logging.info("\n\n##################### Data Transformation Stage Started #####################\n\n")
        self.data_transformation_config = data_transformation_config
        self.data_ingestion_artifact = data_ingestion_artifact

    @classmethod
    def get_data_transformer_object(cls) -> Pipeline:
        try:
            # Missing value imputer
            simple_imputer = SimpleImputer(strategy="constant", fill_value=0)
            # Data scaling
            robust_scaler = RobustScaler()

            # Creating the pipeline
            pipeline = Pipeline(steps=[
                ('Imputer' , simple_imputer),
                ('RobustScaler' , robust_scaler)
            ])

            return pipeline
        except Exception as e:
            raise IPPPredictorException(e, sys)

    
    def initiate_data_transformation(self) -> artifact_entity.DataTransformationArtifact:
        try:
            logging.info("Getting train and test dataframes")
            train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path)
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)

            logging.info("Splitting dependent and independent features")
            input_feature_train_df = train_df.drop(TARGET_COLUMN, axis=1)
            input_feature_test_df = test_df.drop(TARGET_COLUMN, axis=1)
            target_feature_train_df = train_df[TARGET_COLUMN]
            target_feature_test_df = test_df[TARGET_COLUMN]

            # Instantiating label encoder
            label_encoder = LabelEncoder()

            logging.info("Performing label encoding for categorical features")
            for col in input_feature_train_df.columns:
                if input_feature_train_df[col].dtypes == 'O':
                    input_feature_train_df[col] = label_encoder.fit_transform(input_feature_train_df[col])
                    input_feature_test_df[col] = label_encoder.transform(input_feature_test_df[col])
                else:
                    input_feature_train_df[col] = input_feature_train_df[col]
                    input_feature_test_df[col] = input_feature_test_df[col]

            # Getting data transformer pipeline
            data_transformer_pipeline = DataTransformation.get_data_transformer_object()

            logging.info("Fitting data transformer pipeline on train dataset")
            data_transformer_pipeline.fit(input_feature_train_df)

            logging.info("Performing preprocessing for numerical features on train and test dataset")
            input_feature_train_arr =  data_transformer_pipeline.transform(input_feature_train_df)
            input_feature_test_arr = data_transformer_pipeline.transform(input_feature_test_df)

            logging.info("Creating target feature train and test arrays")
            target_feature_train_arr = target_feature_train_df.squeeze()
            target_feature_test_arr = target_feature_test_df.squeeze()

            logging.info("Creating whole train and test data array")
            train_arr = np.c_[input_feature_train_arr, target_feature_train_arr]
            test_arr = np.c_[input_feature_test_arr, target_feature_test_arr]

            logging.info("Saving training and test array objects")
            utils.save_numpy_array_data(train_arr, file_path=self.data_transformation_config.data_transformer_train_path)
            utils.save_numpy_array_data(test_arr, file_path=self.data_transformation_config.data_transformer_test_path)

            logging.info("Saving data transformation pipeline object")
            utils.save_object(data_transformer_pipeline, self.data_transformation_config.data_transformer_object_path)

            logging.info("Saving label encoder object")
            utils.save_object(label_encoder, self.data_transformation_config.encoder_object_path)

            logging.info("Preparing data transformation artifact")
            data_transformation_artifact = artifact_entity.DataTransformationArtifact(
                data_transformer_object_path= self.data_transformation_config.data_transformer_object_path,
                data_transformer_train_path=self.data_transformation_config.data_transformer_train_path,
                data_transformer_test_path=self.data_transformation_config.data_transformer_test_path,
                label_encoder_path=self.data_transformation_config.encoder_object_path
            )

            logging.info("\n\n##################### Data Transformation Stage Ended #####################\n\n")
            return data_transformation_artifact
        except Exception as e:
            raise IPPPredictorException(e, sys)

