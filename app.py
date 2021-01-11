import datetime as dt
import numpy as np
import pandas as pd
from flask import Flask, jsonify, render_template, redirect
import json
import random
import scrape_mars 
import pymongo

#######################################################

app = Flask(__name__)

#mongo init
conn = 'mongodb://localhost:27017'
# Pass connection to the pymongo instance.
client = pymongo.MongoClient(conn)
# Connect to a database. Will create one if not already available.
db = client.mars_app


@app.route("/")
def home():

    # this is hard coded; want to pull data from mongodb
    #mars_articles = {
    #    "news_title": "Alexfdasf dsaf dsafsda fsda fsadf sdafsadander",
    #    "news_paragraph": " dfaf dsafdsa fdas fsdaf sdaf sadfsd afsda fsad fsda fsaf sdafsad "}
    #mars = scrape()
    mars = db.mars_data.find_one()

    return(render_template("index.html", mars = mars)) #, dict_info = myDict))

# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():
    #scrape data
    scraped_data = scrape_mars.scrape()
    #update database
    db.mars_data.update({}, scraped_data, upsert=True)
    return redirect("/", code=302)



if __name__ == "__main__":
    app.run(debug=True)
