from flask import Flask, request, jsonify
from flask_login import (
    UserMixin,
    current_user,
    login_required,
    login_user,
    LoginManager,
    logout_user,
)
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

application = Flask(__name__)
application.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///ecommerce.db"
application.config["SECRET_KEY"] = "mysecretkey123"

db = SQLAlchemy(application)
login_manager = LoginManager()
login_manager.init_app(application)
login_manager.login_view = "login"
CORS(application)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    cart = db.relationship("CartItem", backref="user", lazy=True)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)


class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@application.route("/")
def home():
    return jsonify({"message": "Welcome to the E-commerce API"})


@application.route("/login", methods=["POST"])
def login():
    data = request.json
    user = User.query.filter_by(username=data.get("username")).first()
    if user and user.password == data.get("password"):
        login_user(user)
        return jsonify({"message": "Logged in successfully"}), 200
    return jsonify({"message": "Unauthorized. Invalid credentials"}), 401


@application.route("/logout", methods=["POST"])
def logout():
    logout_user()
    return jsonify({"message": "Logout successfully"}), 200


@application.route("/api/products/add", methods=["POST"])
@login_required
def add_product():
    data = request.json
    if "name" in data and "price" in data:
        product = Product(
            name=data["name"],
            price=data["price"],
            description=data.get("description", ""),
        )
        db.session.add(product)
        db.session.commit()
        return jsonify({"message": "Product added successfully"})
    return jsonify({"message": "Invalid product data"}), 400


@application.route("/api/products/delete/<int:product_id>", methods=["DELETE"])
@login_required
def delete_product(product_id):
    product = Product.query.get(product_id)
    if product:
        db.session.delete(product)
        db.session.commit()
        return jsonify({"message": "Product deleted successfully"})
    return jsonify({"message": "Product not found"}), 404


@application.route("/api/products/update/<int:product_id>", methods=["PUT"])
@login_required
def update_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"message": "Product not found"}), 404

    data = request.json
    if "name" in data:
        product.name = data["name"]
    if "price" in data:
        product.price = data["price"]
    if "description" in data:
        product.description = data["description"]

    db.session.commit()
    return jsonify({"message": "Product updated successfully"}), 200


@application.route("/api/products/<int:product_id>", methods=["GET"])
def get_product_details(product_id):
    product = Product.query.get(product_id)
    if product:
        return jsonify(
            {
                "id": product.id,
                "name": product.name,
                "price": product.price,
                "description": product.description,
            }
        )
    return jsonify({"message": "Product not found"}), 404


@application.route("/api/products", methods=["GET"])
def get_all_products():
    products = Product.query.all()
    product_list = []
    for product in products:
        product_data = {
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "description": product.description,
        }
        product_list.append(product_data)
    return jsonify(product_list), 200


@application.route("/api/cart/add/<int:product_id>", methods=["POST"])
@login_required
def add_to_cart(product_id):
    product = Product.query.get(product_id)
    user = User.query.get(int(current_user.id))

    if user and product:
        cart_item = CartItem(
            user_id=user.id,
            product_id=product.id,
        )
        db.session.add(cart_item)
        db.session.commit()
        return jsonify({"message": "Item added to the cart successfully"}), 200
    return jsonify({"message": "Failed to add item to the cart"}), 400


@application.route("/api/cart/remove/<int:product_id>", methods=["DELETE"])
@login_required
def remove_from_cart(product_id):
    user = User.query.get(int(current_user.id))
    cart_item = CartItem.query.filter_by(user_id=user.id, product_id=product_id).first()
    if cart_item:
        db.session.delete(cart_item)
        db.session.commit()
        return jsonify({"message": "Item removed from the cart successfully"}), 200
    return jsonify({"message": "Failed to remove item from the cart"}), 400


@application.route("/api/cart", methods=["GET"])
@login_required
def get_cart():
    user = User.query.get(int(current_user.id))
    cart_items = user.cart
    cart_list = []
    for cart_item in cart_items:
        product = Product.query.get(cart_item.product_id)
        cart_data = {
            "id": cart_item.id,
            "user_id": user.id,
            "product_id": product.id,
            "product_name": product.name,
            "product_price": product.price,
        }
        cart_list.append(cart_data)
    return jsonify(cart_list), 200


@application.route("/api/cart/checkout", methods=["POST"])
@login_required
def checkout():
    user = User.query.get(int(current_user.id))
    cart_items = user.cart
    total = 0
    for cart_item in cart_items:
        product = Product.query.get(cart_item.product_id)
        total += product.price
        db.session.delete(cart_item)
    db.session.commit()
    return (
        jsonify(
            {
                "message": f"Checkout successful. Total amount: {total}. Cart has been cleared."
            }
        ),
        200,
    )


if __name__ == "__main__":
    application.run(debug=True)
