from pymongo import MongoClient
# -----------------------------------------------------------------------------
# mongoDB connection string
mongodb = 'mongodb+srv://libary:3AvmVMAqu2Xs2v1n@cluster0-uuoo5.gcp.mongodb.net/test?retryWrites=true&w=majority'
client = MongoClient(mongodb)
db = client.library

# token expire time
tokenExpireTime = 1000000000 #seconds

# book dates much return
maxDateBorrow = 7

# limit books per find
limitBooks = 20

# limit history per find
limitBorrow = 20

# role in db
#       0        1          2
role = ['admin', 'manager', 'user']
roleHigherThanUser = ['admin', 'manager']

# status of borrow
statusBorrow = {
    'return' : 'Returned',
    'start': 'On borrowing',
    'order': 'Watting for avaialbe',
    'lost': 'Lost'
}
