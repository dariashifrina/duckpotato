from flask import Flask, redirect, render_template, request, session
from utils import accountManager, postManager, newsManager
import os
import commands
import cgi
import cgitb; cgitb.enable()
from werkzeug import secure_filename

app = Flask(__name__)
app.secret_key = "hello"
@app.route("/")
def home():
    username = ""
    if "username" in session:
        username = session["username"]
    admin = False
    if "admin" in session:
        admin = session["admin"]
    return render_template("index.html", username = username, admin = admin)

@app.route("/editnews", methods=["GET","POST"]) #must put methods for forms
def editnews():
    admin = False
    if "admin" in session:
        admin = session["admin"]
        username = session["username"]
    r = request.form
    if "title" in r and "body" in r and "username" in session: #remember to add admin
        status = newsManager.createNewsPosts(r["title"], r["body"], session["username"])
        if status:
            return redirect("/news")
        return redirect("/editnews")
    return render_template("editnp.html", admin = admin, username=username)

@app.route("/news")
def news():
    username = ""
    if "username" in session:
        username = session["username"]
    admin = False
    if "admin" in session:
        admin = session["admin"]
    newsPosts = newsManager.getNewsPosts()
    return render_template("news.html", newsPosts = newsPosts, username = username, admin = admin)


@app.route("/calendar")
def calendar():
    username = ""
    if "username" in session:
        username = session["username"]
    admin = False
    if "admin" in session:
        admin = session["admin"]
    return render_template("calendar.html",username=username,admin=admin)


@app.route("/sprinters")
def sprinters():
    username = ""
    if "username" in session:
        username = session["username"]
    admin = False
    if "admin" in session:
        admin = session["admin"]
    allSprinters = accountManager.getSprinters()
    return render_template("sprinters.html", username = username, admin=admin, sprinters=allSprinters)

@app.route("/distance")
def distance():
    username = ""
    if "username" in session:
        username = session["username"]
    admin = False
    if "admin" in session:
        admin = session["admin"]
    allDistance = accountManager.getDistance()
    return render_template("distance.html", username = username, admin=admin, distance = allDistance)

@app.route("/fieldeventers")
def fieldeventers():
    username = ""
    if "username" in session:
        username = session["username"]
    admin = False
    if "admin" in session:
        admin = session["admin"]
    allField = accountManager.getFielders()
    return render_template("fieldeventers.html", username = username, admin=admin, fielders = allField)

@app.route("/racewalkers")
def racewalkers():
    username = ""
    if "username" in session:
        username = session["username"]
    admin = False
    if "admin" in session:
        admin = session["admin"]
    allRacewalkers = accountManager.getRacewalkers()
    return render_template("racewalkers.html", username = username, admin=admin, racewalkers = allRacewalkers)

@app.route("/athlete")
def athlete():
    username = ""
    if "username" in session:
        username = session["username"]
    admin = False
    if "admin" in session:
        admin = session["admin"]
    r = request.args
    if "name" not in r:
        return redirect("/athletes")
    name = r["name"]
    fname = name.split(" ")[0]
    lname = name.split(" ")[1]
    athlete = accountManager.getAthlete(fname,lname)
    if not athlete:
        return redirect("/athletes")
    return render_template("athlete.html", username = username, admin=admin, athlete=athlete)

@app.route("/login",methods=["GET","POST"])
def login():
    if "username" in session:
        session.pop("username")
    if "username" in request.form and "password" in request.form:
        status = accountManager.login(request.form["username"],request.form["password"])
        if status == 2:
            session["admin"] = True
            session["username"] = request.form["username"]
            return redirect("/")
        if status == 1:
            session["admin"] = False
            session["username"] = request.form["username"]
            return redirect("/")
        return redirect("/login")
    return render_template("login.html")

