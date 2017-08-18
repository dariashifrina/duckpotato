from pymongo import MongoClient
from hashlib import sha1

def register(username, password, email, first_name, last_name, types, admin):
    users = MongoClient().track.users
    results = users.find_one({"username":username})
    if results:
        return False
    results = users.insert_one({
        "username":username,
        "password":sha1(password).hexdigest(),
        "email":email,
        "first_name":first_name,
        "last_name":last_name,
        "types":types,
        "admin":admin
    })
    return True

def login(username, password):
    users = MongoClient().track.users
    results = users.find_one({"username":username})
    if sha1(password).hexdigest() == results["password"]:
        if results["admin"]:
            return 2
        return 1
    return 0

def editAccountSettings(username, password, email):
    users = MongoClient().track.users
    if password:
        users.find_one_and_update({"username":username}, {"$set":{"password":sha1(password).hexdigest()}})
    if email:
        users.find_one_and_update({"username":username}, {"$set":{"email":email}})
        
def getUser(username):
    users = MongoClient().track.users
    return users.find_one({"username":username})
