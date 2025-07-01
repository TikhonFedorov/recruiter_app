from flask import Blueprint

vacancy_generator_bp = Blueprint('vacancy_generator', __name__, template_folder='templates')

from .routes import vacancy_generator_bp