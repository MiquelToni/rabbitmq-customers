from repository.mongodbBaseRepo import MongodbBaseRepo


class Scrapper:
    def __init__(self, repo: MongodbBaseRepo):
        self.repo = repo

    def run(self):
        pass
