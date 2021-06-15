#!/usr/bin/env python
# coding: utf-8

# In[18]:


#Complete your initial scraping using Jupyter Notebook, BeautifulSoup, Pandas, and Requests/Splinter.
from bs4 import BeautifulSoup
import requests
import os
import pandas as pd
from splinter import Browser
import pymongo
from webdriver_manager.chrome import ChromeDriverManager


# In[19]:


conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)


# In[20]:


db = client.info_mars
collection = db.info_mars


# In[21]:


# Setup splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# In[22]:


#website to scrape
url = 'https://redplanetscience.com/'
browser.visit(url)

text = browser.html
soup = BeautifulSoup(text, 'html.parser')


# #Scrape the Mars News Site and collect the latest News Title and Paragraph Text. 
# #Assign the text to variables that you can reference later.

# In[23]:


titles = soup.find('div', class_="content_title")
print(titles)


# In[24]:


paragraphs = soup.find('div', class_="article_teaser_body")
print(paragraphs)


# After 2 hours of troubleshooting and redoing all code over and over - figured out for some reason my kernel was switched - therfore not working.... found my 2-3 round of code actually works! Ill be sure to keep an eye on this in the future. Oi
# cant get the first result on the page to list - seems like its random. i cannot spend any more time on this so moving on.

# ### JPL Mars Space Images - Featured Image
# * Visit the url for the Featured Space Image site [here](https://spaceimages-mars.com).
# * Use splinter to navigate the site and find the image url for the current Featured Mars Image and assign the url string to a variable called `featured_image_url`.
# * Make sure to find the image url to the full size `.jpg` image.
# * Make sure to save a complete url string for this image.
# ```python
# # Example:
# featured_image_url = 'https://spaceimages-mars.com/image/featured/mars2.jpg'

# In[25]:


url2 = 'https://spaceimages-mars.com/'
browser.visit(url2)

html = browser.html
newsoup = BeautifulSoup(html, 'html.parser')


# In[26]:


img = newsoup.find('div', class_="floating_text_area")('a')
print(img)


# In[27]:


images = newsoup.find('a', class_="showimg fancybox-thumbs")
images


# In[28]:


imag = newsoup.find('img', class_="headerimage fade-in")['src']
imag


# In[29]:


pic_url = 'https://spaceimages-mars.com/' + imag
pic_url


# ### Mars Facts
# * Visit the Mars Facts webpage [here](https://galaxyfacts-mars.com) and use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
# * Use Pandas to convert the data to a HTML table string.

# In[30]:


mars_url = 'https://galaxyfacts-mars.com'
table_facts = pd.read_html(mars_url)
table_facts


# In[31]:


mars_data = table_facts[1]
mars_data.columns=["Data_Point", "Value"]
mars_data.set_index("Data_Point", inplace=True)
mars_data


# In[32]:


mars_data_html = mars_data.to_html()
mars_data_html.replace("\n",'')
mars_data.to_html("mars_data_table_html.html")


# ### Mars Hemispheres
# * Visit the astrogeology site [here](https://marshemispheres.com/) to obtain high resolution images for each of Mar's hemispheres.
# * You will need to click each of the links to the hemispheres in order to find the image url to the full resolution image.
# * Save both the image url string for the full resolution hemisphere image, and the Hemisphere title containing the hemisphere name. Use a Python dictionary to store the data using the keys `img_url` and `title`.
# * Append the dictionary with the image url string and the hemisphere title to a list. This list will contain one dictionary for each hemisphere.
# ```python
# # Example:
# hemisphere_image_urls = [
#     {"title": "Valles Marineris Hemisphere", "img_url": "..."},
#     {"title": "Cerberus Hemisphere", "img_url": "..."},
#     {"title": "Schiaparelli Hemisphere", "img_url": "..."},
#     {"title": "Syrtis Major Hemisphere", "img_url": "..."},
# ]

# In[33]:


hemi_url = "https://marshemispheres.com/"
browser.visit(hemi_url)


# In[34]:


hemi_html = browser.html
hsoup = BeautifulSoup(hemi_html, 'html.parser')


# In[35]:


all_hemis = hsoup.find_all('div', class_="item")
#all_hemis

hemi_data = []

for img in all_hemis:
    h_title = img.find("h3").text
    h_image = img.find("a", class_="itemLink product-item")["href"]
    
    browser.visit(hemi_url + h_image)
    
    image_html = browser.html
    information = BeautifulSoup(image_html, "html.parser")
    
    img_path = hemi_url + information.find("img", class_="thumb")["src"]
    
    hemi_data.append({"h_title" : h_title, "img_path" : img_path})

hemi_data
#print(h_title)
#print(img_path)
#print("-----------------")

