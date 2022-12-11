"""
Scrape the Verizon 'Contact Us' chat.

Main Page: https://www.verizon.com/
Contact Us: https://www.verizon.com/business/contact-us/phone/  Note: doesn't have a chat window
Sign in page (has chat window): https://secure.verizon.com/signin
"""
import json

from bs4 import BeautifulSoup
from seleniumwire import webdriver
from seleniumwire.utils import decode
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
# noinspection PyPep8Naming
from selenium.webdriver.support import expected_conditions as EC
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
        try:
            # TODO: this doesn't find the chat window, even though it loads
            chat_window_elem = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "response-pannel"))
            )
        except Exception as e:  # TODO: handle exception
            print(e)

        responses = [request.response for request in self.driver.requests]

        responses = [
            response for response in responses
            for key, val in response.headers.items()
            if self.response_chat_filters['header_allow_from'] in val
        ]
        decoded_bodies = [decode(response.body, response.headers.get('content-encoding')) for response in responses]
        decoded_bodies = [json.loads(body.decode()) for body in decoded_bodies]


if __name__ == "__main__":
    scraper = VerizonScraper()
    scraper.run_all()
