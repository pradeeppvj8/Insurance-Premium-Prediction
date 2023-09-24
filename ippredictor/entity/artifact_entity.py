from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:
    feature_store_path: str
    train_file_path: str
    test_file_path: str

@dataclass
class DataValidationArtifact:
    report_file_path: str

@dataclass
class DataTransformationArtifact:
    data_transformer_object_path: str
    data_transformer_train_path: str
    data_transformer_test_path: str
    label_encoder_path: str

@dataclass
class ModelTrainerArtifact:
    model_path: str
    r2_score_train : float
    r2_score_test : float

@dataclass
class ModelEvaluationArtifact:
    is_model_accepted : bool
    improved_accuracy : float