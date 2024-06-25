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
    def __init__(self, data_ingestion_artifact: dataingestionartifact, data_validation_artifact: datavalidationartifact, data_transformation_config: datatransformationconfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_artifact = data_validation_artifact
            self.data_transformation_config = data_transformation_config
            self.schema_config = read_yaml_file(file_path = schema_file_path)
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

            oh_columns = self.schema_config["oh_columns"]
            or_columns = self.schema_config["or_columns"]
            transform_columns = self.schema_config["transform_columns"]
            # num_features = self.schema_config["numerical_columns"] #transform_columns == numerical_columns

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
        try:
            if self.data_validation_artifact.validation_status:
                logging.info("Starting data transformation")
                processor = self.get_data_transformer_object()
                logging.info("Got the processor object")

                train_df = DataTransformation.read_data(file_path = self.data_ingestion_artifact.train_file_path)
                test_df = DataTransformation.read_data(file_path = self.data_ingestion_artifact.test_file_path)
                logging.info("Got the train and test dataset of for transformation")

                feature_train_df = train_df.drop(target_column, axis = 1)
                target_train_df = train_df[target_column]
                logging.info("Got the feature and target variables of the train dataset")

                feature_test_df = test_df.drop(target_column, axis = 1)
                target_test_df = test_df[target_column]
                logging.info("Got the feature and target variables of the test dataset")


                feature_train_df["company_age"] = current_year - feature_train_df["yr_of_estab"]
                feature_test_df["company_age"] = current_year - feature_test_df["yr_of_estab"]
                logging.info("Added company age column to the train and test dataset")

                columns_to_drop = self.schema_config["drop_columns"]
                feature_train_df = drop_columns(df = feature_train_df, cols = columns_to_drop)
                feature_test_df = drop_columns(df = feature_test_df, cols = columns_to_drop)
                logging.info(f"Dropped the {columns_to_drop} columns in the train and test data. Not needed for model training")

                target_train_df = target_train_df.replace(TargetValueMapping()._asdict())
                target_test_df = target_test_df.replace(TargetValueMapping()._asdict())
                logging.info("Mapped the target variable to numerical variable")

                logging.info("Applying the preprocessing object on the features of the train and test data")
                # logging.info(f"the train features are {feature_train_df.columns}")
                # logging.info(f"the test features are {feature_test_df.columns}")
                # logging.info(f"the train target are {np.unique(target_train_df)}")
                # logging.info(f"the test target are {np.unique(target_test_df)}")

                processed_feature_train_df = processor.fit_transform(feature_train_df)
                processed_feature_test_df = processor.transform(feature_test_df)
                logging.info("Processor applied on the features of the train and test data")

                logging.info("Applying SMOTEENN on the processed train and test data")
                sm = SMOTEENN(sampling_strategy = "minority")
                feature_train_df_final, target_train_df_final = sm.fit_resample(processed_feature_train_df, target_train_df)
                feature_test_df_final, target_test_df_final = sm.fit_resample(processed_feature_test_df, target_test_df)
                logging.info("Applied SMOTEENN on the train and test data")

                logging.info("Creating the train and test array")
                train_arr = np.c_[feature_train_df_final, np.array(target_train_df_final)]
                test_arr = np.c_[feature_test_df_final, np.array(target_test_df_final)]

                save_object(self.data_transformation_config.transformed_object_file_path, processor)
                logging.info("Processor object saved")
                save_numpy_array_data(self.data_transformation_config.transformed_train_file_path, train_arr)
                save_numpy_array_data(self.data_transformation_config.transformed_test_file_path, test_arr)
                logging.info("Processed train and test data saved as numpy array")
                logging.info("Exited initiate_data_transformation method of Data_Transformation class")
                data_transformation_artifact = datatransformationartifact(transformed_object_file_path = self.data_transformation_config.transformed_object_file_path, 
                                                                          transformed_test_file_path = self.data_transformation_config.transformed_test_file_path, 
                                                                          transformed_train_file_path = self.data_transformation_config.transformed_train_file_path)
                return data_transformation_artifact
            else:
                raise Exception(self.data_validation_artifact.message)
        except Exception as e:
            raise us_visa_exception(e, sys) from e
                

                













    

