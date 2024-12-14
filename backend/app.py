from flask import Flask
from flask_cors import CORS
from api import gpt
from models import database
from dotenv import load_dotenv
import os

app = Flask(__name__)
CORS(app)

# config and initilize databse
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{app.instance_path}/spotify_ai.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
database.init_app(app)

app.register_blueprint(gpt, url_prefix='/gpt')

@app.route('/')
def home():
    return "App is running with the database!"

if __name__ == '__main__':
  app.run(debug=True, port=5001)