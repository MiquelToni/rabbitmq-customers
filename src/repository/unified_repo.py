from dotenv import dotenv_values
from repository.mongodbBaseRepo import MongodbBaseRepo

config = dotenv_values(".env")


class UnifiedRepo(MongodbBaseRepo):
    def __init__(self) -> None:
        MongodbBaseRepo.__init__(self)
        self.collection_name = config["UNIFIED_COLLECTION"]
        self.collection = self.database[self.collection_name]

    def insert_job_offer(self, offer: dict) -> None:
        self.collection.insert_one(offer)
