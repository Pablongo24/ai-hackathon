"""
Scrape the Verizon 'Contact Us' chat.

Main Page: https://www.verizon.com/
Contact Us: https://www.verizon.com/business/contact-us/phone/  Note: doesn't have a chat window
Sign in page (has chat window): https://secure.verizon.com/signin
"""

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys  # noqa  TODO: remove noqa if used, delete if not used
from webdriver_manager.chrome import ChromeDriverManager


class VerizonScraper:

    def __init__(self):
        self.sign_in_page = "https://secure.verizon.com/signin"
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.get(self.sign_in_page)
        self.driver.implicitly_wait(1)

    def get_chat_window(self):
        soup = BeautifulSoup(self.driver.page_source, features='html.parser')
        chatbot_div = soup.find('div', {'id': 'chatbotStartBar'})
        chatbot_button = chatbot_div.find('button')
        chatbot_click_elem = self.driver.find_element(by=By.ID, value=chatbot_button.get('id'))
        chatbot_click_elem.click()
        breakpoint()


if __name__ == "__main__":
    scraper = VerizonScraper()
    scraper.get_chat_window()
