"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Product, Favorite
# from flask_jwt_extended import create_access_token
# from flask_jwt_extended import get_jwt_identity
# from flask_jwt_extended import jwt_required

#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


# @api.route("/token", methods=["POST"])
# def create_token():
#     email = request.json.get("email", None)
#     password = request.json.get("password", None)
#     user = User.query.filter_by(email=email, password=password ).first()
#     print(user.serialize())
#     print(user)
#     if user is None:
#         # the user was not found on the database
#         return jsonify({"msg": "Bad username or password"}), 401
#     access_token = create_access_token(identity=email)
#     return jsonify({'access_token':access_token, 'email': email, 'user': user.serialize()})

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

@app.route('/product', methods=['GET'])
def get_product():
    
    product_query = Product.query.all()
    all_product = list(map(lambda x: x.serialize(),  product_query))
    
    return jsonify(all_product), 200

@app.route('/product', methods=['POST'])
def post_product():
    body = request.get_json()
    price = body['price']
    image = body['image']
    description = body['description']
    product_exist = Product.query.filter_by(description=description).first()
    if product_exist is not None:
        raise APIException("product already exist", 400)
    product = Product(price=price, image=image, description=description, gender=gender )
    db.session.add(product)
    db.session.commit()

    

    return jsonify(product.serialize()), 200

@app.route('/products', methods=['POST'])
def post_products():
    body = request.json
    print(body)
    for item in body:

        product = Product(price=item['price'], image=item['image'], description=item['description'], gender=item['gender'] )
        db.session.add(product)
        db.session.commit()

    product = Product.query.all()
    all_product= list(map(lambda x: x.serialize(),product ))
    

    return jsonify(all_product), 200

@app.route('/product/<int:id>', methods=['PUT'])
def edit_product(id):

    body = request.get_json()

    product_id = Product.query.get(id)
    if product_id is None:
        raise APIException('Product no found', status_code=404)

    if "image" in body:
        product_id.image = body["image"]
    if "price" in body:
        product_id.price = body["price"]
    if "description" in body:
        product_id.description = body["description"]
    if "gender" in body:
        product_id.gender = body["gender"]
        db.session.commit()

    products = Product.query.all()
    all_products = list(map(lambda x: x.serialize(), products))

    return jsonify(all_products), 200

@app.route('/product/<int:id>', methods=['DELETE'])
def delete_product(id):
    product_id = Product.query.get(id)
    if product_id is None:
        raise APIException('Favorite not found', status_code=404)
   
    db.session.delete(product_id)
    db.session.commit()

    products = Product.query.all()
    all_products= list(map(lambda x: x.serialize(), products))
    

    return jsonify(all_products), 200

#///////////////Favorites///////////////////////////////////////////////////////////////////////////////
@app.route('/favorite', methods=['GET'])
def get_all_favorites():
    
    favorite_query = Favorite.query.all()
    all_favorites = list(map(lambda x: x.serialize(),  favorite_query))
    
    return jsonify(all_favorites), 200

@app.route('/favorite/<int:id>', methods=['GET'])
def get_favorite_for_user(id):
    
    favorite_query = Favorite.query.filter_by(user_id = id)
    single_favorites = Favorite.query.get(id)
    
    return jsonify(single_favorites.serialize()), 200

@app.route('/favorite', methods=['POST'])
def post_favorite():
    body = request.json

    favorite_exist = Favorite.query.filter_by(product_id=body['product_id'], user_id=body['user_id']).first()
    if favorite_exist is not None:
        raise APIException("favorite already exist", 400)
    favorite = Favorite(product_id = body['product_id'],user_id = body['user_id'])

    db.session.add(favorite)
    db.session.commit()

    
    

    return jsonify(all_favorites.serialize()), 200

@app.route('/favorite/<int:id>', methods=['PUT'])
def edit_favorite(id):

    body = request.get_json()
    
    favorite = Favorite.query.get(id)
    if favorite is None:
        raise APIException('Product no found', status_code=404)

    if "quantity" in body:
        favorite.quantity = body["quantity"]
    
    
    

    return jsonify(favorite.serialize()), 200

@app.route('/favorite/<int:id>', methods=['DELETE'])
def delete_favorite(id):
    favorite_id = Favorite.query.get(id)
    if favorite_id is None:
        raise APIException('Favorite not found', status_code=404)
   
    db.session.delete(favorite_id)
    db.session.commit()

    favorites = Favorite.query.all()
    all_favorites= list(map(lambda x: x.serialize(), favorites))
    

    return jsonify(all_favorites), 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
