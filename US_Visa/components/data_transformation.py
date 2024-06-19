import sys
import numpy as np
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


class DataTransformation: 
    def __init__(self, data_ingestion_artifact: dataingestionartifact, data_validation_artifact: datavalidationartifact, data_tranformation_config: datatransformationconfig)