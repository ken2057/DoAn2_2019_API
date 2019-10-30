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
			token = getToken(request.args['token'])
			try:
				page = int(request.args['page'])
			except:
				page = 0
		
			# check permission
			if token['role'] not in roleHigherThanUser:
				raise Exception('Not admin or manager: %s', token)
			
			borrowed = []
			for i in db.borrowed.find().skip(page * limitBorrow).limit(limitBorrow):
				i.pop('_id')
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
			bookNew = json['book']
			bookOld

			# if not have permission
			if token['role'] not in roleHigherThanUser:
				raise Exception('Delete book without permission: %s', token)
			
			# update
			db.bookTitle.remove_one({'_id': bookNew['isbn']})
			db.bookTitle.insert_one({
				'_id': bookNew['isbn'],
				'name': bookNew['name'],
				'author': bookNew['author'],
				'subjects': bookNew['subjects'],
				'books': bookNew['books'],
				'image': bookNew['image'],
				'deleted': bookNew['deleted']
				})
			db.logging.insert_one(formatLog(token, 'insert book', {'old':bookOld, 'new':bookNew}))
			return 'done', 200

		except Exception as e:
			logging.info('error editBook: %s', e)
		return 'Invalid', 400

class DeleteBook(Resource):
	def post(self):
		try:
			# json will have: token, bookId
			json = request.get_json()['json']
			token = getToken(json['token'])
			book = getBookWithId(json['bookId'])

			# if not have permission
			if token['role'] not in roleHigherThanUser:
				raise Exception('Delete book without permission: %s', token)
			
			# update book
			db.bookTitle.update_one({'_id': book['_id']}, { '$set': { 'deleted': True }})
			log = formatLog(token, 'delete book', 'bookId: ' + str(book['_id']))
			db.log.insert_one(log)
			return 'done', 200

		except Exception as e:
			logging.info('error deleteBook: %s', e)
		return 'Invalid', 400