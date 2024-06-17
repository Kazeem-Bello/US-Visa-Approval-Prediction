import os
from datetime import date

database_name = "us_visa"

collection_name = "us_visa-data"

connection_url = "mongodb_url"

pipeline_name: str = "us_visa"

artifact_dir: str = "artifact"

model_file_name = "model.pkl"

target_column = "case_study"

current_date = date.today().year

preprocessing_object_file_name = "preprocessing.pkl"

file_name: str = "us_visa.csv"

train_file_name: str = "train.csv"

test_file_name: str = "test.csv"

# Data Ingestion related constant 

data_ingestion_collection_name: str = "us_visa-data"
data_ingestion_dir_name: str = "data_ingestion"
data_ingestion_feature_store_dir: str = "feature_store"
data_ingestion_ingested_dir: str = "ingested"
data_ingestion_train_test_split: float = 0.2








