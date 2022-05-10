from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

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
    def __repr__(self):
        return '<User %r>' % self.username

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
    product_id = db.Column(db.String(120), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=False, nullable=False, )
    user = db.relationship("User")

    def __repr__(self):
        return f'<Favorite {self.product_id}>'

    def serialize(self):
        return {
            "id": self.id,
            "user_id":  self.user_id,
            "drink_name": self.product_id,
            # "shoppinglist_id": self.shoppinglist_id
            # do not serialize the password, its a security breach
        }

