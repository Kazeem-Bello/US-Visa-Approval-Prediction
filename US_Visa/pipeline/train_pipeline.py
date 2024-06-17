import sys
from us_visa.components.data_ingestion import DataIngestion
from us_visa.entity.config_entity import dataingestionconfig
from us_visa.entity.artifact_entity import dataingestionartifact
from us_visa.exception import us_visa_exception
from us_visa.logger import logging



class trainpipeline:
    def __init__(self):
        self.dataingestionconfig = dataingestionconfig()

    def start_data_ingestion(self) -> dataingestionartifact:
        "This method of the train_pipeline is responsible for starting the data ingestion component"
        try:
            logging.info("Getting the data from MongoDB")
            data_ingestion = DataIngestion(data_ingestion_config = self.dataingestionconfig)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logging.info("Got the train and test data from MongoDB")
            return data_ingestion_artifact
        except Exception as e:
            raise us_visa_exception(e, sys) from e
        

    def run_pipeline(self):
        "This method of the train_pipeline is responsible for running the complete pipeline"
        try:
            data_ingestion_artifact = self.start_data_ingestion()
        except Exception as e:
            raise us_visa_exception(e, sys) from e
