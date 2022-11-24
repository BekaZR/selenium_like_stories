from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException

from time import sleep
import sys


class Bot:
    
    driver_path: str
    
    def __init__(self, username, password):
        self._username = username
        self._password = password
        self.driver = webdriver.Firefox(self.driver_path)
        
    
    def login(self):
        self.driver.maximize_window() # For maximizing window
        self.driver.implicitly_wait(20)
        
        self.driver.get("https://instagram.com")
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@name=\"username\"]"))).send_keys(self._username)
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@name=\"password\"]"))).send_keys(self._password)
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@type=\"submit\"]"))).click()
        sleep(10)
    
    def get_profile(self, user):
        self.driver.get(user)
        sleep(2)
    
    def get_subscribers(self):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[2]/div[2]/section/main/div/header/section/ul/li[2]/a/div"))).click()
    
    def get_people_list(self):
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[2]/div[1]/div")))
        
        # subscribers = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "_aarf _aarg")))
        # for i in subscribers:
        #     WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "_aarf _aarg"))).click()
        #     sleep(3)
        print(self.driver.page_source)    
            
            