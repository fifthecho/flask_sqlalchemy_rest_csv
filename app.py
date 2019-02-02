from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow 
import os
import json

# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'jefflovesyou.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Init db
db = SQLAlchemy(app)
# Init ma
ma = Marshmallow(app)

class InsurancePolicy(db.Model):
  rowid = db.Column(db.Integer, primary_key=True)
  policyID = db.Column(db.Integer)
  statecode = db.Column(db.String(2))
  county = db.Column(db.String(255))
  eq_site_limit = db.Column(db.Float)
  hu_site_limit = db.Column(db.Float)
  def __init__(self, policyID, statecode, county, eq_site_limit, hu_site_limit):
    self.policyID = policyID
    self.statecode = statecode
    self.county = county
    self.eq_site_limit = eq_site_limit
    self.hu_site_limit = hu_site_limit

class InsurancePolicySchema(ma.Schema):
  class Meta:
    fields = ('policyID', 'statecode', 'county', 'eq_site_limit', 'hu_site_limit')

# Init schema
policy_schema = InsurancePolicySchema(strict=True)
policies_schema = InsurancePolicySchema(many=True, strict=True)

# Create a Policy
@app.route('/policy', methods=['POST'])
def add_policy():
  data = json.loads(request.data)
  policy_id = data['policyID']
  statecode = data['statecode']
  county = data['county']
  eq_site_limit = data['eq_site_limit']
  hu_site_limit = data['hu_site_limit']

  new_policy = InsurancePolicy(policy_id, statecode, county, eq_site_limit, hu_site_limit)
  db.session.add(new_policy)
  db.session.commit()

  return policy_schema.jsonify(new_policy)

@app.route('/')
def ping():
  return jsonify({'ping': 'pong'})

@app.route('/policy', methods=['GET'])
def get_all_policies():
  all_policies = InsurancePolicy.query.all()
  result = policies_schema.dump(all_policies)
  return jsonify(result.data)

# # Get All Products
# @app.route('/product', methods=['GET'])
# def get_products():
#   all_products = Product.query.all()
#   result = products_schema.dump(all_products)
#   return jsonify(result.data)

# # Get Single Products
# @app.route('/product/<id>', methods=['GET'])
# def get_product(id):
#   product = Product.query.get(id)
#   return product_schema.jsonify(product)

# # Update a Product
# @app.route('/product/<id>', methods=['PUT'])
# def update_product(id):
#   product = Product.query.get(id)

#   name = data['name']
#   description = data['description']
#   price = data['price']
#   qty = data['qty']

#   product.name = name
#   product.description = description
#   product.price = price
#   product.qty = qty

#   db.session.commit()

#   return product_schema.jsonify(product)

# # Delete Product
# @app.route('/product/<id>', methods=['DELETE'])
# def delete_product(id):
#   product = Product.query.get(id)
#   db.session.delete(product)
#   db.session.commit()

#   return product_schema.jsonify(product)

# Run Server
if __name__ == '__main__':
  app.run(debug=True)