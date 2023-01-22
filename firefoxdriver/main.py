from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException

from time import sleep
import sys

from bs4 import BeautifulSoup

from fake_useragent import UserAgent

from firefoxdriver.services import BotClicButton, BotParseBs4, BotScroll, BotValidator, BotSearchElement

useragent = UserAgent()

options = webdriver.FirefoxOptions()

options.add_argument(f'user-agent={useragent.ie}')


class Bot(BotScroll, BotParseBs4, BotClicButton, BotValidator, BotSearchElement):
    
    users = []
    
    driver_path: str
    
    url = "https://instagram.com"
    
    def __init__(self, username, password):
        self._username = username
        self._password = password
        self.driver = webdriver.Firefox(executable_path=self.driver_path, options=options)


    def login(self):
        self.driver.maximize_window() # For maximizing window
        self.driver.implicitly_wait(20)
        
        self.driver.get(self.url)
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@name=\"username\"]"))).send_keys(self._username)
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@name=\"password\"]"))).send_keys(self._password)
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@type=\"submit\"]"))).click()
        sleep(10)


    def get_user_profile(self, user_link):
        self.driver.get(self.url + "/" + user_link)
        self.user = self.driver.current_url
        sleep(2)


    def get_user_subscribers(self):
        self.driver.get(self.driver.current_url + "followers/")
        try:
            self.get_people_list_with_story()
        except Exception as e:
            pass


    def get_people_list_with_story(self):
        self.scroll_slider_down("/html/body/div[2]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[2]")
        div_list_with_stories = self.parse_html_elements(tag="div", class_name="_aarf _aarg")
        self.get_profile_subscribers(usernames=self.get_names_from_html_elements(html_elements=div_list_with_stories), xpath="/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div/header/div/div")


    def get_profile_subscribers(self, usernames, xpath):
        for username in usernames:
            sleep(2)
            
            self.get_user_profile(user_link=username)
            sleep(3)
            
            try:
                self.click_user_stories(xpath=xpath)
            except Exception:
                continue
            sleep(2)
            
            try:
                self.like_stories()
            except Exception as e:
                continue


    def like_stories(self):
        try:
            self.like()
        except Exception as e:
            return " "
        
        self.stories_url = self.driver.current_url
        
        self.check_stories_url()


    def get_all_post(self):
        self.scroll_slider_down(path="/html")
        
        # self.search_element()
        
        div_post = self.parse_html_element(tag="article", class_name="x1iyjqo2")
        
        all_href = div_post.find_all("a")
        
        posts = []
        
        for value in all_href:
            posts.append(value['href'])
        try:
            self.get_all_post_liked_users(posts=posts[1:-1])
        except Exception:
            pass


    def get_all_post_liked_users(self, posts):
        href_list = []
        
        for post in posts:
            self.driver.get(self.url + post)
            
            sleep(2)
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/section/main/div[1]/div[1]/article/div/div[2]/div/div[2]/section[2]/div/div/div/a[2]"))).click()
            sleep(3)
            
            self.scroll_slider_down(path="/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div[3]/div")
            
            div_list_with_stories = self.parse_html_elements(tag="div", class_name="_aarf")
            usernames = self.get_names_from_html_elements(html_elements=div_list_with_stories)
            self.users += usernames
        self.get_profile_subscribers(usernames=set(self.users), xpath="/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/section/main/div/header/div/div")
