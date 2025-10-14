from flask import Blueprint , render_template , redirect , url_for

from form.contact import ContactForm

nav_bp = Blueprint('nav', __name__)

@nav_bp.route('/')
def home():
    return render_template('frontend/home.html')

@nav_bp.route('/contact',methods=['GET','POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        subject = form.subject.data
        message = form.message.data

    return render_template('frontend/pages/contact.html',form=form)

@nav_bp.route('/shop')
def shop():
    return render_template('frontend/pages/shop.html')

@nav_bp.route('/about')
def about():
    return render_template('frontend/pages/about.html')