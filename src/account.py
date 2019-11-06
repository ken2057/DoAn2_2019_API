# all the same import of api will be here
from src.package import *
from uuid import uuid4
# -----------------------------------------------------------------------------
from src.configs import tokenExpireTime, role
from src.utils import calcTokenExprieTime, getAccountWithId, getToken, convertDateForSeria
# -----------------------------------------------------------------------------

## Login and return token
class Login(Resource):
	def findUser(self, username, password):
		return db.account.find_one({'_id': username, 'password': password})

	def createToken(self, account):
		token = str(uuid4()).replace('-','')
		db.token.insert_one(
			{
				'_id': token, 
				'expires': calcTokenExprieTime(),
				'username': account['_id'],
				'role': account['role']
			}
		)
		return token

	def get(self):
		try:
			username = request.args['username']
			password = request.args['password']

			account = self.findUser(username, password)
			if(account != None):
				token = self.createToken(account)
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

			# create new account
			db.account.insert_one(
				{
					'_id': json['username'], 
					'password': json['password'], 
					'email': json['email'], 
					'role': 'user', 
					'borrowed': [] 
				}
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

			account = getAccountWithId(token['username'])

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
			if user['username'] != token['username']:
				raise Exception('Json and token username not match: %s', json)
			# set
			if user['password'] == '':
				newInfo = {'email': user['email']}
			else:
				newInfo = {'email': user['email'], 'password': user['password']}
			# update
			db.account.update_one({'_id': json['username']}, {'$set': newInfo})
			
		except Exception as e:
			logging.info('error postAccountinfo: %s', e)
		return 'Inavlid', 400
