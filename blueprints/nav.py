# blueprints/nav.py
import os
import logging
import requests
from flask import Blueprint, render_template, redirect, url_for, current_app, request, abort

from form.contact import ContactForm

nav_bp = Blueprint('nav', __name__)
API_TIMEOUT = 5

def safe_json(resp):
    if not resp or not resp.ok:
        if resp:
            current_app.logger.warning("Upstream returned %s for %s", resp.status_code, resp.url)
        return None
    content_type = resp.headers.get("Content-Type", "")
    if "application/json" not in content_type and not resp.text.strip():
        current_app.logger.info("Empty or non-JSON response from %s", resp.url)
        return None
    try:
        return resp.json()
    except (ValueError, requests.exceptions.JSONDecodeError) as e:
        current_app.logger.warning("JSON decode failed for %s: %s; body=%r", resp.url, e, resp.text[:300])
        return None

@nav_bp.route('/')
def home():
    try:
        resp = requests.get('https://fakestoreapi.com/products', timeout=API_TIMEOUT, headers={"Accept": "application/json"})
    except requests.RequestException as e:
        current_app.logger.error("Failed to fetch products: %s", e)
        # Render home with empty product list or an error page
        return render_template('frontend/home.html', response=[]), 502

    data = safe_json(resp)
    if data is None:
        current_app.logger.info("No product data received; rendering fallback.")
        return render_template('frontend/home.html', response=[]), 502

    return render_template('frontend/home.html', response=data)


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

        # IMPORTANT: don't commit token to source. Use environment variables.
        token = os.getenv("TELEGRAM_BOT_TOKEN")
        if not token:
            current_app.logger.error("Telegram token not set in environment (TELEGRAM_BOT_TOKEN).")
            # handle the error gracefully
            return redirect(url_for('nav.home'))

        url = f"https://api.telegram.org/bot{token}/sendMessage"

        payload = {
            "chat_id": os.getenv("TELEGRAM_CHAT_ID", "1095872862"),
            "text": f"NAME : {name}\nEMAIL : {email}\nSUBJECT : {subject}\nMESSAGE : {message}\n",
            "disable_web_page_preview": False,
            "disable_notification": False
        }

        headers = {
            "accept": "application/json",
            "content-type": "application/json"
        }

        try:
            resp = requests.post(url, json=payload, headers=headers, timeout=API_TIMEOUT)
            if not resp.ok:
                current_app.logger.warning("Telegram API returned %s: %s", resp.status_code, resp.text[:300])
            else:
                # optionally check response.json() safely
                try:
                    body = resp.json()
                    current_app.logger.debug("Telegram response: %s", body)
                except Exception:
                    current_app.logger.debug("Telegram response not JSON or empty.")
        except requests.RequestException as e:
            current_app.logger.error("Failed to send Telegram message: %s", e)
            # continue gracefully

        return redirect(url_for('nav.home'))

    return render_template('frontend/pages/contact.html', form=form)


@nav_bp.route('/shop')
def shop():
    try:
        resp = requests.get('https://fakestoreapi.com/products', timeout=API_TIMEOUT, headers={"Accept": "application/json"})
    except requests.RequestException as e:
        current_app.logger.error("Failed to fetch shop products: %s", e)
        return render_template('frontend/pages/shop.html', products=[]), 502

    data = safe_json(resp)
    if data is None:
        current_app.logger.info("No products for shop; rendering empty list.")
        return render_template('frontend/pages/shop.html', products=[]), 502

    return render_template('frontend/pages/shop.html', products=data)


@nav_bp.route('/about')
def about():
    return render_template('frontend/pages/about.html')
