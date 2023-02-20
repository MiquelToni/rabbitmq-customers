
from dotenv import dotenv_values
from pymongo import MongoClient

config = dotenv_values(".env")


class MongodbBaseRepo:
    def __init__(self) -> None:
        self.startup_db_client()

    def startup_db_client(self) -> None:
        self.mongodb_client = MongoClient(config["ATLAS_URI"])
        self.database = self.mongodb_client[config["DB_NAME"]]

    def shutdown_db_client(self) -> None:
        self.mongodb_client.close()

    def get_mongodb_client(self) -> MongoClient:
        return self.mongodb_client
