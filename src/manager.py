# all the same import of api will be here
from src.package import *
# -----------------------------------------------------------------------------
from src.configs import role, limitFindBorrowed, roleHigherThanUser
from src.utils import isJsonValid, getToken, getAccountWithId, convertDateForSeria, getBookWithId, formatLog
# -----------------------------------------------------------------------------

class GetBorrowed(Resource):
	def get(self):
		try:
			# params
			token = getToken(request.headers['Authorization'])
			if token == None:
				return 'Unauthorized', 401
			# check permission
			if token['role'] not in roleHigherThanUser:
				return 'Unauthorized', 401
				
			try:
				page = int(request.args['page'])
			except:
				page = 0
		
			
			borrowed = []
			for i in db.borrowed.find({ "deleted" : { "$exists" : False } }).skip(page * limitFindBorrowed).limit(limitFindBorrowed).sort('date_borrow'):
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
			# check user permission
			if token == None or token['role'] not in roleHigherThanUser:
				return 'Unauthorized', 401

			bookNew = json['book']
			bookOld = getBookWithId(bookNew['isbn'])
			
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

			if 'birth' in user:
				user['birth'] = convertDateForSeria(user['birth']).split(' ')[0]
			if 'date_created' in user:
				user['date_created'] = convertDateForSeria(user['date_created']).split(' ')[0]
			if 'date_expire' in user:
				user['date_expire'] = convertDateForSeria(user['date_expire']).split(' ')[0]

			return {'user': user}, 200

		except Exception as e:
			logging.info('error getUserWithId: %s', e)
		return 'Invalid', 400
		
# this route use for block/un-block or active/deactive account
# block => user can't use that account any more
# active => user can borrow book from library
class ActiveAccount(Resource):
	def post(self):
		try:
			# params
			json = request.get_json()['json']
			token = getToken(json['token'])
			# check permission
			if token == None or token['role'] not in roleHigherThanUser:
				return 'Unauthorized', 401

			# get account
			account = getAccountWithId(json['username'])

			# check if that account not admin
			if account['role'] != 'admin':
				update_account = {}
				# get current stage of block/active of account
				if 'active' in account and json['action'] == 'active':
					update_account['active'] = not account['active']
				elif 'blocked' in account and json['action'] == 'block':
					update_account['blocked'] = not account['blocked']
				else:
					return 'none', 200

				# update account
				with client.start_session() as s:
					with s.start_transaction():
						u = db.account.update_one(
							{'_id': account['_id']},
							{'$set': update_account},
							session = s
						)
						# action name
						if json['action'] == 'block' and update_account['blocked']:
							action = 'block account'
						elif json['action'] == 'block':
							action = 'un-block account'
						elif json['action'] == 'active' and update_account['active']:
							action = 'active account'
						else:
							action = 'deactive account'
						# some note
						note = {
							'account': account['_id']
						}
						# add to log
						db.logging.insert_one(formatLog(token, action, note))

			return 'done', 200

		except Exception as e:
			logging.info('error postActiveAccount: %s', e)
		return 'Invalid', 400


class AddBook(Resource):
	def post(self):
		try: 
			# json = {'token', 'book' }
			json = request.get_json()['json']
			token = getToken(json['token'])
			# check permission
			if token == None or token['role'] not in roleHigherThanUser:
				return 'Unauthorized', 401

			book = json['book']
			book['_id'] = db.bookTitle.find().count() + 1
			book.pop('isbn')
			
			with client.start_session() as s:
				with s.start_transaction():
					i = db.bookTitle.insert_one(book)

			return 'done', 200

		except Exception as e:
			logging.info('error postAddBook: %s', e)
		return 'Invalid', 400
