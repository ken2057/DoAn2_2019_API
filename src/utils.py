from datetime import datetime, timedelta
from src.configs import db, tokenExpireTime
# -----------------------------------------------------------------------------
## Check json from post method is enought field require for that func
def isJsonValid(valid, json):
	for i in valid:
		if i not in json:
			return False
	return True

## get token and check expired
def getToken(token):
	r = db.token.find_one({'_id': token})
	if r != None:
		if r['expires'] > datetime.now():
			# change expires time
			db.token.update_one(
				{'_id': token},
				{'$set': {'expires': calcTokenExprieTime()}}
			)
			return r
		db.token.delete_one({'_id': token})
	return None

## Check does username exist in db
def isUserExist(id):
	if db.account.find_one({'_id': id}) == None:
		return True
	return False

def calcTokenExprieTime():
	# expires time = now + second
	return datetime.now() + timedelta(seconds = tokenExpireTime)
