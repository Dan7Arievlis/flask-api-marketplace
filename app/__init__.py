import os
from flask import Flask
from .libraries import db

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///local.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    from .models.user import User
    from .models.wishlist import Wishlist
    from .models.stock import Stock
    from .models.cart import Cart
    from .models.cart_item import CartItem
    from .models.stock_item import StockItem
    from .models.product import Product
    from .models.category import Category
    from .models.payment import Payment

    return app