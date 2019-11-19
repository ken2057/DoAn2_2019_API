# all the same import of api will be here
from src.package import *
from uuid import uuid4
# -----------------------------------------------------------------------------
from src.configs import tokenExpireTime, role, maxDateAccount, minAge, maxAge
from src.utils import calcTokenExprieTime, getAccountWithId, getToken, convertDateForSeria, getTokenWithUser
from src.utils import formatDate, calcDateExpire, formatLog
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
			if account != None:
				# if user have been blocked by admin or manager
				# can't login
				if 'blocked' in account and account['blocked']:
					return 'Your account have been blocked', 403

				# get old token if exist
				result = getTokenWithUser(username)
				if result != None:
					# check valid IP
					# if(result['ip'] != ip):
					#	return 'Already logged in', 409
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
				return 'Username already exist', 409

			if 'address' not in json:
				json['address'] = ''

			# split to convert format from js to format can use
			birth = json['birth'].split('T')[0].split('-')
			# convert all to int
			birth = [int(x) for x in birth]
			# convert to GMT+7
			json['birth'] = formatDate(datetime(birth[0], birth[1], birth[2]) + timedelta(days=1))

			# check does user age is ok
			temp = datetime.now().year - json['birth'].year
			if temp not in range(minAge, maxAge + 1):
				return 'Age much from ' + str(minAge) + ' to ' + str(maxAge), 400

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
							'date_created': formatDate(datetime.now()),
							# based on the requirement, account only work for 6 months
							'date_expire': formatDate(calcDateExpire(maxDateAccount*24)[0]),
							'active': False,
							'blocked': False
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

			account = convertDateForSeria(account)
			# remove time from datetime
			if 'birth' in account:
				account['birth'] = convertDateForSeria(account['birth']).split(' ')[0]
			if 'date_expire' in account:
				account['date_expire'] = convertDateForSeria(account['date_expire']).split(' ')[0]
			if 'date_created' in account:
				account['date_created'] = convertDateForSeria(account['date_created']).split(' ')[0]

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
				return 'Json and token username not match', 407

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
			# account to check admin and write log
			account = None
			# if admin edit account
			if token['role'] == 'admin':
				account = getAccountWithId(user['username'])
				newInfo['role'] = user['role']

			# update
			with client.start_session() as s:
				with s.start_transaction():
					u = db.account.update_one({'_id': user['username']}, {'$set': newInfo}, session=s)
					if account != None:
						note = {
							'username': user['username'],
							'old_role': account['role'],
							'new_role': user['role']
						}
						i = db.log.insert_one(formatLog(token, 'change role', note), session)
			return 'done', 200
		except Exception as e:
			logging.info('error postAccountinfo: %s', e)
		return 'Inavlid', 400
