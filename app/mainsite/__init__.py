from flask import Blueprint

mainsite = Blueprint('mainsite', __name__, template_folder='templates')

import views
