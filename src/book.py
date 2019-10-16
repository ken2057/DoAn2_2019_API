from flask_restful import Resource
from flask import request

import logging

from src.configs import db

## Get book information
class GetBook(Resource):
	def get(self, bookId):
		return db.bookTitle.find_one({'_id': bookId}), 200


