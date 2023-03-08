from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from dataSources.scrapper import Scrapper
from repository.glassdoor_repo import GlassdoorRepo


class GlassDoorScrapper(Scrapper):

    def __init__(self, repo: GlassdoorRepo):
        self.repo = repo
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=options)

    def run(self):
        url = f"""https://www.glassdoor.com/Job/rabbitmq-jobs-SRCH_KO0,8_IP.htm?includeNoSalaryJobs=true"""
        self.driver.get(url)
        self.close_modal()
        self.accept_cookies()

        app_cache = self.get_app_cache()
        total_jobs_count = app_cache['jlData']['totalJobsCount']
        current_count = self.insert_job_offers()
        print("found", current_count, "/", total_jobs_count, "offers")

        while self.goto_next_page():
            self.close_modal()
            self.accept_cookies()
            current_count += self.insert_job_offers()
            print("found", current_count, "/", total_jobs_count, "offers")

        print("Finished with", current_count, "/", total_jobs_count, "offers")
        self.driver.quit()

    def get_app_cache(self):
        return self.driver.execute_script('return window.appCache')

    def insert_job_offers_from_cache(self, jobs_data):
        job_offers = jobs_data['jobListings']
        for job_offer in job_offers:
            job_offer['inserted_at'] = str(
                datetime.today().isoformat(sep='T', timespec='auto'))
            self.repo.insert_job_offer(job_offer)

        return len(job_offers)

    def insert_job_offers(self):
        offers = [
            {"company_name": company_item.get_attribute('innerText')}
            for company_item in self.driver.find_elements(By.CLASS_NAME, 'css-l2wjgv > span')
            if company_item.get_attribute('innerText') != ''
        ]
        for offer in offers:
            self.repo.insert_job_offer(offer)

        return len(offers)

    def goto_next_page(self):
        # Returns "can keep going signal" -> True when "next_page_btn" is found
        try:
            next_page_btn = self.driver.find_element(
                By.CLASS_NAME, 'nextButton')
            self.driver.execute_script(
                "arguments[0].scrollIntoView(true);", next_page_btn)
            if next_page_btn.is_enabled():
                next_page_btn.click()
                return True
            else:
                return False
        except Exception as e:
            print(e)
            return False

    def accept_cookies(self):
        try:
            self.driver.find_element(
                By.ID, 'onetrust-accept-btn-handler').click()
        except:
            pass

    def close_modal(self):
        try:
            self.driver.implicitly_wait(2)
            self.driver.find_element(
                By.CLASS_NAME, 'modal_closeIcon').click()
        except:
            pass
