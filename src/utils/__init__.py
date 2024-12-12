from src.cloud_io import MongoIO
from src.constants import MONGO_DATABASE_NAME
from src.exception import CustomException
import os
import sys

def fetch_product_names_from_cloud():
    """
    Fetches product names from a MongoDB database by retrieving collection names.

    Returns:
        list: A list of product names, where underscores ('_') in collection names 
              are replaced with spaces (' ').

    Raises:
        CustomException: Raised when an error occurs during the operation.
    """
    try:
        # Initialize a connection to MongoDB
        mongo = MongoIO()

        # Retrieve all collection names from the database
        collection_names = mongo.mongo_ins._mongo_operation__connect_database.list_collection_names()

        # Replace underscores in collection names with spaces and return them
        return [collection_name.replace('_', ' ') for collection_name in collection_names]

    except Exception as e:
        # Raise a custom exception in case of an error
        raise CustomException(e, sys)
