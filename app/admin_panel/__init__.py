from flask import Blueprint

bp = Blueprint('admin', __name__, url_prefix='/admin')

from app.admin_panel import routes