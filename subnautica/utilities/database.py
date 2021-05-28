# from flask_mongoengine import MongoEngine
import pymongo

# db = MongoEngine()

user = 'subnautical'
password = 'Eet2nTMBjlEB0Qev'
database = 'Subnautical'
collection = 'playerdata'

client = pymongo.MongoClient(
    f'mongodb+srv://{username}:{password}@cluster0.xg0kc.mongodb.net/{database}?retryWrites=true&w=majority')
# db = client.test

db = client.get_database()

col = db.get_collection(collection)