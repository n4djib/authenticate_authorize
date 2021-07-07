from flask import Blueprint, render_template
from flask_login import login_required
from app import rbac


main = Blueprint('main', __name__)

@main.route('/')
@rbac.allow(['anonymous'], methods=['GET'])
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html')
