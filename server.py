from flask import Flask, render_template, redirect, request, session, flash
from mysqlconnection import connectToMySQL
# import re

app = Flask(__name__)
app.secret_key = 'secretkey'
# EMAIL_REGEX = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")

@app.route("/users")  #show users from database in table
def index():
    mysql = connectToMySQL('users')
    friends = mysql.query_db('SELECT * FROM friends WHERE id=id;')
    # print(friends)
    return render_template("index.html", all_friends = friends)

@app.route("/users/new")   #show template to add new user
def new_user():
    # print(request.form)
    return render_template("add_user.html")

@app.route("/users/create", methods = ["POST"])   #create new user and add to database
def add_user():
    # print(request.form)
    mysql = connectToMySQL('users')
    query = "INSERT INTO friends (first_name, last_name, email, created_at, updated_at) VALUES (%(fn)s, %(ln)s, %(email)s,NOW(), NOW());"
    #fields from database to be inserted in form
    data = {    
    
        "fn": request.form["fname"],
        "ln": request.form["lname"],
        "email": request.form["email"]
    }
    user = mysql.query_db(query, data)
    return redirect("/users")

@app.route("/users/<int:id>")
def display_user(id):
    mysql = connectToMySQL('users')
    query = "SELECT * FROM friends WHERE id=%(id)s;"
    data = {
        "id": id
    }
    user = mysql.query_db(query,data)
    #takes list of user info from dictionary and displays it in html
    return render_template("display_user.html", user=user[0])

@app.route("/users/<int:id>/edit")
def edit(id):
    mysql = connectToMySQL('users')
    query = "SELECT * FROM friends WHERE id=%(id)s;"
    data = {
        "id": id
    }
    user = mysql.query_db(query,data)
    #selects users from db based on id and displays info in edit html
    return render_template("edit_user.html", user=user[0])

@app.route("/users/<int:id>/update", methods=["POST"])
def update(id):
    print(request.form)
    mysql = connectToMySQL('users')
    query = "UPDATE friends SET first_name=%(fn)s, last_name = %(ln)s, email = %(email)s WHERE id=%(id)s;"
    data = {
        "id": id,
        "fn": request.form["fname"],
        "ln": request.form["lname"],
        "email": request.form["email"]
    }
    user =mysql.query_db(query, data)
    return redirect(f"/users/{id}")

@app.route("/users/<int:id>/destroy")
def delete(id):
    mysql = connectToMySQL('users')
    query = "DELETE FROM friends WHERE id = %(id)s;"
    data = {
        "id": id
    }
    user = mysql.query_db(query, data)
    #deletes user row from db based on id and redirects and displays to main table
    return redirect("/users")


if __name__ == "__main__":
    app.run(debug=True)