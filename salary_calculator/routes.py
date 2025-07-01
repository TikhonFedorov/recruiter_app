from flask import render_template, request, Blueprint
from .utils import validate_input, calculate_salary

salary_calculator_bp = Blueprint('salary_calculator', __name__)

@salary_calculator_bp.route('/', methods=['GET', 'POST'])
def salary_calculator():
    results = None
    annual_data = None
    form_data = {}
    errors = []

    if request.method == 'POST':
        form_data = request.form.to_dict()
        errors = validate_input(form_data)

        if not errors:
            try:
                salary = float(form_data.get("salary", 0))
                monthly_bonus = float(form_data.get("monthly_bonus") or 0)
                kpi_enabled = form_data.get("kpi_enabled") == "on"
                kpi_percentage = float(form_data.get("kpi_percentage") or 0)
                kpi_period = form_data.get("kpi_period", "quarter")
                rk_rate = float(form_data.get("rk_rate", 1.0))
                sn_percentage = float(form_data.get("sn_percentage") or 0)

                results, annual_data = calculate_salary(
                    salary, monthly_bonus, kpi_enabled, kpi_percentage,
                    kpi_period, rk_rate, sn_percentage
                )
            except Exception as e:
                errors.append("Ошибка при расчёте. Проверьте введённые данные.")

    return render_template(
        "salary_calculator.html",
        results=results,
        annual_data=annual_data,
        form_data=form_data,
        errors=errors
    )
