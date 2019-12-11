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

def calcDateExpire(timeAdd, time = datetime.now()):
	return time + timedelta(hours = timeAdd),

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
		return data.__str__().replace('-', '/')
	
def run_convertDateForSeria(json):
	for key in json:
		if key != '_id':
			json[key] = convertDateForSeria(json[key])
	return json


# ------------------------------------------------------------------------------
# Get data from db
# ------------------------------------------------------------------------------

## Get account with id
def getAccountWithId(accountId):
	return db.account.find_one({'_id':accountId})

def getBorrowedWithId(borrowedId):
	return db.borrowed.find_one({'_id': borrowedId})

## Get book with id
def getBookWithId(bookId):
	return db.book.find_one({'_id':bookId, 'deleted': False})

# ------------------------------------------------------------------------------
# formating
# ------------------------------------------------------------------------------
def formatLog(token, action, note):
	return {
		'time': formatDate(datetime.now() + timedelta(hours=7)), # convert to GMT+7
		'username': token['username'], 
		'role': token['role'], 
		'action': action,
		'note': note
	}

def formatHistoryStatus(status, date, by):
	return {'status': status, 'date': date, 'by': by}

def formatDate(time):
	return datetime(time.year, time.month, time.day, time.hour, time.minute, time.second)