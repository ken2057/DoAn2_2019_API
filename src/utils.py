from datetime import datetime, timedelta
from src.configs import db, tokenExpireTime, maxDateBorrow
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

def calcBorrowExpireTime(now):
	return now + timedelta(days = maxDateBorrow)

# convert python datetime.datetime to str for json serializable
# input will be dict
def convertDateForSeria(data):
	# incase of input a list of borrow
	if isinstance(data, list):
		allBorrowed = []
		for book in data:
			book.pop('username')
			allBorrowed.append(run_convertDateForSeria(book))
		return allBorrowed
	else:
		return run_convertDateForSeria(data)
	
def run_convertDateForSeria(json):
	for key in json:
		if isinstance(json[key], datetime):
			json[key] = json[key].__str__()
	return json


# ------------------------------------------------------------------------------
# Get data from db
# ------------------------------------------------------------------------------

## Get account with id
def getAccountWithId(accountId):
	return db.account.find_one({'_id':accountId})

## Get book with id
def getBookWithId(bookId):
	return db.bookTitle.find_one({'_id':bookId})

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