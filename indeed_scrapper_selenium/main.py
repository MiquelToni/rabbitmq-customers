
from selenium import webdriver
import time
from selenium.webdriver.common.by import By

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0", "Accept-Encoding": "gzip, deflate",
           "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT": "1", "Connection": "close", "Upgrade-Insecure-Requests": "1"}

driver = webdriver.Chrome()
driver.get('https://es.indeed.com/jobs?q=rabbitmq&start=1')
for content in driver.find_elements(By.CLASS_NAME, 'companyName'):
    print(content.get_attribute("innerText"))

time.sleep(1000)
