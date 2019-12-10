from pymongo import MongoClient
# -----------------------------------------------------------------------------
# mongoDB connection string
mongodb = 'mongodb+srv://libary:3AvmVMAqu2Xs2v1n@cluster0-uuoo5.gcp.mongodb.net/test?retryWrites=true&w=majority'
client = MongoClient(mongodb)
db = client.library