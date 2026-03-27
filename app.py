from flask import Flask, render_template, request, redirect
import sqlite3
import webbrowser
import threading

app = Flask(__name__)

# ---------- DATABASE SETUP ----------
def init_db():
    conn = sqlite3.connect("notes.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()


# ---------- HOME ROUTE ----------
@app.route('/', methods=["GET", "POST"])
def home():
    conn = sqlite3.connect("notes.db")
    cursor = conn.cursor()

    if request.method == "POST":
        note = request.form.get("note")
        if note:
            cursor.execute("INSERT INTO notes (content) VALUES (?)", (note,))
            conn.commit()
        return redirect("/")

    cursor.execute("SELECT * FROM notes")
    notes = cursor.fetchall()

    conn.close()
    return render_template("home.html", notes=notes)


# ---------- DELETE ----------
@app.route('/delete/<int:id>')
def delete(id):
    conn = sqlite3.connect("notes.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM notes WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect("/")
@app.route('/edit/<int:id>', methods=["GET", "POST"])
def edit(id):
    conn = sqlite3.connect("notes.db")
    cursor = conn.cursor()

    if request.method == "POST":
        updated_note = request.form.get("note")
        cursor.execute("UPDATE notes SET content = ? WHERE id = ?", (updated_note, id))
        conn.commit()
        conn.close()
        return redirect("/")

    cursor.execute("SELECT * FROM notes WHERE id = ?", (id,))
    note = cursor.fetchone()
    conn.close()

    return render_template("edit.html", note=note)

# ---------- AUTO OPEN ----------
def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000/")


if __name__ == '__main__':
    threading.Timer(1, open_browser).start()
    app.run(debug=True, use_reloader=False)