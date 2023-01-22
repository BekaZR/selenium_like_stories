from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

from bs4 import BeautifulSoup
class BotScroll:
    
    def scroll_slider_down(self, path):
        scroll_box = WebDriverWait(
            self.driver, 2).until(EC.presence_of_element_located(
                (By.XPATH, path)
            )
        )

        # Scroll till Followers list is there
        last_ht, ht = 0, 1
        while last_ht != ht:
            last_ht = ht
            sleep(2)
            # scroll down and retrun the height of scroll (JS script)
            ht = self.driver.execute_script(""" 
            arguments[0].scrollTo(0, arguments[0].scrollHeight);
            return arguments[0].scrollHeight; """, scroll_box
            )


class BotParseBs4:
    
    def parse_html_elements(self, tag, class_name):
        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        return soup.find_all(tag, class_=class_name)
    
    def parse_html_element(self, tag, class_name):
        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        return soup.find(tag, class_=class_name)

    def get_names_from_html_elements(self, html_elements):
        usernames = []
        for html_element in html_elements:
            try:
                usernames.append((html_element.find('img')['alt']).split()[-1])
            except Exception:
                continue
        return usernames
    
    def get_value_from_html_elements(self, html_elements):
        links = []
        for html_element in html_elements:
            try:
                links.append((html_element['href']))
            except Exception:
                continue
        return links


class BotClicButton:

    def click_user_stories(self, xpath):
        WebDriverWait(
        self.driver, 2).until(EC.presence_of_element_located(
            (By.XPATH, xpath)
            )
        ).click()
    
    def like(self):
        
        # like_1 = WebDriverWait(self.driver, 1).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[1]/section/div[1]/div/section/div/div[3]/div/div/div[2]/span/button")))
        like_1 = self.driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/section/div[1]/div/section/div/div[3]/div/div/div[2]/span/button")
        
        like_1.click()

class BotValidator:
    def check_stories_url(self):
        sleep(2)
        
        if str(self.stories_url) == str(self.driver.current_url):
            self.check_stories_url()

        self.stories_url = self.driver.current_url
        
        if 'stories' not in str(self.driver.current_url):
            return ''
        
        return self.like_stories()


class BotSearchElement:
    def search_element(self):
        WebDriverWait(
            self.driver, 10).until(EC.presence_of_element_located(
                (By.XPATH, "/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[2]/div[2]/section/main/div/div[3]/article/div/div")
                )
            )