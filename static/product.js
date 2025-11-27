let selectedRating = 0;

document.addEventListener('DOMContentLoaded', function() {
    loadProductDetail();
    loadReviews();
    setupStarRating();
    setupReviewForm();
});

async function loadProductDetail() {
    try {
        const response = await fetch(`/api/products/${productId}`);
        if (!response.ok) {
            throw new Error('Product not found');
        }
        const product = await response.json();
        displayProductDetail(product);
    } catch (error) {
        console.error('Error loading product:', error);
        document.getElementById('product-detail').innerHTML = 
            '<p class="loading">Error loading product. Please try again.</p>';
    }
}

function displayProductDetail(product) {
    const container = document.getElementById('product-detail');
    
    container.innerHTML = `
        <div class="product-detail">
            <div>
                <img src="${product.image || 'https://via.placeholder.com/500x400?text=No+Image'}" 
                     alt="${product.name}" class="product-detail-image">
            </div>
            <div class="product-detail-info">
                <h1>${product.name}</h1>
                <p class="product-brand">Brand: ${product.brand}</p>
                <p class="product-category">Category: ${product.category}</p>
                <p class="product-price">₹${product.price.toLocaleString()}</p>
                <div class="product-rating">
                    <span class="stars">${getStars(product.avg_rating)}</span>
                    <span class="rating-count">${product.avg_rating} out of 5 (${product.review_count} reviews)</span>
                </div>
                <span class="product-stock ${getStockClass(product.stock)}">
                    ${getStockText(product.stock)}
                </span>
                <div class="product-tags">
                    ${product.tags.map(tag => `<span class="tag">${tag}</span>`).join('')}
                </div>
            </div>
        </div>
    `;
    
    document.title = `${product.name} - ShopZone`;
}

async function loadReviews() {
    try {
        const response = await fetch(`/api/products/${productId}/reviews`);
        const reviews = await response.json();
        displayReviews(reviews);
    } catch (error) {
        console.error('Error loading reviews:', error);
        document.getElementById('reviews-container').innerHTML = 
            '<p class="loading">Error loading reviews.</p>';
    }
}

function displayReviews(reviews) {
    const container = document.getElementById('reviews-container');
    
    if (reviews.length === 0) {
        container.innerHTML = '<p class="no-reviews">No reviews yet. Be the first to review this product!</p>';
        return;
    }
    
    container.innerHTML = reviews.map(review => `
        <div class="review-card">
            <div class="review-header">
                <span class="review-user">${review.user}</span>
                <span class="review-date">${formatDate(review.created_at)}</span>
            </div>
            <div class="review-rating">${getStarsFromRating(review.rating)}</div>
            <p class="review-comment">${review.comment}</p>
        </div>
    `).join('');
}

function setupStarRating() {
    const stars = document.querySelectorAll('.star-rating .star');
    
    stars.forEach(star => {
        star.addEventListener('click', function() {
            selectedRating = parseInt(this.dataset.rating);
            document.getElementById('rating').value = selectedRating;
            updateStarDisplay();
        });
        
        star.addEventListener('mouseenter', function() {
            const hoverRating = parseInt(this.dataset.rating);
            highlightStars(hoverRating);
        });
        
        star.addEventListener('mouseleave', function() {
            updateStarDisplay();
        });
    });
}

function highlightStars(rating) {
    const stars = document.querySelectorAll('.star-rating .star');
    stars.forEach((star, index) => {
        if (index < rating) {
            star.classList.add('active');
        } else {
            star.classList.remove('active');
        }
    });
}

function updateStarDisplay() {
    highlightStars(selectedRating);
}

function setupReviewForm() {
    const form = document.getElementById('review-form');
    
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const userName = document.getElementById('user-name').value.trim();
        const rating = selectedRating;
        const comment = document.getElementById('comment').value.trim();
        
        if (!userName || !rating || !comment) {
            alert('Please fill in all fields and select a rating.');
            return;
        }
        
        try {
            const response = await fetch('/api/reviews', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    product_id: productId,
                    user: userName,
                    rating: rating,
                    comment: comment
                })
            });
            
            if (response.ok) {
                form.reset();
                selectedRating = 0;
                updateStarDisplay();
                
                const successMsg = document.createElement('div');
                successMsg.className = 'success-message';
                successMsg.textContent = 'Review submitted successfully!';
                form.insertBefore(successMsg, form.firstChild);
                
                setTimeout(() => successMsg.remove(), 3000);
                
                loadReviews();
                loadProductDetail();
            } else {
                throw new Error('Failed to submit review');
            }
        } catch (error) {
            console.error('Error submitting review:', error);
            alert('Error submitting review. Please try again.');
        }
    });
}

function getStars(rating) {
    const fullStars = Math.floor(rating);
    const hasHalf = rating % 1 >= 0.5;
    let stars = '';
    
    for (let i = 0; i < fullStars; i++) {
        stars += '★';
    }
    if (hasHalf) {
        stars += '☆';
    }
    for (let i = stars.length; i < 5; i++) {
        stars += '☆';
    }
    
    return stars;
}

function getStarsFromRating(rating) {
    let stars = '';
    for (let i = 0; i < 5; i++) {
        stars += i < rating ? '★' : '☆';
    }
    return stars;
}

function getStockClass(stock) {
    if (stock === 0) return 'stock-out';
    if (stock < 15) return 'stock-low';
    return 'stock-high';
}

function getStockText(stock) {
    if (stock === 0) return 'Out of Stock';
    if (stock < 15) return `Only ${stock} left`;
    return 'In Stock';
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-IN', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}
