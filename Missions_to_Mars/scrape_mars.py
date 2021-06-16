from splinter import Browser
from bs4 import BeautifulSoup
import time
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager

scraped_data = {}

def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=False) 

browser = init_browser

def scrape():
    browser = init_browser

    url = 'https://redplanetscience.com/'
    browser.visit(url)

    text = browser.html
    soup = BeautifulSoup(text, 'html.parser')

######news article######
    news_title = soup.find('div', class_="content_title").text
    news_p = soup.find('div', class_="article_teaser_body").text

#add to dict
    scraped_data['news_title'] = news_title
    scraped_data['news_p'] = news_p

    browser.quit()

######featured image######
    browser = init_browser()

    url2 = 'https://spaceimages-mars.com/'
    browser.visit(url2)

    html = browser.html
    newsoup = BeautifulSoup(html, 'html.parser')

    img = newsoup.find('div', class_="floating_text_area")('a')
    images = newsoup.find('a', class_="showimg fancybox-thumbs")
    imag = newsoup.find('img', class_="headerimage fade-in")['src']
    featured_image_url = 'https://spaceimages-mars.com/' + imag

#add to dict
    scraped_data['featured_image_url'] = featured_image_url

    browser.quit()


######mars facts table######
    browser = init_browser()

    mars_url = 'https://galaxyfacts-mars.com'
    table_facts = pd.read_html(mars_url)

    mars_data = table_facts[0]
    mars_data.columns=["Description", "Mars", "Earth"]
    mars_data.set_index("Description", inplace=True)

    mars_data_html = mars_data.to_html()
    mars_data_html.replace("\n",'')
    mars_table = mars_data.to_html("mars_facts.html")

#add to dict
    scraped_data['mars_table'] = mars_table

    browser.quit()

#hemishperes
    hemi_url = "https://marshemispheres.com/"
    browser.visit(hemi_url)

    hemi_html = browser.html
    hsoup = BeautifulSoup(hemi_html, 'html.parser')

    all_hemis = hsoup.find_all('div', class_="item")

    hemisphere_image_urls = []

    for img in all_hemis:
        title = img.find("h3").text
        h_image = img.find("a", class_="itemLink product-item")["href"]
    
        browser.visit(hemi_url + h_image)
    
        image_html = browser.html
        information = BeautifulSoup(image_html, "html.parser")
    
        img_url = hemi_url + information.find("img", class_="thumb")["src"]
    
        hemisphere_image_urls.append({"title" : title, "img_url" : img_url})

#add to dict
        scraped_data['hemisphere_image_urls'] = hemisphere_image_urls

    browser.quit()

    return scraped_data
