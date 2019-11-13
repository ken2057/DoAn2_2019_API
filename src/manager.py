# all the same import of api will be here
from src.package import *
# -----------------------------------------------------------------------------
from src.configs import role, limitBorrow, roleHigherThanUser
from src.utils import isJsonValid, getToken, getAccountWithId, convertDateForSeria, getBookWithId, formatLog
# -----------------------------------------------------------------------------

class GetBorrowed(Resource):
	def get(self):
		try:
			# params
			token = getToken(request.headers['Authorization'])
			if token == None:
				return 'Unauthorized', 401
			try:
				page = int(request.args['page'])
			except:
				page = 0
		
			# check permission
			if token['role'] not in roleHigherThanUser:
				raise Exception('Not admin or manager: %s', token)
			
			borrowed = []
			for i in db.borrowed.find({ "deleted" : { "$exists" : False } }).skip(page * limitBorrow).limit(limitBorrow).sort('date_borrow'):
				# convert datetime in history_status
				newHS = []
				for hs in i['history_status']:
					newHS.append({
						'status': hs['status'],
						'date': convertDateForSeria(hs['date'])
					})
				i['history_status'] = newHS
				i['_id'] = i['_id'].__str__()

				borrowed.append(convertDateForSeria(i))

			return { 'borrowed': borrowed }, 200

		except Exception as e:
			logging.info('error getBorrowed: %s', e)
		return 'Invalid', 400

class EditBook(Resource):
	def post(self):
		try:
			# json will have: token, Obj(book)
			json = request.get_json()['json']
			token = getToken(json['token'])
			if token == None:
				return 'Unauthorized', 401

			bookNew = json['book']
			bookOld = getBookWithId(bookNew['isbn'])

			# if not have permission
			if token['role'] not in roleHigherThanUser:
				raise Exception('Delete book without permission: %s', token)
			
			# update
			with client.start_session() as s:
				with s.start_transaction():
					d = db.bookTitle.delete_one({'_id': bookNew['isbn']}, session=s)
					i = db.bookTitle.insert_one({
						'_id': bookNew['isbn'],
						'name': bookNew['name'],
						'author': bookNew['author'],
						'subjects': bookNew['subjects'],
						'books': bookNew['books'],
						'image': bookNew['image'],
						'deleted': False,
						'year_released': bookNew['year_released'],
						'publisher': bookNew['publisher'],
						'price': bookNew['price']
						}, session=s)
					db.logging.insert_one(formatLog(token, 'insert book', {'old':bookOld, 'new':bookNew}))
			return 'done', 200

		except Exception as e:
			logging.info('error editBook: %s', e)
		return 'Invalid', 400

class DeleteBook(Resource):
	def post(self):
		try:

			# json will have: bookId
			json = request.get_json()['json']
			token = getToken(json['token'])
			if token == None:
				return 'Unauthorized', 401
			book = getBookWithId(json['bookId'])

			# if not have permission
			if token['role'] not in roleHigherThanUser:
				raise Exception('Delete book without permission: %s', token)
			
			# update book
			with client.start_session() as s:
				with s.start_transaction():
					u = db.bookTitle.update_one({'_id': book['_id']}, { '$set': { 'deleted': True }}, session=s)
					log = formatLog(token, 'delete book', 'bookId: ' + str(book['_id']))
					i = db.log.insert_one(log, session=s)
			return 'done', 200

		except Exception as e:
			logging.info('error deleteBook: %s', e)
		return 'Invalid', 400

class GetUserWithId(Resource):
	def get(self):
		try:
			# params
			token = getToken(request.headers['Authorization'])
			if token == None:
				return 'Unauthorized', 401

			# check permission
			if(token['role'] not in roleHigherThanUser):
				raise Exception('Not permission to get user info: %s', token)

			user = db.account.find_one({'_id': request.args['username']})
			user = convertDateForSeria(user)
			user.pop('password')

			return {'user': user}, 200

		except Exception as e:
			logging.info('error getUserWithId: %s', e)
		return 'Invalid', 400
		
class ActiveAccount(Resource):
	def post(self):
		try:
			# params
			json = request.get_json()['json']
			token = getToken(json['token'])
			if token == None:
				return 'Unauthorized', 401
			
			# check permission
			if(token['role'] not in roleHigherThanUser):
				raise Exception('Not permission to get user info: %s', token)
			
			# get account
			account = getAccountWithId(json['username'])

			# check if that account not admin
			if account['role'] != 'admin':
				active = True
				if 'active' in account:
					active = account['active']
				# update book
				with client.start_session() as s:
					with s.start_transaction():
						u = db.account.update_one(
							{'_id': account['_id']},
							{'$set': {'active': not active}},
							session = s
						)
			return 'done', 200

		except Exception as e:
			logging.info('error postActiveAccount: %s', e)
		return 'Invalid', 400
