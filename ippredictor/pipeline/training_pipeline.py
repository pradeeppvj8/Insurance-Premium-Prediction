from ippredictor.logger import logging
from ippredictor.exception import IPPPredictorException
import os, sys
from ippredictor.entity.config_entity import (DataIngestionConfig,DataValidationConfig,DataTransformationConfig,
                                              ModelTrainerConfig, ModelEvaluationConfig, ModelPusherConfig)

from ippredictor.entity.config_entity import TrainingPipelineConfig
from ippredictor.components.data_ingestion import DataIngestion
from ippredictor.components.data_validation import DataValidation
from ippredictor.components.data_transformation import DataTransformation
from ippredictor.components.model_trainer import ModelTrainer
from ippredictor.components.model_evaluation import ModelEvaluation
from ippredictor.components.model_pusher import ModelPusher

def start_training_pipeline():
    try:
        # Instatiation of TrainingPipelineConfig
        training_pipeline_config = TrainingPipelineConfig()

        # Data Ingestion
        data_ingestion_config = DataIngestionConfig(training_pipeline_config=training_pipeline_config)
        data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()

        # Data Validation
        data_validation_config = DataValidationConfig(training_pipeline_config=training_pipeline_config)
        data_validation = DataValidation(data_validation_config= data_validation_config, data_ingestion_artifact=data_ingestion_artifact)
        data_validation_artifact = data_validation.initiate_data_validation()

        # Data Transformation
        data_transformation_config = DataTransformationConfig(training_pipeline_config)
        data_transformation = DataTransformation(data_transformation_config, data_ingestion_artifact)
        data_transformation_artifact = data_transformation.initiate_data_transformation()

        # Model Training
        model_trainer_config = ModelTrainerConfig(training_pipeline_config=training_pipeline_config)
        model_trainer = ModelTrainer(model_trainer_config=model_trainer_config, data_transformation_artifact=data_transformation_artifact)
        model_trainer_artifact = model_trainer.initiate_model_training()

        # Model Evaluation
        model_evaluation_config = ModelEvaluationConfig(training_pipeline_config=training_pipeline_config)
        model_eval = ModelEvaluation(model_evaluation_config=model_evaluation_config,
                                    data_ingestion_artifact=data_ingestion_config,
                                    data_transformation_artifact=data_transformation_artifact,
                                    model_trainer_artifact=model_trainer_artifact)
        model_eval_artifact = model_eval.initiate_model_evaluation()

        # Model Pusher
        model_pusher_config = ModelPusherConfig(training_pipeline_config=training_pipeline_config)
        model_pusher = ModelPusher(model_pusher_config=model_pusher_config, 
                                data_transformation_artifact=data_transformation_artifact,
                                model_trainer_artifact=model_trainer_artifact)
        model_pusher_artifact = model_pusher.initiate_model_pusher()
    except Exception as e:
        raise IPPPredictorException(e, sys)