from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///instance/todo.db"  # use instance folder on Render
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Database Model
class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

# Home route
@app.route("/", methods=["GET", "POST"])
def hello_world():
    if request.method == "POST":
        title = request.form["title"]
        desc = request.form["desc"]
        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()

    allTodo = Todo.query.all()
    return render_template("index.html", allTodo=allTodo)

# Products route (example)
@app.route("/products")
def products():
    return "<p>This is products page!</p>"

# Update route
@app.route("/update/<int:sno>", methods=["GET", "POST"])
def update(sno):
    todo = Todo.query.filter_by(sno=sno).first()  # fetch once at start
    if request.method == "POST":
        title = request.form["title"]
        desc = request.form["desc"]

        todo.title = title
        todo.desc = desc

        db.session.commit()  # no add() needed here
        return redirect("/")

    return render_template("update.html", todo=todo)

# Delete route
@app.route("/delete/<int:sno>")
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

# Automatically create database tables
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True, port=8000)
