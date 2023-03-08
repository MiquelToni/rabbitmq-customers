
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import urllib.parse

from repository.IndeedRepo import IndeedRepo

# https://gist.github.com/jonbruner/64fd4774396448a0a96ee2ac396bff20
ISO_COUNTRY_CODES = ["AQ", "AG", "AR",
                     "AM", "AW", "AU", "AT", "AZ", "BS", "BH", "BD", "BB", "BY", "BE",
                     "BZ", "BJ", "BM", "BT", "BO", "BQ", "BA", "BW", "BV", "BR", "IO",
                     "BN", "BG", "BF", "BI", "CV", "KH", "CM", "CA", "KY", "CF", "TD",
                     "CL", "CN", "CX", "CC", "CO", "KM", "CG", "CD", "CK", "CR", "CI",
                     "HR", "CU", "CW", "CY", "CZ", "DK", "DJ", "DM", "DO", "EC", "EG",
                     "SV", "GQ", "ER", "EE", "ET", "FK", "FO", "FJ", "FI", "FR", "GF",
                     "PF", "TF", "GA", "GM", "GE", "DE", "GH", "GI", "GR", "GL", "GD",
                     "GP", "GU", "GT", "GG", "GN", "GW", "GY", "HT", "HM", "VA", "HN",
                     "HK", "HU", "IS", "IN", "ID", "IR", "IQ", "IE", "IM", "IL", "IT",
                     "JM", "JP", "JE", "JO", "KZ", "KE", "KI", "KP", "KR", "KW", "KG",
                     "LA", "LV", "LB", "LS", "LR", "LY", "LI", "LT", "LU", "MO", "MK",
                     "MG", "MW", "MV", "ML", "MT", "MH", "MQ", "MR", "MU", "YT",
                     "MX", "FM", "MD", "MC", "MN", "ME", "MS", "MA", "MZ", "MM", "NA",
                     "NR", "NP", "NL", "NC", "NZ", "NI", "NE", "NG", "NU", "NF", "MP",
                     "NO", "OM", "PK", "PW", "PS", "PA", "PG", "PY", "PE", "PH", "PN",
                     "PL", "PT", "PR", "QA", "RE", "RO", "RU", "RW", "BL", "SH", "KN",
                     "LC", "MF", "PM", "VC", "WS", "SM", "ST", "SA", "SN", "RS", "SC",
                     "SL", "SG", "SX", "SK", "SI", "SB", "SO", "ZA", "GS", "SS", "ES",
                     "LK", "SD", "SR", "SJ", "SZ", "SE", "CH", "SY", "TW", "TJ", "TZ",
                     "TH", "TL", "TG", "TK", "TO", "TT", "TN", "TR", "TM", "TC", "TV",
                     "UG", "UA", "AE", "GB", "US", "UM", "UY", "UZ", "VU", "VE", "VN",
                     "VG", "VI", "WF", "EH", "YE", "ZM", "ZW"]


class IndeedScrapper:
    def __init__(self, repo: IndeedRepo) -> None:
        self.repo = repo
        self.driver = webdriver.Chrome()

    def run(self, keyword: str) -> None:
        driver = self.driver

        for code in ISO_COUNTRY_CODES:
            base_url = f'https://{str(code).lower()}.indeed.com'
            url = base_url + '/jobs?' + urllib.parse.urlencode({'q': keyword})
            try:
                driver.get(url)
                try:
                    print("visiting", url)
                    time.sleep(1.5)

                    window_location_origin = driver.execute_script(
                        'return window.location.origin')
                    offers_found_count = 0
                    if window_location_origin == base_url:
                        offers_found_count += self.get_job_offers_from_page(
                            base_url)
                        while self.goto_next_page():
                            time.sleep(1)
                            self.maybe_close_popup()
                            offers_found_count += self.get_job_offers_from_page(
                                base_url)

                        print('Found', offers_found_count, 'offers at', url)
                    else:
                        print("Abort visit. Reason: redirected to",
                              window_location_origin)
                except Exception as e:
                    print('Error crawl_page', e)
            except Exception as e:
                print("Not Found", url)

    def get_job_offers_from_page(self, base_url) -> None:
        data = self.driver.execute_script(
            'return window.mosaic?.providerData ? window.mosaic.providerData["mosaic-provider-jobcards"] : null')
        offers = data['metaData']['mosaicProviderJobCardsModel']['results'] if data is not None else None
        if offers is None:
            return 0

        for offer in offers:
            details = {}
            # details = self.get_offer_details(base_url, offer) # uncomment when the description becomes relevant
            details['company_name'] = offer['company'] if 'company' in offer else ''
            details['job_location_city'] = offer['jobLocationCity'] if 'jobLocationCity' in offer else (
                offer['formattedLocation'] if 'formattedLocation' in offer else '')
            details['job_location_state'] = offer['jobLocationState'] if 'jobLocationState' in offer else ''
            details['location_name'] = offer['locationName'] if 'locationName' in offer else ''
            details['job_title'] = offer['title'] if 'title' in offer else ''
            details['publication_date'] = offer['pubDate'] if 'pubDate' in offer else ''
            details['view_job_link'] = offer['viewJobLink'] if 'viewJobLink' in offer else ''
            self.repo.insert_job_offer(details)

        return len(offers)

    def get_offer_details(self, baseurl, offer: dict) -> dict:
        driver = self.driver
        view_job_link = baseurl + offer['viewJobLink']
        driver.get(view_job_link)

        maybe_description = driver.find_elements(
            By.CLASS_NAME, 'jobsearch-jobDescriptionText')
        if len(maybe_description) > 0:
            job_description = maybe_description[0].get_attribute('innerHTML')
        else:
            print('Error: empty job_description')
            job_description = ''

        offer_details = {
            'job_description': job_description,
            'inserted_at': str(datetime.today().isoformat(sep='T', timespec='auto')),
        }

        driver.back()
        return offer_details

    def goto_next_page(self) -> bool:
        # Returns "can keep going signal" -> True when "next_page_btn" is found
        try:
            next_page_btn = self.driver.find_element(
                By.CSS_SELECTOR, '[data-testid="pagination-page-next"]')
            next_page_btn.click()
            return True
        except:
            return False

    def maybe_close_popup(self) -> None:
        # Attempts to close modal popup if shown
        try:
            close_modal_btn = self.driver.find_element(
                By.CLASS_NAME, 'icl-Modal-close')
            close_modal_btn.click()
        except:
            pass
