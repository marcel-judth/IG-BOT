from selenium import webdriver
import os
import time

import configparser
import openpyxl
from datetime import datetime
import pandas as pd
from random import randint


#global variables
config_path = './config.ini'
cparser = configparser.ConfigParser()
cparser.read(config_path)



class IGUnfollower:

     def __init__(self, username, password):
         """
         Initializes an instance of the Unfollower class.
         Call the login method to authenticate a user with IG.

         Args:
            username:str: The Instagram username for a user
            password:str: The Instagram password for a user

         Attributes:
            driver:Selenium.webdriver.Chrome: The Chromedriver that is used to automate browser actions
         """
         
         self.username = username
         self.password = password
         self.driver = webdriver.Chrome(cparser['DRIVERS']['CHROME'])
         self.login()
         time.sleep(5)


 
     def login(self):
         self.driver.get(cparser['IG_URLS']['LOGIN'])
         time.sleep(2)
         self.driver.find_element_by_name('username').send_keys(self.username)
         self.driver.find_element_by_name('password').send_keys(self.password)

         self.driver.find_element_by_xpath(cparser['XPATHS']['LOGIN_BUTTON']).click()
         time.sleep(2)


     def nav_user(self, username):
         self.driver.get(cparser['IG_URLS']['NAV_USER'].format(username))

     def unfollow_user(self, username):
         self.nav_user(username)
         unfollow_button = self.driver.find_element_by_css_selector('Button')
         if unfollow_button.text == 'Following':
            unfollow_button.click()
            time.sleep(2)
            confirmButton = self.driver.find_element_by_xpath(cparser['XPATHS']['CONFIRMATION_BUTTON'])
            confirmButton.click()
            time.sleep(randint(30, 40))

         print('not unfollowed')
            





if __name__ == '__main__':
    username = cparser['AUTH']['USERNAME']
    password = cparser['AUTH']['PASSWORD']
    ig_unfollower = IGUnfollower(username, password)

    book = openpyxl.load_workbook(cparser['FILENAMES']['FOLLOWED_USERS_FILE'])
    worksheet = book['USERS']

    for idx, row in enumerate(worksheet.rows):
        dateFollowed = datetime.strptime(row[1].value, "%m/%d/%Y, %H:%M:%S")
        print(row[0].value)
        print((datetime.now() - dateFollowed).days)
        if((datetime.now() - dateFollowed).days >= 1):
            ig_unfollower.unfollow_user(row[0].value)
            worksheet.delete_rows(idx + 1, 1)
            book.save(cparser['FILENAMES']['FOLLOWED_USERS_FILE'])