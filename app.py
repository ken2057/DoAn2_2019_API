from flask import Flask
from flask_restful import Api
from flask_cors import CORS
import logging

from src.book import GetBook
from src.auth import Login, SignUp

app = Flask(__name__)
#for develop
app.debug = True
api = Api(app)
CORS(app)

#for develop
logging.basicConfig(level = logging.INFO)

api.add_resource(GetBook, "/GetBook/<int:bookId>")
api.add_resource(Login, "/Login/")

if __name__ == "__main__":
  app.run()