import sys
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import warnings
from scipy.stats import chi2_contingency
from datetime import datetime
from sklearn.preprocessing import OneHotEncoder, StandardScaler, OrdinalEncoder, PowerTransformer
from sklearn.compose import ColumnTransformer 
from sklearn.pipeline import Pipeline
from imblearn.over_sampling import SMOTE
from imblearn.combine import SMOTETomek, SMOTEENN


from us_visa.exception import us_visa_exception
from us_visa.logger import logging
from us_visa.utils.main_utils import read_yaml_file, save_object, save_numpy_array_data, drop_columns
from us_visa.entity.artifact_entity import dataingestionartifact, datatransformationartifact, datavalidationartifact
from us_visa.entity.config_entity import  datatransformationconfig
from us_visa.constant import target_column, schema_file_path, current_year
from us_visa.entity.estimator import TargetValueMapping

class DataTransformation: 
    def __init__(self, data_ingestion_artifact: dataingestionartifact, data_validation_artifact: datavalidationartifact, data_tranformation_config: datatransformationconfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_artifact = data_validation_artifact
            self.data_transformation_config = data_tranformation_config
            self.schme_config = read_yaml_file(file_path = schema_file_path)
        except Exception as e:
            raise us_visa_exception(e, sys) from e
        
    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try: 
            return pd.read_csv(file_path)
        except Exception as e:
            raise us_visa_exception(e, sys) from e
        
    def get_data_transformer_object(self)-> Pipeline:
        logging.info("Entered get_data_transformer_object method of the DataTransformation class")

        try:
            logging.info("Got numerical columns from schema config")
            scaler = StandardScaler()
            oh_encoder = OneHotEncoder()
            or_encoder = OrdinalEncoder()

            logging.info("Initialized StandardScaler, OneHotEncoder, OrdinalEncoder")

            oh_columns = self.schme_config["oh_columns"]
            or_columns = self.schema_config["or_columns"]
            transform_columns = self.schme_config["transform_columns"]
            # num_features = self.schme_config["numerical_columns"] #transform_columns == numerical_columns

            logging.info("Initialize PowerTransformer")

            tranform_pipeline  = Pipeline(steps = [("transformer", PowerTransformer(method = "yeo-johnson")), ("scaler", scaler)])
            preprocessor = ColumnTransformer([("oh_encoder", oh_encoder, oh_columns),
                                                ("or_encoder", or_encoder, or_columns),
                                                ("transformer", tranform_pipeline, transform_columns)])
            
            logging.info("Exited get_data_transformer_object method of DataTransformation class")
            return preprocessor
        except Exception as e:
            raise us_visa_exception(e, sys) from e
        
    def initiate_data_transformer(self)-> datatransformationartifact:


    

