from flask import Flask
from flask_restful import Api
from flask_cors import CORS
import logging
# -----------------------------------------------------------------------------
from src.book import GetBook, GetBooks, GetSearchBook

from src.auth import Login, SignUp, GetPermission
from src.admin import GetUsersInfo
# ------------------------------------------------------------------------------
app = Flask(__name__)
# for develop
app.debug = True
api = Api(app)
CORS(app)

# for develop
logging.basicConfig(level = logging.INFO)
# book
api.add_resource(GetBook, "/GetBook")
api.add_resource(GetBooks, "/GetBooks")
api.add_resource(GetSearchBook, "/GetSearchBook")

# auth
api.add_resource(Login, "/Login")
api.add_resource(SignUp, "/SignUp")
api.add_resource(GetPermission, "/Permission")

# admin
api.add_resource(GetUsersInfo, "/Admin/GetUsers")

if __name__ == "__main__":
  app.run()