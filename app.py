from flask import Flask
from flask_restful import Api
from flask_cors import CORS
import logging
# -----------------------------------------------------------------------------
from src.book import GetBook, GetSearchBook, BorrowBook, IsBorrowedById, CancelBookOrder
from src.auth import GetPermission, IsTokenExpire, Logout
from src.admin import GetUsersInfo, SetAccountRole
from src.manager import GetBorrowed, DeleteBook, EditBook, GetUserWithId, ActiveAccount, AddBook, Configs
from src.account import Login, SignUp, GetUserBorrowed, AccountInfo
from src.subject import Subjects
from src.borrowed import Borrowed, GetSearchBorrowed, UpdateBorrowed, PayFee
from src.author import GetAuthor
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
api.add_resource(IsBorrowedById, "/IsBorrowedById") # get
api.add_resource(CancelBookOrder, "/CancelBookOrder") # get

# auth
api.add_resource(GetPermission, "/Permission") # get
api.add_resource(IsTokenExpire, "/CheckToken") # get
api.add_resource(Logout, "/Logout") # post

# account
api.add_resource(Login, "/Login") # get
api.add_resource(SignUp, "/SignUp") # post
api.add_resource(GetUserBorrowed, "/User/GetBorrowed") # get 
  # get: get account info
  # post: update account
api.add_resource(AccountInfo, "/User/Info")

# admin
api.add_resource(GetUsersInfo, "/Admin/GetUsers") # get
api.add_resource(SetAccountRole, "/Admin/SetRole") # post

# manager
api.add_resource(GetUserWithId, "/Manager/GetUser") # get
api.add_resource(GetBorrowed, "/Manager/GetBorrowed") # get
api.add_resource(DeleteBook, "/Manager/DeleteBook") # post
api.add_resource(EditBook, "/Manager/EditBook") # post
api.add_resource(AddBook, "/Manager/AddBook") # post
api.add_resource(ActiveAccount, "/Manager/ActiveAccount") # post
api.add_resource(Configs, "/Manager/Config") # get/post

# subject
api.add_resource(Subjects, "/Subjects") # post

# borrowed
api.add_resource(Borrowed, "/Borrowed") # get/post
api.add_resource(GetSearchBorrowed, "/SearchBorrowed") # get
api.add_resource(UpdateBorrowed, "/UpdateBorrowed") # post
api.add_resource(PayFee, "/PayFee") # post

# author
api.add_resource(GetAuthor, "/Author") # get

if __name__ == "__main__":
  app.run()
