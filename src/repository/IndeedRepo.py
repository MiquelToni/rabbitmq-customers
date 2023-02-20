
from dotenv import dotenv_values
from repository.mongodbBaseRepo import MongodbBaseRepo

config = dotenv_values(".env")


class IndeedRepo(MongodbBaseRepo):
    def __init__(self):
        MongodbBaseRepo.__init__(self)
        self.collection = self.database[config["INDEED_COLLECTION"]]

    def insert_job_offer(self, offer: dict) -> None:
        self.collection.insert_one(offer)

    def job_offers(self) -> list:
        return self.collection.find()
