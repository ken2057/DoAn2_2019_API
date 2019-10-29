# all the same import of api will be here
from src.package import *
# -----------------------------------------------------------------------------
from src.configs import tokenExpireTime, role
from src.utils import isJsonValid, isUserExist, calcTokenExprieTime, getToken
# -----------------------------------------------------------------------------

class GetPermission(Resource):
	def get(self):
		try:
			token = request.args['token']
			cache = db.token.find_one({'_id' : token })

			if cache != None:
				return role.index(cache['role']), 200
			return {'role': len(role)}, 200
		except Exception as e:
			logging.info('error GetPermission: %s', e)
		return 'Invalid', 400

class IsTokenExpire(Resource):
	def get(self):
		try:
			token = getToken(request.args['token'])
			return {'username': token['username'], 'expires': tokenExpireTime}, 200

		except Exception as e:
			logging.info('error checkToken: %s', e)
		return 'Invalid', 400