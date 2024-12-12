from pymongo import MongoClient
import pandas as pd

class mongo_operation:
    def __init__(self, client_url: str, database_name: str):
        """
        Initialize MongoDB connection

        Args:
            client_url (str): MongoDB connection URL
            database_name (str): Name of the database to connect to
        """
        try:
            # Create a MongoDB client connection
            self.__client = MongoClient(client_url)
            
            # Select the specified database
            self.__connect_database = self.__client[database_name]
            
            print("MongoDB connection successful")
        
        except Exception as e:
            print(f"Error in MongoDB connection: {e}")
            raise

    def bulk_insert(self, dataframe: pd.DataFrame, collection_name: str):
        """
        Insert a DataFrame into a MongoDB collection in bulk

        Args:
            dataframe (pd.DataFrame): Data to be inserted
            collection_name (str): Name of the collection to insert data into
        """
        try:
            # Convert DataFrame to a list of dictionaries for bulk insertion
            records = dataframe.to_dict('records')
            
            # Insert records into the specified collection
            self.__connect_database[collection_name].insert_many(records)
        
        except Exception as e:
            print(f"Error in bulk insertion: {e}")
            raise

    def find(self, collection_name: str, query: dict = None):
        """
        Find documents in a MongoDB collection

        Args:
            collection_name (str): Name of the collection to search
            query (dict, optional): Query to filter documents. Defaults to None.

        Returns:
            pd.DataFrame: Retrieved data as a pandas DataFrame
        """
        try:
            # If no query is provided, retrieve all documents
            if query is None:
                query = {}
            
            # Find documents in the collection
            cursor = self.__connect_database[collection_name].find(query)
            
            # Convert cursor to DataFrame
            data = pd.DataFrame(list(cursor))
            
            # Drop MongoDB's internal '_id' column if present
            if '_id' in data.columns:
                data = data.drop(columns=['_id'])
            
            return data
        
        except Exception as e:
            print(f"Error in finding documents: {e}")
            raise

