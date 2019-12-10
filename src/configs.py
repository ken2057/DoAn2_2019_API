from src.mongo import db

# minimum accout point
minAccountPoint = -10

# token expire time
tokenExpireTime = 300 #seconds

# limit books per find
limitBooks = 20

# limit history per find
limitFindBorrowed = 20

# fee per day not return
feePerDay = 1000

# max date of account
maxDateAccount = 6*30 # day

# max time hold book 'Get book from librarian'
maxTimeHoldOrder = 12 #hours

# book dates much return
# maxDateBorrow = 4
maxDateBorrow = db.config.find_one({'_id': 'max_date_borrowed'})['value']

# max book can borrow
# maximumBookCanBorrow = 5
maximumBookCanBorrow = db.config.find_one({'_id': 'max_book_borrow'})['value']

# min age
# minAge = 18
minAge = db.config.find_one({'_id': 'min_age'})['value']

# max age
# maxAge = 50
maxAge = db.config.find_one({'_id': 'max_age'})['value']

# role in db
#       0        1          2
role = ['admin', 'manager', 'user']
roleHigherThanUser = ['admin', 'manager']

# status of borrow
statusBorrow = db.status_borrow.find_one({'_id': 'status'})
# statusBorrow = {
#     'return' : 'Returned',
#     'sent': 'On borrowing',
#     'order': 'Watting for avaialbe',
#     'lost': 'Lost',
#     'wait_to_get': 'Get book from librarian',
#     'paid': 'Paid',
#     'cancel': 'Canceled',
#     'hold_timeout': 'Hold order too long',
#     'finish_paid': 'Finish Paid'
# }

# status when borrow book
statusBorrow_block = [
    'Paid',
    'On borrowing',
    'Watting for avaialbe',
    'Get book from librarian'
]

# user point when return/cancel/lost book
userPoint = {
    'return': 1,
    'finish_paid': 1,
    'cancel': -2,
    'hold_timeout': -3,
    'lost': -3
}