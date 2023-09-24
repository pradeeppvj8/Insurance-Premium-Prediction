from ippredictor.entity.config_entity import ModelPusherConfig
from ippredictor.entity.artifact_entity import DataTransformationArtifact, ModelTrainerArtifact, ModelPusherArtifact
from ippredictor.logger import logging
from ippredictor.exception import IPPPredictorException
from ippredictor.predictor import ModelResolver
from ippredictor.utils import load_object,save_object

class ModelPusher:
    def __init__(self, model_pusher_config: ModelPusherConfig,
                 data_transformation_artifact: DataTransformationArtifact,
                 model_trainer_artifact: ModelTrainerArtifact):
        
        logging.info("\n\n##################### Model Pusher Stage Started #####################\n\n")
        self.model_pusher_config = model_pusher_config
        self.data_transformation_artifact = data_transformation_artifact
        self.model_trainer_artifact = model_trainer_artifact
        self.model_resolver = ModelResolver()

    def initiate_model_pusher(self) -> ModelPusherArtifact:

        logging.info("Loading model, transformer & encoder object")
        transformer = load_object(self.data_transformation_artifact.data_transformer_object_path)
        encoder = load_object(self.data_transformation_artifact.label_encoder_path)
        model = load_object(self.model_trainer_artifact.model_path)

        logging.info("Saving model, transformer & encoder in model psuher directory")
        save_object(model, self.model_pusher_config.pusher_model_path)
        save_object(encoder, self.model_pusher_config.pusher_encoder_path)
        save_object(transformer, self.model_pusher_config.pusher_transformer_path)

        logging.info("Saving model, transformer & encoder in saved_models directory")
        save_object(model, self.model_resolver.get_latest_save_model_path())
        save_object(encoder, self.model_resolver.get_latest_encoder_path())
        save_object(transformer, self.model_resolver.get_latest_transformer_path())

        logging.info("Preparing model pusher artifact")
        model_pusher_artifact = ModelPusherArtifact(
            pusher_model_dir=self.model_pusher_config.pusher_model_dir,
            saved_models_dir=self.model_pusher_config.saved_model_dir
        )

        logging.info("\n\n##################### Model Pusher Stage Ended #####################\n\n")
        return model_pusher_artifact