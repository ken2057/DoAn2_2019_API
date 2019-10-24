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
			token = getToken(request.args['token'])
			account = getAccountWithId(token['username'])

			allBorrowed = []

			for book in account['borrowed']:
				book.pop('username')
				allBorrowed.append(convertDateForSeria(book))

			return { 'borrowed': allBorrowed }, 200

		except Exception as e:	
			logging.info('error getBorrowed: %s',e)
		return 'Invalid', 400