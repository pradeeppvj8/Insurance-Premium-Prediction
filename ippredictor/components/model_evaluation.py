from ippredictor.entity import artifact_entity, config_entity
from ippredictor.logger import logging
from ippredictor.predictor import ModelResolver
from ippredictor.exception import IPPPredictorException
import sys
from ippredictor import utils
import pandas as pd
from ippredictor.config import TARGET_COLUMN
from sklearn.metrics import r2_score

class ModelEvaluation:
    def __init__(self, model_evaluation_config: config_entity.ModelEvaluationConfig,
                 data_ingestion_artifact: artifact_entity.DataIngestionArtifact,
                 data_transformation_artifact: artifact_entity.DataTransformationArtifact,
                 model_trainer_artifact: artifact_entity.ModelTrainerArtifact):
        logging.info("\n\n##################### Model Evaluation Stage Started #####################\n\n")

        self.model_evaluation_config = model_evaluation_config
        self.data_ingestion_artifact = data_ingestion_artifact
        self.data_transformation_artifact = data_transformation_artifact
        self.model_trainer_artifact = model_trainer_artifact
        self.model_resolver = ModelResolver()

    def initiate_model_evaluation(self) -> artifact_entity.ModelEvaluationArtifact:
        try:
            latest_dir_path = self.model_resolver.get_latest_dir_path()

            if latest_dir_path is None:
                model_evaluation_artifact = artifact_entity.ModelEvaluationArtifact(
                    is_model_accepted=True,
                    improved_accuracy=None
                )

                logging.info("\n\n##################### Model Evaluation Stage Ended #####################\n\n")
                return model_evaluation_artifact
            
            logging.info("Loading previous model, transformer & label encoder")
            previous_model = utils.load_object(self.model_resolver.get_latest_model_path())
            previous_transformer = utils.load_object(self.model_resolver.get_latest_transformer_path())
            previous_encoder = utils.load_object(self.model_resolver.get_latest_encoder_path())

            logging.info("Loading current model, transformer & label encoder")
            current_model = utils.load_object(self.model_trainer_artifact.model_path)
            current_transformer = utils.load_object(self.data_transformation_artifact.data_transformer_object_path)
            current_encoder = utils.load_object(self.data_transformation_artifact.label_encoder_path)

            logging.info("Loading current test data")
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)
            y_true = test_df[TARGET_COLUMN]

            logging.info("Performing label encoding for categorical features of test data")
            input_features = list(previous_transformer.feature_names_in_);
            for col in input_features:
                if test_df[col].dtypes == 'O':
                    test_df[col] = previous_encoder.fit_transform(test_df[col])

            logging.info("Performing data transformation on test data using previous transformer")
            prev_input_arr = previous_transformer.transform(test_df[input_features])

            logging.info("Performing predictions on test data using previous model")
            prev_y_pred = previous_model.predict(prev_input_arr)

            logging.info("Calculating r2 score on previous model's prediction")
            prev_r2_score = r2_score(y_true=y_true, y_pred=prev_y_pred)

            logging.info("Performing data transformation on test data using current transformer")
            input_arr = current_transformer.transform(test_df[input_features])

            logging.info("Performing predictions on test data using current model")
            y_pred = current_model.predict(input_arr)

            logging.info("Calculating r2 score on current model's prediction")
            current_r2_score = r2_score(y_true=y_true, y_pred=y_pred)

            if current_r2_score <= prev_r2_score:
                logging.info("Current trained model is not better than previous model")
                raise Exception("Current trained model is not better than previous model")

            model_evaluation_artifact = artifact_entity.ModelEvaluationArtifact(
                is_model_accepted=True,
                improved_accuracy=current_r2_score - prev_r2_score
            )

            logging.info("\n\n##################### Model Evaluation Stage Ended #####################\n\n")
            return model_evaluation_artifact
        except Exception as e:
            raise IPPPredictorException(e, sys)