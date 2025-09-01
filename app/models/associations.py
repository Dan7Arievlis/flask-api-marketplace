from app.libraries import db


wishlist_products = db.Table(
    'wishlist_products',
    db.Column('wishlist_id', db.ForeignKey('wishlists.id', ondelete='CASCADE'), primary_key=True),
    db.Column('product_id', db.ForeignKey('products.id', ondelete='CASCADE'), primary_key=True)
)


product_categories = db.Table(
    'product_categories',
    db.Column('product_id', db.ForeignKey('products.id', ondelete='CASCADE'), primary_key=True),
    db.Column('category_id', db.ForeignKey('categories.id', ondelete='CASCADE'), primary_key=True)
)