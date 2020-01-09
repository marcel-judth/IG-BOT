from selenium import webdriver
import os
import time

import configparser

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
         """
         self.username = username
         self.password = password
         self.driver = webdriver.Chrome('./chromedriver.exe')
         self.base_url = 'https://www.instagram.com'
         self.get_tag_url = 'https://www.instagram.com/explore/tags/{}/'
         self.login()


 
     def login(self):
         self.driver.get('{}/accounts/login/'.format(self.base_url))
         time.sleep(2)
         self.driver.find_element_by_name('username').send_keys(self.username)
         self.driver.find_element_by_name('password').send_keys(self.password)

         self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[4]/button/div').click()
         time.sleep(2)
         #notnow = self.driver.find_element_by_css_selector('body > div.RnEpo.Yx5HN > div > div > div.mt3GC > button.aOOlW.bIiDR')
         #notnow.click() #comment these last 2 lines out, if you don't get a pop up asking about notifications

     def nav_user(self, user):
         self.driver.get('{}/{}/'.format(self.base_url, user))


     def follow_user(self, user):
         self.nav_user(user)
         follow_button = self.driver.find_element_by_xpath("//button[contains(text(), 'Follow')]")
         follow_button.click()


     def unfollow_user(self, user):
         self.nav_user(user)
         follow_button = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/div[1]/a/button')
         follow_button.click()
     

     def search_tag(self, tag):
        """
        Naviagtes to a search for posts with a specific tag on IG.
        Args:
            tag:str: Tag to search for
        """
        self.driver.get(self.get_tag_url.format(tag))

     def click_thumbnail(self, index):
        first_thumbnail = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[1]/div/div/div[1]/div[1]/a/div')
        first_thumbnail.click()
        time.sleep(0.5)
        


     def like_users_per_hashtag(self, number_users):
         i = 0
         while i < number_users:
            time.sleep(2)
            button_like = self.driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/article/div[2]/section[1]/span[1]/button/span')
            if button_like.text == '':
                button_like.click()


            if self.driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/article/header/div[2]/div[1]/div[2]/button').text == 'Follow':
                #click follow button
                self.driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/article/header/div[2]/div[1]/div[2]/button').click()
                time.sleep(1)
                #click next button
            #     self.driver.find_element_by_link_text('Next').click()
            # else:
            #     #click next button
            self.driver.find_element_by_link_text('Next').click()

            time.sleep(1)
            i += 1

        

            





if __name__ == '__main__':
    config_path = './config.ini'
    cparser = configparser.ConfigParser()
    cparser.read(config_path)
    username = cparser['AUTH']['USERNAME']
    password = cparser['AUTH']['PASSWORD']

    ig_bot = InstagramBot('lenson_cricket', 'LenDomik2201')
    #ig_bot.nav_user('garyvee')
    # ig_bot.search_tag('fitness')
    # ig_bot.click_thumbnail(1)
    # ig_bot.like_users_per_hashtag(200)
    # ig_bot.search_tag('flirt')
    # ig_bot.click_thumbnail(1)
    # ig_bot.like_users_per_hashtag(200)
    # ig_bot.search_tag('zara')
    # ig_bot.click_thumbnail(1)
    # ig_bot.like_users_per_hashtag(20)
    ig_bot.search_tag('bloggerstyle')
    ig_bot.click_thumbnail(1)
    ig_bot.like_users_per_hashtag(20)
    time.sleep(1)
    ig_bot.search_tag('streetstyle')
    ig_bot.click_thumbnail(1)
    ig_bot.like_users_per_hashtag(20)
    time.sleep(1)
    ig_bot.search_tag('anajohnson')
    ig_bot.click_thumbnail(1)
    ig_bot.like_users_per_hashtag(20)
    time.sleep(1)
    ig_bot.search_tag('nakdfashion')
    ig_bot.click_thumbnail(1)
    ig_bot.like_users_per_hashtag(20)
    time.sleep(1)