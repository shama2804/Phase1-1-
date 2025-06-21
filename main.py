from flask import Flask
from app import flask_app
from routes import hr_bp  # ✅ matches your Blueprint name in routes.py

app = Flask(__name__)

# Register HR (JD-related) Blueprint
app.register_blueprint(hr_bp)

# Register Resume form routes manually from flask_app
app.add_url_rule('/', view_func=flask_app.view_functions['index'])
app.add_url_rule('/upload', view_func=flask_app.view_functions['upload_resume'], methods=['POST'])
app.add_url_rule('/submit', view_func=flask_app.view_functions['submit'], methods=['POST'])
app.add_url_rule('/apply/<jd_id>', view_func=flask_app.view_functions['upload_for_jd'], methods=['GET', 'POST'])

if __name__ == '__main__':
    app.run(debug=True)
