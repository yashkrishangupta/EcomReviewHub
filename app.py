from flask import Flask, render_template, request, jsonify, redirect, url_for
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SESSION_SECRET', 'dev-secret-key')

MONGODB_URI = os.environ.get('MONGODB_URI', '')

if MONGODB_URI:
    client = MongoClient(MONGODB_URI, server_api=ServerApi('1'))
    db = client['ecommerce_db']
else:
    from database import db

products_collection = db['products']
reviews_collection = db['reviews']

def serialize_doc(doc):
    if doc is None:
        return None
    doc = dict(doc)
    if '_id' in doc:
        doc['_id'] = str(doc['_id'])
    if 'created_at' in doc and isinstance(doc['created_at'], datetime):
        doc['created_at'] = doc['created_at'].isoformat()
    return doc

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    return render_template('product.html', product_id=product_id)

@app.route('/api/products', methods=['GET'])
def get_products():
    if MONGODB_URI:
        products = list(products_collection.find())
    else:
        products = products_collection.find()
    
    result = []
    for product in products:
        product = serialize_doc(product)
        product_id = product.get('product_id', product.get('_id'))
        
        if MONGODB_URI:
            reviews = list(reviews_collection.find({'product_id': product_id}))
        else:
            reviews = reviews_collection.find({'product_id': product_id})
        
        if reviews:
            avg_rating = sum(r['rating'] for r in reviews) / len(reviews)
            product['avg_rating'] = round(avg_rating, 1)
            product['review_count'] = len(reviews)
        else:
            product['avg_rating'] = 0
            product['review_count'] = 0
        result.append(product)
    return jsonify(result)

@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = products_collection.find_one({'product_id': product_id})
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    product = serialize_doc(product)
    
    if MONGODB_URI:
        reviews = list(reviews_collection.find({'product_id': product_id}))
    else:
        reviews = reviews_collection.find({'product_id': product_id})
    
    if reviews:
        avg_rating = sum(r['rating'] for r in reviews) / len(reviews)
        product['avg_rating'] = round(avg_rating, 1)
        product['review_count'] = len(reviews)
    else:
        product['avg_rating'] = 0
        product['review_count'] = 0
    return jsonify(product)

@app.route('/api/products/<int:product_id>/reviews', methods=['GET'])
def get_product_reviews(product_id):
    if MONGODB_URI:
        reviews = list(reviews_collection.find({'product_id': product_id}))
        reviews.sort(key=lambda x: x.get('created_at', ''), reverse=True)
    else:
        reviews = reviews_collection.find({'product_id': product_id})
        reviews.sort(key=lambda x: x.get('created_at', ''), reverse=True)
    
    return jsonify([serialize_doc(r) for r in reviews])

@app.route('/api/reviews', methods=['POST'])
def add_review():
    data = request.json
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    required_fields = ['product_id', 'user', 'rating', 'comment']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    review = {
        'product_id': int(data['product_id']),
        'user': data['user'],
        'rating': int(data['rating']),
        'comment': data['comment'],
        'created_at': datetime.utcnow().isoformat()
    }
    
    result = reviews_collection.insert_one(review)
    review['_id'] = str(result['inserted_id']) if isinstance(result, dict) else str(result.inserted_id)
    
    return jsonify(review), 201

@app.route('/api/categories', methods=['GET'])
def get_categories():
    categories = products_collection.distinct('category')
    return jsonify(categories)

@app.route('/api/brands', methods=['GET'])
def get_brands():
    brands = products_collection.distinct('brand')
    return jsonify(brands)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
