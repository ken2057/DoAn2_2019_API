from pymongo import MongoClient
# -----------------------------------------------------------------------------
# mongoDB connection string
mongodb = 'mongodb+srv://libary:3AvmVMAqu2Xs2v1n@cluster0-uuoo5.gcp.mongodb.net/test?retryWrites=true&w=majority'
client = MongoClient(mongodb)
db = client.library

# token expire time
tokenExpireTime = 300 #seconds

# book dates much return
maxDateBorrow = 4

# limit books per find
limitBooks = 20

# limit history per find
limitFindBorrowed = 20

# max book can borrow
maximumBookCanBorrow = 5

# fee per day not return
feePerDay = 1000

# max date of account
maxDateAccount = 6*30 # day

# max time hold book 'Get book from librarian'
maxTimeHoldOrder = 12 #hours

# role in db
#       0        1          2
role = ['admin', 'manager', 'user']
roleHigherThanUser = ['admin', 'manager']

# status of borrow
statusBorrow = {
    'return' : 'Returned',
    'sent': 'On borrowing',
    'order': 'Watting for avaialbe',
    'lost': 'Lost',
    'wait_to_get': 'Get book from librarian',
    'paied': 'Paied',
    'cancel': 'Canceled order',
    'hold_timeout': 'Hold order too long'
}

# status when borrow book
statusBorrow_block = [
    'On borrowing',
    'Watting for avaialbe',
    'Get book from librarian'
]

# user point when return/cancel/lost book
userPoint = {
    'return': 1,
    'cancel': -2,
    'hold_timeout': -3,
    'lost': -3
}