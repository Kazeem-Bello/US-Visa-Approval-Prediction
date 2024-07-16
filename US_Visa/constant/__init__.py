import os
from datetime import date

database_name = "us_visa"

collection_name = "us_visa-data"

connection_url = "mongodb_url"

pipeline_name: str = "us_visa"

artifact_dir: str = "artifact"

model_file_name = "model.pkl"

target_column = "case_status"

current_year = date.today().year

preprocessing_object_file_name = "preprocessing.pkl"

file_name: str = "us_visa.csv"

train_file_name: str = "train.csv"

test_file_name: str = "test.csv"
schema_file_path = os.path.join("config", "schema.yaml")

AWS_access_env_key = "AWS_ACCESS_KEY_ID"
AWS_secret_acces_key_env_key = "AWS_SECRET_ACCESS_KEY"
region_name = "us-east-1"

# Data Ingestion related constant 
data_ingestion_collection_name: str = "us_visa-data"
data_ingestion_dir_name: str = "data_ingestion"
data_ingestion_feature_store_dir: str = "feature_store"
data_ingestion_ingested_dir: str = "ingested"
data_ingestion_train_test_split: float = 0.2

# Data Validation related constant
data_validation_dir_name = "data_validation"
data_validation_drift_report_dir = "drift_report"
data_validation_drift_report_file_name = "report.yaml"

# Data transformation related constant
data_transformation_dir_name = "data_transformation"
data_transformation_transformed_data_dir = "transformed"
data_transformation_transformed_object_dir = "transformed_object"

# Model trainer related constant
model_trainer_dir_name: str = "model_trainer"
model_trainer_trained_model_dir: str = "trained_model"
model_trainer_trained_model_name: str = "model.pkl"
model_trainer_expected_score: float = 0.6

# Model pusher related constants
model_evaluation_changed_threshold: float = 0.02
model_bucket_name = "usvisa-model-bucket"
model_pusher_s3_key = "model-resgistry"











