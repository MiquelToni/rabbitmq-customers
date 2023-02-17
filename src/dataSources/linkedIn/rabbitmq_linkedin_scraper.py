from selenium import webdriver
from selenium.webdriver.common.by import By
import time, datetime
import json, os, sys
from collections import defaultdict
from tqdm import tqdm
import logging

from countries import country_list


class ScrapeLinkedInJobOffers:

    def __init__(self, logger, location):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        self.wd = webdriver.Chrome(executable_path='chromedriver/chromedriver.exe', chrome_options=options)
        self.job_info = defaultdict(list)
        self.logging = logger
        self.job_number = 0
        self.location = location

    def get_web_driver_for_location(self):
        url = f"https://www.linkedin.com/jobs/search?keywords=rabbitmq&location={self.location}&pageNum=0&position=1"
        self.wd.get(url)

    def read_page(self):
        try:
            no_of_jobs = int(self.wd.find_element(By.CLASS_NAME, 'results-context-header__job-count').text)
        except Exception as e:
            self.logging.info(f"No jobs for RabbitMQ found in {self.location}")
            return []

        self.logging.info(f"Found {no_of_jobs} in {self.location}.")
        print(f"Loading {int(no_of_jobs/25)} more pages.")

        pages = tqdm(total=int(no_of_jobs/25)+1)
        i = 2
        while i <= int(no_of_jobs/25)+1: 
            self.wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            i = i + 1
            pages.update(1)
            try:
                self.wd.find_element_by_xpath('/html/body/main/div/section/button').click()
                time.sleep(5)
            except:
                pass
                time.sleep(5)
        pages.close()
        job_lists = self.wd.find_element(By.CLASS_NAME, 'jobs-search__results-list')
        jobs = job_lists.find_elements(By.TAG_NAME, 'li') # return a list
        self.logging.info(f"Saving {len(jobs)} for {self.location}.")
        return jobs

    def read_and_save_jobs(self, jobs):
        # extract job title,company name, location, date, job details link
        for job in tqdm(jobs):
            self.job_number += 1
            job_data = {}
            job_data['job_title'] = job.find_element(By.CLASS_NAME, 'base-search-card__title').get_attribute('innerText')
            job_data['company_name'] = job.find_element(By.CLASS_NAME, 'base-search-card__subtitle').get_attribute('innerText')
            job_data['job_location'] = job.find_element(By.CLASS_NAME, 'job-search-card__location').get_attribute('innerText')
            try:
                job_data['date_posted'] = job.find_element(By.CLASS_NAME, 'job-search-card__listdate').get_attribute('datetime')
            except Exception as e:
                job_data['date_posted'] = None
            url = job.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
            job_data['job_link'] = url
            job_data['saved_timestamp'] = str(datetime.datetime.now())
            job_data['job_count'] = self.job_number
            # job_data['job_description'] = self.get_detailed_job_description(url)

            self.job_info[self.location].append(job_data)

    def get_detailed_job_description(self, url):
        raise(NotImplementedError)

    def read_json(self, path):
        try:
            with open(path, "r") as jsonFile:
                data = json.load(jsonFile)
            return data
        except FileNotFoundError:
            return {}
        

    def write_json_file(self, path, data):
        with open(path, 'w') as f:
            json.dump(data, f)

    def update_json(self, path):
        data = self.read_json(path)
        data[self.location] = self.job_info[self.location]
        self.write_json_file(path, data)

    def run(self):
        self.get_web_driver_for_location()
        jobs = self.read_page()
        self.read_and_save_jobs(jobs)
        self.update_json('data/linkedin_job_offers_info.json')


if __name__ == '__main__':
    os.makedirs('./data', exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format='%(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(f'linkedIn_scrape_{str(datetime.datetime.now())}.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )

    start = time.perf_counter()

    for location in country_list:
        scraper = ScrapeLinkedInJobOffers(logger=logging, location=location)
        scraper.run()
    
    elapsed_seconds = time.perf_counter() - start
    logging.info(f"For {len(country_list)} countries, scraping time is {elapsed_seconds/60} minutes.")


#TODO: We get the first 175 fom scrolling, then we need to press a button and look into another source for each next 25.
