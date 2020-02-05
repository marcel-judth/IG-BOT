from selenium import webdriver
from random import randint
import os
import time

import configparser
import openpyxl
from datetime import datetime
import instaloader
import sys


#global variables
config_path = './config.ini'
cparser = configparser.ConfigParser()
cparser.read(config_path)
loader = instaloader.Instaloader()



class InstagramBot:

     def __init__(self, username, password):
         """
         Initializes an instance of the InstagramBot class.
         Call the login method to authenticate a user with IG.

         Args:
            username:str: The Instagram username for a user
            password:str: The Instagram password for a user

         Attributes:
            driver:Selenium.webdriver.Chrome: The Chromedriver that is used to automate browser actions

         Restirctions
            follow: Instagram allows under 200 followers per hour and maximal 1000 follows per day
            liking: same
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
     

     def search_tag(self, tag):
        """
        Naviagtes to a search for posts with a specific tag on IG.
        Args:
            tag:str: Tag to search for
        """
        self.driver.get(cparser['IG_URLS']['SEARCH_TAGS'].format(tag))


     def click_first_thumbnail(self):
        first_thumbnail = self.driver.find_element_by_xpath(cparser['XPATHS']['THUMBNAIL_BUTTON'])
        first_thumbnail.click()
        time.sleep(0.5)
        

     def follow_like_per_hashtag(self, number_users):
         count = 0
         book = openpyxl.load_workbook(cparser['FILENAMES']['FOLLOWED_USERS_FILE'])
         sheet = book.active

         while count < number_users:
            time.sleep(5)

            if self.driver.find_element_by_xpath(cparser['XPATHS']['FOLLOW_BUTTON']).text == 'Follow':
                try:
                 time.sleep(2)
                 self.like_post()
                 username = self.driver.find_element_by_xpath(cparser['XPATHS']['USERNAME_LABEL']).text
                 sheet.append([username, datetime.now().strftime("%m/%d/%Y, %H:%M:%S")])
                 time.sleep(2)
                 self.follow_user()
                 book.save(cparser['FILENAMES']['FOLLOWED_USERS_FILE'])
                 time.sleep(randint(25, 35))
                except:
                    print("Unexpected error:", sys.exc_info()[0])
                    time.sleep(4)

            self.click_next()
            count += 1
            

     def click_next(self):
         self.driver.find_element_by_link_text('Next').click()


     def follow_user(self):
        self.driver.find_element_by_xpath(cparser['XPATHS']['FOLLOW_BUTTON']).click()
        #   self.driver.find_element_by_xpath('//button[text()="Follow"]').click()
     

     def like_post(self):
          button_like = self.driver.find_element_by_xpath(cparser['XPATHS']['LIKE_BUTTON'])
          if button_like.text == '':
            button_like.click()
            
     def follow_users_followers(self, user, maxFollowers):
         loader.login(self.username, self.password)
         profile = instaloader.Profile.from_username(loader.context, user)
         book = openpyxl.load_workbook(cparser['FILENAMES']['FOLLOWED_USERS_FILE'])
         sheet = book.active


         for index, follower in profile.get_followers():
             if index >= maxFollowers:
                break
             username = follower.username
             self.nav_user(username)
             time.sleep(2)
             self.follow_user()
             sheet.append([username, datetime.now().strftime("%m/%d/%Y, %H:%M:%S")])
             book.save(cparser['FILENAMES']['FOLLOWED_USERS_FILE'])
             time.sleep(randint(30, 40))




if __name__ == '__main__':
    username = cparser['AUTH']['USERNAME']
    password = cparser['AUTH']['PASSWORD']
    hashtags = cparser['IG_TAGS']['TAGS']
    hashtags = hashtags.split(",")
    ig_bot = InstagramBot(username, password)
    time.sleep(4)


    # ig_bot.follow_users_followers(cparser['MISC']['USERNAME_FOLLOWERS'], int(cparser['MISC']['FOLLOWERS_PER_USER']))



    for tag in hashtags:
        tag = tag.strip()
        ig_bot.search_tag(tag)
        time.sleep(2)
        ig_bot.click_first_thumbnail()
        ig_bot.follow_like_per_hashtag(int(cparser['MISC']['USERS_PER_HASHTAG']))