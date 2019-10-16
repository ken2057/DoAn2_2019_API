from pymongo import MongoClient

#mongoDB connection string
mongodb = 'mongodb+srv://libary:ecyfAnTIz058VdrP@cluster0-uuoo5.gcp.mongodb.net/test?retryWrites=true&w=majority'
client = MongoClient(mongodb)
db = client.library

#token
tokenExpireTime = 300 #seconds