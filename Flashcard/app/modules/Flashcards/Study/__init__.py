from flask import Blueprint

study = Blueprint('study', __name__, template_folder='templates', static_folder='static', static_url_path='Study/static')

from . import routes