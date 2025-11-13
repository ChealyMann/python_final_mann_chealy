# blueprints/products.py
import os
import logging
import requests
from flask import Blueprint, render_template, current_app, abort

product_bp = Blueprint('products', __name__)

API_TIMEOUT = 5  # seconds

def safe_json(resp):
    """
    Try to decode JSON safely. Returns None on failure.
    """
    if not resp:
        return None
    # Quick checks
    if not resp.ok:
        current_app.logger.warning("Upstream returned non-OK status %s for %s", resp.status_code, resp.url)
        return None
    content_type = resp.headers.get("Content-Type", "")
    # If there's no content or content-type doesn't look like json, still try if there is text
    if "application/json" not in content_type and not resp.text.strip():
        current_app.logger.info("Empty or non-JSON response from %s (Content-Type=%s)", resp.url, content_type)
        return None
    try:
        return resp.json()
    except (ValueError, requests.exceptions.JSONDecodeError) as e:
        current_app.logger.warning("Failed to parse JSON from %s: %s; body=%r", resp.url, e, resp.text[:300])
        return None

@product_bp.route('/product_detail/<int:id>')
def product_detail(id: int):
    try:
        resp = requests.get(f'https://fakestoreapi.com/products/{id}', timeout=API_TIMEOUT, headers={"Accept": "application/json"})
    except requests.RequestException as e:
        current_app.logger.error("Request to fakestoreapi failed: %s", e)
        # You can return a custom error template or abort with 502
        abort(502)

    data = safe_json(resp)
    if data is None:
        # fallback: render template with empty product or abort
        current_app.logger.info("Using fallback for product id=%s", id)
        return render_template('frontend/pages/product/product_detail.html', product={}), 502

    return render_template('frontend/pages/product/product_detail.html', product=data)
