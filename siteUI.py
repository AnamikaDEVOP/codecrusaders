import streamlit as st
import pandas as pd
import random

# Sample product data
products = [
    {"id": 1, "name": "Smartphone", "category": "Electronics", "price": 499.99, "rating": 4.5},
    {"id": 2, "name": "Laptop", "category": "Electronics", "price": 999.99, "rating": 4.7},
    {"id": 3, "name": "Headphones", "category": "Electronics", "price": 99.99, "rating": 4.3},
    {"id": 4, "name": "T-shirt", "category": "Clothing", "price": 19.99, "rating": 4.0},
    {"id": 5, "name": "Jeans", "category": "Clothing", "price": 49.99, "rating": 4.2},
    {"id": 6, "name": "Sneakers", "category": "Footwear", "price": 79.99, "rating": 4.4},
    {"id": 7, "name": "Watch", "category": "Accessories", "price": 149.99, "rating": 4.6},
    {"id": 8, "name": "Backpack", "category": "Accessories", "price": 39.99, "rating": 4.1},
]

def initialize_session_state():
    if 'cart' not in st.session_state:
        st.session_state.cart = {}

def add_to_cart(product_id):
    if product_id in st.session_state.cart:
        st.session_state.cart[product_id] += 1
    else:
        st.session_state.cart[product_id] = 1

def main():
    st.title("Mini E-commerce Site")

    initialize_session_state()

    # Sidebar for search and filter
    st.sidebar.header("Search and Filter")
    search_term = st.sidebar.text_input("Search products")
    category_filter = st.sidebar.multiselect("Filter by category", options=list(set(p["category"] for p in products)))
    sort_option = st.sidebar.selectbox("Sort by", options=["Price: Low to High", "Price: High to Low", "Rating"])

    # Filter products
    filtered_products = [p for p in products if search_term.lower() in p["name"].lower()]
    if category_filter:
        filtered_products = [p for p in filtered_products if p["category"] in category_filter]

    # Sort products
    if sort_option == "Price: Low to High":
        filtered_products.sort(key=lambda x: x["price"])
    elif sort_option == "Price: High to Low":
        filtered_products.sort(key=lambda x: x["price"], reverse=True)
    elif sort_option == "Rating":
        filtered_products.sort(key=lambda x: x["rating"], reverse=True)

    # Display products
    for product in filtered_products:
        col1, col2, col3 = st.columns([2, 2, 1])
        with col1:
            st.subheader(product["name"])
            st.write(f"Category: {product['category']}")
        with col2:
            st.write(f"Price: ${product['price']:.2f}")
            st.write(f"Rating: {product['rating']}/5")
        with col3:
            if st.button("Add to Cart", key=f"add_{product['id']}"):
                add_to_cart(product['id'])
                st.success(f"{product['name']} added to cart!")

    # Display cart
    st.sidebar.header("Shopping Cart")
    cart_total = 0
    for product_id, quantity in st.session_state.cart.items():
        product = next(p for p in products if p["id"] == product_id)
        st.sidebar.write(f"{product['name']} (x{quantity}): ${product['price'] * quantity:.2f}")
        cart_total += product['price'] * quantity
    st.sidebar.write(f"Total: ${cart_total:.2f}")

    if st.sidebar.button("Checkout"):
        st.sidebar.success("Thank you for your purchase!")
        st.session_state.cart = {}

if __name__ == "__main__":
    main()