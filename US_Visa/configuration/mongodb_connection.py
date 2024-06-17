import os
import pymongo
import certifi
from us_visa.constant import database_name, collection_name, connection_url
from us_visa.logger import logging
from us_visa.exception import us_visa_exception, sys


ca = certifi.where()


class mongodb_client:
    """"
    class_name: export_data_into_feature_store
    description: this method exports dataframe from mongodb feature store as datframe 

    output:  connection to mongodb database 
    on failure: raise an exception 
    """

    client = None

    def __init__(self, database_name = database_name) -> None:
        try:
            if mongodb_client.client is None:
                mongodb_url = os.getenv(connection_url)
                if mongodb_url is None:
                    raise Exception(f"Environment key: {connection_url} is not set")
                mongodb_client.client = pymongo.MongoClient(mongodb_url, tlsCAFile = ca)   
                self.client = mongodb_client.client
                self.database = self.client[database_name]
                self.database_name = database_name
                logging.info("MongoDB connection successful")
        except Exception as e:
            raise us_visa_exception(e, sys) from e
        


