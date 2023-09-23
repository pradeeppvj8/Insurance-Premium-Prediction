import pandas as pd
import numpy as np
import os, sys
from ippredictor.exception import IPPPredictorException
from ippredictor.config import mongo_client
from ippredictor.logger import logging
import yaml, dill


def get_collection_as_data_frame(database_name:str, collection_name:str) -> pd.DataFrame:
    try:
        logging.info(f"Fetching {collection_name} from {database_name}")
        # Returns all the elements stored in DB in dataframe fashion
        df = pd.DataFrame(mongo_client[database_name][collection_name].find())

        if '_id' in df.columns:
            # Drop _id column from df
            df = df.drop("_id", axis=1)
            
        logging.info(f"Fetched dataset with shape {df.shape}")
        return df
    except Exception as e:
        raise IPPPredictorException(e, sys)
    
def convert_columns_to_float(df:pd.DataFrame, exclude_columns:list) -> pd.DataFrame:
    try:
        for col in df.columns:
            if col not in exclude_columns:
                if df[col].dtypes != 'O':
                    df[col] = df[col].astype(float)
        return df
    except Exception as e:
            raise IPPPredictorException(e, sys)

def write_yaml_file(file_path, data):
    try:
        file_dir = os.path.dirname(file_path)
        os.makedirs(file_dir, exist_ok=True)

        with open(file_path, "w") as file_writer:
            yaml.dump(data, file_writer)
    except Exception as e:
            raise IPPPredictorException(e, sys)
    
def save_object(data, file_path):
     try:
          os.makedirs(os.path.dirname(file_path), exist_ok=True)

          with open(file_path, "wb") as file_obj:
               dill.dump(data, file_obj)
     except Exception as e:
        raise IPPPredictorException(e, sys)
     
def load_object(file_path):
     try:
          if not os.path.exists(file_path):
            raise Exception(f"File Path : {file_path} does not exist")
          
          with open(file_path, "rb") as file_Obj:
              return dill.load(file_Obj)
     except Exception as e:
        raise IPPPredictorException(e, sys)
     
def save_numpy_array_data(array_data, file_path):
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "wb") as file_obj:
            np.save(file_obj, array_data)
    except Exception as e:
        raise IPPPredictorException(e, sys)