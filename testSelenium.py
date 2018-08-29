# -*- coding:utf-8 -*-
import sys
import os
from selenium import webdriver
browser = webdriver.Chrome()
browser.get('http://nba.stats.qq.com/player/list.htm')
test = browser.find_element_by_xpath('/html/body/div[2]/div[2]/table/tbody/tr[1]/td[2]/a')
print(test.text)
