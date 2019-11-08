# all the same import of api will be here
from src.package import *
# -----------------------------------------------------------------------------
from src.configs import tokenExpireTime, role
from src.utils import isJsonValid, isUserExist, calcTokenExprieTime, getToken
# -----------------------------------------------------------------------------

class GetPermission(Resource):
	def get(self):
		try:
			token = getToken(request.headers['Authorization'])
			ip = request.headers.get('X-Forwarded-For')
			# check token exist and token ip == request ip
			if token != None and token['ip'] == ip:
				return {'role': role.index(token['role'])}, 200
			return {'role': len(role)}, 200
		except Exception as e:
			logging.info('error GetPermission: %s', e)
		return 'Invalid', 400

class IsTokenExpire(Resource):
	def get(self):
		try:
			token = getToken(request.headers['Authorization'])
			if token == None:
				return 'Unauthorized', 401

			return {'username': token['username'], 'expires': tokenExpireTime}, 200

		except Exception as e:
			logging.info('error checkToken: %s', e)
		return 'Invalid', 400

class Logout(Resource):
	def post(self):
		try:
			json = request.get_json()['json']
			token = getToken(json['token'])
			if token == None:
				return 'Unauthorized', 401

			# remove token
			with client.start_session() as session:
				with session.start_transaction():
					db.token.delete_one({'_id': token['_id']})

			return 'done', 200

		except Exception as e:
			logging.info('error logOut: %s', e)
		return 'Invalid', 400