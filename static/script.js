let allProducts = [];

document.addEventListener('DOMContentLoaded', function() {
    loadProducts();
    loadFilters();
    setupFilterListeners();
});

async function loadProducts() {
    try {
        const response = await fetch('/api/products');
        allProducts = await response.json();
        displayProducts(allProducts);
    } catch (error) {
        console.error('Error loading products:', error);
        document.getElementById('products-container').innerHTML = 
            '<p class="loading">Error loading products. Please try again.</p>';
    }
}

async function loadFilters() {
    try {
        const [categoriesRes, brandsRes] = await Promise.all([
            fetch('/api/categories'),
            fetch('/api/brands')
        ]);
        
        const categories = await categoriesRes.json();
        const brands = await brandsRes.json();
        
        const categorySelect = document.getElementById('category-filter');
        categories.forEach(category => {
            const option = document.createElement('option');
            option.value = category;
            option.textContent = category;
            categorySelect.appendChild(option);
        });
        
        const brandSelect = document.getElementById('brand-filter');
        brands.forEach(brand => {
            const option = document.createElement('option');
            option.value = brand;
            option.textContent = brand;
            brandSelect.appendChild(option);
        });
    } catch (error) {
        console.error('Error loading filters:', error);
    }
}

function setupFilterListeners() {
    document.getElementById('category-filter').addEventListener('change', applyFilters);
    document.getElementById('brand-filter').addEventListener('change', applyFilters);
    document.getElementById('sort-filter').addEventListener('change', applyFilters);
}

function applyFilters() {
    const category = document.getElementById('category-filter').value;
    const brand = document.getElementById('brand-filter').value;
    const sort = document.getElementById('sort-filter').value;
    
    let filtered = [...allProducts];
    
    if (category) {
        filtered = filtered.filter(p => p.category === category);
    }
    
    if (brand) {
        filtered = filtered.filter(p => p.brand === brand);
    }
    
    if (sort === 'price-low') {
        filtered.sort((a, b) => a.price - b.price);
    } else if (sort === 'price-high') {
        filtered.sort((a, b) => b.price - a.price);
    } else if (sort === 'rating') {
        filtered.sort((a, b) => b.avg_rating - a.avg_rating);
    }
    
    displayProducts(filtered);
}

function displayProducts(products) {
    const container = document.getElementById('products-container');
    
    if (products.length === 0) {
        container.innerHTML = '<p class="loading">No products found.</p>';
        return;
    }
    
    container.innerHTML = products.map(product => `
        <div class="product-card" onclick="viewProduct(${product.product_id})">
            <img src="${product.image || 'https://via.placeholder.com/400x200?text=No+Image'}" 
                 alt="${product.name}" class="product-image">
            <div class="product-info">
                <h3 class="product-name">${product.name}</h3>
                <p class="product-brand">${product.brand}</p>
                <p class="product-category">${product.category}</p>
                <p class="product-price">₹${product.price.toLocaleString()}</p>
                <div class="product-rating">
                    <span class="stars">${getStars(product.avg_rating)}</span>
                    <span class="rating-count">(${product.review_count} reviews)</span>
                </div>
                <span class="product-stock ${getStockClass(product.stock)}">
                    ${getStockText(product.stock)}
                </span>
                <div class="product-tags">
                    ${product.tags.map(tag => `<span class="tag">${tag}</span>`).join('')}
                </div>
            </div>
        </div>
    `).join('');
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

function viewProduct(productId) {
    window.location.href = `/product/${productId}`;
}
