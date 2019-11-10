import os
from flask import Flask, render_template, redirect, request, url_for, Response
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from gridfs import GridFS

app = Flask(__name__)

app.config["MONGO_DBNAME"] = 'IraqDB'
app.config["MONGO_URI"] = os.getenv('MONGO_URI', 'mongodb://localhost')

mongo = PyMongo(app)
files = GridFS(mongo.db)
@app.route('/')

# for home page
@app.route('/home')
def home():
    return render_template("home.html", login=mongo.db.IQ2019.find())
    
# for register form to To save data in mongodb
@app.route('/register', methods=['POST']) 
def register():
    print(request.form)
    data = dict(request.form)
    user_name = data['user_name']
    password = data['password']
    mongo.db.users.insert_one({"user_name": user_name, "password": password})
    return redirect(url_for('get_recipes'))
    
# for login form to join with mongodb data
@app.route('/login', methods=['POST'])
def login():
    data = dict(request.form)
    print(data)
    user_name = data['user_name']
    password = data['password']
    mongo_data = mongo.db.users.find_one({"user_name": user_name})
    print(mongo_data)
    return render_template("home.html")
  
 # for add recipes  
@app.route('/add_recipes')
def add_recipes():
    return render_template('addrecipes.html',
                           Categories=mongo.db.OfIraqMDB.find())
    
@app.route('/insert_recipe', methods=['POST'])
def insert_recipe():
    recipes = mongo.db.recipes
    if 'recipe_image' not in request.files:
        return "Error"
    image = request.files.get('recipe_image')
    files.put(
        image,
        content_type=image.content_type,
        filename=image.filename
    )
    recipe_data = (request.form.to_dict())
    recipe_data['recipe_image'] = image.filename
    recipes.insert_one(recipe_data)
    return redirect(url_for('get_recipes'))

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
             port=int(os.environ.get('PORT')),
             debug=True)
