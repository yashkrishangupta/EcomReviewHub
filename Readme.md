# ShopZone - E-commerce Products and Reviews

## Overview
This is a DBMS NoSQL project demonstrating an e-commerce website with products and customer reviews using MongoDB-style document collections.

## Tech Stack
- **Frontend**: HTML, CSS, JavaScript (vanilla)
- **Backend**: Python Flask
- **Database**: File-based JSON storage (simulating MongoDB/pymongo behavior)
- **Collections**: Products, Reviews

## Project Structure
```
├── app.py              # Flask application with API routes
├── database.py         # MongoDB-style database simulator
├── seed_db.py          # Database seeding script
├── templates/
│   ├── index.html      # Product listing page
│   └── product.html    # Product detail and reviews page
├── static/
│   ├── style.css       # Styling
│   ├── script.js       # Homepage JavaScript
│   └── product.js      # Product page JavaScript
└── data/
    ├── products.json   # Products collection
    └── reviews.json    # Reviews collection
```

## Database Schema

### Products Collection
```json
{
  "_id": "uuid",
  "product_id": 101,
  "name": "Noise Smartwatch X1",
  "category": "Electronics",
  "brand": "Noise",
  "price": 2499,
  "tags": ["watch", "smart", "fitness"],
  "stock": 35,
  "image": "url"
}
```

### Reviews Collection
```json
{
  "_id": "uuid",
  "product_id": 101,
  "user": "Yash",
  "rating": 5,
  "comment": "Great battery life and features!",
  "created_at": "2025-11-20T10:00:00"
}
```

## API Endpoints
- `GET /api/products` - Get all products with ratings
- `GET /api/products/<id>` - Get single product details
- `GET /api/products/<id>/reviews` - Get product reviews
- `POST /api/reviews` - Add a new review
- `GET /api/categories` - Get unique categories
- `GET /api/brands` - Get unique brands

## Features
- Product listing with images, prices, and ratings
- Filter products by category and brand
- Sort products by price or rating
- Product detail page with full information
- Customer reviews with star ratings
- Add new reviews functionality
- Average rating calculation
- Stock status display

## Running the Project
The application runs on port 5000. Start with:
```bash
python app.py
```

## MongoDB Atlas Support
To use MongoDB Atlas instead of file storage, set the `MONGODB_URI` environment variable with your connection string.
