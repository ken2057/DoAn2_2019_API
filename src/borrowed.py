# all the same import of api will be here
from src.package import *
# -----------------------------------------------------------------------------
from src.configs import role, limitFindBorrowed, roleHigherThanUser, limitBooks
from src.configs import feePerDay, statusBorrow, statusBorrow_block
from src.utils import formatDate, formatHistoryStatus, formatLog
from src.utils import getToken, getAccountWithId, getBookWithId
from src.utils import convertDateForSeria
# -----------------------------------------------------------------------------

class Borrowed(Resource):
	# get borrowed with id
	def get(self):
		try:
			token = getToken(request.headers['Authorization'])
			# id have bene replace - to / so when receive  borrowedId need change it back
			borrowedId = request.args['borrowedId']
			username = borrowedId.split('-')[0]

			# token expired
			# check if user is admin or is that exact user who borrowed the book
			if token == None or token['role'] not in roleHigherThanUser:
				return 'Unauthorized', 401

			result = db.borrowed.find_one({'_id': borrowedId})
			result = convertDateForSeria(result)

			return {'borrowed': result}, 200
		except Exception as e:
			logging.info('error getBorrowed %s', e)
		return '', 400

	# update info of borrowed
	def post(self):
		try:
			json = request.json
			token = getToken(json['token'])
			borrowed = json['borrowed']

			# check is admin or manager
			if token['role'] not in roleHigherThanUser:
				return 'Unauthorized', 401
			
			with client.start_session() as s:
				with session.start_transaction():
					pass
		except Exception as e:
			logging.info('error postBorrowed: %s', e)
		return 'Invalid', 400

class GetSearchBorrowed(Resource):
	def get(self):
		try:
			# check auth and role of user
			token = getToken(request.headers['Authorization'])
			if token == None or token['role'] not in roleHigherThanUser:
				return 'Unauthorized', 401
			
			# if search borrowed with username => search only with that borrowed by user
			search = {}
			try:
				username = request.args['username']
				if username != '':
					search['username'] = re.compile(username, re.IGNORECASE)
			except:
				pass

			# check if page is in input
			try:
				page = int(request.args['page'])
			except:
				page = 0

			borrowed = []
			if search != {}:
				# when search with param
				result = db.borrowed.find(search).skip(limitFindBorrowed * page).limit(limitFindBorrowed).sort("_id")
			else:
				# when search is empty
				result = db.borrowed.find().skip(limitFindBorrowed * page).limit(limitFindBorrowed).sort("_id")

			for i in result:
				if 'deleted' in i and i['deleted']:
					continue
				# convert datetime in history_status
				newHS = []
				for hs in i['history_status']:
					temp = formatHistoryStatus(hs['status'], convertDateForSeria(hs['date']), hs['by'])
					newHS.append(temp)

				i['history_status'] = newHS
				i['_id'] = i['_id'].__str__()
				
				borrowed.append(convertDateForSeria(i))

			return {'borrowed': borrowed}, 200
		except Exception as e:
			logging.info('error searchBorrowed: %s', e)
		return 'Invalid', 400


class UpdateBorrowed(Resource):
	def post(self):
		try:
			# json will have bookId, status (return/lost)
			json = request.get_json()['json']
			token = getToken(json['token'])
			if token == None or token['role'] not in roleHigherThanUser:
				return 'Unauthorized', 401
			
			# get account, book from db, borrowed info
			history_in_borrowed = db.borrowed.find_one({'_id': json['borrowedId']})
			book = getBookWithId(int(history_in_borrowed['bookId']))
			account = getAccountWithId(history_in_borrowed['username'])

			borrowInfo = None
			for h in account['borrowed']:
				if h['_id'] == json['borrowedId']:
					borrowInfo = h
					break
			else:
				return 'Not exists', 400

			index = book['books'].index(borrowInfo['_id'])
			#
			# remove previous borrowed info
			#
			account['borrowed'].remove(borrowInfo)

			fee = 0
			now = formatDate(datetime.now())
			# if user return book or cancel order
			# cancel can be call user/admin
			if json['status'] == 'cancel':
				book['books'][index] = ''
			# if admin checked user return the book
			elif json['status'] == 'return':
				borrowInfo['date_return'] = now
				book['books'][index] = ''
				# if return late => add fee
				if(now > history_in_borrowed['date_expire']):
					fee = feePerDay * (now - history_in_borrowed['date_expire']).days
			# if admin checked user losted the book
			elif json['status'] == 'lost':
				# if user lost the book
				book['books'][index] = 'Lost by ' + token['username'] + ' - Date: ' + now.__str__()
				# if lost => fee = money of book
				fee = book['price']

			#
			# update borrowed info
			#
			borrowInfo['status'] = statusBorrow[json['status']]
			h = formatHistoryStatus(borrowInfo['status'], now, token['username'])

			account['borrowed'].append(borrowInfo)
			history_in_borrowed['history_status'].append(h)
			# update declare
			update_account = {'borrowed': account['borrowed']}
			if 'account_point' in account and json['status'] != 'cancel':
				update_account['account_point'] = account['account_point'] + userPoint[json['status']]

			update_borrowed = {
				'history_status': history_in_borrowed['history_status'], 
				'status': borrowInfo['status'], 
				'date_return': borrowInfo['date_return']
			}
			# if have fee added it to account and borrowed
			if (fee != 0):
				insert = {'fee': fee, 'paid': 0 }
				update_account.update(insert)
				update_borrowed.update(insert)

			#
			# update db
			#
			with client.start_session() as s:
				with s.start_transaction():
					# update in Account
					u = db.account.update_one(
						{'_id': token['username']},
						{'$set': update_account },
						session=s
					)
					# update in Borrowed
					u = db.borrowed.update_one(
						{'_id': borrowInfo['_id']},
						{'$set': update_borrowed},
						session=s
					)
					# update in bookTitle
					u = db.bookTitle.update_one(
						{'_id': int(history_in_borrowed['bookId'])},
						{'$set': {'books': book['books']}},
						session=s
					)

			return 'done', 200

		except Exception as e:
			logging.info('error updateBorrowed: %s', e)
		return 'Invalid', 400
