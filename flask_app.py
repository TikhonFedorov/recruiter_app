from flask import Flask, render_template
from salary_calculator import salary_calculator_bp
from vacancy_generator import vacancy_generator_bp

app = Flask(__name__)

# Register blueprints
app.register_blueprint(salary_calculator_bp, url_prefix='/salary_calculator')
app.register_blueprint(vacancy_generator_bp, url_prefix='/vacancy_generator')

# Debug check for registered endpoints after registration
print("Registered endpoints:", list(app.url_map.iter_rules()))

@app.route('/')
def index():
    return render_template('index.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)