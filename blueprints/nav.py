from flask import Blueprint , render_template , redirect , url_for
nav_bp = Blueprint('nav', __name__)

@nav_bp.route('/')
def home():
    return render_template('frontend/home.html')

@nav_bp.route('/contact')
def contact():
    return render_template('frontend/pages/contact.html')

@nav_bp.route('/shop')
def shop():
    return render_template('frontend/pages/shop.html')

