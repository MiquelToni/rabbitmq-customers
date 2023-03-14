
from datetime import datetime
from dotenv import dotenv_values
from repository.mongodbBaseRepo import MongodbBaseRepo

config = dotenv_values(".env")


class GithubRepo(MongodbBaseRepo):
    def __init__(self):
        MongodbBaseRepo.__init__(self)
        self.collection_name = f"""{config["GITHUB_COLLECTION"]}_{ datetime.today().isoformat(sep='T', timespec='auto')}"""
        self.collection = self.database[self.collection_name]

    def insert_company(self, offer: dict) -> None:
        self.collection.insert_one(offer)

    def companies(self) -> list:
        return self.collection.find()
