from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException

from time import sleep
import sys

from bs4 import BeautifulSoup

from firefoxdriver.services import get_url

from fake_useragent import UserAgent

useragent = UserAgent()

options = webdriver.FirefoxOptions()

options.add_argument(f'user-agent={useragent.ie}')
class Bot:
    
    driver_path: str
    
    url = "https://instagram.com/"
    
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
    
    def get_profile(self, user):
        self.driver.get(user)
        self.user = user
        sleep(2)
    
    
    def get_subscribers(self):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[2]/div[2]/section/main/div/header/section/ul/li[2]/a/div"))).click()
    

    def get_people_list(self):
        scroll_box = WebDriverWait(
            self.driver, 2).until(EC.presence_of_element_located(
                (By.XPATH, "/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[2]")
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
        
        
        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        div_list_with_stories = soup.find_all('div', class_="_aarf _aarg")
        
        usernames = []
        for div_with_stories in div_list_with_stories:
            try:
                usernames.append((div_with_stories.find('img')['alt']).split()[-1])
            except Exception:
                continue
        print('\n'*2, f'all users --- {usernames}')
        self.profile_subscribers(usernames=usernames)


    def profile_subscribers(self, usernames):
        for username in usernames:
            print('\n'*2, f'now we working with --- {username}')
            self.driver.get(self.url + username)
            print('\n'*2, f'url to user --- {self.url}{username}')
            sleep(5)
            WebDriverWait(
            self.driver, 2).until(EC.presence_of_element_located(
                (By.XPATH, "/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[2]/div[2]/section/main/div/header/div/div")
                )
            ).click()
            print('\n'*2, f'we click to --- {self.url}{username}')
            self.like_stories()
            

    def like_stories(self):
        print('\n'*2, f'we starting like stories')
        try:
            WebDriverWait(self.driver, 1).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[1]/section/div[1]/div/section/div/div[3]/div/div/div[2]/span/button"))).click()
        except TimeoutException:
            WebDriverWait(self.driver, 1).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[1]/section/div[1]/div/div[5]/section/div/div[3]/div/div/div[2]/span/button"))).click()
        except Exception:
            WebDriverWait(self.driver, 1).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[1]/section/div[1]/div/section/div/div[3]/div/div/span/button"))).click()
        print('\n', "we check stories url")
        self.stories_url = self.driver.current_url
        
        self.check_stories_url()


    def check_stories_url(self):
        
        print('\n', "now url ", self.stories_url)
        
        print(f'{self.stories_url == self.driver.current_url}')
        
        sleep(2)
        
        if str(self.stories_url) == str(self.driver.current_url):
            self.check_stories_url()
            print(f'{self.stories_url} ---- {self.driver.current_url}')

        self.stories_url = self.driver.current_url
        
        if 'stories' not in str(self.driver.current_url):
            return ''
        
        return self.like_stories()
    
    
    def get_all_post(self):
    
        scroll_box = WebDriverWait(
        self.driver, 2).until(EC.presence_of_element_located(
            (By.XPATH, "/html")
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
        
        WebDriverWait(
            self.driver, 10).until(EC.presence_of_element_located(
                (By.XPATH, "/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[2]/div[2]/section/main/div/div[3]")
                )
            )
        
        posts = WebDriverWait(
            self.driver, 10).until(EC.presence_of_all_elements_located(
                (By.TAG_NAME, "a")
                )
            )
        
        names = [post.text for post in posts if post.text != '']
        print(names)


    # def next_stories(self):
    #         WebDriverWait(
    #         self.driver, 2).until(EC.presence_of_element_located(
    #             (By.XPATH, "/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[1]/section/div[1]/div/section/div/button")
    #             )
    #         ).click()
    #         sleep(5)

# /html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[1]/section/div[1]/div/section/div/div[3]/div/div/span/button


# /html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[1]/section/div[1]/div/section/div/div[3]/div/div/div[2]/span/button


# /html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[1]/section/div[1]/div/div[5]/section/div/div[3]/div/div/div[2]/span/button
