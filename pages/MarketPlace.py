import streamlit as st
import pandas as pd
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# Initialize Firebase
try:
    cred = credentials.Certificate('keys/iaaids-9da95-firebase-adminsdk-oy159-374219d78d.json')
    firebase_admin.initialize_app(cred, {'databaseURL': 'https://iaaids-9da95-default-rtdb.firebaseio.com/'})
except:
    pass

from streamlit_navigation_bar import st_navbar
pages = ["Home", "About Us", "Logout", "", "", ""]
styles = {
    "nav": {
        "background-color": "green",
        "justify-content": "left",
    },
    "img": {
        "padding-right": "14px",
    },
    "span": {
        "color": "white",
        "padding": "14px",
    },
    "active": {
        "background-color": "white",
        "color": "var(--text-color)",
        "font-weight": "normal",
        "padding": "14px",
    }
}
st.set_page_config(initial_sidebar_state="collapsed", layout="wide", page_icon="🪴", page_title="Home Page")
page = st_navbar(pages, styles=styles, selected="Home", logo_path="pages/ZenTech_Logo.svg")
m = st.markdown("""
        <style>
        div.stButton > button:first-child {
            background-color: green;
            color: white;
            width: 230px;
            margin-bottom: 20px;
            text-alingn: center;
                        
        }
        </style>""", unsafe_allow_html=True)
if page == "About Us":
    st.switch_page("pages/About_Us.py")
if page == "Logout":
    st.switch_page("Home_Page.py")


# Page Title
st.markdown("""
    <div style="text-align:center;">
        <h1 style="color:green;">🌾 Marketplace</h1>
        <h4 style="color:#555;">Select and buy fresh crops directly from farmers!</h4>
    </div>
""", unsafe_allow_html=True)

st.markdown('''<hr style="border: solid 2px green">''',unsafe_allow_html=True)

# Firebase Reference to Farmer Inventory
farmers_ref = db.reference("credentials/farmer")

# Fetch All Farmers' Inventories
all_farmers = farmers_ref.get()
inventory_list = []
farmer_info = {}

if all_farmers:
    for farmer_id, details in all_farmers.items():
        if 'inventory' in details:
            inventory_ref = farmers_ref.child(farmer_id).child('inventory')
            for item_id, item_details in details['inventory'].items():
                # Validate Quantity
                if item_details['Quantity_KG'] < 0.0:
                    # Delete invalid inventory data
                    inventory_ref.child(item_id).delete()
                else:
                    # Add valid inventory items to the list
                    inventory_list.append({
                        'Crop_Name': item_details['Crop_Name'],
                        'Quantity_KG': item_details['Quantity_KG'],
                        'Price_INR': item_details['Price_INR'],
                        'Farmer_Name': details.get('fullname', 'Unknown'),
                        'Farmer_Contact': details.get('mobile', 'Unknown')
                    })

# Convert Inventory to DataFrame
inventory_df = pd.DataFrame(inventory_list)

# Left Column: Crop Selection
left_col, right_col = st.columns([0.4, 0.6])

with left_col:
    st.markdown("### Available Crops")
    if inventory_df.empty:
        st.info("No crops available currently.")
    else:
        with st.container(border=True):
            selected_crop = st.radio("Select a crop", inventory_df['Crop_Name'].unique())

# Right Column: Crop Details and Checkout
with right_col:
    if inventory_df.empty:
        st.info("Select a crop to view details.")
    elif selected_crop:
        # Fetch Selected Crop Details
        crop_data = inventory_df[inventory_df['Crop_Name'] == selected_crop].iloc[0]
        farmer_name = crop_data['Farmer_Name']
        farmer_contact = crop_data['Farmer_Contact']
        crop_price = crop_data['Price_INR']
        crop_quantity = crop_data['Quantity_KG']

        # Display Crop Details
        with st.container(border=True):
            st.markdown(f"### Selected Crop: {selected_crop}")
            st.write(f"**Farmer Name:** {farmer_name}")
            st.write(f"**Contact:** {farmer_contact}")
            st.write(f"**Price per kg:** ₹{crop_price}")
            st.write(f"**Quantity Available:** {crop_quantity:.2f} kg")

            # Quantity Selection and Checkout
            st.markdown("---")
            st.markdown("### Checkout")

            quantity_to_buy = st.number_input("Enter quantity to buy (kg):", min_value=0.0, max_value=crop_quantity, step=0.1)
            total_price = quantity_to_buy * crop_price
            st.write(f"**Total Price:** ₹{total_price:.2f}")

            if st.button("Buy Now"):
                if quantity_to_buy > 0:
                    st.success(f"You have successfully purchased {quantity_to_buy} kg of {selected_crop} for ₹{total_price:.2f}.")
                    st.write(f"**Contact Farmer**: {farmer_name} ({farmer_contact}) for further details.")
                    
                    # Update Firebase Inventory
                    farmer_inventory_ref = farmers_ref.child(farmer_id).child("inventory")
                    all_inventory = farmer_inventory_ref.get()
                    for key, value in all_inventory.items():
                        if value['Crop_Name'] == selected_crop:
                            remaining_quantity = value['Quantity_KG'] - quantity_to_buy
                            if remaining_quantity <= 0:
                                farmer_inventory_ref.child(key).delete()  # Remove crop if sold out
                            else:
                                farmer_inventory_ref.child(key).update({'Quantity_KG': remaining_quantity})
                            break
                else:
                    st.error("Please select a valid quantity to buy.")
