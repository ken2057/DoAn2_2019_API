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
limitBorrow = 20

# max book can borrow
maximumBookCanBorrow = 5

# fee per day not return
feePerDay = 1000

# role in db
#       0        1          2
role = ['admin', 'manager', 'user']
roleHigherThanUser = ['admin', 'manager']

# status of borrow
statusBorrow = {
    'return' : 'Returned',
    'start': 'On borrowing',
    'order': 'Watting for avaialbe',
    'lost': 'Lost',
    'wait_to_get': 'Get book from librarian',
    'paied': 'Paied',
    'cancel': 'Canceled order'
}

# status when borrow book
statusBorrow_block = [
    'On borrowing',
    'Watting for avaialbe',
    'Get book from librarian'
]