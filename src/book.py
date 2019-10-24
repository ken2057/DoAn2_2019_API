from flask_restful import Resource
from flask import request
from datetime import datetime, timedelta
import logging, re
# -----------------------------------------------------------------------------
from src.configs import db, limitBooks, statusBorrow
from src.utils import isJsonValid, getToken, calcBorrowExpireTime
from src.utils import getAccountWithId, getBookWithId
# -----------------------------------------------------------------------------
## Get book
class GetBook(Resource):
	def get(self):
		bookId = int(request.args['bookId'])
		try:
			return getBookWithId(bookId), 200
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

		try:
			find = None
			if search != []:
				find = db.bookTitle.find(find).skip(limitBooks * page).limit(limitBooks)
			else:
				# find all
				find = db.bookTitle.find().skip(limitBooks * page).limit(limitBooks)

			for book in find:
					books.append(book)

			return {'books': books}, 200
		except Exception as e:
			logging.info('error searchBook: %s', e)
		return '', 400

class BorrowBook(Resource):
	# check can borrow book or not
	def get(self):
		try:
			bookId = int(request.args['bookId'])
			book = getBookWithId(bookId)

			flag = ('' in book['books'])
			return flag, 200
		except Exception as e:
			logging.info('error get borrowBook: %s', e)
		return '', 400

	# update book borrow
	def post(self):
		try:
			# json will have token + bookId
			json = request.get_json()
			token = getToken(json['token'])
			
			# get account, book from db
			account = getAccountWithId(token['username'])
			book = getBookWithId(int(json['bookId']))
			# some varibles
			now = datetime.now()
			borrowInfo = {
				'username': token['username'],
				'bookId': json['bookId'],
				'status': statusBorrow['start'],
				'date_borrow': now,
				'date_expire': calcBorrowExpireTime(now)
			}
			# add new Order
			account['borrowed'].append(borrowInfo)
			# get index of book not borrowed
			index = book['books'].index('')
			book['books'][index] = token['username']

			#
			# update db
			#
			db.account.update_one({'_id':token['username']}, { '$set': {'borrowed':account['borrowed']}})
			db.borrowed.insert_one(borrowInfo)
			db.bookTitle.update_one({'_id': json['bookId']}, { '$set': {'books': book['books']}})

			return 'done', 200

		except Exception as e:
			logging.info('error post orderBook: %s', e)
		return '', 400

class ReturnBook(Resource):
	def post(self):
		try:
			# json will have token, bookId, status (return/lost)
			json = request.get_json()
			token = getToken(json['token'])

			# get account, book from db
			account = getAccountWithId(token['username'])
			book = getBookWithId(int(json['bookId']))
			# get borrowed info
			borrowInfo = None
			for info in account['borrowed']:
				if info['bookId'] == json['bookId'] and info['status'] == statusBorrow['start']:
					borrowInfo = info
					break
			index = book['books'].index(token['username'])
			#
			# remove previous borrowed info
			#
			account['borrowed'].remove(borrowInfo)
			db.borrowed.delete_one(borrowInfo)
				# if user return book
			if json['status'] == 'return':
				book['books'][index] = ''
			else:
				# if user lost the book
				book['books'].remove(token['username'])
			
			#
			# update borrowed info
			#
			borrowInfo['status'] = statusBorrow[json['status']]
			if json['status'] == 'return':
				borrowInfo['date_return'] = datetime.now()

			account['borrowed'].append(borrowInfo)
			#
			# update db
			#
			db.account.update_one({'_id':token['username']}, { '$set': {'borrowed':account['borrowed']}})
			db.borrowed.insert_one(borrowInfo)
			db.bookTitle.update_one({'_id': json['bookId']}, { '$set': {'books': book['books']}})

			return 'done', 200

		except Exception as e:
			logging.info('error returnBook: %s', e)
