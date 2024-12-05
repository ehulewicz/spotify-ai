from flask import Flask
from flask_cors import CORS
from backend.gpt import gpt

app = Flask(__name__)
CORS(app)

app.register_blueprint(chat_route, url_prefix='/gpt')

if __name__ == '__main__':
  app.run(debug=True, port=5001)