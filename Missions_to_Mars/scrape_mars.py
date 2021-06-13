#Complete your initial scraping using Jupyter Notebook, BeautifulSoup, Pandas, and Requests/Splinter.
from bs4 import BeautifulSoup
import requests
import os
import pandas as pd
from splinter import Browser
import pymongo
from webdriver_manager.chrome import ChromeDriverManager

def browse():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    
info_mars = {}

def scrape():
    browser = browse()
    
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    text = browser.html
    soup = BeautifulSoup(text, 'html.parser')
    
    titles = soup.find('div', class_="content_title").text
    paragraphs = soup.find('div', class_="article_teaser_body").text
    
    info_mars["titles"] = titles
    info_mars["paragraphs"] = paragraphs
    
