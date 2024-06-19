import sys
from us_visa.components.data_ingestion import DataIngestion
from us_visa.entity.config_entity import dataingestionconfig, datavalidationconfig
from us_visa.entity.artifact_entity import dataingestionartifact,datavalidationartifact
from us_visa.exception import us_visa_exception
from us_visa.logger import logging
from us_visa.components.data_validation import DataValidation



class trainpipeline:
    def __init__(self):
        self.dataingestionconfig = dataingestionconfig()
        self.datavalidationconfig = datavalidationconfig()

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
        
    def start_data_validation(self, data_ingestion_artifact) -> dataingestionartifact:
        try:
            logging.info("Entered data validation method of the training pipeline")
            data_validation = DataValidation(data_ingestion_artifact = data_ingestion_artifact, data_validation_config = self.datavalidationconfig)
            data_validation_artifact = data_validation.initiate_data_validation()
            logging.info("Performed the data validation operation")
            logging.info("Exited the start_data_validation method of the training pipeline")
            return data_validation_artifact
        except Exception as e:
            raise us_visa_exception(e, sys) from e


    def run_pipeline(self):
        "This method of the train_pipeline is responsible for running the complete pipeline"
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact)
        except Exception as e:
            raise us_visa_exception(e, sys) from e
