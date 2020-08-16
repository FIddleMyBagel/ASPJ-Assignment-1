from flask import Blueprint, request, redirect, url_for
from flask_login import current_user
from Database import db, Cart
cart_api = Blueprint('cart_api', __name__)


@cart_api.route('/add_cart/<int:product_id>', methods=['POST', 'GET'])
def add_cart(product_id):
    if request.method == 'POST':
        current_cart = Cart.query.filter_by(cart_id=current_user.id, product_id=product_id).first()
        if current_cart is not None:
            current_cart.quantity += 1
        else:
            new_cart = Cart(cart_id=current_user.id,
                            product_id=product_id,
                            quantity=1,
                            id=current_user.id)
            db.session.add(new_cart)
        db.session.commit()
    return redirect(request.referrer)


@cart_api.route('/remove_cart/<int:product_id>', methods=['POST', 'GET'])
def remove_cart(product_id):
    if request.method == 'POST':
        db.session.rollback()
        current_cart = Cart.query.filter_by(cart_id=current_user.id, product_id=product_id).first()
        current_cart.quantity -= 1
        if current_cart.quantity == 0:
            db.session.delete(current_cart)
        db.session.commit()
    return redirect(url_for('cart'))


@cart_api.route('/clear_cart/<int:product_id>', methods=['POST', 'GET'])
def clear_cart(product_id):
    if request.method == 'POST':
        current_cart = Cart.query.filter_by(cart_id=current_user.id, product_id=product_id).first()
        db.session.delete(current_cart)
        db.session.commit()
    return redirect(url_for('cart'))
