from flask import Blueprint

create = Blueprint('create', __name__, template_folder='templates', static_folder='static', static_url_path='Create/static')

from . import routes