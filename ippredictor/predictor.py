import os, sys
from ippredictor.logger import logging
from typing import Optional
from ippredictor.exception import IPPPredictorException
from ippredictor.entity.config_entity import MODEL_NAME, TRANSFORMER_OBJECT_PATH, LABEL_ENCODER_PATH

class ModelResolver:
    def __init__(self, model_registry = "saved_models", transformer_dir_name = "transformer",
                 encoder_dir_name = "encoder", model_dir_name = "model"):
        self.model_registry = model_registry
        os.makedirs(self.model_registry, exist_ok= True)
        self.transformer_dir_name = transformer_dir_name
        self.encoder_dir_name = encoder_dir_name
        self.model_dir_name = model_dir_name

    def get_latest_dir_path(self) -> Optional[str]:
        try:
            dir_name = os.listdir(self.model_registry)

            if len(dir_name) == 0:
                return None
            
            dir_name = list(map(int, dir_name))
            latest_dir_name = max(dir_name)
            return os.path.join(self.model_registry, f"{latest_dir_name}")
        except Exception as e:
            raise IPPPredictorException(e, sys)

    def get_latest_model_path(self):
        try:
            latest_dir = self.get_latest_dir_path()

            if latest_dir is None:
                raise Exception("Model is not available")
            
            return os.path.join(latest_dir,self.model_dir_name, MODEL_NAME)
        except Exception as e:
            raise IPPPredictorException(e, sys)

    def get_latest_transformer_path(self):
        try:
            latest_dir = self.get_latest_dir_path()

            if latest_dir is None:
                raise Exception("Transformer is not available")
            
            return os.path.join(latest_dir, self.transformer_dir_name, TRANSFORMER_OBJECT_PATH)
        except Exception as e:
            raise IPPPredictorException(e, sys)
        
    def get_latest_encoder_path(self):
        try:
            latest_dir = self.get_latest_dir_path()

            if latest_dir is None:
                raise Exception("Encoder is not available")
            
            return os.path.join(latest_dir, self.encoder_dir_name, LABEL_ENCODER_PATH)
        except Exception as e:
            raise IPPPredictorException(e, sys)
        
    def get_latest_save_dir_path(self) -> str:
        try:
            latest_dir = self.get_latest_dir_path()

            if latest_dir is None:
                return os.path.join(self.model_registry, f"{0}")
            
            latest_dir_num = int(os.path.basename(self.get_latest_dir_path()))
            return os.path.join(self.model_registry, f"{latest_dir_num + 1}")
        except Exception as e:
            raise IPPPredictorException(e, sys)
        
    def get_latest_save_model_path(self) -> str:
        try:
            latest_dir = self.get_latest_save_dir_path()
            return os.path.join(latest_dir, self.model_dir_name, MODEL_NAME)
        except Exception as e:
            raise IPPPredictorException(e, sys)   
        
    def get_latest_save_transformer_path(self) -> str:
        try:
            latest_dir = self.get_latest_save_dir_path()
            return os.path.join(latest_dir, self.transformer_dir_name, TRANSFORMER_OBJECT_PATH)
        except Exception as e:
            raise IPPPredictorException(e, sys)
        
    def get_latest_save_encoder_path(self) -> str:
        try:
            latest_dir = self.get_latest_save_dir_path()
            return os.path.join(latest_dir, self.encoder_dir_name, LABEL_ENCODER_PATH)
        except Exception as e:
            raise IPPPredictorException(e, sys)