import requests
from dataSources.scrapper import Scrapper
from repository.glassdoor_repo import GlassdoorRepo


class GlassDoorScrapper(Scrapper):

    def __init__(self, repo: GlassdoorRepo):
        self.repo = repo

    def run(self):
        url = f"""https://www.glassdoor.com/Job/rabbitmq-jobs-SRCH_KO0,8_IP.htm?includeNoSalaryJobs=true"""
        response = self.fetch(url)
        print(response)

    def fetch(self, url) -> str:
        payload = {}
        headers = {
            'accept': 'text/html',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        if response.status_code == 200:
            return response.text
        else:
            raise Exception(
                f"Request '{url}' recived response status_code '{response.status_code}'")
