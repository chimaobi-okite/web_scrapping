import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class JijiScraper:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 10)

    def load_website(self, url="https://jiji.ng/"):
        self.driver.get(url)

    def search_items(self, keyword):
        search = self.driver.find_element(
            By.CSS_SELECTOR, "#__layout > div > div.h-bg-jiji-body.h-min-height-100p.h-width-100p.h-flex > div > div.b-content-wrapper > div:nth-child(1) > div > div.b-main-page-header.h-pos-rel > div > div > div > div:nth-child(2) > div > div > div.multiselect > div.multiselect__tags > input")
        search.send_keys(keyword)
        search.send_keys(Keys.RETURN)

    def change_view(self):
        view_button_selector = "#__layout > div > div.h-bg-jiji-body.h-min-height-100p.h-width-100p.h-flex > div > div > div > div.container.h-mt-10 > div.h-dflex > div.b-listing-wrapper.h-flex.b-adverts-listing__inner > div > div > div.h-dflex.h-flex-cross-center.h-flex-space-between.h-pv-10 > div.b-adverts-listing-change-view > svg:nth-child(2)"
        view = self.wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, view_button_selector)))
        view.click()

    def extract_items_data(self, max_items=3):
        listing_wrapper_selector = "js-advert-listing-wrapper"
        search_element = self.wait.until(
            EC.presence_of_element_located((By.ID, listing_wrapper_selector)))
        items = search_element.find_elements(
            By.CLASS_NAME, "b-list-advert__item-wrapper")

        results = []
        for i, item in enumerate(items):
            title = item.find_element(
                By.CLASS_NAME, "b-advert-title-inner").text
            price = item.find_element(By.CLASS_NAME, "qa-advert-price").text
            photo_url = item.find_element(
                By.TAG_NAME, "img").get_attribute('src')
            results.append((title, price, photo_url))

            if i == (max_items - 1):
                break
        return results

    def close(self):
        self.driver.quit()

    def scrape(self, keyword, max_items=3):
        try:
            self.load_website()
            self.search_items(keyword)
            self.change_view()
            results = self.extract_items_data(max_items)
            for result in results:
                print(result)
        except Exception as e:
            print("Error occurred:", str(e))
        finally:
            self.close()


if __name__ == "__main__":
    scraper = JijiScraper()
    scraper.scrape("chairs", 3)
