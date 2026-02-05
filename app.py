from flask import Flask, render_template, request
import sqlite3
import os

app = Flask(__name__)

FLAG = "cyber{sqli_login_bypass}"

# -----------------------------
# In-memory SQLite database
# -----------------------------
conn = sqlite3.connect(":memory:", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE users (
    username TEXT,
    password TEXT
)
""")

cursor.execute("""
INSERT INTO users VALUES ('admin', 'hidden_password')
""")

conn.commit()


# -----------------------------
# Vulnerable Login Route (CTF)
# -----------------------------
@app.route("/", methods=["GET", "POST"])
def login():
    message = ""

    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        # ❌ INTENTIONALLY VULNERABLE QUERY (for SQLi challenge)
        query = (
            "SELECT * FROM users "
            "WHERE username = '" + username + "' "
            "AND password = '" + password + "'"
        )

        try:
            result = cursor.execute(query).fetchone()
        except Exception:
            message = "SQL Error"
            return render_template("login.html", message=message)

        if result:
            return render_template("success.html", flag=FLAG)
        else:
            message = "Invalid credentials"

    return render_template("login.html", message=message)


# -----------------------------
# Localhost + Cloud Runner
# -----------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
