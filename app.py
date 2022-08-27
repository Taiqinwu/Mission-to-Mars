# The first line says that we'll use Flask to render a template, redirecting to another url, and creating a URL.
from flask import Flask, render_template, redirect, url_for
# The second line says we'll use PyMongo to interact with our Mongo database.
from flask_pymongo import PyMongo
# The third line says that to use the scraping code, we will convert from Jupyter notebook to Python.
import scraping

# __name__ is the name of the current Python module. 
# The app needs to know where it’s located to set up some paths.
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
# app.config["MONGO_URI"] tells Python that our app will connect to Mongo using a URI, 
# a uniform resource identifier similar to a URL.

# "mongodb://localhost:27017/mars_app" is the URI we'll be using to connect our app to Mongo. 
# This URI is saying that the app can reach Mongo through our localhost server, 
# using port 27017, using a database named "mars_app".
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"

mongo = PyMongo(app)

@app.route("/") # tells Flask what to display when we're looking at the home page
def index():
   mars = mongo.db.mars.find_one()
   return render_template("index.html", mars=mars)

# Create a button that scrape date
@app.route("/scrape")
def scrape():
   mars = mongo.db.mars
   mars_data = scraping.scrape_all() # In this line, we're referencing the scrape_all function in the scraping.py file exported from Jupyter Notebook.
   mars.update_one({}, {"$set":mars_data}, upsert=True)
   return redirect('/', code=302) # This will navigate our page back to / where we can see the updated content

if __name__ == "__main__":
   app.run()