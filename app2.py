import streamlit as st
import pandas as pd
import qrcode
from io import BytesIO
import base64
import datetime

st.set_page_config(page_title="ShopEase", layout="wide")

# Custom CSS to improve the UI
st.markdown("""
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
<style>
    .product-card {
        background-color: #ffffff;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        padding: 20px;
        margin-bottom: 20px;
    }
    .product-name {
        font-size: 18px;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .product-category {
        color: #666;
        font-size: 14px;
        margin-bottom: 5px;
    }
    .product-price {
        font-size: 16px;
        font-weight: bold;
        color: #B12704;
        margin-bottom: 5px;
    }
    .product-rating {
        color: #FFA41C;
        margin-bottom: 10px;
    }
    .add-to-cart-btn {
        background-color: #FFD814;
        color: #0F1111;
        border: none;
        padding: 8px 16px;
        border-radius: 20px;
        cursor: pointer;
        font-weight: bold;
    }
    .sidebar-content {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
    }
    .main-content {
        padding: 20px;
    }
    .navbar {
        display: flex;
        justify-content: space-around;
        padding: 10px;
        background-color: #232f3e;
        color: white;
        margin-bottom: 20px;
    }
    .nav-item {
        display: flex;
        flex-direction: column;
        align-items: center;
        color: white;
        text-decoration: none;
        font-size: 14px;
    }
    .nav-item i {
        font-size: 24px;
        margin-bottom: 5px;
    }
    .qr-code {
        width: 100px;
        height: 100px;
        margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Sample product data with real image URLs
products = [
    {"id": 1, "name": "Smartphone", "category": "Electronics", "price": 499.99, "rating": 4.5, "image": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?ixlib=rb-1.2.1&auto=format&fit=crop&w=300&q=80"},
    {"id": 2, "name": "Laptop", "category": "Electronics", "price": 999.99, "rating": 4.7, "image": "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?ixlib=rb-1.2.1&auto=format&fit=crop&w=300&q=80"},
    {"id": 3, "name": "Headphones", "category": "Electronics", "price": 99.99, "rating": 4.3, "image": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?ixlib=rb-1.2.1&auto=format&fit=crop&w=300&q=80"},
    {"id": 4, "name": "T-shirt", "category": "Clothing", "price": 19.99, "rating": 4.0, "image": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?ixlib=rb-1.2.1&auto=format&fit=crop&w=300&q=80"},
    {"id": 5, "name": "Jeans", "category": "Clothing", "price": 49.99, "rating": 4.2, "image": "https://images.unsplash.com/photo-1542272604-787c3835535d?ixlib=rb-1.2.1&auto=format&fit=crop&w=300&q=80"},
    {"id": 6, "name": "Sneakers", "category": "Footwear", "price": 79.99, "rating": 4.4, "image": "https://images.unsplash.com/photo-1549298916-b41d501d3772?ixlib=rb-1.2.1&auto=format&fit=crop&w=300&q=80"},
    {"id": 7, "name": "Watch", "category": "Accessories", "price": 149.99, "rating": 4.6, "image": "https://images.unsplash.com/photo-1524592094714-0f0654e20314?ixlib=rb-1.2.1&auto=format&fit=crop&w=300&q=80"},
    {"id": 8, "name": "Backpack", "category": "Accessories", "price": 39.99, "rating": 4.1, "image": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?ixlib=rb-1.2.1&auto=format&fit=crop&w=300&q=80"},
]

# Sample feedback data
if 'feedback_data' not in st.session_state:
    st.session_state.feedback_data = [
        {"user_name": "John Doe", "product_id": 1, "product_name": "Smartphone", "feedback": "Great phone, amazing camera!", "timestamp": datetime.datetime(2024, 8, 1, 10, 30)},
        {"user_name": "Jane Smith", "product_id": 2, "product_name": "Laptop", "feedback": "Powerful laptop, but a bit heavy.", "timestamp": datetime.datetime(2024, 8, 2, 14, 15)},
    ]

def initialize_session_state():
    if 'cart' not in st.session_state:
        st.session_state.cart = {}
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'Home'

def add_to_cart(product_id):
    if product_id in st.session_state.cart:
        st.session_state.cart[product_id] += 1
    else:
        st.session_state.cart[product_id] = 1

def navbar():
    st.markdown("""
    <div class="navbar">
        <a href="#" class="nav-item" onclick="handleNavClick('Electronics')">
            <i class="fas fa-laptop"></i>
            <span>Electronics</span>
        </a>
        <a href="#" class="nav-item" onclick="handleNavClick('Clothing')">
            <i class="fas fa-tshirt"></i>
            <span>Clothing</span>
        </a>
        <a href="#" class="nav-item" onclick="handleNavClick('Footwear')">
            <i class="fas fa-shoe-prints"></i>
            <span>Footwear</span>
        </a>
        <a href="#" class="nav-item" onclick="handleNavClick('Accessories')">
            <i class="fas fa-glasses"></i>
            <span>Accessories</span>
        </a>
        <a href="#" class="nav-item" onclick="handleNavClick('Cart')">
            <i class="fas fa-shopping-cart"></i>
            <span>Cart</span>
        </a>
        <a href="#" class="nav-item" onclick="handleNavClick('Feedback')">
            <i class="fas fa-comment"></i>
            <span>Feedback</span>
        </a>
    </div>
    <script>
    function handleNavClick(page) {
        console.log('Clicked:', page);
        window.parent.postMessage({type: 'streamlit:setComponentValue', value: page}, '*');
    }
    </script>
    """, unsafe_allow_html=True)


def generate_qr_code(url):
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()
    

def main():
    st.title("ShopEase")
    initialize_session_state()
    navbar()

    # Check if the navbar has been clicked
    if st.session_state.get('widget_clicked'):
        st.session_state.current_page = st.session_state.widget_clicked

    # Sidebar for search and filter
    with st.sidebar:
        st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
        st.header("Search and Filter")
        search_term = st.text_input("Search products")
        category_filter = st.multiselect("Filter by category", options=list(set(p["category"] for p in products)))
        sort_option = st.selectbox("Sort by", options=["Price: Low to High", "Price: High to Low", "Rating"])
        
        st.header("Shopping Cart")
        cart_total = 0
        for product_id, quantity in st.session_state.cart.items():
            product = next(p for p in products if p["id"] == product_id)
            st.write(f"{product['name']} (x{quantity}): ${product['price'] * quantity:.2f}")
            cart_total += product['price'] * quantity
        st.write(f"Total: ${cart_total:.2f}")

        if st.button("Checkout"):
            st.success("Thank you for your purchase!")
            st.session_state.cart = {}
        st.markdown('</div>', unsafe_allow_html=True)

    # Display content based on current page
    if st.session_state.current_page == 'Home':
        display_products(products)
    elif st.session_state.current_page in ['Electronics', 'Clothing', 'Footwear', 'Accessories']:
        category_products = [p for p in products if p['category'] == st.session_state.current_page]
        display_products(category_products)
    elif st.session_state.current_page == 'Cart':
        display_cart()
    elif st.session_state.current_page == 'Feedback':
        display_feedback_list()
    elif st.session_state.current_page.startswith('Product_Feedback_'):
        product_id = int(st.session_state.current_page.split('_')[-1])
        display_product_feedback(product_id)

def display_products(products):
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    for i in range(0, len(products), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(products):
                product = products[i + j]
                with cols[j]:
                    st.markdown(f'<div class="product-card">', unsafe_allow_html=True)
                    st.image(product["image"], width=200)
                    st.markdown(f'<div class="product-name">{product["name"]}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="product-category">{product["category"]}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="product-price">${product["price"]:.2f}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="product-rating">{"★" * int(product["rating"])}{"☆" * (5 - int(product["rating"]))}</div>', unsafe_allow_html=True)
                    if st.button("Add to Cart", key=f"add_{product['id']}", help=f"Add {product['name']} to your cart"):
                        add_to_cart(product['id'])
                        st.success(f"{product['name']} added to cart!")
                    
                    # Generate QR code for product feedback
                    feedback_url = f"Product_Feedback_{product['id']}"
                    qr_code = generate_qr_code(feedback_url)
                    st.markdown(f'<img src="data:image/png;base64,{qr_code}" class="qr-code" alt="Feedback QR Code">', unsafe_allow_html=True)
                    st.markdown(f'<div>Scan for feedback</div>', unsafe_allow_html=True)
                    
                    if st.button("View Feedback", key=f"feedback_{product['id']}"):
                        st.session_state.current_page = f"Product_Feedback_{product['id']}"
                        st.experimental_rerun()
                    
                    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def display_cart():
    st.header("Shopping Cart")
    for product_id, quantity in st.session_state.cart.items():
        product = next(p for p in products if p["id"] == product_id)
        st.write(f"{product['name']} (x{quantity}): ${product['price'] * quantity:.2f}")
    
    cart_total = sum(products[product_id-1]["price"] * quantity for product_id, quantity in st.session_state.cart.items())
    st.write(f"Total: ${cart_total:.2f}")
    
    if st.button("Checkout"):
        st.success("Thank you for your purchase!")
        st.session_state.cart = {}

def display_feedback_list():
    st.header("Product Feedback")
    for product in products:
        if st.button(f"View feedback for {product['name']}", key=f"view_feedback_{product['id']}"):
            st.session_state.current_page = f"Product_Feedback_{product['id']}"
            st.experimental_rerun()

def display_product_feedback(product_id):
    product = next(p for p in products if p['id'] == product_id)
    st.header(f"Feedback for {product['name']}")
    
    # Display existing feedback
    st.subheader("Existing Reviews")
    product_feedback = [f for f in st.session_state.feedback_data if f['product_id'] == product_id]
    for feedback in product_feedback:
        st.markdown(f"**{feedback['user_name']}** - {feedback['timestamp'].strftime('%Y-%m-%d %H:%M')}")
        st.write(feedback['feedback'])
        st.markdown("---")
    
    # Form for new feedback
    st.subheader("Submit Your Feedback")
    user_name = st.text_input("Your Name")
    feedback_text = st.text_area("Your Feedback")
    if st.button("Submit Feedback"):
        if user_name and feedback_text:
            new_feedback = {
                "user_name": user_name,
                "product_id": product_id,
                "product_name": product['name'],
                "feedback": feedback_text,
                "timestamp": datetime.datetime.now()
            }
            st.session_state.feedback_data.append(new_feedback)
            st.success("Thank you for your feedback!")
            st.experimental_rerun()
        else:
            st.warning("Please enter your name and feedback before submitting.")

if __name__ == "__main__":
    main()    