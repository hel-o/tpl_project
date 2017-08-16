from flask import Blueprint, render_template


urls_frontend = Blueprint(
    'urls_frontend',
    __name__
)


@urls_frontend.route('/')
def home():
    return render_template('home.html')
