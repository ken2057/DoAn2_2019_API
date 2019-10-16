from datetime import datetime, timedelta
from flask_restful import Resource
from flask import request
from uuid import uuid4
import logging

from src.configs import *
from src.utils import checkJsonValid

## Login and return token
class Login(Resource):
	def findUser(self, username, password):
		return db.account.find_one({'_id': username, 'password': password})

	def createToken(self, account):
		token = str(uuid4()).replace('-','')
		db.token.insert_one(
			{
				'_id': token, 
				'expires': datetime.now() + timedelta(seconds = tokenExpireTime),
				'username': account['_id'],
				'role': account['role']
			}
		)
		return token

	def post(self):
		try:
			json = request.get_json()
			valid = ['username', 'password']
			if (checkJsonValid(valid, json)):
				account = self.findUser(json['username'], json['password'])
				if(account != None):
					token = self.createToken(account)
					return { 'token': token, 'expires': tokenExpireTime }, 200
				return 401, 401
			return 400, 400
		except Exception as e:
			logging.info('error login: %s',e)
		return 404, 404


class SignUp(Resource):
    def post(self):
        return 200, 200