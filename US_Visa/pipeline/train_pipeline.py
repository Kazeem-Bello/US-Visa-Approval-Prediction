import sys
from us_visa.components.data_ingestion import DataIngestion
from us_visa.components.data_validation import DataValidation
from us_visa.components.data_transformation import DataTransformation
from us_visa.components.model_trainer import ModelTrainer
from us_visa.entity.config_entity import dataingestionconfig, datavalidationconfig, datatransformationconfig, modeltrainerconfig
from us_visa.entity.artifact_entity import dataingestionartifact,datavalidationartifact, datatransformationartifact, modeltrainerartifact
from us_visa.exception import us_visa_exception
from us_visa.logger import logging




class trainpipeline:
    def __init__(self):
        self.dataingestionconfig = dataingestionconfig()
        self.datavalidationconfig = datavalidationconfig()
        self.datatransformationconfig = datatransformationconfig()
        self.modeltrainerconfig = modeltrainerconfig()

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
        
    def start_data_validation(self, data_ingestion_artifact: dataingestionartifact) -> datavalidationartifact:
        try:
            logging.info("Entered data validation method of the training pipeline")
            data_validation = DataValidation(data_ingestion_artifact = data_ingestion_artifact, data_validation_config = self.datavalidationconfig)
            data_validation_artifact = data_validation.initiate_data_validation()
            logging.info("Performed the data validation operation")
            logging.info("Exited the start_data_validation method of the training pipeline")
            return data_validation_artifact
        except Exception as e:
            raise us_visa_exception(e, sys) from e
        
    def start_data_transformation(self, data_ingestion_artifact:dataingestionartifact, data_validation_artifact: datavalidationartifact) -> datatransformationartifact:
        try:
            data_transformation = DataTransformation(data_ingestion_artifact = data_ingestion_artifact, data_validation_artifact = data_validation_artifact,
                                                    data_transformation_config = self.datatransformationconfig)
            data_transformation_artifact = data_transformation.initiate_data_transformer()
            return data_transformation_artifact
        except Exception as e:
            raise us_visa_exception(e, sys) from e
        
    def start_model_trainer(self, data_transformation_artifact:datatransformationartifact) -> modeltrainerartifact:
        try:
            model_trainer = ModelTrainer(data_transformation_artifact = data_transformation_artifact, model_trainer_config = self.modeltrainerconfig)
            model_trainer_artifact = model_trainer.initiate_model_trainer()
            return model_trainer_artifact
        except Exception as e:
            raise us_visa_exception(e, sys) from e
    
    def run_pipeline(self):
        "This method of the train_pipeline is responsible for running the complete pipeline"
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact = data_ingestion_artifact)
            data_transformation_artifact = self.start_data_transformation(data_ingestion_artifact = data_ingestion_artifact, 
                                                                          data_validation_artifact = data_validation_artifact)
            model_trainer_artifact = self.start_model_trainer(data_transformation_artifact = data_transformation_artifact)
            
        except Exception as e:
            raise us_visa_exception(e, sys) from e
