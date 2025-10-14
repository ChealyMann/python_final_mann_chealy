from flask import Blueprint , render_template
product_bp = Blueprint('products', __name__)

@product_bp.route('/product_detail')
def product_detail():
    return render_template('frontend/pages/product/product_detail.html')