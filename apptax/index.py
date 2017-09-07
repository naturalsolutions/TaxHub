from flask import Blueprint, render_template

from pypnusershub import routes as fnauth

routes = Blueprint('index', __name__)
@routes.route("/")
def index():
    return render_template('index.html')


@routes.route("/admin")
def admin():
    return render_template('admin/admin.html')
