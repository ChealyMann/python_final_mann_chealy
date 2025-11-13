import requests
from flask import Blueprint , render_template
product_bp = Blueprint('products', __name__)

@product_bp.route('/product_detail/<int:id>')
def product_detail(id:int):
    response = requests.get(f'https://fakestoreapi.com/products/{id}')
    response = response.json()
    return render_template('frontend/pages/product/product_detail.html',product=response)