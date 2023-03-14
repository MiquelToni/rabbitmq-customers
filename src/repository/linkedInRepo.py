
from datetime import datetime
from dotenv import dotenv_values
from repository.mongodbBaseRepo import MongodbBaseRepo

config = dotenv_values(".env")


class LinkedInRepo(MongodbBaseRepo):
    def __init__(self):
        MongodbBaseRepo.__init__(self)
        self.collection_name = f"""{config["LINKEDIN_COLLECTION"]}_{ datetime.today().isoformat(sep='T', timespec='auto')}"""
        self.collection = self.database[self.collection_name]

    def insert_job_offer(self, offer: dict) -> None:
        self.collection.insert_one(offer)

    def job_offers(self) -> list:
        return self.collection.find()
