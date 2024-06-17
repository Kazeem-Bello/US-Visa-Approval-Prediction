import os
import sys
from us_visa.entity.config_entity import dataingestionconfig
from us_visa.entity.artifact_entity import dataingestionartifact
from us_visa.exception import us_visa_exception
from us_visa.logger import logging
from us_visa.data_access.usvisa_data import Usvisa_Data
import pandas as pd 
from sklearn.model_selection import train_test_split



class DataIngestion:
    def __init__(self, data_ingestion_config: dataingestionconfig = dataingestionconfig()):
        """
        data ingestion config: configuration for data ingestion
        """
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise us_visa_exception(e, sys) from e
        

    def export_to_feature_store(self) -> pd.DataFrame:
        """
        description: this method export data from mongodb to csv file
        output: data is returned as artifact of data ingestion components
        """

        try:
            logging.info(f"Exporting data from MongoDB")
            usvisadata = Usvisa_Data()
            dataframe = usvisadata.export_collection(collection_name = self.data_ingestion_config.collection_name)
            logging.info(f"Shape of dataframe: {dataframe.shape}")
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path, exist_ok = True)
            logging.info(f"Saving exported data into feature store file path: {feature_store_file_path}")
            dataframe.to_csv(feature_store_file_path, index = False, header = True)
            return dataframe
        except Exception as e:
            raise us_visa_exception(e, sys) from e
        

    def train_test_split(self, dataframe: pd.DataFrame) -> None:
        """
        description: this method splits the dataframe into train and test sets based of the split ratio
        output: folder is created in s3 bucket
        """
        logging.info("Entered train_test_split method of DataIngestion class")

        try:
            train_set, test_set = train_test_split(dataframe, test_size = self.data_ingestion_config.train_test_split_ratio)
            logging.info("Performed train test split on dataframe")
            logging.info("Exited train_test_split method of DataIngestion class")
            dir_path = os.path.dirname(self.data_ingestion_config.train_file_path)
            os.makedirs(dir_path, exist_ok = True)
            logging.info("Exporting train and test file path")
            train_set.to_csv(self.data_ingestion_config.train_file_path, index = False, header = True)
            test_set.to_csv(self.data_ingestion_config.test_file_path, index = False, header = True)
            logging.info("Exported train and test file path")
        except Exception as e:
            raise us_visa_exception(e, sys) from e
        

    def initiate_data_ingestion(self)-> dataingestionartifact:
        """
        description: this method initiates the data ingestion component of the training pipeline
        output: train and test set are returned as an artifact of the data ingestion component
        """
        try:
            dataframe = self.export_to_feature_store()
            logging.info("Got data from mongoDB")
            self.train_test_split(dataframe)
            logging.info("Perfomed train test split on the dataset")

            data_ingestion_artifact = dataingestionartifact(train_file_path = self.data_ingestion_config.train_file_path, test_file_path = self.data_ingestion_config.test_file_path)
            logging.info(f"Data ingestion artifact: {data_ingestion_artifact}")
            return data_ingestion_artifact
        except Exception as e:
            raise us_visa_exception(e, sys) from e 
