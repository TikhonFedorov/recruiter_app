from flask import Blueprint

salary_calculator_bp = Blueprint('salary_calculator', __name__, template_folder='templates')

from .routes import salary_calculator_bp
