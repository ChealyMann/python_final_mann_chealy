from pprint import pprint

import requests
from flask import Blueprint , render_template , redirect , url_for

from form.contact import ContactForm
from flask import request

nav_bp = Blueprint('nav', __name__)

@nav_bp.route('/')
def home():
    response = requests.get('https://fakestoreapi.com/products')
    response = response.json()
    return render_template('frontend/home.html',response=response)

@nav_bp.route('/cart')
def cart():
    return render_template('frontend/pages/cart.html')

@nav_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        subject = form.subject.data
        message = form.message.data


        token = '8257940589:AAGiMrNXXpHPP9YqMDG5e06fyjJaYo58nM0'


        url = f"https://api.telegram.org/bot{token}/sendMessage"

        payload = {
            "chat_id": "1095872862",
            "text": f"""
NAME : {name}
EMAIL : {email}
SUBJECT : {subject}
MESSAGE : {message}
""",
            "disable_web_page_preview": False,
            "disable_notification": False
        }

        headers = {
            "accept": "application/json",
            "content-type": "application/json"
        }

        response = requests.post(url, json=payload, headers=headers)

        return redirect(url_for('nav.home'))

    return render_template('frontend/pages/contact.html', form=form)


@nav_bp.route('/shop')
def shop():
    response = requests.get('https://fakestoreapi.com/products')
    response = response.json()
    return render_template('frontend/pages/shop.html',products=response)

@nav_bp.route('/about')
def about():
    return render_template('frontend/pages/about.html')