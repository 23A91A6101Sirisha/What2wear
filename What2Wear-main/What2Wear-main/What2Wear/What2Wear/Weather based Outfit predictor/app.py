from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import utils

app = Flask(__name__)
app.secret_key = "your_secret_key"  # required for session handling


def get_db_connection():
    conn = sqlite3.connect("users.db")
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")


@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "username" not in session:
        return redirect(url_for("login"))

    outfit = None
    weather_data = None

    if request.method == "POST":
        city = request.form.get("city")
        if not city:
            city = "peddapuram"  
        weather_data = utils.get_weather(city)
        if weather_data:
            outfit = utils.get_outfit_suggestion(weather_data)

    return render_template("dashboard.html", outfit=outfit, weather=weather_data)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        conn = get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE username=? AND password=?", 
                            (username, password)).fetchone()
        conn.close()

        if user:
            session["username"] = username
            return redirect(url_for("dashboard"))
        else:
            return "Invalid username or password!"

    return render_template("login.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        conn = get_db_connection()
        try:
            conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", 
                         (username, password))
            conn.commit()
        except sqlite3.IntegrityError:
            return "Username already exists!"
        finally:
            conn.close()

        return redirect(url_for("login"))

    return render_template("signup.html")


@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
