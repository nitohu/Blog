# -*- coding= utf-8 -*-
from flask import Flask, render_template, request, url_for, redirect, session, escape
from scripts.dbconnect import connect
import time
from time import strftime, gmtime
import os
from werkzeug.security import generate_password_hash, check_password_hash

# Set Up
app = Flask(__name__)
# Secret Key muss geändert werden
app.secret_key = "!\xc6\x8f\x12)\x9a\xa1L\x1a\xf2\xca\xa1W\xd8\x0c\xe4\xcb\x9f\x8b\xc4\xbf\x87F\x0e"
conn, c = connect()
os.environ["TZ"] = "Europe/Berlin"
time.tzset()

# Routes
## Startseite
@app.route("/")
def index():
	rows = []
	c.execute("SELECT * FROM posts")
	for row in c.fetchall():
		rows.append(row)
	rows.reverse()
	return render_template("index.html", rows = rows)

## "Über" Seite
@app.route("/about/")
def about():
	return render_template("about.html")

## Login Seite
@app.route("/login/", methods=["GET", "POST"])
def loginPage():
	# Wenn ein Post Request gemacht wurde
	if request.method == "POST":
		# Und Username und Password ungleich "" sind
		if request.form["username"] != "" != request.form["passwd"]:
			# Checkt ob der User existiert wenn ja wird der Benutzer zum Dashboard weitergeleitet
			username = request.form["username"]
			pw = request.form["passwd"]
			c.execute("SELECT name, passwd, rank FROM users WHERE name = '%s'" % username)
			for row in c.fetchall():
				if row[0] == username and check_password_hash(row[1], pw):
					session["username"] = username
					session["rank"] = row[2]
					return redirect( url_for("dashboardPage") )

			return render_template("login.html", error = "Bitte überprüfe deine angegebenen Daten.")
		else:
			return render_template("login.html", error = "Bitte fülle alle Felder aus.")
	return render_template("login.html")

@app.route("/dashboard/", methods=["POST", "GET"])
def dashboardPage():
	if "username" in session:
		users = []
		c.execute("SELECT name, email, rank FROM users")
		for row in c.fetchall():
			users.append(row)
		if request.method == "POST":
			if request.form["submit-post"]:
				if request.form["post-title"] != "" != request.form["post-content"]:
					c.execute("INSERT INTO posts (title, published, author, content) VALUES ('%s', '%s', '%s', '%s')" % ( request.form["post-title"], strftime("%d %b %Y %H:%M:%S"), session["username"], request.form["post-content"]) )
					conn.commit()
		return render_template("dashboard.html", users = users)
	else:
		return render_template("dashboard.html", error = "Bitte logge dich ein.")

@app.route("/signup/", methods=["POST", "GET"])
def registPage():
	# Checkt ob eine Post Methode vorhanden ist und alles klar ist
	if request.method == "POST":
		if request.form["username"] != "" != request.form["email"] and request.form["passwd"] != "" != request.form["passwdconfirm"]:
			if request.form["passwd"] == request.form["passwdconfirm"]:
				c.execute("SELECT name, email FROM users")
				for row in c.fetchall():
					if row[0] == request.form["username"]:
						return render_template("register.html", error = "Benutzername bereits vorhanden")
					elif row[1] == request.form["email"]:
						return render_template("register.html", error = "E-Mail bereits vorhanden")
				# Wenn die Daten noch nicht eingetragen wurden, query ausführen
				c.execute("INSERT INTO users (name, email, rank, passwd) VALUES ('%s', '%s', 'user', '%s')" % (request.form["username"], request.form["email"], generate_password_hash(request.form["passwd"]) ) )
				conn.commit()
				session["username"] = request.form["username"]
				session["rank"] = "user"
				return redirect( url_for("dashboardPage") )
	return render_template("register.html")

@app.route("/logout/")
def logoutPage():
	session.clear()
	return redirect( url_for("index") )

# Errorhandler
@app.errorhandler(404)
def not_found(error):
	return render_template("not_found.html", e = error)

if __name__ == "__main__":
	app.run(debug = True)
