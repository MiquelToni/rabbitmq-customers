
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json

# https://gist.github.com/jonbruner/64fd4774396448a0a96ee2ac396bff20
ISO_COUNTRY_CODES = ["AF", "AX", "AL", "DZ", "AS", "AD", "AO", "AI", "AQ", "AG", "AR",
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
                     "MG", "MW", "MY", "MV", "ML", "MT", "MH", "MQ", "MR", "MU", "YT",
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
    # options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    # driver = webdriver.Chrome(options=options)
    driver = webdriver.Chrome()
    return driver


def get_job_offers_from_page(driver: webdriver.Chrome):
    data = driver.execute_script(
        'return window.mosaic.providerData["mosaic-provider-jobcards"]')

    return data['metaData']['mosaicProviderJobCardsModel']['results']


def crawl_page():
    driver = init_driver()
    offers = []

    for code in ISO_COUNTRY_CODES:
        url = f'https://{code}.indeed.com/jobs?q=rabbitmq'
        try:
            driver.get(url)
            try:
                print("visiting", url)
                time.sleep(1.5)

                get_job_offers_from_page(driver)
                while goto_next_page(driver):
                    time.sleep(1)

                    maybe_close_popup(driver)
                    new_offers = get_job_offers_from_page(driver)
                    print("found", len(new_offers), "new offers")
                    offers = offers + new_offers

                print("Finished visiting", url)
            except Exception as e:
                print(e)
        except Exception as e:
            print("Not Found", url)

    save_found_offers(offers)


crawl_page()
