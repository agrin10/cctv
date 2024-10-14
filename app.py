from src import  create_app
from flask_jwt_extended import jwt_required , get_jwt_identity ,verify_jwt_in_request 
from flask import request , url_for , render_template ,redirect


app = create_app()


def to_persian_digits(number):
    persian_digits = '۰۱۲۳۴۵۶۷۸۹'
    return ''.join(persian_digits[int(digit)] if digit.isdigit() else digit for digit in str(number))

# Registering it as a filter in Jinja2
app.jinja_env.filters['persian'] = to_persian_digits

if __name__ == "__main__":
    app.run(debug=True , port=8080 , host='0.0.0.0')




