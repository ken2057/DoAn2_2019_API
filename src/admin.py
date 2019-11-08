# all the same import of api will be here
from src.package import *
# -----------------------------------------------------------------------------
from src.configs import role
from src.utils import isJsonValid, getToken, getAccountWithId, convertDateForSeria
# -----------------------------------------------------------------------------

class GetUsersInfo(Resource):
	def get(self):
		try:
			token = getToken(request.headers['Authorization'])
			# token expired or not admin
			if token == None or token['role'] != role[0]:
				return 'Unauthorized', 401
			# get all user info
			users = []
			for user in db.account.find():
				if 'email' not in user:
					user['email'] = ''
				# convert datetime into json
				user['borrowed'] = convertDateForSeria(user['borrowed'])
				user.pop('password')
				users.append(user)
			return {'users': users}, 200
				
		except Exception as e:
			logging.info('error GetAllUserInfo: %s',e)
		return 'Invalid', 400

class SetAccountRole(Resource):
	def post(self):
		try:
			json = request.get_json()['json']
			# valid = ['token', 'accountId', 'role']

			# get token check is admin
			token = getToken(json['token'])
			# token is not admin or if new role not exist => false
			if token == None or not token['role'] == 'admin' or json['role'] not in role or json['role'] == 'admin':
				return 'Unauthorized', 401
			
			# check account exists => return false
			account = getAccountWithId(json['accountId'])
			# account is admin ? => return false
			if account['role'] == 'admin':
				raise Exception("Account is admin, can't change")
			
			# update role
			with client.start_session() as session:
				with session.start_transaction():
					db.account.update_one({'_id': json['accountId']}, { '$set': {'role': json['role']}})

		except Exception as e:
			logging.info('error setAccountRole: %s', e)
		return 'Invalid', 400