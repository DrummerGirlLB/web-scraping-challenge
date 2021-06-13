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
    

    url2 = 'https://spaceimages-mars.com/'
    browser.visit(url2)
    
    html = browser.html
    newsoup = BeautifulSoup(html, 'html.parser')
    
    imag = newsoup.find('img', class_="headerimage fade-in")['src']
    
    pic_url = 'https://spaceimages-mars.com/' + imag
    
    info_mars["pic_url"] = pic_url
    
    mars_url = 'https://galaxyfacts-mars.com'
    table_facts = pd.read_html(mars_url)
    
    mars_data = table_facts[1]
    mars_data.columns=["Data_Point", "Value"]
    mars_data.set_index("Data_Point", inplace=True)
    
    mars_data_html = mars_data.to_html()
    mars_data_html.replace("\n",'')
    mars_data.to_html("mars_data_table_html.html")
    
    info_mars["table_facts"] = mars_data_html
    
    hemi_url = "https://marshemispheres.com/"
    browser.visit(hemi_url)
    
    hemi_html = browser.html
    hsoup = BeautifulSoup(hemi_html, 'html.parser')
    
    all_hemis = hsoup.find_all('div', class_="item")
    hemi_data = []
    
    for img in all_hemis:
        h_title = img.find("h3").text
        h_image = img.find("a", class_="itemLink product-item")["href"]
    
        browser.visit(hemi_url + h_image)
    
        image_html = browser.html
        information = BeautifulSoup(image_html, "html.parser")

        img_path = hemi_url + information.find("img", class_="thumb")["src"]
    
        info_mars["h_title"] = h_title.strip()
        info_mars["img_path"] = img_path
        
        hemi_data.append({"h_title" : h_title, "img_path" : img_path})
        
        info_mars["hemi_data"] = hemi_data
        
    browser.quit()
    
    return info_mars