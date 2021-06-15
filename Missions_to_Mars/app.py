from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

@app.route('/')
def index():

    mars_d = mongo.db.mars_d.find_one()
    return render_template('index.html', mars_d = mars_d)
    
@app.route('/scrape')
def scrape():
    mars = scrape_mars.scrape()

    mars_d = mongo.db.mars_d
    mars_d.update(
        {},
        mars,
        upset=True
    )
    return redirect("/", code=302)

if __name__ == "__main__":
	app.run(debug=True) 


