from datetime import datetime, timedelta
from flask_restful import Resource
from flask import request
from uuid import uuid4
import logging
# -----------------------------------------------------------------------------
from src.configs import db, tokenExpireTime, role
from src.utils import isJsonValid, isUserExist, calcTokenExprieTime, getToken
# -----------------------------------------------------------------------------

class GetPermission(Resource):
	def get(self):
		try:
			token = request.args['token']
			cache = db.token.find_one({'_id' : token })

			if cache != None:
				return role.index(cache['role']), 200
			return len(role), 200
		except Exception as e:
			logging.info('error GetPermission: %s', e)

class IsTokenExpire(Resource):
	def get(self):
		try:
			token = getToken(request.args['token'])
			if token == None:
				return '', 203
				
			return {'username': token['username'], 'expires': tokenExpireTime}, 200

		except Exception as e:
			logging.info('error checkToken: %s', e)