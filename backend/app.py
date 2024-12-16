from flask import Flask
from flask_cors import CORS
from api import gpt
from models import database
import os

app = Flask(__name__)
CORS(app)

print(f"Instance Path: {app.instance_path}")
print(f"Database Path: {os.path.join(app.instance_path, 'spotify_ai.db')}")
print(f"Current Directory: {os.getcwd()}")

# config and initilize databse
os.makedirs("instance", exist_ok=True)
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{app.instance_path}/spotify_ai.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
database.init_app(app)

app.register_blueprint(gpt, url_prefix='/gpt')

@app.route('/')
def home():
    return "App is running with the database!"

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5001, debug=True)