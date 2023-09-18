import pymongo
import pandas as pd 
import json
from pymongo.mongo_client import MongoClient

uri = "mongodb+srv://pradeep:2609@cluster0.odq2exp.mongodb.net/?retryWrites=true&w=majority"
# Create a new client and connect to the server
client = MongoClient(uri)

DATA_FILE_PATH = (r"D:\Projects\Learning\Insurance-Premium-Prediction\insurance.csv")
DATABASE_NAME = "INSURANCE"
COLLECTION_NAME = "INSURANCE_DETAILS"

if __name__ == "__main__":
    # Get the dataset
    df = pd.read_csv(DATA_FILE_PATH)
    # Remove index column
    df.reset_index(drop=True, inplace=True)
    # Convert dataframe into json format
    json_record = list(json.loads(df.T.to_json()).values())
    # Insert records into mongo DB
    client[DATABASE_NAME][COLLECTION_NAME].insert_many(json_record)


