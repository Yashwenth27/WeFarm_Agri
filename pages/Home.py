import streamlit as st
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

st.set_page_config(initial_sidebar_state="collapsed",layout="wide")
st.write('<style>div.block-container{padding-top:2rem;}</style>', unsafe_allow_html=True)

# Initialize Firebase
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
def construct_farmer(image_urls,labels):
    rows = 2
    cols = 4
    for i in range(rows):
        columns = st.columns(cols)
        for j in range(cols):
            with columns[j]:
                if i * cols + j < len(image_urls):
                    page_name = f"pages/{labels[i * cols + j].replace(' ', '_')}.py"
                    create_card(image_urls[i * cols + j], labels[i * cols + j], page_name)

username = st.session_state['user_id']
type = st.session_state['utype']

if type=="farmer":
    ref = db.reference("credentials/farmer")
    name = ref.child(username).child("fullname").get()
    st.title(f"Welcome, {name}")
    st.markdown('<hr style="border: 4px solid green;">', unsafe_allow_html=True)

    image_urls = [
        "https://store-images.s-microsoft.com/image/apps.16894.c02476d2-2378-4f60-8290-b6d4b3842643.79a2ef6a-4775-4c79-8d93-9caf077660eb.1bbd88a4-0a17-4750-91a0-cd7d98f58e9d",  # Example image URL
        "https://www.csm.tech/storage/uploads/images/6108f2cbda0a61627976395Meta.webp",
        "https://s3.envato.com/files/251358231/2018_07_12_1522_01.jpg",
        "https://gardenerspath.com/wp-content/uploads/2020/09/Common-Tomato-Diseases-Cover.jpg",
        "https://c8.alamy.com/comp/2JRMJW8/farmer-shaking-hands-with-a-businessman-on-a-vineyard-with-grape-nursery-stock-2JRMJW8.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/0/08/Agricultural_machinery.jpg/292px-Agricultural_machinery.jpg",
        "https://www.gardendesign.com/pictures/images/675x529Max/site_3/tomato-blossom-end-rot-tomato-black-end-shutterstock-com_15736.jpg",
    ]

    labels = ["Weather Forecast", "Soil Info", "Select Crop", "Affected Crop", "Buyer Details", "Machine Requirements", "Disease Detection"]
    construct_farmer(image_urls,labels)