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

def exist_username(username):
    ref = db.reference('credentials/Whole Seller')
    if ref.get()==None:
        return 1
    if username not in ref.get():
        return 1
    return 0

def store_to_db(fullname,email,username,password,mobile,location):
    ref = db.reference('credentials/Whole Seller')
    ref.child(username).set(
        {
            "fullname":fullname,
            "email":email,
            "password":password,
            "mobile":mobile,
            "location":location
        }
    )
    return 1


st.markdown("<h1><center><u>Intelligent Agri-App Information Dissemination System</u></h1></center><br>",unsafe_allow_html=True)
with st.container(border=True):
    st.subheader("Whole Seller Sign Up:")
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
        fullname = st.text_input("Company Name")
        mobile = st.text_input("Mobile Number")
        username = st.text_input("Whole Seller ID")
    with c2:
        email = st.text_input("Email ID")
        password = st.text_input("Password")
        location = st.text_input("District")
    if st.button("Sign Up"):
        #verfication
        ok = exist_username(username)
        if fullname and email and username and password and mobile and location:
            save = store_to_db(fullname,email,username,password,mobile,location)
            if ok and not save:
                st.warning("Retry Signing Up after some time!")
            elif ok and save:
                st.success("Signed Up")
                st.switch_page("pages/w_login.py")
            else:
                st.warning("Username Taken. Retry with other Username")
        else:
            st.warning("Fill all the fields and try again!")
    if st.button("Back to Login!"):
        st.switch_page("pages/w_login.py") 


    
        
