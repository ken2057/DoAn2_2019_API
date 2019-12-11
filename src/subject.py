# all the same import of api will be here
from src.package import *
import re
# -----------------------------------------------------------------------------
from src.utils import getToken, formatLog
from src.configs import roleHigherThanUser
# -----------------------------------------------------------------------------

class Subjects(Resource):
	def get(self):
		subjects = []
		for subject in db.subject.find():
			subjects.append(subject['_id'])

		return {'subjects': subjects}, 200

	def post(self):
		try:
			# json = {'token', 'subjectName', 'action', 'oldSubject' }
			json = request.get_json()['json']
			token = getToken(json['token'])
			# check permission
			if token == None or token['role'] not in roleHigherThanUser:
				return 'Unauthorized', 401
			# 'action' will be 'add' / 'edit'
			if json['action'] not in ['add', 'edit', 'delete']:
				raise Exception(json)

			with client.start_session() as s:
				with s.start_transaction():
					if json['action'] in ['add', 'edit']:
						# check exists subject._id and method is add/edit
						subjects = db.subject.find()
						for sub in subjects:
							if sub['_id'].lower() == json['subjectName']:
								message = 'Already exist Subject name "' + json['subjectName'] +'"'
								return message, 400
					else:
						# delete subject in subject doc
						d = db.subject.delete_one({'_id': json['subjectName']})

						# delete subject in book
						books = db.book.find({'subjects': {'$elemMatch': {'$eq': json['subjectName']}}})
						list_books = []
						for b in books:
							list_books.append(b['_id'])
							b['subjects'].remove(json['subjectName'])
							d = db.book.update_one({'_id': b['_id']}, { '$set': {'subjects': b['subjects']}}, session=s)

						# add log
						note = {
							'subject': json['subjectName'],
							'books_affected': list_books
						}
						db.log.insert_one(formatLog(token, 'delete subject', note))

					# add or edit subject
					if json['action'] == 'add':
						# insert
						i = db.subject.insert_one({'_id': json['subjectName']}, session=s)

						# add log
						note = {
							'subject': json['subjectName']
						}
						db.log.insert_one(formatLog(token, 'add subject', note))
					elif json['action'] == 'edit':
						# update subject
						d = db.subject.delete_one({'_id': json['oldSubject']}, session=s)
						i = db.subject.insert_one({'_id': json['subjectName']}, session=s)
						
						# change subject in book
						books = db.book.find({'subjects': {'$elemMatch': {'$eq': json['oldSubject']}}})
						for b in books:
							b['subjects'][b['subjects'].index(json['oldSubject'])] = json['subjectName']
							u = db.book.update_one({'_id': b['_id']}, { '$set': {'subjects': b['subjects']}}, session=s)

						# add log
						note = {
							'oldSubject': json['oldSubject'],
							'newSubject': json['subjectName'],
						}
						db.log.insert_one(formatLog(token, 'edit subject', note))
						
			return 'done', 200
			
		except Exception as e:
			logging.info('error postSubjects: %s', e)
		return 'Invalid', 400
