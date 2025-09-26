from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from .models import Task
from .extensions import db

todo_bp = Blueprint("todo_bp", __name__)

@todo_bp.route("/todo")
def todo():
    return render_template("todo.html")


@todo_bp.route("/add_task", methods=["GET", "POST"])
@login_required
def add_task():
    if request.method == "POST":
        form_task = request.form.get("task")
        if form_task:
            new_task = Task(description=form_task, user_id=current_user.id)
            db.session.add(new_task)
            db.session.commit()
    tasks=Task.query.filter_by(user_id=current_user.id).all()
    return render_template("todo.html", user=current_user, tasks=tasks)
