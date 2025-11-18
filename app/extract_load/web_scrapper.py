from bs4 import BeautifulSoup
import re

class WebScrapper:
    def __init__(self, url_text):
        self.url_text = url_text
        self.__page_content = None

    def __fetch_page(self):
        self.__page_content = BeautifulSoup(self.url_text, 'html.parser')
        return self
    
    def find_elements(self, tag, **kwargs):
        self.__fetch_page()
        elements = self.__page_content.find_all(tag, **kwargs)
        return elements
    
    def find_urls(self, color, year):
        pattern = re.compile(f"(?=.*{color})(?=.*{year})")
        elements = self.find_elements("a", href=pattern)
        if not elements:
            raise ValueError(f"No URLs found for color={color} and year={year}")
        urls = [el.get("href") for el in elements if el.get("href")]
        return urls
