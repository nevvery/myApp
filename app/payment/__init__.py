from flask import Blueprint


bp = Blueprint('payment', __name__, url_prefix='/payment')

from app.payment import routes