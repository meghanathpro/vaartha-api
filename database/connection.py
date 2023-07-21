from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection


# MongoDB configuration
MONGO_URI = "mongodb://localhost:27017/"  # Replace with your MongoDB URI
DATABASE_NAME = "my_database"  # Replace with your database name


# Create a MongoDB client
client = MongoClient(MONGO_URI)

# Function to get the database connection


def get_database() -> Database:
    return client[DATABASE_NAME]

# Function to get the news collection


def get_news_collection() -> Collection:
    return client[DATABASE_NAME]["news"]
