from datetime import datetime, timedelta
from flask_restful import Resource
from flask import request
from uuid import uuid4
import logging
# -----------------------------------------------------------------------------
from src.configs import db, tokenExpireTime, role
from src.utils import isJsonValid, isUserExist, calcTokenExprieTime
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
			return 401, 401
			
		except Exception as e:
			logging.info('error login: %s',e)
		return '', 400

class SignUp(Resource):
	def post(self):
		try:
			# username = request.args['username']
			# password = request.args['password']
			# email = request.args['email']
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
		return '', 400

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
