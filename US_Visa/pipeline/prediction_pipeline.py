import os
import sys
import numpy as np
import pandas as pd
from us_visa.entity.config_entity import predictionconfig
from us_visa.entity.s3_estimator import USvisaEstimator
from us_visa.exception import us_visa_exception
from us_visa.logger import logging
from us_visa.utils.main_utils import read_yaml_file


class UsvisaData:
    def __init__(self, 
                 continent,
                 education_of_employee,
                 has_job_experience,
                 requires_job_training,
                 no_of_employees,
                 region_of_employment,
                 prevailing_wage,
                 unit_of_wage,
                 full_time_position,
                 company_age):
        try:
            self.continent = continent
            self.education_of_employee = education_of_employee
            self.has_job_experience = has_job_experience
            self.requires_job_training = requires_job_training
            self.no_of_employees = no_of_employees
            self.region_of_employment = region_of_employment
            self.prevailing_wage = prevailing_wage
            self.unit_of_wage = unit_of_wage
            self.full_time_position = full_time_position
            self.company_age = company_age
        except Exception as e:
            raise us_visa_exception(e, sys) from e
        
    def get_usvisa_input_data_frame(self) ->pd.DataFrame:
        try:
            usvisa_input_dict =self.get_usvisa_data_as_dict()
            return pd.DataFrame(usvisa_input_dict)
        except Exception as e:
            raise us_visa_exception(e, sys) from e
        
    def get_usvisa_data_as_dict(self):
        logging.info("Entered get_visa_data_as_dict method of the USvisaDAta class")
        try: 
            input_data = {
                "continent" : [self.continent],
                "education_of_employee" : [self.education_of_employee],
                "has_job_experience" : [self.has_job_experience] ,
                "requires_job_training" : [self.requires_job_training],
                "no_of_employees" : [self.no_of_employees],
                "region_of_employment" : [self.region_of_employment],
                "prevailing_wage" : [self.prevailing_wage],
                "unit_of_wage" : [self.unit_of_wage],
                "full_time_position" : [self.full_time_position],
                "company_age" : [self.company_age]}
        
            logging.info("Created us_visa data dict")
            logging.info("Exited get_visa_data_as_dict method of the USvisaDAta class")

            return input_data
        except Exception as e:
            raise us_visa_exception(e, sys) from e
        

class USvisaClassifier:
    def __init__(self, prediction_config: predictionconfig = predictionconfig()) -> None:
        try:
            self.prediction_config = prediction_config
        except Exception as e:
            raise us_visa_exception(e, sys) from e
        
    def predict(self, dataframe):
        try:
            logging.info("Entered the predict method of USvisaClassifier class")
            model = USvisaEstimator(bucket_name = self.prediction_config.model_bucket_name, model_path = self.prediction_config.model_file_name)
            result = model.predict(dataframe)
            return result
        except Exception as e:
            raise us_visa_exception(e, sys) from e

