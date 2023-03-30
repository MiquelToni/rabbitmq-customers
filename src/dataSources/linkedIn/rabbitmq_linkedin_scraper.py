from selenium import webdriver
from selenium.webdriver.common.by import By
import time, datetime
import json
from collections import defaultdict
from tqdm import tqdm


class ScrapeLinkedInJobOffers:

    def __init__(self, logger, location, database):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("window-size=1200x600")
        self.wd = webdriver.Chrome()
        self.job_info = defaultdict(list)
        self.logging = logger
        self.job_number = 0
        self.location = location
        self.db = database

    def get_web_driver_for_location(self):
        url = f"https://www.linkedin.com/jobs/search?keywords=rabbitmq&location={self.location}&pageNum=0&position=1"
        self.wd.get(url)

    def read_page(self):
        no_of_jobs = self.get_number_of_jobs()    
        self.logging.info(f"Found {no_of_jobs} in {self.location}.")     
        if no_of_jobs == 0:
            return None
        pages = tqdm(total=int(no_of_jobs/25)+1) if int(no_of_jobs/25)+1 < 40 else tqdm(total=40)
        current_page = 0
        jobs = []
        while current_page <= int(no_of_jobs/25) and current_page < 40:
            # page => 25 results, 7 * 25 = 175 ( after that we need to click )
            # last time we scroll down is in page 6, the 7th time we'll have the button
            if current_page <= 6: 
                self.wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            else:
                try:
                   self.wd.find_element(by=By.XPATH, value='/html/body/div/div/main/section/button').click()
                except Exception as e:
                    self.logging.info(e)
                    pass
            current_page = current_page + 1
            self.logging.info(f"Saving page {current_page}.")
            pages.update(1)
            time.sleep(5)
        pages.close()
        try:
            job_lists = self.wd.find_element(By.CLASS_NAME, 'jobs-search__results-list')
            jobs = job_lists.find_elements(By.TAG_NAME, 'li')
            return  jobs    
        except Exception as e:
            self.logging.info(e)
            pass

    def get_number_of_jobs(self):
        try:
            txt = self.wd.find_element(By.CLASS_NAME, 'results-context-header__job-count').text
            no_of_jobs = 0
            if txt[-1] == '+':
                no_of_jobs = int(txt[:-1].replace(',',''))
            else:
                no_of_jobs = int(txt)
            return no_of_jobs
            
        except Exception as e:
            self.logging.info(f"No jobs for RabbitMQ found in {self.location}")
            self.logging.info(e)
            return 0

    def read_and_save_jobs(self, jobs):
        # extract job title,company name, location, date, job details link
        self.logging.info(f"Saving {len(jobs)} for {self.location}.")
        for job in jobs:
            self.job_number += 1
            job_data = {}
            job_data['source'] = 'LINKEDIN'
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
            # job_data['job_description'] = self.get_detailed_job_description(url)
            self.logging.info(f"Saving {job_data['job_title']} - {job_data['company_name']}.")

            # save to db
            self.db.insert_job_offer(job_data)

            job_data['job_count'] = self.job_number
            del job_data['_id']
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
        if jobs != None:
            self.read_and_save_jobs(jobs)
            self.update_json('./data/linkedIn/linkedin_job_offers_info.json')
