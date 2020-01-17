from selenium import webdriver
from random import randint
import os
import time

import configparser
import openpyxl
from datetime import datetime

#global variables
config_path = './config.ini'
cparser = configparser.ConfigParser()
cparser.read(config_path)



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
                self.like_post()
                username = self.driver.find_element_by_xpath(cparser['XPATHS']['USERNAME_LABEL']).text
                sheet.append([username, datetime.now().strftime("%m/%d/%Y, %H:%M:%S")])
                self.follow_user()
                book.save(cparser['FILENAMES']['FOLLOWED_USERS_FILE'])
                time.sleep(randint(30, 40))

            self.click_next()
            count += 1
            
         
     def follow_users_follower(self, user):
         self.nav_user(user)
         buttons = self.driver.find_elements_by_class_name('-nal3')

         for button in buttons:
             if 'followers' in button.text:
                button.click()
                break
        
         index = 0
         buttons = self.driver.find_elements_by_xpath('//button[text()="Following"]')
         while len(buttons) > 0 and index < int(cparser['MISC']['FOLLOWERS_PER_USER']):
            buttons = self.driver.find_elements_by_xpath('//button[text()="Following"]')
            
            if len(buttons) > 0:
                buttons[0].location_once_scrolled_into_view
                buttons[0].click()
            index += 1

     def click_next(self):
         self.driver.find_element_by_link_text('Next').click()


     def follow_user(self):
          self.driver.find_element_by_xpath(cparser['XPATHS']['FOLLOW_BUTTON']).click()
     

     def like_post(self):
          button_like = self.driver.find_element_by_xpath(cparser['XPATHS']['LIKE_BUTTON'])
          if button_like.text == '':
            button_like.click()
            





if __name__ == '__main__':
    username = cparser['AUTH']['USERNAME']
    password = cparser['AUTH']['PASSWORD']
    hashtags = cparser['IG_TAGS']['TAGS']
    hashtags = hashtags.split(",")
    ig_bot = InstagramBot(username, password)
    time.sleep(4)
    ig_bot.follow_users_follower('pamela_rf')
    # for tag in hashtags:
    #     tag = tag.strip()
    #     ig_bot.search_tag(tag)
    #     time.sleep(2)
    #     ig_bot.click_first_thumbnail()
    #     ig_bot.follow_like_per_hashtag(int(cparser['MISC']['USERS_PER_HASHTAG']))