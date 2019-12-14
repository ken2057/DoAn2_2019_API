# all the same import of api will be here
from src.package import *
# -----------------------------------------------------------------------------
from src.utils import getToken, formatDate, convertDateForSeria
from src.configs import roleHigherThanUser
# -----------------------------------------------------------------------------

class RpExpireBorrowed(Resource):
	def get(self):
		try:
			token = getToken(request.headers['Authorization'])
			# token expired or not admin
			if token == None or token['role'] not in roleHigherThanUser:
				return 'Unauthorized', 401

			month = int(request.args['month'])
			year = int(request.args['year'])

			borrowedInfo = []
			listBookId = []

			# get borrowed info match condition
			searchBorrowed = {
				'date_borrow': {'$exists': True},
				'date_return': {'$ne': ''}
			}
			for r in db.borrowed.find(searchBorrowed):
				date_borrow = r['date_borrow']
				if date_borrow.year == year and date_borrow.month == month:
					if r['bookId'] not in listBookId:
						listBookId.append(r['bookId'])

					borrowedInfo.append({
						'bookId': r['bookId'],
						'date_borrow': convertDateForSeria(r['date_borrow']).split(' ')[0],
						'total_date_late': (r['date_return'] - r['date_borrow']).days
					})

			# get the book name from above
			searchBook = {
				'_id': {'$in': listBookId}
			}
			for b in db.book.find(searchBook):
				for i in borrowedInfo:
					if 'bookId' in i and i['bookId'] == b['_id']:
						i['bookName'] = b['name']
						i.pop('bookId')

			return {'reports': borrowedInfo}, 200

		except Exception as e:
			logging.info('error getRpExpireBorrowed: %s', e)
		return 'Invalid', 400

class RpSubjectBorrowed(Resource):
	def get(self):
		try:
			token = getToken(request.headers['Authorization'])
			# token expired or not admin
			if token == None or token['role'] not in roleHigherThanUser:
				return 'Unauthorized', 401

			month = int(request.args['month'])
			year = int(request.args['year'])

			borrowedInfo = []
			dictBookId = {}
			totalBorrow = 0

			# get borrowed info match condition
			searchBorrowed = {
				'date_borrow': {'$exists': True},
				'date_return': {'$ne': ''}
			}
			for r in db.borrowed.find(searchBorrowed):
				date_borrow = r['date_borrow']
				if date_borrow.year == year and date_borrow.month == month:
					if r['bookId'] not in dictBookId:
						dictBookId[r['bookId']] = 1
					else:
						dictBookId[r['bookId']] += 1
					totalBorrow += 1

			# get the book subject from above
			searchBook = {
				'_id': {'$in': [x for x in dictBookId]}
			}
			
			for b in db.book.find(searchBook):
				subject = [x for x in b['subjects'] if x != '']
				subject.sort()
				if len(subject) == 0:
					i = 'none'
				else:
					i = ','.join(subject)

				for borrowed in borrowedInfo:
					if i == borrowed['subject']:
						borrowed['total_borrowed'] += dictBookId[b['_id']]
						break
				else:
					borrowedInfo.append({
						'subject': i,
						'total_borrowed': dictBookId[b['_id']]
					})
				
						
			# calculate ratio
			sumRatio = float(sum([x['total_borrowed'] for x in borrowedInfo]))
			for i in borrowedInfo:
				i['ratio'] = i['total_borrowed'] / sumRatio * 100

			return {'reports': borrowedInfo, 'total': totalBorrow}, 200
		except Exception as e:
			logging.info('error getRpExpireBorrowed: %s', e)
		return 'Invalid', 400
