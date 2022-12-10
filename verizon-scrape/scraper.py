"""
Scrape the Verizon 'Contact Us' chat.

Main Page: https://www.verizon.com/
Contact Us: https://www.verizon.com/business/contact-us/phone/  Note: doesn't have a chat window
Sign in page (has chat window): https://secure.verizon.com/signin
"""

from bs4 import BeautifulSoup
# from selenium import webdriver
from seleniumwire import webdriver
from seleniumwire.utils import decode
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys  # noqa  TODO: remove noqa if used, delete if not used
from webdriver_manager.chrome import ChromeDriverManager


class VerizonScraper:

    def __init__(self):
        self.sign_in_page = "https://secure.verizon.com/signin"
        self.response_chat_filters = {
            'header_allow_from': 'ALLOW-FROM https://autochatva.verizon.com/'
        }
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    def run_all(self):
        self.driver.get(self.sign_in_page)
        self.driver.implicitly_wait(1)
        self.activate_chat_window()
        self.get_chat_response()  # TODO: only returns initial response, generalize

    def activate_chat_window(self):
        soup = BeautifulSoup(self.driver.page_source, features='html.parser')
        chatbot_div = soup.find('div', {'id': 'chatbotStartBar'})
        chatbot_button = chatbot_div.find('button')
        chatbot_click_elem = self.driver.find_element(by=By.ID, value=chatbot_button.get('id'))
        chatbot_click_elem.click()

    def get_chat_response(self):
        # Get all response objects tracked in selenium driver
        responses = [request.response for request in self.driver.requests if request.response]

        responses = [  # TODO: this is not filtering correctly, working on it now
            response for response in responses
            if self.response_chat_filters['header_allow_from'] in response.headers.values()
        ]
        decoded_bodies = [decode(response.body, response.headers.get('content-encoding')) for response in responses]
        breakpoint()


if __name__ == "__main__":
    scraper = VerizonScraper()
    scraper.run_all()
