from flask import Flask
from flask_restful import Api
from flask_cors import CORS
import logging
# -----------------------------------------------------------------------------
from src.book import GetBook, GetBooks
from src.book import GetBooksWithName, GetBooksWithSubject
from src.book import GetBooksWithAuthor

from src.auth import Login, SignUp, GetPermission
from src.admin import GetUsersInfo
# -----------------------------------------------------------------------------
app = Flask(__name__)
# for develop
app.debug = True
api = Api(app)
CORS(app)

# for develop
logging.basicConfig(level = logging.INFO)
# book
api.add_resource(GetBook, "/GetBook/<int:bookId>")
api.add_resource(GetBooks, "/GetBooks/<int:page>")
api.add_resource(GetBooksWithName, "/GetBooksName/<string:name>/<int:page>")
api.add_resource(GetBooksWithSubject, "/GetBooksSubject/<string:subject>/<int:page>")
api.add_resource(GetBooksWithAuthor, "/GetBooksAuthor/<string:author>/<int:page>")

# auth
api.add_resource(Login, "/Login")
api.add_resource(SignUp, "/SignUp")
api.add_resource(GetPermission, "/Permission/<string:token>")

# admin
api.add_resource(GetUsersInfo, "/Admin/GetUsers")

if __name__ == "__main__":
  app.run()