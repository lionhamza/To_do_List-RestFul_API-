from flask import Flask, render_template, request, jsonify
from models import db, Task
import os

app = Flask(__name__)

# PostgreSQL configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost/todo_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

# Render HTML page
@app.route("/")
def index():
    return render_template("index.html")

# ---------------- API ROUTES ---------------- #

# Get all tasks
@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    tasks = Task.query.order_by(Task.created_at.desc()).all()
    return jsonify([task.to_dict() for task in tasks])

# Create new task
@app.route("/api/tasks", methods=["POST"])
def create_task():
    data = request.get_json()
    new_task = Task(title=data["title"])
    db.session.add(new_task)
    db.session.commit()
    return jsonify(new_task.to_dict()), 201

# Update task
@app.route("/api/tasks/<int:id>", methods=["PUT"])
def update_task(id):
    task = Task.query.get_or_404(id)
    data = request.get_json()
    task.completed = data["completed"]
    db.session.commit()
    return jsonify(task.to_dict())

# Delete task
@app.route("/api/tasks/<int:id>", methods=["DELETE"])
def delete_task(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Task deleted"})
    

if __name__ == "__main__":
    app.run(debug=True)
