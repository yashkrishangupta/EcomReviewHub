from datetime import datetime, timedelta
import random
import os

MONGODB_URI = os.environ.get('MONGODB_URI', '')

if MONGODB_URI:
    from pymongo import MongoClient
    from pymongo.server_api import ServerApi
    client = MongoClient(MONGODB_URI, server_api=ServerApi('1'))
    db = client['ecommerce_db']
    products_collection = db['products']
    reviews_collection = db['reviews']
else:
    from database import products_collection, reviews_collection

products_collection.drop()
reviews_collection.drop()

products = [
    {
        "product_id": 101,
        "name": "Noise Smartwatch X1",
        "category": "Electronics",
        "brand": "Noise",
        "price": 2499,
        "tags": ["watch", "smart", "fitness"],
        "stock": 35,
        "image": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400"
    },
    {
        "product_id": 102,
        "name": "boAt Airdopes 141",
        "category": "Electronics",
        "brand": "boAt",
        "price": 1299,
        "tags": ["earbuds", "wireless", "bluetooth"],
        "stock": 50,
        "image": "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=400"
    },
    {
        "product_id": 103,
        "name": "Samsung Galaxy M14",
        "category": "Electronics",
        "brand": "Samsung",
        "price": 13999,
        "tags": ["phone", "smartphone", "5g"],
        "stock": 20,
        "image": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400"
    },
    {
        "product_id": 104,
        "name": "Nike Air Max 270",
        "category": "Footwear",
        "brand": "Nike",
        "price": 8995,
        "tags": ["shoes", "sports", "running"],
        "stock": 15,
        "image": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400"
    },
    {
        "product_id": 105,
        "name": "Adidas Ultraboost",
        "category": "Footwear",
        "brand": "Adidas",
        "price": 12999,
        "tags": ["shoes", "running", "comfort"],
        "stock": 10,
        "image": "https://images.unsplash.com/photo-1608231387042-66d1773070a5?w=400"
    },
    {
        "product_id": 106,
        "name": "Levi's 501 Original Jeans",
        "category": "Clothing",
        "brand": "Levi's",
        "price": 2999,
        "tags": ["jeans", "denim", "casual"],
        "stock": 40,
        "image": "https://images.unsplash.com/photo-1542272604-787c3835535d?w=400"
    },
    {
        "product_id": 107,
        "name": "HP Pavilion Laptop",
        "category": "Electronics",
        "brand": "HP",
        "price": 54999,
        "tags": ["laptop", "computer", "gaming"],
        "stock": 8,
        "image": "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=400"
    },
    {
        "product_id": 108,
        "name": "Sony WH-1000XM5",
        "category": "Electronics",
        "brand": "Sony",
        "price": 29990,
        "tags": ["headphones", "wireless", "noise-cancelling"],
        "stock": 12,
        "image": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400"
    },
    {
        "product_id": 109,
        "name": "Puma RS-X Sneakers",
        "category": "Footwear",
        "brand": "Puma",
        "price": 6999,
        "tags": ["sneakers", "casual", "trendy"],
        "stock": 25,
        "image": "https://images.unsplash.com/photo-1600185365926-3a2ce3cdb9eb?w=400"
    },
    {
        "product_id": 110,
        "name": "Ray-Ban Aviator Sunglasses",
        "category": "Accessories",
        "brand": "Ray-Ban",
        "price": 7490,
        "tags": ["sunglasses", "fashion", "UV protection"],
        "stock": 30,
        "image": "https://images.unsplash.com/photo-1572635196237-14b3f281503f?w=400"
    }
]

users = ["Yash", "Priya", "Rahul", "Sneha", "Amit", "Kavya", "Rohan", "Ananya", "Vikram", "Neha"]

comments_positive = [
    "Great product! Highly recommended.",
    "Excellent quality and fast delivery.",
    "Love it! Exactly what I was looking for.",
    "Amazing value for money.",
    "Superb quality, exceeded expectations!",
    "Best purchase I've made this year.",
    "Fantastic product, will buy again!"
]

comments_neutral = [
    "Good product, serves its purpose.",
    "Decent quality for the price.",
    "It's okay, nothing special.",
    "Average product, could be better."
]

comments_negative = [
    "Not as expected, quality could be better.",
    "Delivery was delayed but product is okay.",
    "Could have been better for this price."
]

products_collection.insert_many(products)
print(f"Inserted {len(products)} products")

reviews = []
base_date = datetime(2025, 11, 1)

for product in products:
    num_reviews = random.randint(2, 5)
    for i in range(num_reviews):
        rating = random.choices([5, 4, 3, 2, 1], weights=[40, 30, 15, 10, 5])[0]
        
        if rating >= 4:
            comment = random.choice(comments_positive)
        elif rating == 3:
            comment = random.choice(comments_neutral)
        else:
            comment = random.choice(comments_negative)
        
        review_date = base_date + timedelta(days=random.randint(0, 26), hours=random.randint(0, 23))
        
        review = {
            "product_id": product["product_id"],
            "user": random.choice(users),
            "rating": rating,
            "comment": comment,
            "created_at": review_date.isoformat()
        }
        reviews.append(review)

reviews_collection.insert_many(reviews)
print(f"Inserted {len(reviews)} reviews")

print("\nDatabase seeded successfully!")
print(f"Products collection count: {products_collection.count_documents({})}")
print(f"Reviews collection count: {reviews_collection.count_documents({})}")

print("\n--- Sample Product Document ---")
sample_product = products_collection.find_one({'product_id': 101})
print(sample_product)

print("\n--- Sample Review Document ---")
sample_review = reviews_collection.find_one({'product_id': 101})
print(sample_review)
