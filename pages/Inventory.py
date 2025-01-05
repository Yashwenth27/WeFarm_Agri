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

# Streamlit Navbar
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

# If user is logged in
if st.session_state["logged_in"] and st.session_state["user_id"]:
    username = st.session_state['user_id']
    ref = db.reference(f"credentials/farmer/{username}/inventory")

    # Load Inventory from Firebase if not already in session state
    if 'inventory' not in st.session_state:
        inventory_data = ref.get()
        if inventory_data:
            st.session_state['inventory'] = pd.DataFrame(inventory_data.values())
        else:
            st.session_state['inventory'] = pd.DataFrame(columns=['Crop_Name', 'Quantity_KG', 'Price_INR'])

    # Page Title
    st.markdown("""
        <style>
            .main-header {
                text-align: center;
                font-size: 32px;
                font-weight: bold;
                color: #4CAF50;
            }
            .sub-header {
                text-align: center;
                font-size: 20px;
                color: #555;
            }
            .footer {
                text-align: center;
                font-size: 14px;
                margin-top: 20px;
                color: #888;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="main-header">🌾 After Harvest Inventory</div>
    <div class="sub-header">Easily add your fresh crops to the inventory</div>
    """, unsafe_allow_html=True)

    # Add Crop Section
    st.markdown('''<hr style="border:solid 2px green;">''', unsafe_allow_html=True)

    a, b = st.columns([0.4, 0.6])

    with a:
        st.markdown("### Add Crop to Inventory")

        with st.form("add_crop_form"):
            crop_name = st.text_input("Crop Name", placeholder="Enter the name of the crop")
            quantity = st.number_input("Quantity (kg)", min_value=0.0, step=0.1, format="%.2f")
            price = st.number_input("Price (₹/kg)", min_value=0.0, step=0.1, format="%.2f")

            add_crop, refresh_inventory = st.columns([0.5, 0.5])

            with add_crop:
                submit = st.form_submit_button("Add to Inventory")
            with refresh_inventory:
                refresh = st.form_submit_button("Refresh Inventory")

        if refresh:
            st.experimental_rerun()

        if submit:
            if crop_name.strip() == "":
                st.error("Crop Name cannot be empty!")
            elif quantity <= 0:
                st.error("Quantity should be greater than zero!")
            elif price <= 0:
                st.error("Price should be greater than zero!")
            else:
                new_entry = {'Crop_Name': crop_name, 'Quantity_KG': quantity, 'Price_INR': price}
                st.session_state['inventory'] = pd.concat([st.session_state['inventory'], pd.DataFrame([new_entry])], ignore_index=True)
                st.success(f"Successfully added {crop_name} to the inventory!")
                
                # Push new entry to Firebase
                ref.push(new_entry)


    # Delete Crop Section
    with st.expander("### Remove Crop from Inventory"):

        crop_to_remove = st.selectbox("Select crop to remove", options=st.session_state['inventory']['Crop_Name'].tolist())
        remove_crop_button = st.button("Remove Crop")

        if remove_crop_button:
            if crop_to_remove in st.session_state['inventory']['Crop_Name'].values:
                # Remove the crop locally
                st.session_state['inventory'] = st.session_state['inventory'][st.session_state['inventory']['Crop_Name'] != crop_to_remove]
                st.success(f"Successfully removed {crop_to_remove} from the inventory!")
                
                # Update Firebase: Find and remove the crop from Firebase as well
                all_data = ref.get()
                for key, value in all_data.items():
                    if value['Crop_Name'] == crop_to_remove:
                        ref.child(key).delete()
                        break
            else:
                st.error(f"{crop_to_remove} not found in inventory!")
    
    if st.button("Go to MarketPlace"):
        st.switch_page("pages/Marketplace.py")

    with b:
        # Display Inventory Section
        st.markdown("### Current Inventory")
        
        # Fetch inventory from Firebase
        inventory_data = ref.get()
        if inventory_data:
            current_inventory = pd.DataFrame(inventory_data.values())
        else:
            current_inventory = pd.DataFrame(columns=['Crop_Name', 'Quantity_KG', 'Price_INR'])
        
        if current_inventory.empty:
            st.info("No crops in the inventory yet. Add some crops to get started!")
        else:
            st.dataframe(current_inventory.style.format({
                'Quantity_KG': "{:.2f}",
                'Price_INR': "{:.2f}"
            }), use_container_width=True)

            # Download Inventory as CSV
            st.markdown("#### Download Inventory")
            csv = current_inventory.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name="inventory.csv",
                mime="text/csv"
            )

    # Footer
    st.markdown(
        """
        <div class="footer"><center><i>Empowering farmers to manage their harvest effectively! 🌾</i></center>
        """, unsafe_allow_html=True
    )

    st.markdown("""
    <div class="footer">Crafted with ❤️ by ZenTech</div>
    """, unsafe_allow_html=True)
