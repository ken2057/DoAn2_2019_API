from pymongo import MongoClient
# -----------------------------------------------------------------------------
# mongoDB connection string
mongodb = ''
client = MongoClient(mongodb)
db = client.library