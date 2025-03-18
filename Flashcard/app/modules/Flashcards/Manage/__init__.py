from flask import Blueprint

manage = Blueprint('manage', __name__, template_folder='templates', static_folder='static', static_url_path='Manage/static')

from . import routes