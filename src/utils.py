from datetime import datetime, timedelta
from src.configs import db, tokenExpireTime, maxDateBorrow
import logging
# -----------------------------------------------------------------------------
## Check json from post method is enought field require for that func
def isJsonValid(valid, json):
	for i in valid:
		if i not in json:
			return False
	return True

def checkTokenExpire(token):
	# check token expire or not
	if token['expires'] > datetime.now():
		# not expire
		# add more expires time
		db.token.update_one(
			{'_id': token['_id']},
			{'$set': {'expires': calcTokenExprieTime()}}
		)
		return token
	# if expired delete that token
	db.token.delete_one({'_id': token['_id']})
	return None

## get token and check expired
def getToken(token):
	result = db.token.find_one({'_id': token})
	if result != None:
		return checkTokenExpire(result)

## get token with username
def getTokenWithUser(username):
	results = db.token.find({'username': username})
	for result in results:
		r = checkTokenExpire(result)
		if r != None:
			return r
	return None

## Check does username exist in db
def isUserExist(id):
	if db.account.find_one({'_id': id}) == None:
		return True
	return False

def calcTokenExprieTime():
	# expires time = now + second
	return datetime.now() + timedelta(seconds = tokenExpireTime)

def calcDateExpire(time):
	return datetime.now() + timedelta(hours = time),

def calcBorrowExpireTime(now):
	return now + timedelta(days = maxDateBorrow)

# convert python datetime.datetime to str for json serializable
# input can be list/dict/datetime
# it will run through every thing in list/dict to convert datetime into json
def convertDateForSeria(data):
	# inputis list
	if isinstance(data, list):
		allBorrowed = []
		for book in data:
			if 'username' in book:
				book.pop('username')
			allBorrowed.append(run_convertDateForSeria(book))
		return allBorrowed
	# input is dict
	elif isinstance(data, dict):
		return run_convertDateForSeria(data)
	# input is datetime
	else:
		return data.__str__()
	
def run_convertDateForSeria(json):
	for key in json:
		json[key] = convertDateForSeria(json[key])
	return json


# ------------------------------------------------------------------------------
# Get data from db
# ------------------------------------------------------------------------------

## Get account with id
def getAccountWithId(accountId):
	return db.account.find_one({'_id':accountId})

## Get book with id
def getBookWithId(bookId):
	return db.bookTitle.find_one({'_id':bookId, 'deleted': False})

# ------------------------------------------------------------------------------
# Logging
# ------------------------------------------------------------------------------
def formatLog(token, action, note):
	return {
		'time': datetime.now(),
		'username': token['username'], 
		'role': token['role'], 
		'action': action,
		'note': note
	}