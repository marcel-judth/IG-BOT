from selenium import webdriver
import os
import time

import configparser
import openpyxl
from datetime import datetime
import pandas as pd


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


 
     def login(self):
         self.driver.get(cparser['IG_URLS']['LOGIN'])
         time.sleep(2)
         self.driver.find_element_by_name('username').send_keys(self.username)
         self.driver.find_element_by_name('password').send_keys(self.password)

         self.driver.find_element_by_xpath(cparser['XPATHS']['LOGIN_BUTTON']).click()
         time.sleep(2)


     def nav_user(self, user):
         self.driver.get(cparser['IG_URLS']['NAV_USER'].format(user))

     def unfollow_user(self):
          self.driver.find_element_by_xpath(cparser['XPATHS']['UNFOLLOW_BUTTON']).click()
            





if __name__ == '__main__':
    username = cparser['AUTH']['USERNAME']
    password = cparser['AUTH']['PASSWORD']
    ig_unfollower = IGUnfollower(username, password)

    file = 'followed_users.xlsx'

    # Load spreadsheet
    xl = pd.ExcelFile(file)

    # Load a sheet into a DataFrame by name: df1
    df = xl.parse('Sheet')
    df = df.sort_values('time')


    for i in range(len(df)) : 
        dateFollowed = datetime.strptime(df.loc[i, "time"], "%m/%d/%Y, %H:%M:%S")
        print((datetime.now() - dateFollowed).days)
        if((datetime.now() - dateFollowed).days >= 1):
            ig_unfollower.nav_user(df.loc[i, "username"])
            # ig_unfollower.unfollow_user()
            df.drop(i)
            df.to_excel('output1.xlsx')