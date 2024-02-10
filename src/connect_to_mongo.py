from pymongo import MongoClient

client = MongoClient("classifai.tcu.edu", 27017)

# print mongo client
print(client.list_database_names())

# show all things within database 'local'
db = client.classifai
print(db.list_collection_names())

# show all events in 'startup_log'
collection = db.startup_log
for doc in collection.find():
    print(doc)
