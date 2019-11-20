import re
# all the same import of api will be here
from src.package import *
# -----------------------------------------------------------------------------
from src.configs import role
from src.utils import isJsonValid, getToken, getAccountWithId, convertDateForSeria, formatDate
from src.utils import formatLog
# -----------------------------------------------------------------------------

# get all user into
class GetUsersInfo(Resource):
	def get(self):
		try:
			token = getToken(request.headers['Authorization'])
			username = request.args['username']
			search = {}
			if username == "":
				search['_id'] = re.compile(username, re.IGNORECASE)

			# token expired or not admin
			if token == None or token['role'] != role[0]:
				return 'Unauthorized', 401
			# get all user info
			users = []
			for user in db.account.find(search).sort([('role', 1), ('_id', 1)]):
				if 'email' not in user:
					user['email'] = ''
				if 'address' not in user:
					user['address'] = ''
				# convert datetime into json
				user['borrowed'] = convertDateForSeria(user['borrowed'])
				#
				if 'birth' in user:
					user['birth'] = convertDateForSeria(user['birth']).split(' ')[0]
				else:
					user['birth'] = ''
				#
				if 'date_created' in user:
					user['date_created'] = convertDateForSeria(user['date_created']).split(' ')[0]
				else:
					user['date_created'] = ''
				#
				if 'date_expire' in user:
					user['date_expire'] = convertDateForSeria(user['date_expire']).split(' ')[0]
				else:
					user['date_expire'] = ''
				# remove some unnecessary infomartion
				user.pop('password')
				#
				users.append(user)

			# get total of documents in collection
			total = db.account.find(search).count()

			return {'users': users, 'total': total}, 200
				
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
				return "Can't change admin role", 400
			
			# update role
			with client.start_session() as s:
				with s.start_transaction():
					u = db.account.update_one({'_id': json['accountId']}, { '$set': {'role': json['role']}}, session=s)
					note = {
						'username': account['_id'],
						'old_role': account['role'],
						'new_role': json['role']
					}
					db.logging.insert_one(formatLog(token, 'change role', note))

		except Exception as e:
			logging.info('error setAccountRole: %s', e)
		return 'Invalid', 400