import streamlit as st
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
try:
    cred = credentials.Certificate('keys/iaaids-9da95-firebase-adminsdk-oy159-374219d78d.json')
    firebase_admin.initialize_app(cred, {'databaseURL': 'https://iaaids-9da95-default-rtdb.firebaseio.com/'})
except:
    pass
# <button style="
#                 width: 80%; 
#                 padding: 10px; 
#                 margin-top: 10px; 
#                 background-color: green; 
#                 color: white;
#                 border-radius: 10px;
#                 font-size: 16px;" onclick="switch_page('{page_name}')">{label}</button>
from streamlit_navigation_bar import st_navbar
pages = ["Home", "About Us","Logout","","",""]
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
st.set_page_config(initial_sidebar_state="collapsed",layout="wide",page_icon="🪴",page_title="Home Page")
page = st_navbar(pages, styles=styles, selected="Home",logo_path="pages/ZenTech_Logo.svg")
if page=="About Us":
    st.switch_page("pages/About_Us.py")
if page=="Logout":
    st.switch_page("Home_Page.py")
if st.session_state["logged_in"] and st.session_state["user_id"]:
    username = st.session_state['user_id']
    ref = db.reference("credentials")
    st.title(f"Welcome, {ref.child('farmer').child(username).child('fullname').get()}")
    st.markdown('<hr style="border: 4px solid green;">', unsafe_allow_html=True)

    image_urls = [
        "https://store-images.s-microsoft.com/image/apps.16894.c02476d2-2378-4f60-8290-b6d4b3842643.79a2ef6a-4775-4c79-8d93-9caf077660eb.1bbd88a4-0a17-4750-91a0-cd7d98f58e9d",  # Example image URL
        "https://www.csm.tech/storage/uploads/images/6108f2cbda0a61627976395Meta.webp",
        "https://s3.envato.com/files/251358231/2018_07_12_1522_01.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/0/08/Agricultural_machinery.jpg/292px-Agricultural_machinery.jpg",
        "https://www.gardendesign.com/pictures/images/675x529Max/site_3/tomato-blossom-end-rot-tomato-black-end-shutterstock-com_15736.jpg",
        "https://photos.peopleimages.com/picture/202308/2754890-farmer-tablet-and-vegetables-box-for-agriculture-sustainability-and-farming-in-greenhouse-or-agro-business.-person-on-digital-technology-harvest-and-gardening-e-commerce-inventory-and-market-sales-fit_400_400.jpg"
    ]

    labels = ["Weather Forecast", "Soil Info", "Select Crop", "Machine Requirements", "Disease Detection", "Inventory"]

    # Function to create a card-like button
    def create_card(image_url, label, page_name):
        st.markdown(
            f"""
            <div style="text-align: left; margin-bottom: 10px;">
                <img src="{image_url}" alt="{label}" style="width: 230px; height:230px; border-radius: 10px;">
                
            </div>
            """,
            unsafe_allow_html=True
        )
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
        if st.button(label,key=image_url):
            st.switch_page(page_name)

    # Function to switch page
    def switch_page(page_name):
        st.switch_page(page_name)

    # Create a 3x3 grid
    rows = 2
    cols = 4
    for i in range(rows):
        columns = st.columns(cols)
        for j in range(cols):
            with columns[j]:
                if i * cols + j < len(image_urls):
                    page_name = f"pages/{labels[i * cols + j].replace(' ', '_')}.py"
                    create_card(image_urls[i * cols + j], labels[i * cols + j], page_name)
else:
    with st.container():
        st.title("Access Blocked!")
        if st.button("Login to Access"):
            st.switch_page("pages/f_login.py")

