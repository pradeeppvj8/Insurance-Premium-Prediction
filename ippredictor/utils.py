import pandas as pd
import numpy as np
import os, sys
from ippredictor.exception import IPPPredictorException
from ippredictor.config import mongo_client
from ippredictor.logger import logging
import yaml

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