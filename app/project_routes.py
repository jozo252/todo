from app.extensions import db, login_manager
from app.models import Project, Task
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from datetime import datetime

project_bp = Blueprint("project_bp", __name__)

@project_bp.route("/projects")
@login_required
def projects():
    user_projects = Project.query.filter_by(user_id=current_user.id).all()
    return render_template("projects.html", projects=user_projects)

@project_bp.route("/add_project", methods=["GET", "POST"])
@login_required
def add_project():
    if request.method == "POST":
        name = request.form.get("name")
        description = request.form.get("description")
        start_date = datetime.strptime(request.form.get("start_date"), "%Y-%m-%d")
        end_date_str = request.form.get("end_date")
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d") if end_date_str else None

        if name:
            new_project = Project(
                name=name,
                description=description,
                start_date=start_date,
                end_date=end_date,
                user_id=current_user.id
            )
            db.session.add(new_project)
            db.session.commit()
            return redirect(url_for("project_bp.projects"))

    return render_template("add_project.html")

@project_bp.route("/view_project/<int:project_id>")
@login_required
def view_project(project_id):
    project = Project.query.get_or_404(project_id)
    if project.user_id != current_user.id:
        return "Unauthorized", 403
    tasks = Task.query.filter_by(project_id=project.id).all()
    return render_template("view_project.html", project=project, tasks=tasks)




@project_bp.route("/projects/<int:project_id>/add_task", methods=["GET", "POST"])
@login_required
def add_task(project_id):
    project = Project.query.filter_by(id=project_id, user_id=current_user.id).first_or_404()

    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        due_date = request.form.get("due_date")
        if title and description:
            new_task = Task(
                description=description,
                user_id=current_user.id,
                project_id=project.id,
                created_at=datetime.utcnow(),
                # add due_date if your model supports it
            )
            db.session.add(new_task)
            db.session.commit()
            flash("Task added!", "success")
            return redirect(url_for("project_bp.view_project", project_id=project.id))

    tasks = project.tasks
    return render_template("view_project.html", project=project, tasks=tasks, user=current_user)


@project_bp.route("/toggle_task/<int:task_id>", methods=["POST"])
@login_required
def toggle_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        return "Unauthorized", 403

    task.completed = not task.completed
    if task.completed:
        task.completed_at = datetime.utcnow()
    else:
        task.completed_at = None
    db.session.commit()
    flash("Task status updated!", "success")
    return redirect(url_for("project_bp.view_project", project_id=task.project_id))


@project_bp.route("/delete_task/<int:task_id>", methods=["POST"])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        return "Unauthorized", 403

    project_id = task.project_id
    db.session.delete(task)
    db.session.commit()
    flash("Task deleted!", "success")
    return redirect(url_for("project_bp.view_project", project_id=project_id))

