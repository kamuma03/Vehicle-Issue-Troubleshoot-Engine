from selenium import webdriver
import json
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, WebDriverException
from time import sleep, time
import random
import re
import subprocess, os
import requests

max_time = 10

class Bot():
    def __init__(self, headless=False, verbose=False):
        print('initialising bot')

        options = Options()
        options.add_argument("--no-sandbox")	# without this, the chrome webdriver can't start (SECURITY RISK)
        if headless:
            options.add_argument("--headless")
        #options.add_argument("--window-size=1920x1080")
        self.driver = webdriver.Chrome(chrome_options=options)			# create webdriver
        self.verbose = verbose

    def click_btn(self, text):
        if self.verbose: print(f'clicking {text} btn')
        element_types = ['button', 'div', 'input', 'a', 'label']
        for element_type in element_types:
            btns = self.driver.find_elements_by_xpath(f'//{element_type}')
            # for btn in btns:
            #     print(btn.text)
            
            # SEARCH BY TEXT
            try:
                btn = [b for b in btns if b.text.lower() == text.lower()][0]
                btn.click()
                return
            except IndexError:
                pass

            # SEARCH BY VALUE ATTRIBUTE IF NOT YET FOUND
            try:
                btn = self.driver.find_elements_by_xpath(f'//{element_type}[@value="{text}"]')[0]
                btn.click()
                return
            except:
                continue

        raise ValueError(f'button containing "{text}" not found')

    def _search(self, query, _type='search', placeholder=None):
        sleep(1)
        s = self.driver.find_elements_by_xpath(f'//input[@type="{_type}"]')
        print(s)
        if placeholder:
            s = [i for i in s if i.get_attribute('placeholder').lower() == placeholder.lower()][0]
        else:
            s = s[0]
        s.send_keys(query) 

    def toggle_verbose(self):
        self.verbose = not self.verbose

def discussion_link(forums, total_pages, element_class):

    sleepTimes = [1.1, 1.5, 2]
    discussion_links = []
    for idx, forum in enumerate(forums):
        results =[]
        for i in range(total_pages[idx]):
            page = f'/page{i+1}'
            page = forum + page
            bot.driver.get(page)

            elements = bot.driver.find_elements_by_class_name(element_class[idx])
            elements = [r.get_attribute('href') for r in elements]

            results = results + elements           

            print(len(results))
        
        

        sleep(random.choice(sleepTimes))

        discussion_links.append(results)

    return discussion_links

def discussion_content(forums, question_links):

    for i in range(len(forums)):

        for j in range(len(question_links[i])):
            page = f'/page{j+1}'
            page = question_links[i][j] + page
            bot.driver.get(page)





    return


if __name__ == '__main__':
    # EXAMPLE USAGE
    bot = Bot()

    sleepTimes = [1.1, 1.5, 2]

    forums = ['https://www.bimmerforums.com/forum/forumdisplay.php?145-General-BMW-Mechanical-Help-sponsored-by-RM-European-Auto-Parts']
    total_pages = [34]
    element_class = ['title']

    question_links = discussion_link(forums, total_pages, element_class)
    
    print(len(question_links))

    dataset = discussion_content(forums, question_links)
