from ippredictor.entity import artifact_entity, config_entity
from ippredictor.logger import logging
from ippredictor.exception import IPPPredictorException
import sys
from sklearn.linear_model import LinearRegression
from ippredictor import utils
from sklearn.metrics import r2_score

class ModelTrainer:
    def __init__(self, model_trainer_config: config_entity.ModelTrainerConfig,
                 data_transformation_artifact: artifact_entity.DataTransformationArtifact):
        logging.info("\n\n##################### Model Training Stage Started #####################\n\n")
        self.model_trainer_config = model_trainer_config
        self.data_transformation_artifact = data_transformation_artifact

    def train_model(self, X, y):
        try:
            lr = LinearRegression()
            lr.fit(X, y)
            return lr
        except Exception as e:
            raise IPPPredictorException(e, sys)
        
    def initiate_model_training(self) -> artifact_entity.ModelTrainerArtifact:
        try:
            logging.info("Getting train and test dataset arrays")
            train_arr = utils.load_numpy_array_data(self.data_transformation_artifact.data_transformer_train_path)
            test_arr = utils.load_numpy_array_data(self.data_transformation_artifact.data_transformer_test_path)

            logging.info("Splitting train and test data into X & y")
            X_train, y_train = train_arr[:,:-1] , train_arr[:,-1]
            X_test, y_test = test_arr[:, :-1], test_arr[:, -1]

            logging.info("Performing model training")
            model = self.train_model(X_train, y_train)

            logging.info("Getting training & testing data predictions")
            y_train_pred = model.predict(X_train)
            y_test_pred = model.predict(X_test)

            logging.info("Calculating r2 score on train and test data")
            r2_score_train = r2_score(y_true=y_train, y_pred=y_train_pred)
            r2_score_test = r2_score(y_true=y_test, y_pred= y_test_pred)

            if r2_score_test < self.model_trainer_config.expected_accuracy:
                raise Exception(f"The expected accuracy is {self.model_trainer_config.expected_accuracy} but model " + 
                                "got only {r2_score_test} hence this model is not good")
            
            diff = abs(r2_score_test - r2_score_train)

            if diff > self.model_trainer_config.overfitting_threshold:
                raise Exception(f"The expected overfitting threshold is {self.model_trainer_config.overfitting_threshold}"  + 
                                " but model got {diff} hence this model is overfitting")
            
            logging.info("Saving the model")
            utils.save_object(model, self.model_trainer_config.model_path)

            logging.info("Preparing model trainer artifact")
            model_trainer_artifact = artifact_entity.ModelTrainerArtifact(
                model_path=self.model_trainer_config.model_path,
                r2_score_train = r2_score_train,
                r2_score_test = r2_score_test
            )

            logging.info("\n\n##################### Model Training Stage Ended #####################\n\n")
            return model_trainer_artifact
        except Exception as e:
            raise IPPPredictorException(e, sys)