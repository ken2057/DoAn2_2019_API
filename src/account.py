# all the same import of api will be here
from src.package import *
from uuid import uuid4
# -----------------------------------------------------------------------------
from src.configs import tokenExpireTime, role, maxDateAccount
from src.utils import calcTokenExprieTime, getAccountWithId, getToken, convertDateForSeria, getTokenWithUser, calcDateExpire
# -----------------------------------------------------------------------------

## Login and return token
class Login(Resource):
	def findUser(self, username, password):
		return db.account.find_one({'_id': username, 'password': password})

	def createToken(self, account, ip):
		token = str(uuid4()).replace('-','')
		db.token.insert_one(
			{
				'_id': token, 
				'expires': calcTokenExprieTime(),
				'username': account['_id'],
				'role': account['role'],
				'ip': ip
			}
		)
		return token

	def get(self):
		try:
			username = request.args['username']
			password = request.args['password']
			ip = request.headers.get('X-Forwarded-For')

			account = self.findUser(username, password)
			if(account != None):
				# get old token if exist
				result = getTokenWithUser(username)
				if result != None:
					# check valid IP
					if(result['ip'] != ip):
						return 'Already logged in', 409
					token = result['_id']
				else:
					token = self.createToken(account, ip)
				return { 'token': token, 'expires': tokenExpireTime }, 200
			return 'Wrong username/password', 401
			
		except Exception as e:
			logging.info('error login: %s',e)
		return 'Invalid', 400

class SignUp(Resource):
	def post(self):
		try:
			json = request.json['user']

			if db.account.find_one({'_id': json['username']}) != None:
				return '', 409

			if 'birth' not in json:
				json['birth'] = ''
			if 'address' not in json:
				json['address'] = ''

			# create new account
			with client.start_session() as s:
				with s.start_transaction():
					i = db.account.insert_one(
						{
							'_id': json['username'], 
							'password': json['password'], 
							'email': json['email'], 
							'role': 'user', 
							'borrowed': [],
							'birth': json['birth'],
							'address': json['address'],
							'account_point': 0,
							'date_created': datetime.now(),
							# based on the requirement, account only work for 6 months
							'date_expire': calcDateExpire(maxDateAccount*24)[0],
							'active': False
						}, session = s
					)
			return 'done', 200

		except Exception as e:
			logging.info('error signup: %s',e)
		return 'Invalid', 400

class GetUserBorrowed(Resource):
	def get(self):
		try:
			token = getToken(request.headers['Authorization'])
			if token == None:
				return 'Unauthorized', 401
			# get account
			account = getAccountWithId(token['username'])
			# get history borrowed
			allBorrowed = convertDateForSeria(account['borrowed'])

			return { 'borrowed': allBorrowed }, 200

		except Exception as e:	
			logging.info('error getBorrowed: %s',e)
		return 'Invalid', 400

class AccountInfo(Resource):
	# get account info
	def get(self):
		try:
			token = getToken(request.headers['Authorization'])
			if token == None:
				return 'Unauthorized', 401

			account = getAccountWithId(token['username'])

			account.pop('password')
			account.pop('role')
			if 'account_point' in account:
				account.pop('account_point')

			account['borrowed'] = convertDateForSeria(account['borrowed'])

			return {'account': account}, 200

		except Exception as e:
			logging.info('error getAccountInfo: %s', e)
		return 'Invalid', 400
	
	def post(self):
		try:

			json = request.json['json']
			user = json['user']
			token = getToken(json['token'])
			if token == None:
				return 'Unauthorized', 401
			
			# if not match username in token and user in
			# or token is a admin
			if user['username'] != token['username'] and token['role'] != 'admin':
				raise Exception('Json and token username not match: %s', json)
			# set
			newInfo = {}
			if user['password'] != '':
				newInfo['password'] = user['password']
			if 'email' in user:
				newInfo['email'] = user['email']
			if 'address' in user:
				newInfo['address'] = user['address']	
			if 'birth' in user:
				newInfo['birth'] = user['birth']
				
			# if admin edit account
			if token['role'] == 'admin':
				newInfo['role'] = user['role']

			# update
			with client.start_session() as s:
				with s.start_transaction():
					u = db.account.update_one({'_id': user['username']}, {'$set': newInfo}, session=s)
			return 'done', 200
		except Exception as e:
			logging.info('error postAccountinfo: %s', e)
		return 'Inavlid', 400
