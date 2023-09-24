from ippredictor.entity import artifact_entity, config_entity
from ippredictor.logger import logging
from ippredictor.predictor import ModelResolver
from ippredictor.exception import IPPPredictorException
import sys

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
        except Exception as e:
            raise IPPPredictorException(e, sys)