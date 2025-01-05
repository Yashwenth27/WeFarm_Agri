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

st.markdown("<h1><center><u>Intelligent Agri-App Information Dissemination System</u></h1></center>",unsafe_allow_html=True)
c1,c2,c3 = st.columns(3)
with c3:
    st.image("https://images.pexels.com/photos/1058401/pexels-photo-1058401.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1")
with c1:
    st.image("https://images.pexels.com/photos/1058401/pexels-photo-1058401.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1")
with c2:
    with st.container(border=True):
        st.title("Whole Seller Login:")
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
        fid = st.text_input("Whole Seller ID")
        pwd = st.text_input("Password",type="password")
        if st.button("Login"):
            ref = db.reference('credentials/Whole Seller')
            if fid in ref.get():
                if pwd==ref.child(fid).child('password').get():
                    st.session_state["logged_in"]=True
                    st.session_state["user_id"]=fid
                    st.switch_page("pages/c_dash.py")
                else:
                    st.error("Wrong Password!")
            else:
                st.error("Wrong Username!")
        if st.button("New Whole Seller? Sign Up"):
            st.switch_page("pages/w_sign.py")
        if st.button("Back to Home Page 🏠"):
            st.switch_page("Home_Page.py")