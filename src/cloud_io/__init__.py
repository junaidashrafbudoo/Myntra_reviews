import pandas as pd
from src.database_connect import mongo_operation as mongo
  # Importing a custom module for MongoDB operations. Ignoring type checking for this module.
import os, sys  # Importing modules for interacting with the operating system and system-specific parameters.
from src.constants import *  # Importing constants (likely defined in a separate module).
from src.exception import CustomException  # Importing a custom exception class for error handling.

# Define a class for MongoDB operations
class MongoIO:
    # Static variable to hold the MongoDB instance. This ensures only one instance is created (singleton pattern).
    mongo_ins = None

    def __init__(self):
        """
        Constructor to initialize a connection to the MongoDB database.
        Ensures that only one MongoDB instance exists by using a static variable.
        """
        # Check if the static variable `mongo_ins` is None
        if MongoIO.mongo_ins is None:
            # MongoDB connection URL. This should ideally be stored securely (e.g., in environment variables).
            mongo_db_url = "mongodb+srv://junaidashraf131:JsufinHvqbxWl9KT@cluster0.0yxxn.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
            # Check if the connection URL is not set
            if mongo_db_url is None:
                raise Exception(f"Environment key: {MONGO_URL_KEY} is not set.")  # Raise an exception if the URL is missing.
            # Initialize the MongoDB connection using the custom `mongo` class.
            MongoIO.mongo_ins = mongo(client_url=mongo_db_url, database_name=MONGO_DATABASE_NAME)
        
        # Set the instance variable to the static MongoDB instance
        self.mongo_ins = MongoIO.mongo_ins

    def store_reviews(self, product_name: str, reviews: pd.DataFrame):
        """
        Store product reviews in the MongoDB database.

        Args:
        - product_name (str): The name of the product whose reviews are to be stored.
        - reviews (pd.DataFrame): A pandas DataFrame containing the reviews.

        This function saves the reviews in a collection named after the product (with spaces replaced by underscores).
        """
        try:
            # Replace spaces in the product name with underscores to create a valid collection name.
            collection_name = product_name.replace(" ", "_")
            # Insert the reviews into the specified MongoDB collection in bulk.
            self.mongo_ins.bulk_insert(reviews, collection_name)
        except Exception as e:
            # Handle exceptions and raise a custom exception with the error and system information.
            raise CustomException(e, sys)
        
    def get_reviews(self, product_name: str):
        """
        Retrieve product reviews from the MongoDB database.

        Args:
        - product_name (str): The name of the product whose reviews are to be fetched.

        Returns:
        - data: The reviews retrieved from the database.

        This function fetches the reviews from the collection named after the product (with spaces replaced by underscores).
        """
        try:
            # Replace spaces in the product name with underscores to get the correct collection name.
            data = self.mongo_ins.find(collection_name=product_name.replace(" ", "_"))
            return data  # Return the fetched data.
        except Exception as e:
            # Handle exceptions and raise a custom exception with the error and system information.
            raise CustomException(e, sys)
