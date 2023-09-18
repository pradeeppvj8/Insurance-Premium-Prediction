import pandas as pd
import numpy as np
import os, sys
from ippredictor.exception import IPPPredictorException
from ippredictor.config import mongo_client
from ippredictor.logger import logging

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