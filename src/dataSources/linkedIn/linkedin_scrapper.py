from repository.linkedInRepo import LinkedInRepo
import time, datetime
import os, sys
import logging

from dataSources.linkedIn.countries import country_list
from dataSources.linkedIn.rabbitmq_linkedin_scraper import ScrapeLinkedInJobOffers


class LinkedInScrapper:
    def __init__(self, repo: LinkedInRepo) -> None:
        os.makedirs('./data/linkedIn', exist_ok=True)
        self.repo = repo
        
    def run(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(f'./data/linkedIn/linkedIn_scrape_{str(datetime.datetime.now())}.log'),
                logging.StreamHandler(sys.stdout)
            ]
        )

        start = time.perf_counter()
        for location in country_list:
            scraper = ScrapeLinkedInJobOffers(logger=logging, location=location, database=self.repo)
            scraper.run()
    
        elapsed_seconds = time.perf_counter() - start
        logging.info(f"For {len(country_list)} countries, scraping time is {elapsed_seconds/60} minutes.")
