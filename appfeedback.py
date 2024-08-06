import streamlit as st
import datetime
from urllib.parse import parse_qs

# Sample product data (you should replace this with your actual product data)
products = [
    {"id": 1, "name": "Smartphone", "category": "Electronics", "price": 499.99, "rating": 4.5},
    {"id": 2, "name": "Laptop", "category": "Electronics", "price": 999.99, "rating": 4.7},
    # Add more products as needed
]

# Sample feedback data (you should replace this with your actual feedback data)
feedback_data = [
    {"user_name": "John Doe", "product_id": 1, "product_name": "Smartphone", "feedback": "Great phone, amazing camera!", "timestamp": datetime.datetime(2024, 8, 1, 10, 30)},
    {"user_name": "Jane Smith", "product_id": 2, "product_name": "Laptop", "feedback": "Powerful laptop, but a bit heavy.", "timestamp": datetime.datetime(2024, 8, 2, 14, 15)},
    # Add more feedback as needed
]

def main():
    st.set_page_config(page_title="Product Feedback", layout="wide")
    st.title("Product Feedback")

    # Get the product_id from the URL query parameters
    query_params = st.experimental_get_query_params()
    product_id = parse_qs(st.experimental_get_query_params().get("id", [""])[0]).get("id", [""])[0]

    if product_id:
        display_product_feedback(int(product_id))
    else:
        st.error("No product ID specified. Please scan a valid QR code.")

def display_product_feedback(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    
    if product:
        st.header(f"Feedback for {product['name']}")
        
        # Display existing feedback
        st.subheader("Existing Reviews")
        product_feedback = [f for f in feedback_data if f['product_id'] == product_id]
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
                feedback_data.append(new_feedback)
                st.success("Thank you for your feedback!")
                st.experimental_rerun()
            else:
                st.warning("Please enter your name and feedback before submitting.")
    else:
        st.error("Product not found.")

if __name__ == "__main__":
    main()