# all the same import of api will be here
from src.package import *
# -----------------------------------------------------------------------------
from src.configs import role, limitFindBorrowed, roleHigherThanUser, limitBooks
from src.utils import getToken, getAccountWithId, convertDateForSeria, formatLog
# -----------------------------------------------------------------------------

class Borrowed(Resource):
	# get borrowed with id
	def get(self):
		try:
			token = getToken(request.headers['Authorization'])
			borrowedId = request.args['borrowedId']
			username = borrowedId.split('-')[0]

			# token expired
			if token == None:
				return 'Unauthorized', 401
			# check if user is admin or is that exact user who borrowed the book
			if(token['role'] not in roleHigherThanUser):
				if(username == role['username']):
					return 'Unauthorized', 401

			result = db.borrowed.find_one({'_id': borrowedId})
			result = convertDateForSeria(result)

			return {'borrowed': result}, 200
		except Exception as e:
			logging.info('error getBorrowed %s', e)
		return '', 400

	# update info of borrowed
	def post(self):
		try:
			json = request.json
			token = getToken(json['token'])
			borrowed = json['borrowed']

			# check is admin or manager
			if token['role'] not in roleHigherThanUser:
				return 'Unauthorized', 401
			
			with client.start_session() as s:
				with session.start_transaction():
					pass
		except Exception as e:
			logging.info('error postBorrowed: %s', e)
		return 'Invalid', 400

class GetSearchBorrowed(Resource):
	def get(self):
		try:
			# check auth and role of user
			token = getToken(request.headers['Authorization'])
			if token == None:
				return 'Unauthorized', 401
			# check permission
			if token['role'] not in roleHigherThanUser:
				return 'Unauthorized', 401
			
			# if search borrowed with username => search only with that borrowed by user
			search = {}
			try:
				username = request.args['username']
				if username != '':
					search['username'] = re.compile(username, re.IGNORECASE)
			except:
				pass

			# check if page is in input
			try:
				page = int(request.args['page'])
			except:
				page = 0

			borrowed = []
			if search != {}:
				# when search with param
				result = db.borrowed.find(search).skip(limitFindBorrowed * page).limit(limitFindBorrowed).sort("_id")
			else:
				# when search is empty
				result = db.borrowed.find().skip(limitFindBorrowed * page).limit(limitFindBorrowed).sort("_id")

			for borrwed in result:
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

			return {'borrowed': borrowed}, 200
		except Exception as e:
			logging.info('error searchBorrowed: %s', e)
		return 'Invalid', 400
