import time, datetime
import os, sys
import logging

from dataSources.linkedIn.countries import region_list
from dataSources.linkedIn.rabbitmq_linkedin_scraper import ScrapeLinkedInJobOffers

from repository.linkedInRepo import LinkedInRepo



if __name__ == '__main__':
    os.makedirs('./data/linkedIn', exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format='%(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(f'./data/linkedIn/linkedIn_scrape_{str(datetime.datetime.now())}.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )

    repo = LinkedInRepo()

    start = time.perf_counter()
    
    for location in region_list:
        scraper = ScrapeLinkedInJobOffers(logger=logging, location=location, database=repo)
        scraper.run()
    
    elapsed_seconds = time.perf_counter() - start
    logging.info(f"For {len(region_list)} regions, scraping time is {elapsed_seconds/60} minutes.")