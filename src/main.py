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
from models import db, User, Product
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
    body = request.json

    product = Product(price=body['price'], image=body['image'], description=body['description'], gender=body['gender'] )
    db.session.add(product)
    db.session.commit()

    product = Product.query.all()
    all_product= list(map(lambda x: x.serialize(),product ))
    

    return jsonify(all_product), 200

# @app.route('/products', methods=['POST'])
# def post_products():
#     body = request.json
#     for item in body:

#         product = Product(price=body['price'], image=body['image'], description=body['description'] )
#         db.session.add(product)
#         db.session.commit()

#     product = Product.query.all()
#     all_product= list(map(lambda x: x.serialize(),product ))
    

    # return jsonify(all_product), 200

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


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
