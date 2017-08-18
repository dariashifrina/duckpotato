from flask import Flask, redirect, render_template, request, session
from utils import accountManager, postManager, newsManager

app = Flask(__name__)
app.secret_key = "hello"
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/editnews", methods=["GET","POST"]) #must put methods for forms
def editnews():
    r = request.form
    if "title" in r and "body" in r and "username" in session: #remember to add admin
        status = newsManager.createNewsPosts(r["title"], r["body"], session["username"])
        if status:
            return redirect("/news")
        return redirect("/editnews")
    return render_template("editnp.html")

@app.route("/news")
def news():
    newsPosts = newsManager.getNewsPosts()
    return render_template("news.html", newsPosts = newsPosts)


@app.route("/calendar")
def calendar():
    return "Hello World!"

@app.route("/athletes")
def athletes():
    return "Hello World!"

@app.route("/sprinters")
def sprinters():
    return "Hello World!"

@app.route("/distance")
def distance():
    return "Hello World!"

@app.route("/login",methods=["GET","POST"])
def login():
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
    r = request.form
    password = None if "password" not in r else r["password"]
    email = None if "email" not in r else r["email"]
    if (password or email) and "username" in session:
        accountManager.editAccountSettings(session["username"], password, email)
        return redirect("/accountsettings")
    user = accountManager.getUser(session["username"])
    return render_template("accountsettings.html", user = user)


@app.route("/editannouncements", methods=["GET","POST"]) #must put methods for forms
def editannouncements():
    r = request.form
    if "title" in r and "body" in r and "username" in session: #remember to add admin
        status = postManager.createPost(r["title"], r["body"], session["username"])
        if status:
            return redirect("/announcements")
        return redirect("/editannouncements")
    return render_template("editta.html")

@app.route("/announcements")
def announcements():
    posts = postManager.getPosts()
    return render_template("announcements.html", posts = posts)

@app.route("/editprofile")
def profile():
    return "Hello World!"

@app.route("/editathletes",methods=["GET","POST"])
def editathletes():
    r = request.form
    if "username" in r and "password" in r and "email" in r and "first_name" in r and "last_name" in r and "types" in r and "admin" in r:
        status = accountManager.register(r["username"],r["password"],r["email"],r["first_name"],r["last_name"],r["types"],r["admin"])
        if status:
            return redirect("/")
        return redirect("/editathletes")
    return render_template("editathletes.html")
@app.route("/editcalendar")
def editcalendar():
    return "Hello World!"

#unfinished business :(
@app.route("/editresources")
def editresources():
    return "Hello World!"

@app.route("/resources")
def resources():
    return "Hello World!"

if __name__ == "__main__":
    app.run()