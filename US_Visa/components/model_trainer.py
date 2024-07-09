import sys
from typing import Tuple

import numpy as np
import pandas as pd
from pandas import DataFrame
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from neuro_mf  import ModelFactory

from us_visa.exception import us_visa_exception
from us_visa.logger import logging
from us_visa.utils.main_utils import load_numpy_array_data, read_yaml_file, load_object, save_object
from us_visa.entity.config_entity import modeltrainerconfig
from us_visa.entity.artifact_entity import datatransformationartifact, modeltrainerartifact, classificationmtericartifact
from us_visa.entity.estimator import USvisaModel


class ModelTrainer:
    def __init__(self, data_transformation_artifact: datatransformationartifact, model_trainer_config: modeltrainerconfig):
        self.data_transformation_artifact = data_transformation_artifact
        self.model_trainer_config = model_trainer_config
        
    def get_model_object_and_report(self, train: np.array, test: np.array) -> Tuple[object, object]: 
        try: 
            logging.info("Using Neuro_mf to get the best model objectand report")
            model_factory = ModelFactory(model_config_path = self.model_trainer_config.model_config_file_path)
            x_train, y_train, x_test, y_test = train[:, :-1], train[:, -1], test[:, :-1], test[:, -1]
            best_model_detail = model_factory.get_best_model(X = x_train, y = y_train, base_accuracy = self.model_trainer_config.expected_score)
            model_obj = best_model_detail.best_model
            y_pred = model_obj.predict(x_test)
            accuray = accuracy_score(y_test, y_pred)
            precision = precision_score(y_test, y_pred)
            recall = recall_score(y_test, y_pred)
            f1 = f1_score(y_test, y_pred)
            metric_artifact = classificationmtericartifact(f1_score = f1, precision_score = precision, recall_score = recall)

            return best_model_detail, metric_artifact

        except Exception as e:
            raise us_visa_exception(e, sys) from e
        

    def initiate_model_trainer(self) -> modeltrainerartifact:
        logging.info("Entered initiate_model_trainer method of ModelTrainer class")

        try:
            train_arr = 

