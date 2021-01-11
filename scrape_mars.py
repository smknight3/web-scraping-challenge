from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import requests
import datetime
import pymongo
import json
import time
import pandas as pd

def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = init_browser()
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url) 
    #browser.reload()
    time.sleep(2)
    soup = BeautifulSoup(browser.html, "lxml")

    newsTitle = soup.find_all("div", class_="content_title")[1].text.strip()
    print(newsTitle)

    newsPara = soup.find("div", class_="article_teaser_body").text.strip()
    print(newsPara)

    #is this assigning url string? src="/spaceimages/images/mediumsize/PIA19141_ip.jpg"
    # featured_image_url = soup.find("img", class_= "fancybox-image")
    # #or, altho this doesn't include the https 
    # url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    # browser.visit(url) 

    featured_image_url = 'https://www.jpl.nasa.gov/spaceimages/images/mediumsize/PIA19141_ip.jpg'


    url = 'https://space-facts.com/mars/'
    response = requests.get(url)
    print(response.status_code)

    tables = pd.read_html(url)

    df = tables[0]

    html_table = df.to_html()
    print(html_table)

    html_table.replace('\n', '') 

    # df.to_html('table.html') 

    hemisphere_image_urls = [
        {"title": "Valles Marineris Hemisphere", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg"},
        {"title": "Cerberus Hemisphere", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg"},
        {"title": "Schiaparelli Hemisphere", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif/full.jpg"},
        {"title": "Syrtis Major Hemisphere", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg"},
    ]
    
    browser.quit()

    data = {
        "news_title": newsTitle,
        "news_paragraph": newsPara, 
        "hemisphere_images": hemisphere_image_urls,
        "imglink": featured_image_url,
        "htmltable": html_table
        }

    return data

if __name__ == "__main__":
   scrape()

# html = response.content
# chowder = BeautifulSoup(html, "lxml")
# data = chowder.find_all("article", {"class":"article-item"})

# scraped_data = []

# for article in data:
#     header = article.find("h1", class_="article-item__headline").text.strip()
#     subheader = article.find("h2", class_="article-item__subheader").text.strip()
#     dude = article.find("span", class_="article-item__contributor").text.strip()
#     date_pub = article.find("span", class_="article-item__date")["data-date"]
    
#     clean = {
#         "header": header,
#         "subheader": subheader,
#         "writer": dude,
#         "published_date": date_pub,
#         "scraped_date": datetime.datetime.now()
#     }
    
#     scraped_data.append(clean)

# #init  lists
# teams = []
# ranks = []
# names = []
# ages = []
# etas = []

# for row in data:
#     #grab the text from each cell (identified by class)
#     team = row.find("td", class_= "rankings__table__cell--team").text.strip()
#     rank = row.find("td", class_= "rankings__table__cell--rank").text
#     name = row.find("td", class_= "rankings__table__cell--player").text.strip()
#     age = row.find("td", class_= "rankings__table__cell--currentAge").text
#     eta = row.find("td", class_= "rankings__table__cell--eta").text

#     #append to lists
#     teams.append(team)
#     ranks.append(rank)
#     names.append(name)
#     ages.append(age)
#     etas.append(eta)

# #append to dataframe
# df = pd.DataFrame()
# df["Team"] = teams
# df["Rank"] = ranks
# df["Name"] = names
# df["Age"] = ages
# df["ETAs"] = etas

# #clean columns
# df["Age"] = pd.to_numeric(df["Age"])
# df["ETAs"] = pd.to_numeric(df["ETAs"])


