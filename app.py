import os
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, url_for, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
import datetime
from werkzeug.utils import secure_filename

from helpers import login_required, apology

# Configure application
app = Flask(__name__)




# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['UPLOAD_FOLDER'] = './static/uploads/'
app.config['USERS_PHOTOS_FOLDER'] = './static/user_images/'

# ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///sattler.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Global functions
def get_user():
    returned_user = db.execute("SELECT username, id, photo, bio, email FROM users WHERE id = ?", session["user_id"] )

    return returned_user

# Get posts from database
def get_posts(of_user=''):
    if of_user != '':
        query = """
            SELECT users.name AS username, posts.user_id, post, likes, image, posted_at, photo
            FROM posts
            INNER JOIN users ON posts.user_id = users.id
            WHERE posts.user_id = ?
            ORDER BY posts.id DESC
        """
        result = db.execute(query, of_user)
    else:
        query = """
            SELECT users.name AS username, posts.user_id, post, likes, image, posted_at, photo
            FROM posts
            INNER JOIN users ON posts.user_id = users.id
            ORDER BY posts.id DESC
        """
        result = db.execute(query)

    return result

# HOME PAGE ROUTE
@app.route("/")
@login_required
def index():
    posts = get_posts()
    print(posts)
    user = get_user()
    return render_template("index.html", posts=posts, user=user[0])

@app.route("/post")
@login_required
def post():
    return render_template("post.html")

@app.route("/profile")
@login_required
def profile():

    if 'user_id' in session:
        user = get_user()
        print(user)
        return render_template("profile.html", user=user[0])

@app.route("/notifications")
@login_required
def notifications():

    if 'user_id' in session:
        user = get_user()
        posts = get_posts()
        print(user)

        return render_template("notifications.html", posts=posts, user=user[0])



ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/new_post", methods=["POST"])
def new_post():

    post_data = request.form.get('post_data')
    user_id = session["user_id"]
    current_date = datetime.datetime.now()
    post_date = current_date.strftime("%B %d, %Y")
    name = session.get("username")
    image = request.files['image']
    name_query_result = db.execute("SELECT username FROM users WHERE id=?", user_id)
    name = name_query_result[0]["username"]

    if len(name_query_result) != 1:
        return apology("User not found", 500)

    if image and allowed_file(image.filename):
        filename = secure_filename(image.filename)
        # SAVE PATH TO DIRECTORY
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # QUERY DATABASE
        db.execute("INSERT INTO posts (post, user_id, posted_at, image, name) VALUES (?, ?, ?, ?, ?)",
                   post_data, user_id, post_date, os.path.join(app.config['UPLOAD_FOLDER'], filename), name)
        flash('Post created successfully!', 'success')
        return redirect("/")
    else:
        flash('Failed to create post. Allowed image types are - png, jpg, jpeg, gif', 'danger')
        return redirect("/post")

# LOGIN ROUTE
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

# CORREcT

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "GET":
        return render_template("register.html")
    else:

        # getting data from the form
        name = request.form.get("name")
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        bio = request.form.get("bio")
        photo = request.form.get("photo")

        # CHEKING EXCEPTIONS / ERROR
        if not name:
            return apology("You did not give us a name")
        if not bio:
            return apology("You did not give us a bio")
        if not photo:
            return apology("You did not provide a profile image")
        if not username:
            return apology("You did not give us a username")
        if not password:
            return apology("You did not put a password")
        if not confirmation:
            return apology("You did not confirm your password")

        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        userHash = generate_password_hash(password)
        if len(rows) != 0:

            flash('Someone with those credetials has an account!')
            return apology("User already exists")

        else:
            db.execute("INSERT INTO users (username, hash, photo, email, bio, name) VALUES(?, ?, ?, ?, ?, ?)", username, userHash, photo, email, bio, name)

            flash('Account created successfully')

                # return redirect("/register")
            return redirect("/")
