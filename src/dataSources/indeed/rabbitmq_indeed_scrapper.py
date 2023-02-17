
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json
from ...domain.constants.iso_country_codes import ISO_COUNTRY_CODES


def save_found_offers(found_offers):
    # Serializing json
    json_object = json.dumps(found_offers, indent=4)

    # Writing to sample.json
    with open("indeed_offers.json", "w") as outfile:
        outfile.write(json_object)


# Returns "can keep going signal" -> True when "next_page_btn" is found
def goto_next_page(driver: webdriver.Chrome):
    try:
        next_page_btn = driver.find_element(
            By.CSS_SELECTOR, '[data-testid="pagination-page-next"]')
        next_page_btn.click()
        return True
    except:
        return False


def maybe_close_popup(driver: webdriver.Chrome):
    try:
        close_modal_btn = driver.find_element(By.CLASS_NAME, 'icl-Modal-close')
        close_modal_btn.click()
    except:
        print("no modal")


def init_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    return driver


def get_job_offers_from_page(driver: webdriver.Chrome):
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")

    data = driver.execute_script(
        'return window.mosaic.providerData["mosaic-provider-jobcards"]')

    return data['metaData']['mosaicProviderJobCardsModel']['results']


def crawl_page():
    driver = init_driver()
    offers = []

    for code in ISO_COUNTRY_CODES:
        url = f'https://{code}.indeed.com/jobs?q=rabbitmq'
        print("visiting", url)
        try:
            driver.get(url)

            driver.implicitly_wait(1)
            reject_cookies_btn = driver.find_element(
                By.ID, 'onetrust-reject-all-handler')
            reject_cookies_btn.click()

            get_job_offers_from_page(driver)
            while goto_next_page(driver):
                maybe_close_popup(driver)
                offers = offers + get_job_offers_from_page(driver)
                break
            print("Finished visiting", url)
        except:
            print("Not Found", url)
    save_found_offers(offers)


crawl_page()
time.sleep(100)
