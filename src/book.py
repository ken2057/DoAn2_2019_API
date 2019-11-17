# all the same import of api will be here
from src.package import *
import re
from copy import copy
# ------------------------------------------------------------------------------
from src.configs import limitBooks, statusBorrow, statusBorrow_block, minAccountPoint
from src.configs import maximumBookCanBorrow, maxTimeHoldOrder, userPoint
from src.utils import isJsonValid, getToken, calcBorrowExpireTime, calcDateExpire
from src.utils import getAccountWithId, getBookWithId, formatDate, formatHistoryStatus
# ------------------------------------------------------------------------------
# Get book


class GetBook(Resource):
	def removeHold(self, book, borrowId):
		# get data
		account = getAccountWithId(borrowId.split('-')[0])
		borrowed = db.borrowed.find_one({'_id': borrowId})

		# get borrow from user borrowed list
		acc_borrow = None
		acc_borrow_index = None
		for pos, b in enumerate(account['borrowed']):
			if b['_id'] == borrowId:
				acc_borrow = b
				acc_borrow_index = pos
				break

		# update local data
		book_index = book['books'].index(borrowId)
		book['books'][book_index] = ''

		acc_borrow['status'] = statusBorrow['hold_timeout']
		account['borrowed'].pop(acc_borrow_index)
		account['borrowed'].append(acc_borrow)
		update_account = {'borrowed': account['borrowed']}
		# if user have account_point remove -3 points for timeout hold
		if 'account_point' in account:			
			update_one['account_point'] = account['account_point'] + userPoint['hold_timeout']

		now = formatDate(datetime.now())
		h = formatHistoryStatus(statusBorrow['hold_timeout'], now, 'system')
		borrowed['history_status'].append(h)
		
		# start session to remove the hold
		with client.start_session() as s:
			with s.start_transaction():
				u = db.bookTitle.update_one(
					{'_id': book['_id']},
					{'$set': {'books': book['books']}},
					session = s
				)

				u = db.account.update_one(
					{'_id': account['_id']},
					{'$set': update_account},
					session = s	
				)

				u = db.borrowed.update_one(
					{'_id': borrowed['_id']},
					{'$set': {
						'status': statusBorrow['hold_timeout'],
						'history_status': borrowed['history_status']
					}},
					session = s	
				)

	def get(self):
		bookId = int(request.args['bookId'])
		try:
			book = getBookWithId(bookId)

			if book == None:
				return 'Not found', 400

			# check if any 'Get book from librarian' expire
			listBorrwedId = [x for x in book['books'] if x != '']
			for borrow in db.borrowed.find({'_id': {'$in': listBorrwedId}}):
				# if on hold
				if borrow['status'] == 'Get book from librarian':
					# get max time order will be keep
					# by getting the time borrowed + maxTimeHoldOrder
					timeHold = calcDateExpire(maxTimeHoldOrder, borrow['date_borrow'])[0]
					# if time from start hold expired
					if timeHold < datetime.now():
						# remove hold request and break
						self.removeHold(book, borrow['_id'])
						break

			return getBookWithId(bookId), 200
		except Exception as e:
			logging.info('error getbook: %s', e)
		return 'Invalid', 400


class GetSearchBook(Resource):
	def get(self):
		search = {'deleted': False}

		try:
			name = request.args['name']
			if name != '':
				search['name'] = re.compile(name, re.IGNORECASE)
		except:
			pass

		try:
			subject = request.args['subject']
			if subject != '':
				search['subjects'] = re.compile(subject, re.IGNORECASE)
		except:
			pass

		try:
			author = request.args['author']
			if author != '':
				search['author'] = re.compile(author, re.IGNORECASE)
		except:
			pass

		# check int
		try:
			page = int(request.args['page'])
		except:
			page = 0

		books = []
		try:
			find = db.bookTitle.find(search).skip(
				limitBooks * page).limit(limitBooks).sort("_id")

			for book in find:
				books.append(book)

			return {'books': books}, 200
		except Exception as e:
			logging.info('error searchBook: %s', e)
		return 'Invalid', 400


