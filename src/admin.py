from datetime import datetime, timedelta
from flask_restful import Resource
from flask import request
from uuid import uuid4
import logging
# -----------------------------------------------------------------------------
from src.configs import db, role
from src.utils import isJsonValid, getToken, getAccountWithId
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

class SetAccountRole(Resource):
	def post(self):
		try:
			json = request.get_json()
			# valid = ['token', 'accountId', 'role']

			# get token check is admin
			token = getToken(json['token'])
			# token is not admin or if new role not exist => false
			if not token['role'] == 'admin' or json['role'] not in role or json['role'] == 'admin':
				raise Exception('Invalid json/token: %s', json)
			
			# check account exists => return false
			account = getAccountWithId(json['accountId'])
			# account is admin ? => return false
			if account['role'] == 'admin':
				raise Exception("Account is admin, can't change")
			
			# update role
			db.account.update_one({'_id': json['accountId']}, { '$set': {'role': json['role']}})

		except Exception as e:
			logging.info('error setAccountRole: %s', e)
		return '', 400