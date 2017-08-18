from pymongo import MongoClient

def createPost(body, title, username):
    posts = MongoClient().track.posts
    posts.insert_one({
        "username": username,
        "title": title,
        "body": body
    })
    return True

def getPosts():
    posts = MongoClient().track.posts
    return posts.find({})

