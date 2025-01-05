import streamlit as st
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

st.set_page_config(initial_sidebar_state="collapsed")

# Initialize Firebase
try:
    cred = credentials.Certificate('keys/iaaids-9da95-firebase-adminsdk-oy159-374219d78d.json')
    firebase_admin.initialize_app(cred, {'databaseURL': 'https://iaaids-9da95-default-rtdb.firebaseio.com/'})
except:
    pass

# Function to verify user credentials
def verify_credentials(username, password, type):
    f_ref = db.reference('creds/farmer')
    w_ref = db.reference('creds/whole')
    c_ref = db.reference('creds/customer')

    farmers = f_ref.get()
    customers = c_ref.get()
    wholers = w_ref.get()

    if type=="farmer":
        if farmers and username in farmers:
            if farmers[username]["pass"] == password:
                return True
    if type=="customer":
        if customers and username in customers:
            if customers[username]["pass"] == password:
                return True
    if type=="whole":
        if wholers and username in wholers:
            if wholers[username]["pass"] == password:
                return True
    return False

# Function to sign up new users
def sign_up_user(username, password, name):
    ref = db.reference('creds')
    ref.child(username).set({"pass": password, "name": name})

# Initialize session state for storing login info
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
    st.session_state['username'] = ''
    st.session_state['password'] = ''
if 'signup' not in st.session_state:
    st.session_state['signup'] = False

# Function to display login page
def login_page():
    if st.session_state["utype"]=="farmer":
        username = st.text_input("Farmer ID")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if verify_credentials(username, password, "farmer"):
                st.session_state['logged_in'] = True
                st.session_state['uid'] = username
                st.session_state['pwd'] = password
                st.success("You have successfully logged in.")
                st.experimental_rerun()
                return
            else:
                st.error("Invalid username or password")
        if st.button("New User? Sign Up"):
            st.session_state['signup'] = True
            st.experimental_rerun()
        
    if st.session_state["utype"]=="customer":
        username = st.text_input("Customer ID")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if verify_credentials(username, password, "customer"):
                st.session_state['logged_in'] = True
                st.session_state['uid'] = username
                st.session_state['pwd'] = password
                st.success("You have successfully logged in.")
                st.experimental_rerun()
                return
            else:
                st.error("Invalid username or password")
        if st.button("New User? Sign Up"):
            st.session_state['signup'] = True
            st.experimental_rerun()
    if st.session_state["utype"]=="whole":
        username = st.text_input("Whole Seller ID")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if verify_credentials(username, password, "whole"):
                st.session_state['logged_in'] = True
                st.session_state['uid'] = username
                st.session_state['pwd'] = password
                st.success("You have successfully logged in.")
                st.experimental_rerun()
                return
            else:
                st.error("Invalid username or password")
        if st.button("New User? Sign Up"):
            st.session_state
            st.session_state['signup'] = True
            st.experimental_rerun()

# Function to display signup page
def signup_page():
    st.title("Sign Up")

    username = st.text_input("New Username")
    password = st.text_input("New Password", type="password")
    name = st.text_input("Full Name")

    if st.button("Sign Up"):
        if username and password and name:
            sign_up_user(username, password, name)
            st.success("You have successfully signed up. Please log in.")
            st.session_state['signup'] = False
            st.experimental_rerun()
        else:
            st.error("Please fill out all fields.")

    if st.button("Back to Login"):
        st.session_state['signup'] = False
        st.experimental_rerun()

def prelogin():
    #login_page()
            st.markdown("<h1><center><u>Intelligent Agri-App Information Dissemination System</u></h1></center><br>",unsafe_allow_html=True)
            c1,c2,c3 = st.columns(3)
            with c3:
                st.image("https://images.pexels.com/photos/1058401/pexels-photo-1058401.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1")
            with c1:
                st.image("https://images.unsplash.com/photo-1519082572439-7ed19908e47e?q=80&w=1935&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D")
            with c2:
                with st.container(border=True):
                    st.warning(st.session_state)
                    st.title("Login As:")
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
                    if st.button("🧑🏻‍🌾Farmer"):
                        st.session_state['utype']="farmer"
                        login_page()
                    if st.button("Customer"):
                        st.session_state['utype']="customer"
                        login_page()
                    if st.button("Whole Seller"):
                        st.session_state['utype']="whole"
                        login_page()

# Main function to control page navigation
def main():
    if st.session_state['logged_in']:
        st.switch_page("pages/Home.py")
    else:
        if st.session_state['signup']:
            signup_page()
        else:
            prelogin()
            
                    

if __name__ == "__main__":
    st.warning(st.session_state)
    main()
