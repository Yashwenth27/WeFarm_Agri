import streamlit as st
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from streamlit_navigation_bar import st_navbar
pages = ["Home", "About Us","","","",""]


    
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
page = st_navbar(pages, styles=styles, selected=None,logo_path="pages/ZenTech_Logo.svg")
if page=="Home":
    st.switch_page("Home_Page.py")
if page=="About Us":
    st.switch_page("pages/About_Us.py")

# Initialize Firebase
try:
    cred = credentials.Certificate('keys/iaaids-9da95-firebase-adminsdk-oy159-374219d78d.json')
    firebase_admin.initialize_app(cred, {'databaseURL': 'https://iaaids-9da95-default-rtdb.firebaseio.com/'})
except:
    pass

def exist_username(username):
    ref = db.reference('credentials/farmer')
    if ref.get()==None:
        return 1
    if username not in ref.get():
        return 1
    return 0

def store_to_db(fullname,email,username,password,mobile,aadhar):
    ref = db.reference('credentials/farmer')
    ref.child(username).set(
        {
            "fullname":fullname,
            "email":email,
            "password":password,
            "mobile":mobile,
            "aadhar":aadhar
        }
    )
    return 1


st.markdown("<h1><center><u>Intelligent Agri-App Information Dissemination System</u></h1></center><br>",unsafe_allow_html=True)
with st.container(border=True):
    st.subheader("Farmer Sign Up:")
    st.markdown('<hr style="border: 4px solid green;">', unsafe_allow_html=True)
    m = st.markdown("""
        <style>
        div.stButton > button:first-child {
        background-color: green;
        color: white;
        width: 400px;
        text-alingn: center;
        }
        </style>""", unsafe_allow_html=True)
    c1,c2 = st.columns(2)
    with c1:
        fullname = st.text_input("Full Name")
        mobile = st.text_input("Mobile Number")
        username = st.text_input("Farmer ID")
    with c2:
        email = st.text_input("Email ID")
        password = st.text_input("Password")
        aadhar = st.text_input("Aadhar Number")
    if st.button("Sign Up"):
        #verfication
        ok = exist_username(username)
        if fullname and email and username and password and mobile and aadhar:
            save = store_to_db(fullname,email,username,password,mobile,aadhar)
            if ok and not save:
                st.warning("Retry Signing Up after some time!")
            elif ok and save:
                st.success("Signed Up")
                st.switch_page("pages/f_login.py")
            else:
                st.warning("Username Taken. Retry with other Username")
        else:
            st.warning("Fill all the fields and try again!")
    if st.button("Back to Login!"):
        st.switch_page("pages/f_login.py") 


    
        
