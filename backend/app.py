from flask import Flask
from flask_cors import CORS
from gpt import gpt

app = Flask(__name__)
CORS(app)

app.register_blueprint(gpt, url_prefix='/gpt')

if __name__ == '__main__':
  app.run(debug=True, port=5001)