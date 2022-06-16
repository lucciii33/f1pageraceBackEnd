from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    favorite = db.relationship('Favorite')
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    favorite = db.relationship('Favorite',back_populates="user")

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer, unique=False, nullable=False)
    image = db.Column(db.String(550), unique=False, nullable=False)
    description = db.Column(db.String(150), unique=False, nullable=False)
    gender = db.Column(db.String(550), unique=False, nullable=False)
    favorite = db.relationship('Favorite',back_populates="product")
    def __repr__(self):
        return  self.description

    def serialize(self):
        return {
            "id": self.id,
            "price": self.price,
            "image": self.image,
            "description": self.description,
            "gender": self.gender
        }

class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), unique=False, nullable=False, )
    product = db.relationship("Product", back_populates="favorite")
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=False, nullable=False, )
    user = db.relationship("User", back_populates="favorite")
    quantity = db.Column(db.Integer, default = 1)


    # user = db.relationship("User")
    # product = db.relationship("Product")


    def __repr__(self):
        return f'<Favorite {self.product_id}>'

    def serialize(self):
        return {
            "id": self.id,
            "user_id":  self.user_id,
            "product_id": self.product_id,
            "quantity": self.quantity,
            "product": self.product.serialize()
            # "shoppinglist_id": self.shoppinglist_id
            # do not serialize the password, its a security breach
        }