@app.route("/accountsettings", methods=["GET","POST"])
def accountsettings():
    username = ""
    if "username" in session:
        username = session["username"]
    admin = False
    if "admin" in session:
        admin = session["admin"]
    r = request.form
    password = None if "password" not in r else r["password"]
    email = None if "email" not in r else r["email"]
    if (password or email) and "username" in session:
        accountManager.editAccountSettings(session["username"], password, email)
        return redirect("/accountsettings")
    user = accountManager.getUser(session["username"])
    return render_template("accountsettings.html", user = user, username = username, admin = admin)


@app.route("/editannouncements", methods=["GET","POST"]) #must put methods for forms
def editannouncements():
    admin = False
    if "admin" in session:
        admin = session["admin"]
        username = session["username"]
    #return redirect("/")
    r = request.form
    if "title" in r and "body" in r and "username" in session: #remember to add admin
        status = postManager.createPost(r["title"], r["body"], session["username"])
        if status:
            return redirect("/announcements")
        return redirect("/editannouncements")
    return render_template("editta.html", username =username, admin = admin)

@app.route("/announcements")
def announcements():
    username = ""
    if "username" in session:
        username = session["username"]
    else:
        return redirect("/login")
    admin = False
    if "admin" in session:
        admin = session["admin"]
    posts = postManager.getPosts()
    return render_template("announcements.html", posts = posts, username = username, admin = admin)

@app.route("/editprofile")
def profile():
    username = ""
    if "username" in session:
        username = session["username"]
    admin = False
    if "admin" in session:
        admin = session["admin"]
    return render_template("editprofile.html",username=username,admin=admin)

@app.route("/editProfileDesc", methods=["GET","POST"])
def editProfileDesc():
    if "username" in session:
        username = session["username"]
    else:
        return redirect("/")
    r = request.form
    if "description" in r and "username" in session: #remember to add admin
        body = r["description"]
        accountManager.editProfileSettings(username, body)
    return redirect("/")

@app.route("/editProfilePic", methods=["GET","POST"])
def editProfilePic():
    admin = False
    if "admin" in session:
        admin = session["admin"]
        username = session["username"]
    #return redirect("/")
    f = request.files['profilepic']
    sfname = "static/img/" + accountManager.getName(username) + ".jpeg"
    f.save(sfname)
    return render_template("editprofile.html",username=username,admin=admin)
''''''

@app.route("/editathletes",methods=["GET","POST"])
def editathletes():
    admin = False
    if "admin" in session:
        admin = session["admin"]
        username = session["username"]
   # return redirect("/")
    r = request.form
    types = []
    if "racewalker" in r:
        if r["racewalker"]:
            types.append("racewalker")
    if "sprinter" in r:
        if r["sprinter"]:
            types.append("sprinter")
    if "fieldeventer" in r:
        if r["fieldeventer"]:
            types.append("fieldeventer")
    if "distance" in r:
        if r["distance"]:
            types.append("distance")
    if "admin" in r:
        admin = True
    if "username" in r and "password" in r and "email" in r and "first_name" in r and "last_name" in r:
        status = accountManager.register(r["username"],r["password"],r["email"],r["first_name"],r["last_name"],types, admin)
        if status:
            return redirect("/")
        return redirect("/editathletes")
    return render_template("editathletes.html", username=username, admin=admin)

@app.route("/editcalendar")
def editcalendar():
    admin = False
    if "admin" in session:
        admin = session["admin"]
        username = session["username"]
    return redirect("/")
    return "Hello World!"

#unfinished business :(
@app.route("/editresources")
def editresources():
    admin = False
    if "admin" in session:
        admin = session["admin"]
        username = session["username"]
    return redirect("/")
    return "Hello World!"

@app.route("/resources")
def resources():
    username = ""
    if "username" in session:
        username = session["username"]
    admin = False
    if "admin" in session:
        admin = session["admin"]
    return render_template("resources.html", username = username, admin = admin)

if __name__ == "__main__":
    app.debug = True
    app.run()
