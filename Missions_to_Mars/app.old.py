from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/info_mars"
mongo = PyMongo(app)

@app.route('/')
def index():

    info_mars = mongo.db.info_mars.find_one()
    return render_template('index.html', info_mars = info_mars)
    
@app.route('/scrape')
def scrape():
    info_mars = mongo.db.info_mars
    scrape_mars.scrape()
    info_mars.update(
        {},
        info_mars,
        upset=True
    )
    return redirect("/", code=302)

if __name__ == "__main__":
	app.run(debug=True) 