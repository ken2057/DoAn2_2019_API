from datetime import datetime, timedelta
from flask_restful import Resource
from flask import request
from uuid import uuid4
import logging
# -----------------------------------------------------------------------------
from src.configs import db, role
from src.utils import isJsonValid, getToken
# -----------------------------------------------------------------------------

class GetUsersInfo(Resource):
	def get(self):
		try:
			token = getToken(request.args['token'])
			# token expired or not admin
			if token == None or token['role'] != role[0]:
				return '', 403
			# get all user info
			users = []
			for user in db.account.find():
				if 'email' not in user:
					user['email'] = ''
				users.append(
					{
						'username': user['_id'],
						'email': user['email'],
						'role': user['role'],
						'borrowed': user['borrowed']
					}
				)
			return {'users': users}, 200
				
		except Exception as e:
			logging.info('error GetAllUserInfo: %s',e)
		return '', 400