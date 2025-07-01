from flask import render_template, request, Blueprint

vacancy_generator_bp = Blueprint('vacancy_generator', __name__)

@vacancy_generator_bp.route('/', methods=['GET', 'POST'])
def vacancy_generator():
    vacancy = None
    if request.method == 'POST':
        position = request.form['position']
        experience = request.form['experience']
        vacancy = f"Требуется {position} с опытом работы от {experience} лет."
    return render_template('vacancy_generator.html', vacancy=vacancy)