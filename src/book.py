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

## Get books 
class GetBooks(Resource):
	def get(self):
		# check int
		try:
			page = int(request.args['page'])
		except:
			page = 0

		books = []
		for book in db.bookTitle.find().skip(limitBooks * page).limit(limitBooks):
			books.append(book)
		return {'books': books}, 200

## Get books with name
class GetBooksWithName(Resource):
	def get(self):
		name = request.args['name']
		# check int
		try:
			page = int(request.args['page'])
		except:
			page = 0

		books = []
		# pymongo query
		regex = re.compile(name, re.IGNORECASE)
		find = {'name': regex}

		for book in db.bookTitle.find(find).skip(limitBooks * page).limit(limitBooks):
			books.append(book)
		return {'books': books}, 200

## Get books with subject
class GetBooksWithSubject(Resource):
	def get(self):
		subject = request.args['subject']
		# check int
		try:
			page = int(request.args['page'])
		except:
			page = 0

		books = []
		# pymongo query
		regex = re.compile(subject, re.IGNORECASE)
		find = {'subjects': regex}

		for book in db.bookTitle.find(find).skip(limitBooks * page).limit(limitBooks):
			books.append(book)
		return {'books': books}, 200

## Get books with author
class GetBooksWithAuthor(Resource):
	def get(self):
		author = request.args['author']
		# check int
		try:
			page = int(request.args['page'])
		except:
			page = 0

		books = []
		# pymongo query
		regex = re.compile(author, re.IGNORECASE)
		find = {'author': regex}

		for book in db.bookTitle.find(find).skip(limitBooks * page).limit(limitBooks):
			books.append(book)
		return {'books': books}, 200

