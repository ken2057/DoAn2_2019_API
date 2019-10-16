from datetime import datetime
from src.configs import db

## Check json from post method is enought field require for that func
def checkJsonValid(valid, json):
	for i in valid:
		if i not in json:
			return False
	return True

## Check token expired or not
def checkToken(token):
	r = db.token.find_one({'_id': token})
	if r != None:
		if r['expires'] > datetime.now():
			return True
		db.token.delete_one({'_id': token})
	return False