from pymongo import MongoClient
from hashlib import sha1
import shutil

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
        "admin":admin,
        "body":"hi"
    })
    shutil.copy("duck.jpeg","static/img/"+ first_name + last_name +".jpeg")

    return True

def login(username, password):
    users = MongoClient().track.users
    results = users.find_one({"username":username})
    #if password == results["password"]:
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
#def editProfilePic(username, password)

def editProfileSettings(username, body):
    users = MongoClient().track.users
    if body:
        users.find_one_and_update({"username":username}, {"$set":{"body":body}})
    #if profilepic:
        #users.find_one_and_update({"username":username}, {"$set":{"email":email}})
        
def getUser(username):
    users = MongoClient().track.users
    return users.find_one({"username":username})

def getFielders():
    users = MongoClient().track.users
    allRunners = users.find({})
    ret = []
    for runner in allRunners:
        if 'fieldeventer' in runner['types']:
            ret.append(runner)
    return ret

def getSprinters():
    users = MongoClient().track.users
    allRunners = users.find({})
    ret = []
    for runner in allRunners:
        if 'sprinter' in runner['types']:
            ret.append(runner)
    return ret
def getDistance():
    users = MongoClient().track.users
    allRunners = users.find({})
    ret = []
    for runner in allRunners:
        if 'distance' in runner['types']:
            ret.append(runner)
    return ret
def getRacewalkers():
    users = MongoClient().track.users
    allRunners = users.find({})
    ret = []
    for runner in allRunners:
        if 'racewalker' in runner['types']:
            ret.append(runner)
    return ret

def getAthlete(fname, lname):
    users = MongoClient().track.users
    allRunners = users.find({})
    for runner in allRunners:
        if fname in runner['first_name'] and lname in runner['last_name']:
            return runner

def getName(usernamez):
    nameyay = ""
    users = MongoClient().track.users
    allRunners = users.find({})
    for runner in allRunners:
        if runner['username'] == usernamez:
            nameyay += runner['first_name']
            nameyay += runner['last_name']
            return nameyay
