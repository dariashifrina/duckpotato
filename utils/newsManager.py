from pymongo import MongoClient

def createNewsPosts(body, title, username):
    newsPosts = MongoClient().track.newsPosts
    newsPosts.insert_one({
        "username": username,
        "title": title,
        "body": body
    })
    return True

def getNewsPosts():
    newsPosts = MongoClient().track.newsPosts
    return newsPosts.find({})

