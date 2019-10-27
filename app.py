from flask import Flask
from flask_restful import Api
from flask_cors import CORS
import logging
# -----------------------------------------------------------------------------
from src.book import GetBook, GetSearchBook, BorrowBook, ReturnBook, IsBorrowedById
from src.auth import GetPermission, IsTokenExpire
from src.admin import GetUsersInfo, SetAccountRole
from src.manager import GetBorrowed
from src.account import Login, SignUp, GetUserBorrowed
# ------------------------------------------------------------------------------
app = Flask(__name__)
# for develop
app.debug = True
api = Api(app)
CORS(app)

# for develop
logging.basicConfig(level = logging.INFO)

# book
api.add_resource(GetBook, "/GetBook") #get
api.add_resource(GetSearchBook, "/GetSearchBook") #get
  # post: borrow a book
  # get: check does that book still avaiable
api.add_resource(BorrowBook, "/BorrowBook") # post/get
api.add_resource(ReturnBook, "/ReturnBook") # post
api.add_resource(IsBorrowedById, "/IsBorrowedById") # get

# auth
api.add_resource(GetPermission, "/Permission") # get
api.add_resource(IsTokenExpire, "/CheckToken") # get

# account
api.add_resource(Login, "/Login") # get
api.add_resource(SignUp, "/SignUp") # post
api.add_resource(GetUserBorrowed, "/User/GetBorrowed") # get

# admin
api.add_resource(GetUsersInfo, "/Admin/GetUsers") # get
api.add_resource(SetAccountRole, "/Admin/SetRole") # post

# manager
api.add_resource(GetBorrowed, "/Manager/GetBorrowed") # get

if __name__ == "__main__":
  app.run()