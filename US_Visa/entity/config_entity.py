import os
from us_visa.constant import *
from dataclasses import dataclass
from datetime import datetime

timestamp: str = datetime.now().strftime("%m_%d_%Y_%H_%M_%S") 

@dataclass
class trainingpipelineconfig:
    pipeline_name: str = pipeline_name
    artifact_dir: str = os.path.join(artifact_dir, timestamp)
    timestamp:str = timestamp

trainingpipeline_config: trainingpipelineconfig = trainingpipelineconfig()

@dataclass
class dataingestionconfig:
    data_ingestion_dir: str = os.path.join(trainingpipeline_config.artifact_dir, data_ingestion_dir_name)
    feature_store_file_path: str = os.path.join(data_ingestion_dir, data_ingestion_feature_store_dir, file_name)
    train_file_path: str = os.path.join(data_ingestion_dir, data_ingestion_ingested_dir, train_file_name)
    test_file_path: str = os.path.join(data_ingestion_dir, data_ingestion_ingested_dir, test_file_name)
    train_test_split_ratio: float = data_ingestion_train_test_split
    collection_name: str = data_ingestion_collection_name


@dataclass
class datavalidationconfig:
    data_validation_dir: str = os.path.join(trainingpipeline_config.artifact_dir, data_validation_dir_name)
    drift_report_file_path: str = os.path.join(data_validation_dir, data_validation_drift_report_dir, data_validation_drift_report_file_name)


@dataclass
class datatransformationconfig:
    data_transformation_dir: str = os.path.join(trainingpipeline_config.artifact_dir, data_transformation_dir_name)
    transformed_train_file_path: str = os.path.join(data_transformation_dir, data_transformation_transformed_data_dir, train_file_name.replace("csv", "npy"))
    transformed_test_file_path: str = os.path.join(data_transformation_dir, data_transformation_transformed_data_dir, test_file_name.replace("csv", "npy"))
    transformed_object_file_path: str = os.path.join(data_transformation_dir, data_transformation_transformed_object_dir, preprocessing_object_file_name)




    