class BorrowBook(Resource):
	# check can borrow book or not
	def get(self):
		try:
			bookId = int(request.args['bookId'])
			book = getBookWithId(bookId)
			# check an empty book of that book can be borrow
			flag = ('' in book['books'])
			return flag, 200
		except Exception as e:
			logging.info('error get borrowBook: %s', e)
		return 'Invalid', 400

	# update book borrow
	def post(self):
		try:
			# json will have bookId
			json = request.get_json()['json']
			token = getToken(json['token'])
			if token == None:
				return 'Unauthorized', 401

			# get account, book from db
			account = getAccountWithId(token['username'])
			book = getBookWithId(int(json['bookId']))
			# if user already borrow this book, he/she can't borrow the second
			
			if token['username'] in book['books']:
				return "Can't borrow 2 same book", 400
			# if book not avaiable
			if '' not in book['books']:
				return 'Out of order', 400
			if (account['date_expire'] - datetime.now()).days < 0:
				return 'Your account have been expired', 400

			
			# some varibles
			now = formatDate(datetime.now())
			borrowInfo = {
				'_id': token['username'] + '-' + json['bookId'] + '-' + now.__str__(),
				'username': token['username'],
				'bookId': int(json['bookId']),
				'status': statusBorrow['wait_to_get'],
				'date_borrow': now,
				'date_expire': formatDate(calcBorrowExpireTime(now)),
				'date_return': ''
			}
			# add new Order
			account['borrowed'].append(copy(borrowInfo))
			# get index of book not borrowed
			index = book['books'].index('')
			book['books'][index] = borrowInfo['_id']
			# add data that only show in collection borrowed
			borrowInfo['history_status'] = [
				formatHistoryStatus(statusBorrow['wait_to_get'], now, token['username'])
			]

			#
			# update db
			#
			with client.start_session() as s:
				with s.start_transaction():
					u = db.bookTitle.update_one(
						{'_id': int(json['bookId'])},
						{'$set': {'books': book['books']}},
						session=s
					)
					u = db.account.update_one(
						{'_id': token['username']},
						{'$set': {'borrowed': account['borrowed']}},
						session=s
					)
					i = db.borrowed.insert_one(borrowInfo, session=s)

			return 'done', 200

		except Exception as e:
			logging.info('error post orderBook: %s', e)
		return 'Invalid', 400


class IsBorrowedById(Resource):
	def get(self):
		try:
			token = getToken(request.headers['Authorization'])
			flag = (token != None)
			# if token == None:
			# 	return 'Unauthorized', 401
			bookId = int(request.args['bookId'])
			book = getBookWithId(bookId)

			if flag:
				account = getAccountWithId(token['username'])
				history = account['borrowed']
				# if account not active by manager or admin
				# => it can't borrow the book
				if 'active' in account and not account['active']:
					return {'status': 'Your account is not active, contact the manager'}, 200
				# check if account_point <= -10 => block user from borrow
				if 'account_point' in account and account['account_point'] <= minAccountPoint:
					return {'status': 'You have been blocked from borrow book'}, 200
				if (account['date_expire'] - datetime.now()).days < 0:
					return {'status': 'Your account have been expired'}, 200

			# check if current user have been borrowed this book
			for i in book['books']:
				# if token not null and username- in string of borrowedId
				if flag and token['username']+'-' in i:
					# get all book on borrowed and order by user
					for h in history:
						if h['bookId'] == bookId and h['status'] in statusBorrow_block:
							return {'status': h['status']}, 200
				# when client access without login and have free book
				elif i == '':
					return {'status': 'Borrow'}, 200
			else:
				# if user borrowed 5 books then can't borrow any more
				if flag and maximumBookCanBorrow == len([h for h in history if h['status'] in statusBorrow_block]):
					return {'status': 'Maximum Book Can Borrow'}, 200

			return {'status': 'Out of order'}, 200

		except Exception as e:
			logging.info('error IsBorrowedById: %s', e)
		return 'Invalid', 400

class CancelBookOrder(Resource):
	def post(self):
		try:
			# json will have bookId, status (return/lost)
			json = request.get_json()['json']
			token = getToken(json['token'])
			if token == None:
				return 'Unauthorized', 401

			# get account, book from db
			book = getBookWithId(int(json['bookId']))
			account = getAccountWithId(token['username'])
			# get borrowed info
			borrowInfo = None
			for info in account['borrowed']:
				if info['bookId'] == int(json['bookId']) and info['status'] in statusBorrow_block:
					borrowInfo = info
					break
			else:
				return 'Not exists', 400

			index = book['books'].index(borrowInfo['_id'])
			#
			# remove previous borrowed info
			#
			account['borrowed'].remove(borrowInfo)
			history_in_borrowed = db.borrowed.find_one(
				{'_id': borrowInfo['_id']}
			)
			
			now = formatDate(datetime.now())
			# if user return book or cancel order
			# cancel can be call user/admin
			if account['_id'] == token['username']:
				book['books'][index] = ''
			else:
				return 'Unauthorized', 401

			#
			# update borrowed info
			#
			borrowInfo['status'] = statusBorrow['cancel']
			h = formatHistoryStatus(borrowInfo['status'], now, token['username'])

			account['borrowed'].append(borrowInfo)
			history_in_borrowed['history_status'].append(h)

			# update declare
			update_account = {'borrowed': account['borrowed']}
			# subtract account_point if account have point
			if 'account_point' in account:
				update_account['account_point'] = account['account_point'] + userPoint['cancel']

			update_borrowed = {
				'history_status': history_in_borrowed['history_status'], 
				'status': borrowInfo['status']
			}

			#
			# update db
			#
			with client.start_session() as s:
				with s.start_transaction():
					# update in Account
					u = db.account.update_one(
						{'_id': token['username']},
						{'$set': update_account },
						session=s
					)
					# update in Borrowed
					u = db.borrowed.update_one(
						{'_id': borrowInfo['_id']},
						{'$set': update_borrowed},
						session=s
					)
					# update in bookTitle
					u = db.bookTitle.update_one(
						{'_id': int(json['bookId'])},
						{'$set': {'books': book['books']}},
						session=s
					)

			return 'done', 200

		except Exception as e:
			logging.info('error CancelBookOrder: %s', e)
		return 'Invalid', 400
