'''
Owned and authored by Ian Loeb.

Description: A webscraping script to pull "hot search" data from mytoken.io using BS4 and Selenium.
The script will save the data to a mytoken_data.xlsx spreadsheet.

Instructions:
install:
	beautifulsoup4
	selenium
	pandas
	geckodriver
	openpyxl
	xlrd

To run:
	python(python3) scrape.py

To change intervcal between requests:
	read line 79 comment

To change time length script will run:
	read line 67 comment

'''

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import os
import time
import pandas as pd
import datetime
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

def scrape(url, df):
	driver.get(url)
	soup = BeautifulSoup(driver.page_source, 'lxml')
	divs = soup.findAll('tr', attrs={'class':'ant-table-row ant-table-row-level-0'})
	time_now = datetime.datetime.now()
	count = 1
	for div in divs:
		name_div = div.find('div', attrs={'class': 'name'})
		fire_div = div.findAll('div', attrs={'class': 'fire-item'})
		name = name_div.find(text=True)
		fire=0
		for i in fire_div:
			img = i.find('img')
			if img['alt'] == '0':
				fire += 0.5
			elif img['alt'] == '1':
				fire += 1
		df.at[time_now, name+'_rank'] = count
		df.at[time_now, name+'_heat'] = fire
		count += 1

url = 'http://www.mytoken.io'

options = Options()
options.add_argument('--headless')
driver = webdriver.Firefox(options=options)

df = pd.read_excel('mytoken_data.xlsx', index_col=0)

count = 0
while count<6: #number of x*interval seconds script will run
	scrape(url, df)
	time.sleep(5) #interval in seconds
	count += 1
df.to_excel('mytoken_data.xlsx')