from flask import Blueprint , render_template , redirect , url_for
home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def home():
    return render_template('frontend/home.html')

@home_bp.route('/contact')
def contact():
    return render_template('frontend/pages/contact.html')