from flask_restful import Resource
from flask import request
import logging, re
# -----------------------------------------------------------------------------
from src.configs import db, limitBooks
from src.utils import isJsonValid, getToken
# -----------------------------------------------------------------------------
## Get book
class GetBook(Resource):
	def get(self):
		bookId = request.args['bookId']
		try:
			return db.bookTitle.find_one({'_id': int(bookId)}), 200
		except Exception as e:
			print('error getbook: ', e)
		return '', 400

class GetSearchBook(Resource):
	def get(self):
		search = []

		try:
			name = request.args['name']
			if name != '':
				search.append({'name': re.compile(name, re.IGNORECASE)})
		except:
			pass

		try:
			subject = request.args['subject']
			if subject != '':
				search.append({'subjects': re.compile(subject, re.IGNORECASE)})
		except:
			pass

		try:
			author = request.args['author']
			if author != '':
				search.append({'author': re.compile(author, re.IGNORECASE)})
		except:
			pass

		# check int
		try:
			page = int(request.args['page'])
		except:
			page = 0

		books = []
		# pymongo query
		find = { '$and': search}


		if search != []:
			for book in db.bookTitle.find(find).skip(limitBooks * page).limit(limitBooks):
				books.append(book)
		else:
			# find all
			for book in db.bookTitle.find().skip(limitBooks * page).limit(limitBooks):
				books.append(book)

		return {'books': books}, 200
