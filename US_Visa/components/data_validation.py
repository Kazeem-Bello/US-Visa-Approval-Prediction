import json
import os
import sys
import pandas as pd
from evidently.model_profile import Profile
from evidently.model_profile.sections import DataDriftProfileSection
from us_visa.exception import us_visa_exception
from us_visa.logger import logging
from us_visa.utils.main_utils import read_yaml_file, write_yaml_file
from us_visa.entity.artifact_entity import dataingestionartifact, datavalidationartifact
from us_visa.entity.config_entity import datavalidationconfig
from us_visa.constant import schema_file_path



class DataValidation:
    def __init__(self, data_ingestion_artifact: dataingestionartifact , data_validation_config: datavalidationconfig):
        """_summary_

        Args:
            data_ingestion_artifact (dataingestionartifact): Output reference of data ingestion artifact stage
            data_validation_config (datavalidationartifact): configuration for data validation
        """
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self.schema_config = read_yaml_file(file_path = schema_file_path)
        except Exception as e:
            raise us_visa_exception(e, sys) from e

    def validate_number_of_columns(self, dataframe: pd.DataFrame)-> bool:
        try: 
            status = len(dataframe.columns) == len(self.schema_config["columns"])
            logging.info(f"Is required number of column present: {status}")
            return status
        except Exception as e:
            raise us_visa_exception(e, sys) from e
        
    def is_column_exist(self, dataframe: pd.DataFrame)-> bool:
        try: 
            dataframe_columns = dataframe.columns
            missing_numerical_columns = []
            missing_categorical_columns = []
            for column in self.schema_config["numerical_columns"]:
                if column not in dataframe_columns:
                    missing_numerical_columns.append(column)
            if len(missing_numerical_columns) > 0:
                logging.info((f"Missing numerical columns: {missing_numerical_columns}"))

            for column in self.schema_config["categorical_columns"]:
                if column not in dataframe_columns:
                    missing_categorical_columns.append(column)
            if len(missing_categorical_columns) > 0:
                logging.info((f"Missing categorical columns: {missing_categorical_columns}"))
            return False if len(missing_categorical_columns) > 0 or len(missing_numerical_columns) > 0 else True

        except Exception as e:
            raise us_visa_exception(e, sys) from e
        
    @staticmethod
    def read_data(file_path)-> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise us_visa_exception(e, sys) from e

    def detect_dataset_drift(self, reference_df: pd.DataFrame, current_df:pd.DataFrame) -> bool:
        try: 
            data_drift_profile = Profile(sections = [DataDriftProfileSection()])
            data_drift_profile.calculate(reference_df, current_df)
            report = data_drift_profile.json()
            json_report = json.loads(report)

            write_yaml_file(file_path = self.data_validation_config.drift_report_file_path, content = json_report)
            n_features = json_report["data_drift"]["data"]["metrics"]["n_features"]
            n_drifted_features = json_report["data_drift"]["data"]["metrics"]["n_drifted_features"]

            logging.info(f"{n_drifted_features}/{n_features} drift detected.")
            drift_status = json_report["data_drift"]["data"]["metrics"]["dataset_drift"]
            return drift_status
        except Exception as e:
            raise us_visa_exception(e, sys) from e
        
    def initiate_data_validation(self) -> datavalidationartifact:
        """
        Method Name :   initiate_data_validation
        Description :   This method initiates the data validation component for the pipeline
        
        Output      :   Returns bool value based on validation results
        On Failure  :   Write an exception log and then raise an exception
        """

        try:
            validation_error_msg = ""
            logging.info("Starting data validation")
            train_df, test_df = (DataValidation.read_data(file_path=self.data_ingestion_artifact.train_file_path),
                                    DataValidation.read_data(file_path=self.data_ingestion_artifact.test_file_path))

            status = self.validate_number_of_columns(dataframe=train_df)
            logging.info(f"All required columns present in training dataframe: {status}")
            if not status:
                validation_error_msg += f"Columns are missing in training dataframe."
            status = self.validate_number_of_columns(dataframe=test_df)

            logging.info(f"All required columns present in testing dataframe: {status}")
            if not status:
                validation_error_msg += f"Columns are missing in test dataframe."

            status = self.is_column_exist(dataframe = train_df)

            if not status:
                validation_error_msg += f"Columns are missing in training dataframe."
            status = self.is_column_exist(dataframe = test_df)

            if not status:
                validation_error_msg += f"columns are missing in test dataframe."

            validation_status = len(validation_error_msg) == 0

            if validation_status:
                drift_status = self.detect_dataset_drift(train_df, test_df)
                if drift_status:
                    logging.info(f"Drift detected.")
                    validation_error_msg = "Drift detected"
                else:
                    validation_error_msg = "Drift not detected"
            else:
                logging.info(f"Validation_error: {validation_error_msg}")
                

            data_validation_artifact = datavalidationartifact(validation_status=validation_status, message = validation_error_msg, 
                                                              drift_report_file_path = self.data_validation_config.drift_report_file_path)

            logging.info(f"Data validation artifact: {data_validation_artifact}")
            return data_validation_artifact
        
        except Exception as e:
            raise us_visa_exception(e, sys) from e












            
































        


