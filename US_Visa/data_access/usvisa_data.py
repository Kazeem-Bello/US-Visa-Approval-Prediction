from us_visa.constant import database_name, collection_name, connection_url
from us_visa.logger import logging
from us_visa.exception import us_visa_exception, sys
from us_visa.configuration.mongodb_connection import mongodb_client
import pandas as pd
import numpy as np
from typing import Optional

class Usvisa_Data:
    """
    this class help0s to export entire mongo db record as pandas data frame
    """

    def __init__(self):
        try: 
            self.mongo_client = mongodb_client(database_name = database_name)
        except Exception as e:
            raise us_visa_exception(e, sys) from e


    def export_collection(self, collection_name: str, database_name: Optional[str] = None)->  pd.DataFrame:
        try:
            """
            export entire collection as dataframe
            """
            if database_name is None:
                collection = self.mongo_client.database[collection_name]
            else:
                collection = self.mongo_client[database_name][collection_name]

            df = pd.DataFrame(list(collection.find()))
            if "_id" in df.columns.to_list():
                df = df.drop("_id", axis = 1)
            df.replace({"na": np.nan}, inplace = True)
            return df
        except Exception as e:
            raise us_visa_exception(e, sys) from e